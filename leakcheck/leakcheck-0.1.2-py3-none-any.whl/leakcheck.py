import requests
import json

class LeakCheckAPI:

	version = "0.1.2"
	headers = {"User-Agent": "PyLCAPI/{}".format(version)}
	allowed_types = ["auto", "email", "mass", "login", "phone", "mc", "pass_email", "domain_email", "pass_login", "pass_phone", "pass_mc", "hash"]

	def __init__(self):
		self.url = "https://leakcheck.net"
		self.key = ""
		self.proxy = ""
		self.type = ""
		self.query = ""
		self.result = []

	def set_proxy(self, proxy):
		self.proxy = proxy

	def set_key(self, key):
		try:
			if len(key) != 40:
				raise Exception("set_key returned an exception: key is invalid, it must be 40 characters long")
			self.key = key
		except Exception as e:
			print(e)

	def set_type(self, type):
		try:
			if type not in self.allowed_types:
				raise Exception("set_type returned an exception: type is invalid")
			self.type = type
		except Exception as e:
			print(e)

	def set_query(self, query):
		self.query = query

	def use_mirror(self):
		self.url = "https://leakcheck.io"

	def lookup(self):
		try:
			if self.key is "":
				raise Exception("Key is missing, use LeakCheckAPI.set_key()")
			elif self.type is "":
				raise Exception("Type is missing, use LeakCheckAPI.set_type()")
			elif self.query is "":
				raise Exception("Query is missing, use LeakCheckAPI.set_query()")
			data = {'key': self.key, 'type': self.type, "check": self.query}
			request = requests.get(self.url + "/api/",
				 data, 
				 headers = self.headers,
				 proxies = {'https': self.proxy}
			)
			if request.json().get("success") == False:
				raise Exception(request.json().get("error"))
			else:
				for result in request.json().get("result"):
					self.result.append(result['line'])
				return self.result
		except Exception as e:
			return e

	def getLimits(self):
		try:
			if self.key is "":
				raise Exception("Key is missing, use LeakCheckAPI.set_key()")
			data = {'key': self.key, 'type': 'limits'}
			request = requests.get(self.url + "/api/",
				 data, 
				 headers = self.headers,
				 proxies = {'https': self.proxy}
			)
			if request.json().get("success") == False:
				raise Exception(request.json().get("error"))
			else:
				return request.json().get("limits")
		except Exception as e:
			return e

	def getIP(self):
		try:
			return requests.post(self.url + "/ip", 
				headers = self.headers, 
				proxies = {'https': self.proxy}
			).text
		except Exception as e:
			return e