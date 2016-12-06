from event import Event
from flow import Flow 
from host import Host
from router import Router
import network_map as nwm 
import constants
import BellmanFord

def EventHandler(cur_event):
    if cur_event.event_type == Event.flow_start:
        print(nwm.flows)
        print(cur_event.data[0])
        cur_flow = nwm.flows[cur_event.data[0]]    # Convert flow ID into flow

        cur_flow.flowStart()

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
        ack_time = cur_event.data[2]

        if constants.cngstn_ctrl == constants.NO_CNGSTN_CTRL:
            cur_flow.getACK(packetID, ack_time)
        else:
            cur_flow.congestionGetAck(packetID, ack_time)

    elif cur_event.event_type == Event.pckt_send:
        cur_link = nwm.links[cur_event.data[0]]
        cur_pckt = cur_event.data[1]

        cur_link.enqueue_packet(cur_pckt)

    elif cur_event.event_type == Event.update_FAST:
        cur_flow = nwm.flows[cur_event.data[0]]
        cur_flow.fastTCP_updateW()

    elif cur_event.event_type == Event.pckt_timeout:
        cur_pckt = cur_event.data[0]
        cur_flow = nwm.flows[cur_pckt.owner_flow]
        cur_flow.handlePacketTimeout(cur_pckt.packet_id)

    elif cur_event.event_type == Event.bellman_ford: 
        newTime = cur_event.time + constants.BELLMAN_PERIOD
        print("TIME BF: " + str(newTime))
        bellman_event = Event(Event.bellman_ford, newTime, None)
        constants.system_EQ.enqueue(bellman_event)
        BellmanFord.runBellmanFord()

    elif cur_event.event_type == Event.flow_done:
        done_cnt = 0
        for flow in nwm.flows.keys():
            if nwm.flows[flow].done == True:
                done_cnt += 1
        if done_cnt == len(nwm.flows):
            constants.all_flows_done = True
            print("Time all flows done")
            print(cur_event.data[0])
