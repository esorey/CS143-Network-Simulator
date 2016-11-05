from host import sendPackets 
class flow:
	"""Flow Class"""
	def __init__(self, source, destination, data, start):
		super(ClassName, self).__init__()
		self.source = source
		self.dest = destination
		self.data = data # data
		self.start = start # time at which flow begins
		self.windowSize = 0 # set in congestion control algorithm 
		self.currACK = 0 # the last acknowledged packet ID
		self.droppedPackets = [] # dropped packets (IDs)
		
	def congestionControlAlg(pcktReceived, pcktSent): 
		# run congestion control alg
		# TCP Reno
		# FAST-TCP
		windowSize = 100
		return windowSize

	def hostSendPckts(): 
		sendPckts = []
		if len(droppedPackets) != 0: 
			# send packets from dropped packets
			if len(droppedPackets) >= windowSize:
				sendPckts = droppedPackets[:windowSize]
			elif len(droppedPackets) < windowSize:
				sendPckts.append(droppedPackets)
				temp = windowSize - len(droppedPackets)
				sendPckts.append(other[temp:])
			else:
				sendPckts.append(other[:windowSize])

	def sendPckts(packets, destination): 
		sendPackets(packets, destination)

	''' When a host receives an acknowledgement packet it will call this 
	function for the flow to update what packets have been received. The 
	flow deals with packet loss.'''
	def getACK(packetID):
		if packetID  > currACK+1:  // dropped a packet
			append(droppedPacket, range(currACK+1, packetID))
		currACK += 1
		elif packetID < currACK: 
		Delete packetID from droppedPacket
		else:
		currACK += 1

# Global ID variable for packet ID
# Check by flow