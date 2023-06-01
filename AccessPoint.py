class AccessPoint:

	def __init__(self, kwargs):
		self.ssid = kwargs["SSID"]
		self.net_type = kwargs["Network type"]
		self.auth = kwargs["Authentication"]
		self.encrypt = kwargs["Encryption"]
		self.bssid = kwargs["BSSID"]
		self.bssidf = self.bssid.replace(':', '.')
		self.strength = kwargs["Signal"]

		self.radio_type = kwargs["Radio type"]
		self.channel = kwargs["Channel"]
		#self.basic_rates = kwargs["Basic Rates (Mbps)"]
		#self.other_rates = kwargs["Other Rates (Mbps)"]

	def __dict__(self):
		return {
			"SSID": self.ssid,
			"Network type": self.net_type,
			"Authentication": self.auth,
			"Encryption": self.encrypt,
			"BSSID": self.bssid,
			"Signal": self.strength,
			"Radio type": self.radio_type,
			"Channel": self.channel,
			#"Basic Rates (Mbps)": self.basic_rates,
			#"Other Rates (Mbps)": self.other_rates,
		}
