from event import Event
from flow import Flow 
from host import Host
from router import Router
import network_map as nwm 

def EventHandler(cur_event):
    if cur_event.event_type == Event.flow_start:
        print(nwm.flows)
        print(cur_event.data[0])
        cur_flow = nwm.flows[cur_event.data[0]]    # Convert flow ID into flow
        cur_flow.flowSendPackets()

    elif cur_event.event_type == Event.pckt_rcv:
        if cur_event.data[0][0] == 'H':
            rcv_host = nwm.hosts[cur_event.data[0]]                # Convert host ID to host
            rcv_packet = cur_event.data[1]
            rcv_host.receivePacket(rcv_packet)
        elif cur_event.data[0][0] == 'R':
            rcv_router = nwm.routers[cur_event.data[0]]
            rcv_packet = cur_event.data[1]
            rcv_router.receivePackets(rcv_packet)

    elif cur_event.event_type == Event.link_free:
        lnk = nwm.links[cur_event.data[0]]
        lnk.handle_link_free()

    elif cur_event.event_type == Event.flow_src_send_packets:
        src_host = nwm.hosts[cur_event.data[0]]
        pkts_to_send = cur_event.data[1]
        if constants.debug: 
            print("Event Handler - Sending packets: ")
            print("Source Host: %s" % src_host)
            print("Packets to Send: %s" % pkts_to_send)

        src_host.sendPackets(pkts_to_send)

    elif cur_event.event_type == Event.ack_rcv:
        if constants.debug: print("ACK data: %s" % cur_event.data)
        cur_flow = nwm.flows[cur_event.data[1]]
        packetID = cur_event.data[0]

        cur_flow.getACK(packetID)

    elif cur_event.event_type == Event.pckt_send:
        cur_link = nwm.links[cur_event.data[0]]
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
