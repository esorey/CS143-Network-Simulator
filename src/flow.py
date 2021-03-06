from event import Event
from packet import DataPacket
from event_queue import EventQueue
import constants
import math
import queue

class Flow:
    """Flow Class"""
    def __init__(self, ID, source, destination, data_amt, start):
        self.ID = ID                # Flow ID

        self.source = source        # Source host
        self.dest = destination     # Destination host
        self.data_amt = data_amt    # Size of data in MB
        self.start = start          # Time at which flow begins
        
        self.windowSize = 75        # set in congestion control algorithm
                                    # initialize to 1 for RENO and FAST

        self.done = False

        # Number of data packets the flow needs to send
        self.num_packets = math.ceil(data_amt * constants.MB_TO_BYTES /\
            constants.DATA_PKT_SIZE)


        # TCP Reno and Fast TCP stuff
        self.unackPackets = []  
        self.packetsToSend = queue.Queue()
        self.expectedAckID = 0




    def getACK(self, packetID, ackTime):
        ''' 
        Sends a list of packets depending on the windowSize to the host. The
        function sends packets from dropped packets and new packets (gives 
        dropped packets priority). If there are not enough packets, the
        function sends whatever packets it can. 
        '''
        #print("Received acknowledgement %s" % packetID)
        #print("Unacknowledged packets")
        #print(self.unackPackets)

        #if self.numRTT != 0:
        #    print("Avg RTT %f" % (self.sumRTT/self.numRTT))

        self.updateRTTandLogRTD(ackTime)

        #if packetID == 0:
        #    print("First ack")
        #    print(constants.system_EQ.currentTime)

        # Packet wasn't dropped
        if (len(self.unackPackets) > 0) and (packetID == self.unackPackets[0]):    
            self.unackPackets.remove(packetID)  # Mark as acknowledged

        elif packetID in self.unackPackets:  # if we dropped some packet
            indofpkt = self.unackPackets.index(packetID)

            for i in range(indofpkt):
                PID = self.unackPackets[i]
                self.packetsToSend.put_nowait(PID)
                #print("%s was lost" % PID)

            for i in range(indofpkt):
                del self.unackPackets[0]
                
        # The flow is finished 
        if len(self.unackPackets) == 0 and self.packetsToSend.empty(): 
            self.done = True
            flow_done_event = Event(Event.flow_done, \
                constants.system_EQ.currentTime, \
                [constants.system_EQ.currentTime])
            constants.system_EQ.enqueue(flow_done_event)
            return

        # We're finished with this window
        elif len(self.unackPackets) == 0: 
            #print("Send a new flow")
            # send a new one
            self.flowSendNPackets(self.windowSize)


    ''' Functions for TCP Congestion Control ''' 

    def flowStart(self):
        # Initialize packetsToSend queue to contain all the packets
        for pkt_ID in range(self.num_packets):
            self.packetsToSend.put_nowait(pkt_ID)

        # Send initial packets (windowSize will likely be 1)
        self.flowSendNPackets(self.windowSize)

    # Sends N packets from teh packetsToSendQueue
    def flowSendNPackets(self, N):
        pkt_list = []       # list of packets to send

        for i in range(N):
            if self.packetsToSend.empty():
                break

            pktID = self.packetsToSend.get_nowait()     # Get Packet to send
            #print("FLOW: Sending Packet with ID %s" % pktID )
            pkt = DataPacket(pktID, self.source, self.dest, self.ID, \
                constants.system_EQ.currentTime)    # Create data packet
            pkt_list.append(pkt)    # Add to list of packets to send to host

            if (len(self.unackPackets) == 0) and (i == 0):
                self.expectedAckID = pktID

            self.unackPackets.append(pktID) # Add to list of packets in pipeline

            # Calculate the time at which to timeout
            if self.numRTT == 0:
                timeout_time = constants.system_EQ.currentTime + self.windowSize
            else:
                timeout_time = constants.system_EQ.currentTime \
                    + constants.TIMEOUT_TIME

            # Create and enqueue timeout event
            timeout_ev = Event(Event.pckt_timeout, timeout_time, [pkt])
            constants.system_EQ.enqueue(timeout_ev)


        # Send a "flow send packets" event to send pkt_list
        event_to_send = Event(Event.flow_send_packets, \
            constants.system_EQ.currentTime, [self.source, pkt_list])
        constants.system_EQ.enqueue(event_to_send)

        # Log that packets were sent
        constants.system_analytics.log_flow_send_rate(self.ID, \
            len(pkt_list) * constants.DATA_PKT_SIZE, \
            constants.system_EQ.currentTime)



    # This will be called by event handler in the case of a packet timeout
    def handlePacketTimeout(self, packetID):
        if packetID in self.unackPackets:       # If packet is unacknowledged
            #print("Got timeout event for packet %d" % packetID)
            # Remove packet from unacknowledged packets
            self.unackPackets.remove(packetID)          
            self.packetsToSend.put_nowait(packetID)     # Send packet again

            # If the packet we timed out was the next packet we were 
            # expecting (and we are still expecting more packets) 
            # then update the expected ack ID
            if packetID == self.expectedAckID and len(self.unackPackets) != 0:
                self.expectedAckID = self.unackPackets[0]

            if (len(self.unackPackets) == 0) and \
                (self.packetsToSend.empty() == False):
                self.flowSendNPackets(self.windowSize)


    def updateRTTandLogRTD(self, ackTime):
        RTT = constants.system_EQ.currentTime - ackTime
        constants.system_analytics.log_packet_RTD(self.ID,
            RTT, constants.system_EQ.currentTime)



