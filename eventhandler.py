from event import Event
from flow import Flow 
from host import Host 

def EventHandler(cur_event):
    if cur_event.event_type == Event.flow_start:
        cur_flow = cur_event.data[0]
    	cur_flow.flowSendPackets()

    elif cur_event.event_type == Event.pckt_rcv:
    	rcv_host = cur_event.data[0]
    	rcv_packet = cur_event.data[1]
    	rcv_host.receivePacket(rcv_packet)

    elif cur_event.event_type == Event.link_free:
    	lnk = cur_event.data[0]
    	lnk.handle_link_free()

    elif cur_event.event_type == Event.flow_src_send_packets:
        src_host = cur_event.data[0]
        pkts_to_send = cur_event.data[1]

        src_host.sendPackets(pkts_to_send)

    elif cur_event.event_type == Event.ack_rcv:
        cur_flow = cur_event.data[0]
        packetID = cur_event.data[1]

        cur_flow.getACK(packetID)

    elif cur_event.event_type == Event.pckt_send:
        cur_link = cur_event.data[0]
        cur_pckt = cur_event.data[1]

        cur_link.enqueue_packet(cur_pckt)

    ''' Dealing with events:
        pckt_rcv:
            needs: host/router, packet, time
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
                this is called by a host when it realizes it has
                received an ack

        pckt_send:
            needs: link, packet
                call link.enqueue_packet(packet)'''
