import constants
from packet import Packet
from packet import AckPacket, DataPacket
from event_queue import EventQueue
from event import Event
from analytics import Analytics
import network_map as nwm
from flow import Flow

class Host:
    '''
    A Host: end points of the network. Hosts send and receive data and 
    acknowledgement packets.
    '''
    def __init__(self, id, out_link):
        super(Host, self).__init__()
        self.id = id
        self.out_link = out_link    # ID of link connected to host

    def sendPackets(self, packetlist):
        '''
        Send packets across this host's link
        '''

        for pckt in packetlist:
            sendPckt = Event(Event.pckt_send, constants.system_EQ.currentTime,
                        [self.out_link, pckt])
            constants.system_EQ.enqueue(sendPckt)

    def receivePacket(self, pckt):
        '''
        Receive packets from the link and determine what to do 
        '''
        if type(pckt) is AckPacket:
            self.tellFlowAckReceived(pckt)

        elif type(pckt) is DataPacket:
            if type(nwm.flows[pckt.owner_flow]) is Flow:
                self.directlySendAck(pckt)
            else:
                self.tellFlowDataReceived(pckt)

            self.logReceivedDataPacket(pckt)


    def tellFlowAckReceived(self, ackpkt):
        '''
        Send the acknowledgment packet to the flow (through the event queue)
        to deal with packet losses/sending new packets.
        '''
        ackEvent = Event(Event.ack_rcv, constants.system_EQ.currentTime, 
                    [ackpkt.packet_id, ackpkt.owner_flow, ackpkt.timestamp])

        constants.system_EQ.enqueue(ackEvent)

    def tellFlowDataReceived(self, datapkt):
        '''
        If we're running any congestion control, tell the flow that a data
        packet was received so the flow can keep track of unreceived packets
        and send an ack for the next expected packet.
        '''
        flow_gets_data = Event(Event.flow_rcv_data, constants.system_EQ.currentTime,
                            [datapkt.owner_flow, datapkt])

        constants.system_EQ.enqueue(flow_gets_data)

    def directlySendAck(self, datapkt):
        '''
        If we're not running any congestion control, send an acknowledgement 
        for the exact packet we received.
        '''
        src = datapkt.destination_id        # Ack goes in opposite direction
        dest = datapkt.origin_id
        ackpckt = AckPacket(datapkt.packet_id, src, dest, datapkt.owner_flow,
                    datapkt.timestamp)

        sendAckEvent = Event(Event.pckt_send, constants.system_EQ.currentTime,
                        [self.out_link, ackpckt])

        constants.system_EQ.enqueue(sendAckEvent)
