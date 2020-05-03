import json
import requests

class Nonfig:
	"""Initialize API instance to fetch data from Nonfig"""
	base_url = 'https://api.nonfig.com'
	api_url = '{}/configurations'.format(base_url)

	def __init__(self,
		app_id: str,
		app_secret: str,
		debug: bool = False,
		cache_enable: bool = False,
		cache_ttl: int = 60
	):
		self.app_id = app_id
		self.app_secret = app_secret
		self.debug = debug
		self.cache_enable = cache_enable
		self.cache_ttl = cache_ttl

	def get_headers(self):
		return {
			'user-agent': 'nonfig/pythong-sdk/1.0',
			'authorization': '{}:{}'.format(self.app_id, self.app_secret)
		}

	def find_by_id(self, id: str) -> dict:
		headers = self.get_headers()
		full_url = '{}/id/{}'.format(self.api_url, id)
		request = requests.get(full_url, headers=headers)

		return request.json()

	def find_by_name(self, name: str):
		headers = self.get_headers()
		full_url = '{}/name/{}'.format(self.api_url, name)
		request = requests.get(full_url, headers=headers)

		return request.json()

	def find_by_path(self, path: str) -> list:
		headers = self.get_headers()
		full_url = '{}/path/{}'.format(self.api_url, path)
		request = requests.get(full_url, headers=headers)

		return request.json()

	def find_by_labels(self, labels: list) -> list:
		headers = self.get_headers()
		full_url = '{}/labels/{}'.format(self.api_url, ','.join(labels))
		request = requests.get(full_url, headers=headers)

		return request.json()