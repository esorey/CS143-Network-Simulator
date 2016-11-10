from enum import Enum

class event:
	class event_type(Enum):
		pckt_rcv = 1
		pckt_send = 2
		flow_start = 3
		link_inuse = 4
		link_free = 5
	def __init__(self, ev_type, time):
		'''
			event_type - enumerated type that indicates what sort of event 
						 this is 
			time - integer, when the event occurs
		'''
		self.event_type = ev_type
		self.time = time
		'''
		pckt_rcv = origin, destination, flowID
		pckt_send = origin, destination, flowID
		flow_start = flowID
		link_inuse = flowID
		link_free = flowID
		'''

	def getTime(self):
		return self.time

	def getEventType(self):
		return self.event_type

	''' Dealing with events:
		pckt_rcv:
			needs: host, packet, time
				if data packet: call host.receivePackets(packet)
				if ack packet: call flow.getAck(packetID)
				if routing table packet: 
		flow_start:
			needs: flow, time
				call flow.flowSendPackets()

		link_free:
			needs: link, time
				call handle_link_free
		
	#		if host re