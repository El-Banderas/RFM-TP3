# https://pypi.org/project/simple-http-server/
from simple_http_server import route, server, PathValue, request_map
import simple_http_server.logger
import signal

import winwifi
from threading import Thread
import time

from winwifi import WiFiAp

from AccessPoint import AccessPoint
from html_stuff import render_main_page, render_ap_details

available_aps = {}
refresh_seconds = 5
wifi = None
uthread = None
sthread = None
is_running = False


def update():
	global available_aps, wifi

	try:
		available_aps_tmp = {}  # buffer

		for ap in wifi.scan():
			new_ap = AccessPoint(ap.ssid, ap.auth, ap.encrypt, ap.bssid, ap.strength, "?", "?", ap.raw_data)
			available_aps_tmp[ap.ssid] = new_ap

		available_aps = available_aps_tmp  # write full list

		time.sleep(refresh_seconds)

	except RuntimeError:
		# Retry
		update()


def handler(signum, frame):
	global is_running
	if is_running:
		print("Stopping...")
		is_running = False
		server.stop()
		#sthread.join()
		#exit(1)


@request_map("/", method="GET")
def _root():
	return render_main_page(available_aps.values())


@request_map("/{ap_ssid}", method="GET")
def _root_xxx(ap_ssid=PathValue()):
	if ap_ssid in available_aps:
		return render_ap_details(available_aps[ap_ssid], refresh_seconds)
	else:
		return {"code": 404, "message": f"AP with SSID {ap_ssid} not found!"}


if __name__ == "__main__":
	simple_http_server.logger.set_level("ERROR")  # Doesn't have critical -_-

	# Initialize WinWiFi
	wifi = winwifi.WinWiFi()

	# temporary
	ap = wifi.scan()[0]
	print()
	print(ap.__dict__.keys())
	print(ap.__dir__())
	print()

	update()

	print("Starting server... ", end="")
	sthread = Thread(target=server.start, kwargs={"port": 8080}, daemon=False)
	sthread.start()
	print("OK")

	is_running = True
	signal.signal(signal.SIGINT, handler)

	while is_running:
		update()
