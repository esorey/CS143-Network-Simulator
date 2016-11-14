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
	def sendPackets(self, packetlist):
		for pckt in packetlist:
			sendPckt = Event(Event.pckt_send, system_EQ.currentTime, [self.link, pckt])
			constants.system_EQ.enqueue(sendPckt)

	'''Receive the packets from the link queue'''
	def receivePacket(self, pckt):
		if type(pckt) is AckPacket: # Acknowledgment packet
			# make and enqueue an event for the event queue 
			# for acknowledging a received acknowledgment packet
			ackEvent = Event(Event.ack_rcv, constants.system_EQ.currentTime, 
				[pckt.packet_id, pckt.owner_flow])
			constants.system_EQ.enqueue(ackEvent)

		if type(pckt) is DataPacket: # Data packet
			# create an acknowledgment packet
			ackpckt = AckPacket(pckt.packet_id, pckt.origin_id, pckt.destination_id, flow.ID)
			# push the new acknowledgment
			sendAckPckt = Event(Event.pckt_send, constants.system_EQ.currentTime, [self.link, ackpckt])
			constants.system_EQ.enqueue(sendAckPckt)

