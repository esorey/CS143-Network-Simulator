from link import Link
import constant
from flow import Flow
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
	def sendPackets(packets):
		for packet in packets:
			link.send_packets(packet)

	'''Receive the packets from the link queue'''
	def receivePacket(packet):
		if type(packet) is AckPacket: # Acknowledgment packet
			# make and enqueue an event for the event queue 
			# for acknowledging a received acknowledgment packet
			ackEvent = Event(Event.ack_rcv, event_queue.currentTime, 
				[packet.packet_id, packet.flow_id])
			system_eq.enqueue(ackEvent)

		if type(packet) is DataPacket: # Data packet
			# create an acknowledgment packet
			ackpckt = AckPacket(packet.packet_id, packet.origin_id, packet.destination_id, flow.ID)
			# push the new acknowledgment
			Link.send_packet(ackpckt)

