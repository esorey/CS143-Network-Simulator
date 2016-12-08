from event import Event
from flow import Flow 
from flowReno import FlowReno
from host import Host
from router import Router
import network_map as nwm 
import constants
import BellmanFord

def EventHandler(cur_event):
    ''' 
    Based on the current event's event type, the event handler will perform
    different functions. 
    '''
    if cur_event.event_type == Event.flow_start:    # Start the flow
        print(nwm.flows)
        print(cur_event.data[0])
        cur_flow = nwm.flows[cur_event.data[0]]    # Convert flow ID into flow
        cur_flow.flowStart()

    elif cur_event.event_type == Event.pckt_rcv:    
        # notify host or router of packet it has received
        if cur_event.data[0][0] == 'H':
            rcv_host = nwm.hosts[cur_event.data[0]] # Convert host ID to host
            rcv_packet = cur_event.data[1]
            rcv_host.receivePacket(rcv_packet)
        elif cur_event.data[0][0] == 'R':
            rcv_router = nwm.routers[cur_event.data[0]]
            rcv_packet = cur_event.data[1]
            rcv_router.receivePackets(rcv_packet)

    elif cur_event.event_type == Event.link_free:   
        # indicate the link is free to send more packets across it
        lnk = nwm.links[cur_event.data[0]]
        lnk.handle_link_free()

    elif cur_event.event_type == Event.flow_send_packets:
        # Host is assigned a list of packets to send
        src_host = nwm.hosts[cur_event.data[0]]
        pkts_to_send = cur_event.data[1]
        if constants.debug: 
            print("Event Handler - Sending packets: ")
            print("Source Host: %s" % src_host)
            print("Packets to Send: %s" % pkts_to_send)

        src_host.sendPackets(pkts_to_send)

    elif cur_event.event_type == Event.ack_rcv:
        # Log the appropriate acknowledgment received in the correct flow
        if constants.debug: print("ACK data: %s" % cur_event.data)
        cur_flow = nwm.flows[cur_event.data[1]]
        packetID = cur_event.data[0]
        ack_time = cur_event.data[2]
        cur_flow.getACK(packetID, ack_time)


    elif cur_event.event_type == Event.pckt_send:
        # Enqueues a packet onto cur_link's buffer
        cur_link = nwm.links[cur_event.data[0]]
        cur_pckt = cur_event.data[1]

        cur_link.enqueue_packet(cur_pckt)

    elif cur_event.event_type == Event.update_FAST:
        # Fast TCP window size is updated peridically. 
        cur_flow = nwm.flows[cur_event.data[0]]
        cur_flow.updateW()

    elif cur_event.event_type == Event.pckt_timeout:
        # Instruct the flow of the event to handle the packet timeout
        cur_pckt = cur_event.data[0]
        cur_flow = nwm.flows[cur_pckt.owner_flow]
        cur_flow.handlePacketTimeout(cur_pckt.packet_id)

    elif cur_event.event_type == Event.bellman_ford: 
        # Run Bellman Ford and enqueue the next instance of bellman ford
        newTime = cur_event.time + constants.BELLMAN_PERIOD
        bellman_event = Event(Event.bellman_ford, newTime, None)
        constants.system_EQ.enqueue(bellman_event)
        BellmanFord.runBellmanFord()

    elif cur_event.event_type == Event.flow_done:
        # count how many flows are finished. Main will run analytics when all
        # flows are done
        done_cnt = 0
        for flow in nwm.flows.keys():
            if nwm.flows[flow].done == True:
                done_cnt += 1
        if done_cnt == len(nwm.flows):
            constants.all_flows_done = True
            print("Time all flows done")
            print(cur_event.data[0])

    elif cur_event.event_type == Event.flow_rcv_data:
        # indicate to the appropriate flow that it has received a data packet
        cur_flow = nwm.flows[cur_event.data[0]]
        cur_pkt = cur_event.data[1]
        cur_flow.flowReceiveDataPacket(cur_pkt)
