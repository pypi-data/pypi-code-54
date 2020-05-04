import os, random, socket, requests, struct
from enet import *
class Growtopia:
	def __init__(self,path=os.getenv("LOCALAPPDATA")+"\\Growtopia"):
		
		"""
		ATTRIBUTES:
			Path path		Path to Growtopia folder, default is %LOCALAPPDATA%\Growtopia
		
		DESCRIPTION:
			Growtopia class for setting the Growtopia folder path
		"""
		
		if os.path.isdir(path) is not True:
			raise self.Exceptions.InvalidGrowtopiaPath("The Growtopia path is invalid.")
		
		self.path = path
	
	def loadSaveDat(self, path=os.getenv("LOCALAPPDATA")+"\\Growtopia\\save.dat"):
		
		"""
		ATTRIBUTES:
			Path path 		Path to the save.dat file, default is %LOCALAPPDATA%\Growtopia\save.dat
		
		DESCRIPTION:
			Loads Growtopia custom save.dat file
		"""
		
		if os.path.isexist(path) is not True:
			raise self.Exceptions.InvalidGrowtopiaPath("Wrong file path!")
		
		self.saveDatPath = path
		
	def login(self, username, password, version="3.38"):
	
		"""
		ATTRIBUTES:
			str username		Username to login
			str password		Password to complete the login process
			str version			String that contain float string of current Growtopia version (eg. "3.56")
			
		DESCRIPTION:
			Login to an account and return Player object
		
		Example:
			>> myAccount = Growtopia.login("Gogo333", "GogoIsTheBest", "1.00")
			>> print(myAccount.world)
			WHITETOPIANS
			>> myAccount.warp("WHITETOPIANS2")
			True
			>> pprint(myAccount.friends)
			[{
				"name": "HanzHaxors",
				"status": "online",
				"currentWorld": "WHITETOPIANS"
			 },{
				"name": "Seth",
				"status": "online",
				"currentWorld": "WHITETOPIANS"
			 },{
				"name": "Hamumu",
				"status": "offline",
				"currentWorld": ""
			}]
		"""
		
		try:
			float(version)
		except:
			raise InvalidGrowtopiaVersion("Invalid Growtopia version you should put float number without any letter(s)")
		
		# LOGIN PROCESS
		
		# SendPacket(2, "tankIDName|" + uname + "\ntankIDPass|" + upass + "\nrequestedName|WhiteTopia\nf|0\nprotocol|38\ngame_version|" + ver + "\nfz|13812200\nlmode|0\ncbits|0\nhash2|"+hash2+"\nmeta|" + generateMeta() + "\nfhash|-716928004\nrid|" + generateRid() + "\nplatformID|0\ndeviceVersion|0\ncountry|cz\nhash|" + hash + "\nmac|" + generateMac() + "\nwk|" + generateRid() + "\nzf|13837395" + token, peer)
		# TODO:
		# [x] Version
		# [ ] hash2
		# [ ] Meta
		# [ ] RId
		# [ ] hash
		# [ ] token
		# [ ] peer
		# [ ] SendPacket in python
	
	#def isServerUp():
		#
		#"""Function to check wheter the Growtopia server is up or not
#		
		#Type: bool
		#"""
#	
		#txt = requests.get("https://growtopiagame.com/").text
		#if "Server is up" in txt:
			#return True
		#elif "Server is down for maintenance" in txt:
			#return False
#	
	#def onlines():
		#
		#"""Function to check how many people are online right now
		#Type: int"""
#		
		#txt = requests.get("https://growtopiagame.com/").text
		
	
	# Classes
	class Exceptions:
		class InvalidGrowtopiaPath(self, Error):
			"""If the Growtopia Path is invalid or its a file, then raise this"""
		class WrongCredential(self, Error):
			"""If the credential is wrong, raise this"""
		class InvalidGrowtopiaVersion(self, Error):
			"""Raised when user put letter 'V' or anything else instead of
			floating numbers
			"""
		class InvalidIntValue(self, Error):
			"""Raise this when user input something invalid that expected
			to be int
			"""
		class InvalidFloatValue(self, Error):
			"""Raise this when user input something invalid that expected
			to be float
			"""
		class InvalidPacketType(self, Error):
			"""Raise this when there is no packet type available in the list
			"""
	
	class Generate:
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
	
	class Packet: # Should be merged with Player Class
	
		# This class should never be instantiated directly, but rather via enet.Host.connect or enet.Event.Peer that were in Player Class
		def __init__(self, type, data, peer):
			"""
			ATTRIBUTES:
				int type		Packet type 0 - 30
				str data		Packet data
				Peer peer		EnetPeer object that own this packet
			
			DESCRIPTION:
				An ENet data packet that may be sent to or received from a peer
			"""
			self.Packet.type = [0,1,2,3,4,5,6,7,8,9,0xA,0xB,0xC,0xD,0xE,0xF,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24]
			self.Packet.message_types = [1,2,3,4]
			
			try:
				int(type)
			except ValueError:
				raise InvalidIntValue("This should be integer, read the documentation for more info.")
			
			type = int(type)
				
			if type in self.Packet.type:
				self.Packet.type = type
				self.Packet.data = data
				self.Packet.peer = peer
				
				
				#* Is used to represent a pointer but in python its nothing
				
				#& Is used to get the address but in python its a built-in function id()
				
				#memcpy(destination, dataSource, bytesToCopy)
				#memcpy(var+i, data, b) in python is var[i:i+b] = struct.pack('!h', )
				#struct.pack(format, v1, v2, ...) returns bytes
				
				#return Packet()
			else:
				raise InvalidPacketType("The packet type doesn't exist.")
			
			def send(self, channel, packet):
				"""
				ATTRIBUTES:
					int channel		Packet sending channel ID
					Packet packet	Packet to send
				
				DESCRIPTION:
					Queue a packet to be sent.
					
					returns True on success, False on failure
				"""
				
				if self.Packet.peer.send(channel, packet) is 0:
					return True
				else:
					return False
				
	
	class Events:
		pass
	
	class Player:
		def __init__(self, username, password):
			# Position
			self.Player.X = 0.00
			self.Player.Y = 0.00
			
			# Status and Profile
			self.Player.level = 0
			self.Player.world = ""
			self.Player.username = ""
			self.Player.guildName = ""
			self.Player.expression = ""
			self.Player.trading = False
			self.Player.hasGuild = False
			self.Player.isMod = False
			
			# Network
			self.Player.peer = Peer()
			self.Player.mac = ""
			self.Player.token = ""
			self.Player.rtid = ""
			self.Player.slowNet = False
			self.Player.ping = 0 # in microsecond
		
	
	"""class Server:
		self.Server.fake_server = Host()
		self.Server.real_server = Host()
		self.Server.server_peer = Peer()
		self.Server.gt_peer = Peer()
		self.Server.user = 0
		self.Server.token = 0
		self.Server.server_ip = "209.59.191.76"
		self.Server.server_port = 17093
		self.Server.fake_port = 170
		self.Server.world = ""
		
		
		# Functions
		def handle_outgoing():
			evt = Event()
			while 
		
		def handle_incoming():
			pass
		
		def connect():
			pass
		
		def disconnect(reset):
			pass
		
		
		def start():
			pass
		
		def quit():
			pass
		
		def setup_client():
			pass
			
		def redirect_server(varList):
			pass
		
		def send(client, type, data, length): # There are 3 of them
			pass
		
		def poll():
			pass
		
		######## THE END :D ########"""