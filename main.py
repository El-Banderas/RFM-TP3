# https://pypi.org/project/simple-http-server/
import threading

from simple_http_server import server, PathValue, request_map
import simple_http_server.logger
import signal

import winwifi
from threading import Thread
import time

from winwifi import WiFiAp
import re

import json
import datetime

from AccessPoint import AccessPoint
from html_stuff import render_main_page, render_ssid_details, render_bssid_details

available_aps = {}
"""
ssid1   -> bssid1 -> ap1
		-> bssid2 -> ap2
		-> bssid3 -> ap3
		
ssid2   -> bssid4 -> ap4
...
"""

refresh_seconds = 5
write_in = 0
wifi = None
uthread = None
sthread = None
is_running = False


def process(up_ap: WiFiAp):
	result = []
	raw = up_ap.raw_data

	# parse SSID
	match = re.search(r"^SSID +\d+ +: (?P<SSID>[\w-]+)?\s+(?P<remaining>(?:.|\s)*)", raw)
	# There was a case without match, so I put this conditionally
	if match is not None:
		ssid = match.group("SSID")
		ssid = ssid if ssid else "-hidden-"
		raw = match.group("remaining")
	else:
		ssid = "---"
		ssid = "---"
		raw = "---"

	# parse Network type
	match = re.search(r"^Network type +: (?P<NT>\w+)\s+(?P<remaining>(?:.|\s)*)", raw)
	if match is not None:
		nt = match.group("NT")
		raw = match.group("remaining")
	else:
		nt = "---"
		raw = "---"

	# BSSIDs
	sbssids = raw.split("BSSID")[1:]
	for sbssid in sbssids:
		match = re.search(r"^ \d+ +: (?P<BSSID>[\dabcdef:]+)\s+(?P<content>(?:.|\s)+)", sbssid)

		bssid = match.group("BSSID")
		content = match.group("content")

		m = re.search(r"Signal +: (?P<signal>\d+%)\s", content)
		ssignal = m.group("signal")

		m = re.search(r"Radio type +: (?P<radio_type>[\d.a-z]+)\s", content)
		radio_type = m.group("radio_type")

		m = re.search(r"Channel +: (?P<channel>\d+)\s", content)
		channel = m.group("channel")

		kwargs = {
			"SSID": ssid,
			"Network type": nt,
			"Authentication": up_ap.auth,
			"Encryption": up_ap.encrypt,

			"BSSID": bssid,
			"Signal": ssignal,
			"Radio type": radio_type,
			"Channel": channel,
			"Basic Rates (Mbps)": [],
			"Other Rates (Mbps)": [],
		}
		result.append(AccessPoint(kwargs))

	return result


def save():
	global available_aps

	final_dict = available_aps
	for ssid in final_dict:
		for bssid in final_dict[ssid]:
			final_dict[ssid][bssid] = final_dict[ssid][bssid].__dict__()

	jsons = json.dumps(final_dict)
	now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

	with open(f"wlanreport-{now}.json", "w") as f:
		f.write(jsons)
		f.close()


def update():
	global available_aps, wifi, write_in

	try:
		available_aps_tmp = {}  # buffer

		unprocessed_aps = wifi.scan()  # this takes a while :/

		# Translate their AP to our AP
		for up_ap in unprocessed_aps:
			processed_aps = process(up_ap)
			for p_ap in processed_aps:
				available_aps_tmp.setdefault(p_ap.ssid, {})
				available_aps_tmp[p_ap.ssid][p_ap.bssidf] = p_ap

		available_aps = available_aps_tmp  # write full list

		if write_in == 0:
			write_in = 12
			save()
		else:
			write_in -= 1

		time.sleep(refresh_seconds)

	except RuntimeError:
		pass


def handler(signum, frame):
	global is_running
	if is_running:
		print("Stopping...")
		is_running = False
		server.stop()


@request_map("/", method="GET")
def _root():
	return render_main_page(available_aps)


# @request_map("/{ap_ssid}", method="GET")
# http://127.0.0.1:8080/MATOS-MESH
def _root_xxx(ap_ssid=PathValue()):
	if ap_ssid not in available_aps:
		return {"code": 404, "message": f"SSID {ap_ssid} not found!"}

	return render_ssid_details(ap_ssid, available_aps[ap_ssid])


@request_map("/**", method="GET")
# http://127.0.0.1:8080/MATOS-MESH
# or
# http://127.0.0.1:8080/MATOS-MESH/9e.a2.f4.75.dc.bf
def _root_xxx_xxx(path_val=PathValue()):
	# {ap_ssid} - show ssid details
	if '/' not in path_val:
		return _root_xxx(path_val)

	# {ap_ssid} / {ap_bssidf} - show bssid details
	ap_ssid, _, ap_bssidf = path_val.partition('/')

	if ap_ssid not in available_aps:
		return {"code": 404, "message": f"SSID {ap_ssid} not found!"}

	if ap_bssidf not in available_aps[ap_ssid]:
		return {"code": 404, "message": f"BSSID {ap_bssidf.replace('.', ':')} not found in SSID {ap_ssid}!"}

	return render_bssid_details(available_aps[ap_ssid][ap_bssidf], refresh_seconds)


if __name__ == "__main__":
	simple_http_server.logger.set_level("ERROR")  # Doesn't have critical -_-

	# Initialize WinWiFi
	wifi = winwifi.WinWiFi()

	# netsh wlan show all

	print("Initial scan... ", end="")
	update()
	print("OK")

	print("Starting server... ", end="")
	sthread = Thread(target=server.start, kwargs={"port": 8080}, daemon=False)
	sthread.start()
	print("OK")

	is_running = True
	signal.signal(signal.SIGINT, handler)

	while is_running:
		update()
