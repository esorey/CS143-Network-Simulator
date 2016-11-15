import constants
from packet import Packet
from event_queue import EventQueue
from event import Event
from analytics import Analytics

class Host:
	"""A Host: end points of the network"""
        def __init__(self, id, out_link):
		super(Host, self).__init__()
		self.id = id
                self.out_link = out_link
		self.pckt_counters = {}
		# possibly needed for host send/receive rate
		self.num_received = 0
		self.num_sent = 0

	'''Add the passed packets to the link queue of the 
	outlink it is connected to'''
	def sendPackets(self, packetlist):
		for pckt in packetlist:
			sendPckt = Event(Event.pckt_send, system_EQ.currentTime, [self.out_link, pckt])
			constants.system_EQ.enqueue(sendPckt)

	'''Receive the packets from the inlink queue'''
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
			sendAckPckt = Event(Event.pckt_send, constants.system_EQ.currentTime, [self.out_link, ackpckt])
			constants.system_EQ.enqueue(sendAckPckt)
			# Add to analytics
			if flow.ID in self.pckt_counters:
				self.pckt_counters[flow.ID] += 1
			else:
				self.pckt_counters[flow.ID] = 1
			constants.system_analytics.log_flow_receive_rate(flow.ID, constants.system_EQ.currentTime, self.pckt_counters[flow.ID])


