from threading import Thread
from threading import Event
from AcessPoint import AcessPoint
import time


class Update_APS(Thread):
	def __init__(self, available_AP, refresh_time):
		Thread.__init__(self)
		self.available_AP = available_AP
		self.refresh_time = refresh_time  # * 0.001

	def run(self):
		while True:
			# Em segundos
			time.sleep(self.refresh_time)
			print("Vai adicionar?")
			AP_novo = AcessPoint("NOS-asdd", "88:88:88:as:ds:ds", "65%", "2.4Ghz", "11")
			self.available_AP.append(AP_novo)
