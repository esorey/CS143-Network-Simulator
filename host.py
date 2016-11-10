import constants
from packet import Packet
from event_queue import EventQueue
from event import Event

class Host:
	"""A Host: end points of the network"""
	def __init__(self, id, link):
		super(Host, self).__init__()
		self.id = id
		self.link = link

	'''Add the passed packets to the link queue of the 
	link it is connected to'''
	def sendPackets(packetlist):
		for pkt in packetlist:
			sendPckt = Event(Event.pckt_send, system_EQ.currentTime, [self.link, pkt])
			system_EQ.enqueue(sendPckt)

	'''Receive the packets from the link queue'''
	def receivePacket(packet):
		if type(packet) is AckPacket: # Acknowledgment packet
			# make and enqueue an event for the event queue 
			# for acknowledging a received acknowledgment packet
			ackEvent = Event(Event.ack_rcv, system_EQ.currentTime, 
				[packet.packet_id, packet.owner_flow])
			system_EQ.enqueue(ackEvent)

		if type(packet) is DataPacket: # Data packet
			# create an acknowledgment packet
			ackpckt = AckPacket(packet.packet_id, packet.origin_id, packet.destination_id, flow.ID)
			# push the new acknowledgment
			sendAckPckt = Event(Event.pckt_send, system_EQ.currentTime, [self.link, ackpckt])
			system_EQ.enqueue(sendAckPckt)

