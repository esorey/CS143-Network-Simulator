from link import Link
from flow import Flow
from packet import Packet

class Host:
	"""A Host: end points of the network"""
	def __init__(self, id, link):
		super(Host, self).__init__()
		self.id = id
		self.link = link

	'''Add the passed packets to the link queue of the 
	link it is connected to'''
	def sendPackets(packets):
		for packet in packets:
			link.send_packets(packet)

	'''Receive the packets from the link queue'''
	def receivePacket(packet):
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

