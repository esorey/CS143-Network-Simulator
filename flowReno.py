from event import Event
from packet import DataPacket
from packet import AckPacket
from event_queue import EventQueue
import constants
import math
import queue


class FlowReno():
    """Flow Class"""
    def __init__(self, ID, source, destination, data_amt, start):
        self.ID = ID                # Flow ID

        self.source = source        # Source host
        self.dest = destination     # Destination host
        self.data_amt = data_amt    # Size of data in MB
        self.start = start          # Time at which flow begins
        
        self.windowSize = 1.0       # set in congestion control algorithm
                                    # initialize to 1 for RENO and FAST

        self.done = False

        # Number of data packets the flow needs to send
        self.num_packets = math.ceil(data_amt * constants.MB_TO_BYTES / \
            constants.DATA_PKT_SIZE)

        # Packet that we will send next, if this is equal to num_packets
        #   then we have attempted to send all packets. Packets should now be
        #   sent from dropped array, if there are no packets there, we are
        #   done. 

        self.minRTT = 0.0
        self.numRTT = 0.0
        self.sumRTT = 0.0
        self.gamma = 0.5
        self.alpha = 15

        # TCP Reno and Fast TCP stuff
        self.unackPackets = [] 
        self.last_unackd = 0  
        self.dupAckCtr = 0

        # TCP Reno Stuff Only 
        # Slow start threshold (max buffer size converted to data packets)
        self.sst = 1000000

        # Holds packets the source has not yet received
        self.unreceivedpackets = []

        self.fast_recovery = False
        self.fast_recovery_pkts = -1    # Max packet received in fast recovery
        self.timeouts_to_cancel = []

        self.timeout_ctr = 0

    def flowStart(self):
        # Initialize unreceived packets to contain all the packets in order 
        for pkt_ID in range(self.num_packets):
            self.unreceivedpackets.append(pkt_ID)

        # Send initial packets
        self.flowSendNPackets(math.ceil(self.windowSize))

    def flowReceiveDataPacket(self, data_packet):
        if data_packet.packet_id in self.unreceivedpackets:
            self.unreceivedpackets.remove(data_packet.packet_id)
        # Update expected ACK ID
        if len(self.unreceivedpackets) > 0:
            next_expected_packet = self.unreceivedpackets[0]  
        else:
            next_expected_packet = self.num_packets

        # Create and send an acknowledgement packet
        ackpckt = AckPacket(next_expected_packet, self.dest, self.source, \
            self.ID, data_packet.timestamp)
        self.sendPacket(ackpckt)

    # Sends N new packets starting from the expected ack packet
    def flowSendNPackets(self, N):
        num_packets_sent = 0       # list of packets to send

        for PID in range(self.last_unackd, self.last_unackd+N):
            if PID >= self.num_packets:
                break

            if PID not in self.unackPackets:    # Only send new packets
                pkt = DataPacket(PID, self.source, self.dest, self.ID,\
                    constants.system_EQ.currentTime)    # Create data packet
                self.sendPacket(pkt)
                num_packets_sent += 1

        # Log that packets were sent
        constants.system_analytics.log_flow_send_rate(self.ID, \
            num_packets_sent * constants.DATA_PKT_SIZE, \
            constants.system_EQ.currentTime)



    # This will be called by event handler in the case of a packet timeout
    def handlePacketTimeout(self, packetID):
        # If packet is unacknowledged
        if packetID in self.unackPackets and\
             packetID not in self.timeouts_to_cancel:   
            #print("Got timeout event for packet %d" % packetID)
            self.timeout_ctr += 1
            # Remove packet from unacknowledged packets
            self.unackPackets.remove(packetID)          
            self.sst = max(float(self.windowSize)/2.0, 1.0)
            self.windowSize = 1.0
            self.dupAckCtr = 0

            self.unackPackets.clear()
            self.fast_recovery = False
            self.fast_recovery_pkts = -1

            self.flowSendNPackets(math.ceil(self.windowSize))
  
            self.logWindowSize()

        if packetID in self.timeouts_to_cancel:
            self.timeouts_to_cancel.remove(packetID)


    def updateW(self):
        if self.fast_recovery:
            self.fast_recovery = False
            self.windowSize = math.ceil(self.sst)
            self.duplicate_counter = 0
        else:
            if self.windowSize <= self.sst:     # Slow start phase
                self.windowSize += 1.0     # Increase window size with each ack
                
            else:                          # Congestion avoidance phase
                self.windowSize = float(self.windowSize) + \
                    1.0 / float(math.floor(self.windowSize))

        self.logWindowSize()

    def getACK(self, packetID, ackTime):
        self.updateRTTandLogRTD(ackTime)
        #print("Flow received an acknowledgement with ID %d" %packetID)
        #print("Last Unack'd: %d" %self.last_unackd)


        if packetID > self.last_unackd:
            self.last_unackd = packetID

            if self.last_unackd == self.num_packets:
                self.unackPackets.clear()
                self.done = True
                #print("Flow %s is done at time %s" % (self.ID, constants.system_EQ.currentTime))
                #print("Number of timeouts %d" %self.timeout_ctr)
                flow_done_event = Event(Event.flow_done, \
                    constants.system_EQ.currentTime, \
                    [constants.system_EQ.currentTime])
                constants.system_EQ.enqueue(flow_done_event)
                return

            # If we're in the fast recovery phase and we received a 
            # packet request for a packet in this window, then send it
            if self.fast_recovery and self.last_unackd <= self.fast_recovery_pkts:
                pkt = DataPacket(self.last_unackd, self.source, self.dest, \
                    self.ID, constants.system_EQ.currentTime)
                self.timeouts_to_cancel.append(self.last_unackd)
                self.sendPacket(pkt)

                num_removed = self.removeAckdPackets()
                self.dupAckCtr -= num_removed

            else:   # Otherwise we are sending from a new window
                self.updateW()
                self.removeAckdPackets()
                
            lengthPktsToSend = math.ceil(self.getWindowSize()) -\
                len(self.unackPackets)
            self.flowSendNPackets(int(lengthPktsToSend))

        elif packetID == self.last_unackd:
            self.dupAckCtr += 1
            lengthPktsToSend = math.ceil(self.getWindowSize()) - \
                len(self.unackPackets)
            self.flowSendNPackets(lengthPktsToSend)

            if self.windowSize > self.sst and not self.fast_recovery\
                and self.dupAckCtr == 3:
                self.sst = max(float(self.windowSize)/2.0, 1.0)
                self.windowSize = math.ceil(self.sst)
                self.logWindowSize()
                self.fast_recovery = True
                self.fast_recovery_pkts = max(self.unackPackets)

                pkt = DataPacket(self.last_unackd, self.source, self.dest, \
                    self.ID, constants.system_EQ.currentTime)
                self.timeouts_to_cancel.append(packetID)
                self.sendPacket(pkt)

        if self.last_unackd == self.num_packets: # We're done with this flow...YAY!
            self.unackPackets.clear()
            self.done = True
            #print("Flow %s is done at time %s" % (self.ID, constants.system_EQ.currentTime))
            flow_done_event = Event(Event.flow_done, \
                constants.system_EQ.currentTime, \
                [constants.system_EQ.currentTime])
            constants.system_EQ.enqueue(flow_done_event)
            return


    def updateRTTandLogRTD(self, ackTime):
        RTT = constants.system_EQ.currentTime - ackTime
        constants.system_analytics.log_packet_RTD(self.ID,
            RTT, constants.system_EQ.currentTime)

        if self.minRTT == 0:        # Save minimum RTT time
            self.minRTT = RTT
        elif RTT < self.minRTT:
            self.minRTT = RTT
        # CHECK: is average only over current time period or over whole time
        self.sumRTT += RTT


    def sendPacket(self, pkt):
        if type(pkt) is DataPacket:
            #print("Sending DATA packet ID %d" %pkt.packet_id)
            self.unackPackets.append(pkt.packet_id)

            # Calculate the time at which to timeout
            timeout_time = constants.system_EQ.currentTime \
                + constants.TIMEOUT_TIME

            # Create and enqueue timeout event
            timeout_ev = Event(Event.pckt_timeout, timeout_time, [pkt])
            constants.system_EQ.enqueue(timeout_ev)
            event_to_send = Event(Event.flow_send_packets, \
                constants.system_EQ.currentTime, [self.source, [pkt]])

        else:
            event_to_send = Event(Event.flow_send_packets, \
                constants.system_EQ.currentTime, [self.dest, [pkt]])
            #print("Sending ACK packet ID %d" %pkt.packet_id)

        
        constants.system_EQ.enqueue(event_to_send)

    def logWindowSize(self):
        constants.system_analytics.log_window_size(self.ID, \
            constants.system_EQ.currentTime, self.windowSize)

    def removeAckdPackets(self):
        cur_length = len(self.unackPackets)
        for PID in self.unackPackets:
            if PID < self.last_unackd:
                self.unackPackets.remove(PID)

        return (len(self.unackPackets)-cur_length)

    def getWindowSize(self):
        if self.fast_recovery:
            ret_WS = self.windowSize + self.dupAckCtr
        else:
            ret_WS = self.windowSize

        return ret_WS





