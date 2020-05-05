class Player:
	def __init__(self, username, password):
		# Position
		self.X = 0.00
		self.Y = 0.00
			
		# Status and Profile
		self.level = 0
		self.world = ""
		self.username = ""
		self.guildName = ""
		self.expression = ""
		self.trading = False
		self.hasGuild = False
		self.isMod = False
			
		# Network
		self.peer = Peer()
		self.mac = ""
		self.token = ""
		self.rtid = ""
		self.slowNet = False
		self.ping = 0 # in microsecond
	
	def __repr__(self):
		return f'<Player {self.username}>'
	
	def login():
		pass # TODO