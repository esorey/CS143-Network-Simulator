from enum import Enum
from flow import Flow

class Event:
	flow_start = 1
	pckt_rcv = 2
	link_free = 3

	def __init__(self, ev_type, time, data):
		'''
			event_type - enumerated type that indicates what sort of event 
						 this is 
			time - integer, when the event occurs
			data - information required for the events (list of varying size
				   depending on event)
				   flow_start data: [flow]
				   pckt_rcv data: [host, packet]
				   link_free data: [link]
		'''
		self.event_type = ev_type
		self.time = time
		self.data = data
    
    def handleEvent(self):
        if self.event_type == Event.flow_start:
        	(self.data[0]).flowSendPackts()

        elif self.event_type == Event.

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
				call handle_link_free '''

