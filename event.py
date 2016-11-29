class Event:
	flow_start = 1
	pckt_rcv = 2
	link_free = 3
	flow_src_send_packets = 4
	ack_rcv = 5
	pckt_send = 6
	update_FAST = 7
	update_RENO = 8

	def __init__(self, ev_type, time, data):
		'''
			event_type - enumerated type that indicates what sort of event 
						 this is 
			time - integer, when the event occurs
			data - information required for the events (list of varying size
				   depending on event, see below for details.
		'''
		self.event_type = ev_type
		self.time = time
		self.data = data
		
		''' Dealing with events:
        pckt_rcv:
            needs: host, packet, time
                changed to calling receive packet
                if data packet: call host.receivePackets(packet)
                if ack packet: call flow.getAck(packetID)
                if routing table packet: 
        flow_start:
            needs: flow, time
                call flow.flowSendPackets()

        link_free:
            needs: link, time
                call handle_link_free

        flow_src_send_packets
            needs: host, packets to send (list)

        ack_rcv:
            needs: packet ID and flow ID 
                call flow.getACK

        pckt_send:
        	needs: link, packet
        		call link.enqueue_packet(packet)'''
