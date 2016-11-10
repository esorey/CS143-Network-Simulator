from host import sendPackets
import constants

class flow:
	"""Flow Class"""
	def __init__(self, ID, source, destination, data_amt, start):
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

		# Packet that we will send next, if this is greater than num_packets+1
		#	then we have attempted to send all packets, check the dropped 
		#	packet array (should be empty) to ensure everything was sent. 
		self.currPCK = 0


	def congestionControlAlg(pcktReceived, pcktSent): 
		# run congestion control alg
		# TCP Reno
		# FAST-TCP
		windowSize = 100
		return windowSize

	## ADD CHECKS FOR IF YOU'RE AT THE END OF SENDING PCKTS
	def flowSendPackts(self): 
		packets_to_send = []
		# Send ALL packets from dropped packets
		if len(self.droppedPackets) >= self.windowSize:
			packets_to_send = self.generatePackets(self, self.droppedPackets[:(self.windowSize)])

		# send SOME (could be 0) packets from dropped packets and SOME from new packets
		else:
			# Generate and get ready to send packets from dropped packets
			getPcktsToSend = self.generatePackets(self, self.droppedPackets)
			packets_to_send.extend(getPcktsToSend)

			# Generate and get ready to send new packets
			temp = windowSize - len(droppedPackets)

			# If we reach the end of all the packets to send
			if self.currPCK + temp > self.num_packets + 1:
				end_pckt_index = self.num_packets + 1
			else:	# Otherwise
				end_pckt_index = self.currPCK + temp

			getPcktsToSend = self.generatePackets(self, range(self.currPCK, end_pckt_index))
			packets_to_send.extend(getPcktsToSend)

			# Update the current packet we want to send
			self.currPCK = end_pckt_index

		(self.source).sendPackets(packets_to_send)

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
	

	def generateDataPackets(self, listPacketIDs):
		packets_list = []
		for PID in listPacketIDs:
			pckt = DataPacket()



