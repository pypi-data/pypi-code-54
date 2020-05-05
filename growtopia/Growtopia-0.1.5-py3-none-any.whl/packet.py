class Packet: # Should be merged with Player Class

	def __init__(self, type, data, peer):
		"""
			An ENet data packet that may be sent to or received from a peer
		"""
		self.type = [0,1,2,3,4,5,6,7,8,9,0xA,0xB,0xC,0xD,0xE,0xF,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1A,0x1B,0x1C,0x1D,0x1E,0x1F,0x20,0x21,0x22,0x23,0x24]
		self.message_types = [1,2,3,4]
			
		try:
			int(type)
		except ValueError:
			raise InvalidIntValue("This should be integer, read the documentation for more info.")
			
		type = int(type)
			
		if type in self.type:
			self.type = type
			self.data = data
			self.peer = peer
			
			
			#* Is used to represent a pointer but in python its nothing
			
			#& Is used to get the address but in python its a built-in function id()
			
			#memcpy(destination, dataSource, bytesToCopy)
			#memcpy(var+i, data, b) in python is var[i:i+b] = struct.pack('!h', )
			#struct.pack(format, v1, v2, ...) returns bytes
			
			#return Packet()
		else:
			raise InvalidPacketType("The packet type doesn't exist.")
		
		def __repr__(self):
			return f'<Packet {id(self)}>'
		
		def send(self, channel, packet):
			"""
				Queue a packet to be sent.
				
				returns True on success, False on failure
			"""
			
			if self.peer.send(channel, packet) is 0:
				return True
			else:
				return False
		