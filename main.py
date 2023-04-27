# https://pypi.org/project/simple-http-server/
from simple_http_server import route, server

from scapy.all import *
from scapy.layers.dot11 import Dot11

redes = {
	"Olá": "Adeus",
	"Olá2": "Adeus1",
	"Olá3": "Adeus2",
	"Olá4": "Adeus3",
}


def _render_map():
	result = ""
	result += "<ul>"
	for key in redes:
		result += "<li>{key} - {value}</li>".format(key=key, value=redes[key])
	result += " </ul>\n"
	return result


@route("/")
def _main_page():
	return """
		<html>
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
server.start(port=8080)
