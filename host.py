import link
import flow
import packet

class host:
	"""A Host: end points of the network"""
	def __init__(self, id, link):
		super(Host, self).__init__()
		self.id = id
		self.link = link

	'''Add the passed packets to the link queue of the 
	link it is connected to'''
	def sendPackets(packets, destination):
		linkqueue.sendPackets(packets)

	'''Receive the packets from the link queue'''
	def receivePackets():
		packet = linkqueue.get()
		# 2 = acknowledgment packet --> confirm received ack
		# 1 = Data packet --> send ack
		# 0 = routing packet --> do nothing
		if type(packet) is AckPacket:
			# inform that acknowledgmetn received
			flow.getAck(packet.ID)
		elif type(packet) is DataPacket: # Data packet
			# create an acknowledgment packet
			ackpckt = AckPacket(packet.packet_id, packet.origin_id, packet.destination_id, flow.ID)
			# push the new acknowledgment
			Link.send_packet(ackpckt)
