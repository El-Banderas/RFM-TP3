class AccessPoint:
	def __init__(self, ssid, auth, encrypt, bssid, strength, band, channel, raw=""):
		self.ssid = ssid
		self.auth = auth
		self.encrypt = encrypt
		self.bssid = bssid
		self.strength = strength
		self.band = band
		self.channel = channel
		self.raw = raw

	def __dict__(self):
		return {
			"ssid": self.ssid,
			"auth": self.auth,
			"encrypt": self.encrypt,
			"bssid": self.bssid,
			"strength": self.strength,
			"band": self.band,
			"channel": self.channel
		}
