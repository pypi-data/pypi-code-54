def Mac(self):
	"""
	Generate random MAC Address
	"""
	return ':'.join('%02x'%random.randrange(256) for _ in range(5))
		
def JSONFromPacketData(self, data):
	"""
	Converts your Growtopia packet data to JSON automatically
	"""
	incomplete = re.split(r"\r|\n|(?=^$)", data)
	complete = []
	try:
		for a in incomplete:
			if a is '':
				pass
			else:
				u = a.split("|")
				try:
					complete[u[0]] = int(u[1])
				except:
					complete[u[0]] = u[1]
	except IndexError:
		pass # Reach the RT-END means done
	
	return complete