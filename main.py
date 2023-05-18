# https://pypi.org/project/simple-http-server/
from simple_http_server import route, server

from scapy.all import *
from scapy.layers.dot11 import Dot11
from AcessPoint import AcessPoint
from render_html import render_main_page
from refresh_points import Update_APS
import signal

AP1 = AcessPoint("NOS-asdd", "88:88:88:as:ds:ds", "65%", "2.4Ghz", "11")
AP2 = AcessPoint("MEO-asdd", "88:88:88:as:ds:ds", "65%", "2.4Ghz", "11")
AP3 = AcessPoint("Vodafone-asdd", "88:88:88:as:ds:ds", "65%", "2.4Ghz", "11")
AP4 = AcessPoint("MAE-asdd", "88:88:88:as:ds:ds", "65%", "2.4Ghz", "11")

available_AP = [AP1, AP2, AP3, AP4]
refresh_seconds = 5


def _render_map():
	result = ""
	result += "<ul>"
	for AP in available_AP:
		result += f"<li><a href=\"/queijo\">{AP.ssid} - {AP.band}</li>"
	result += " </ul>\n"
	return result


def _style():
	return f"<head><meta http-equiv=\"refresh\" content=\"{refresh_seconds}\">" + """
			<style>
			body{
				margin: auto;
				width: 50%;
			}
			li{
				list-style-type: none;
				margin: 0;
				border: 5px solid black;
			}
</style>
</head>"""


@route("/")
def _main_page():
	return render_main_page(available_AP)
	return "<html>\n" \
		+ _style() + \
		"""
			<title>HTTP Server in java</title>
			<body>
		""" \
		"<b> This is the HTTP Server Home Page.... </b><BR>\n" \
		"<b> Olá Amigos.... </b><BR>\n" \
		+ _render_map() + \
		"""
			</body>
		</html>
		"""


@route("/queijo")
def _main_page1():
	return "<html>\n" \
		+ _style() + \
		"""
			<title>Queijo</title>
			<body>
		""" \
		"<b> This is the HTTP Server Home Page.... </b><BR>\n" \
		"<b> Olá Amigos queijo.... </b><BR>\n" \
		"""
			</body>
		</html>
		"""


# netsh wlan show interfaces
IFACE_NAME = "WiFi"
devices = set()


def _packet_handler(pkt):
	if pkt.haslayer(Dot11):
		dot11_layer = pkt.getlayer(Dot11)

		if dot11_layer.addr2 and (dot11_layer.addr2 not in devices):
			devices.add(dot11_layer.addr2)
			print(len(devices), dot11_layer.addr2, dot11_layer.payload.name)


# sniff(iface=IFACE_NAME, count=100, prn=_packet_handler)
# print(list(devices))

# print(_main_page())
'''
is_running = True

def handler(signum, frame):
	msg = "Ctrl-c was pressed\n"
	print(msg, end="", flush=True)
	is_running = False
	exit(1)
 
signal.signal(signal.SIGINT, handler)
'''

if __name__ == "__main__":
	#	thread = Update_APS(available_AP,  refresh_seconds)
	#	thread.daemon = True
	#	thread.start()
	server.start(port=8080)
