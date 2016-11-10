from host import sendPackets
import constants

class flow:
	"""Flow Class"""
	def __init__(self, ID, source, destination, data_amt, start):
		super(ClassName, self).__init__()
		self.ID = ID

		self.source = source
		self.dest = destination
		self.data_amt = data_amt	# Size of data in MB
		self.start = start 			# Time at which flow begins
		
		self.windowSize = 0 		# set in congestion control algorithm 
		self.currACK = 0 			# the last acknowledged packet ID
		self.droppedPackets = [] 	# dropped packets (IDs)

		# Number of data packets the flow needs to send
		self.num_packets = data_amt * constants.MBTOBYTES / constants.DATA_PKT_SIZE
		self.currPCK = 0			# current packet that we're sending


	def congestionControlAlg(pcktReceived, pcktSent): 
		# run congestion control alg
		# TCP Reno
		# FAST-TCP
		windowSize = 100
		return windowSize

	def hostSendPckts(self): 
		packets_to_send = []
		if len(self.droppedPackets) != 0: 		# Send packets from dropped packets
			# send ALL packets from dropped packets
			if len(self.droppedPackets) >= self.windowSize:
				packets_to_send = generatePackets(self, self.droppedPackets[:(self.windowSize)])

			# send SOME packets from dropped packets and SOME from new packets
			elif len(self.droppedPackets) < self.windowSize:
				# Generate and get ready to send packets from dropped packets
				getPcktsToSend = generatePackets(self, self.droppedPackets)
				sendPckts.append(getPcktsToSend)

				# Generate and get ready to send new packets
				temp = windowSize - len(droppedPackets)
				getPcktsToSend = generatePackets(self, range(self.currPCK, self.currPCK+temp))
				sendPckts.append(getPcktsToSend)

				self.currPCK = self.currPCK+temp
			else:
				# This also needs to be fixed
				sendPckts.append(other[:windowSize])

	def sendPckts(packets, destination): 
		sendPackets(packets, destination)

	''' When a host receives an acknowledgement packet it will call this 
	function for the flow to update what packets have been received. The 
	flow deals with packet loss.'''
	def getACK(self, packetID):
		if packetID  > currACK+1:  # if we dropped a packet
			# Add the packets we dropped to the droppedPackets list
			self.droppedPackets.append(range(currACK+1, packetID))
			currACK += 1
		elif packetID < currACK: 	# If we receive an ack for packet that was
									# 	dropped
			# Remove this packet from list of dropped packets
			self.droppedPackets.remove(packetID)
		else:
			currACK += 1 	# We received correct packet, increment currACK
	

	def generatePackets(self, listPacketIDs):
