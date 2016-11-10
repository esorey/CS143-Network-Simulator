from flow import Flow
from packet import Packet
from link import Link

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

        elif self.event_type == Event.pckt_rcv:
        	rcv_host = self.data[0]
        	rcv_packet = self.data[1]

        	packet_type = rcv_packet.__class__.__name__

        	if packet_type == 'RoutingTablePacket':

        	elif packet_type == 'DataPacket':
        		rcv_host.receivePackets(rcv_packet)
        	elif packet_type == 'AckPacket':
        		# TODO: This won't work because in packets we only have flow ID and not actual flow :()
        		rcv_flow = rcv_packet.flowSendPackets()

        elif self.event_type == Event.link_free:
        	lnk = self.data[0]
        	lnk.handle_link_free()




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

