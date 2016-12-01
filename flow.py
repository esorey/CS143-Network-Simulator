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
        
        self.windowSize = 75        # set in congestion control algorithm, initialize to 1 for RENO and FAST

        self.done = False

        # Number of data packets the flow needs to send
        self.num_packets = 10#math.ceil(data_amt * constants.MB_TO_BYTES / constants.DATA_PKT_SIZE)

        # Packet that we will send next, if this is equal to num_packets
        #   then we have attempted to send all packets. Packets should now be
        #   sent from dropped array, if there are no packets there, we are
        #   done. 

        self.pkt_entry_times = {}

        self.minRTT = 0.0
        self.numRTT = 0.0
        self.sumRTT = 0.0
        self.gamma = 0.5
        self.alpha = 15

        # TCP Reno and Fast TCP stuff
        self.unackPackets = []  
        self.packetsToSend = queue.Queue()
        self.expectedAckID = 0
        self.dupAckCtr = 0

        # TCP Reno Stuff Only 
        # Slow start threshold (max buffer size converted to data packets)
        self.sst = 64 * constants.KB_TO_BYTES / constants.DATA_PKT_SIZE

    ''' Sends a list of packets depending on the windowSize to the host. The
        function sends packets from dropped packets and new packets (gives 
        dropped packets priority). If there are not enough packets, the
        function sends whatever packets it can. '''

    def getACK(self, packetID, ackTime):

        print("Received acknowledgement %s" % packetID)
        print("Unacknowledged packets")
        print(self.unackPackets)

        if self.numRTT != 0:
            print("Avg RTT %f" % (self.sumRTT/self.numRTT))

        self.updateRTTandLogRTD(packetID, ackTime)

        if packetID == 0:
            print("First ack")
            print(constants.system_EQ.currentTime)

        if (len(self.unackPackets) > 0) and (packetID == self.unackPackets[0]):    # Packet wasn't dropped
            self.unackPackets.remove(packetID)  # Mark as acknowledged

        elif packetID in self.unackPackets:  # if we dropped some packet
            indofpkt = self.unackPackets.index(packetID)

            for i in range(indofpkt):
                PID = self.unackPackets[i]
                self.packetsToSend.put_nowait(PID)
                print("%s was lost" % PID)

            for i in range(indofpkt):
                del self.unackPackets[0]
                

        if len(self.unackPackets) == 0 and self.packetsToSend.empty(): # We're done with this flow...YAY!
            self.done = True
            print("Flow %s is done at time %s" % (self.ID, constants.system_EQ.currentTime))
            flow_done_event = Event(Event.flow_done, constants.system_EQ.currentTime, [constants.system_EQ.currentTime])
            constants.system_EQ.enqueue(flow_done_event)
            return

        elif len(self.unackPackets) == 0: # We're finished with this window; send a new one
            print("Send a new flow")
            self.flowSendNPackets(self.windowSize)


    ''' Functions for TCP Congestion Control ''' 

    def flowStart(self):
        if constants.cngstn_ctrl != constants.NO_CNGSTN_CTRL:
            print("Set window size to 1")
            self.windowSize = 1         # Initial window size for congestion control algorithms

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
            print("FLOW: Sending Packet with ID %s" % pktID )
            pkt = DataPacket(pktID, self.source, self.dest, self.ID)    # Create data packet
            pkt_list.append(pkt)                        # Add to list of packets to send to host

            if (len(self.unackPackets) == 0) and (i == 0):
                self.expectedAckID = pktID

            self.unackPackets.append(pktID)             # Add to list of packets in pipeline

            if pktID in self.pkt_entry_times:
                print("Resending a packet ID %s, only makes sense if packet was lost" % pktID)
            self.pkt_entry_times[pktID] = constants.system_EQ.currentTime

            # Calculate the time at which to timeout
            if self.numRTT == 0:
                if constants.cngstn_ctrl == constants.NO_CNGSTN_CTRL:
                    timeout_time = constants.system_EQ.currentTime + self.windowSize
                else:
                    timeout_time = constants.system_EQ.currentTime + self.windowSize * 10

            else:
                timeout_time = constants.system_EQ.currentTime + 1.5 * float(self.sumRTT)/self.numRTT

                # Create and enqueue timeout event
            timeout_ev = Event(Event.pckt_timeout, timeout_time, [pkt])
            constants.system_EQ.enqueue(timeout_ev)

        if constants.cngstn_ctrl == constants.FAST_TCP:
            # Enqueue an update FAST TCP W after certain time
            FAST_event = Event(Event.update_FAST, constants.system_EQ.currentTime + 20, [self.ID])
            constants.system_EQ.enqueue(FAST_event)


        # Send a "flow source send packets" event to send pkt_list
        event_to_send = Event(Event.flow_src_send_packets, constants.system_EQ.currentTime, [self.source, pkt_list])
        constants.system_EQ.enqueue(event_to_send)

        # Log that packets were sent
        constants.system_analytics.log_flow_send_rate(self.ID, len(pkt_list), constants.system_EQ.currentTime)



    # This will be called by event handler in the case of a packet timeout
    def handlePacketTimeout(self, packetID):
        if packetID in self.unackPackets:               # If packet is unacknowledged
            print("Got timeout event for packet %d" % packetID)
            self.unackPackets.remove(packetID)          # Remove packet from unacknowledged packets
            self.packetsToSend.put_nowait(packetID)     # Send packet again

            if constants.cngstn_ctrl != constants.NO_CNGSTN_CTRL:
                self.windowSize = 1                         # Update window size
                constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)

                if constants.cngstn_ctrl == constants.TCP_RENO:     # Update slow start threshold if necessary
                    self.sst = max(float(self.windowSize)/2, 1)

            if (len(self.unackPackets) == 0) and (self.packetsToSend.empty() == False):
                self.flowSendNPackets(self.windowSize)


    def fastTCP_updateW(self):
        # TODO: remove slow start threshold and confirm if average RTT or last RTT
        #       also fix potential divide by 0
        # Update self.windowSize based on Fast TCP

        if self.numRTT == 0:
            self.windowSize = 1
            constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)
        else:
            avgRTT = float(self.sumRTT)/float(self.numRTT)
            doubW = 2 * self.windowSize
            eqW = (1-self.gamma) * float(self.windowSize) + self.gamma * float(self.minRTT/avgRTT * self.windowSize + self.alpha)
            self.windowSize = min(doubW, eqW)
            constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)

        # Enqueue an event to update Fast TCP W after certain time
        FAST_event = Event(Event.update_FAST, constants.system_EQ.currentTime + 20, [self.ID])
        constants.system_EQ.enqueue(FAST_event)


    def TCPReno_updateW(self):
        if self.windowSize <= self.sst:     # Slow start phase
            self.windowSize += 1            # Increase window size with each ack
            constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)
        else:                               # Congestion avoidance phase
            self.windowSize = self.windowSize + 1.0/self.windowSize
            constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)

    def congestionGetAck(self, packetID, ackTime):
        self.updateRTTandLogRTD(packetID, ackTime)     # Log packet delay and 

        
        
        if packetID == self.expectedAckID:          # Received correct packet
            print("FLOW Received CORRECT acknowledgement %d" % packetID)
            if constants.cngstn_ctrl == constants.TCP_RENO:
                self.TCPReno_updateW()              # For TCP Reno, update W


            self.unackPackets.remove(packetID)          # Remove packet from unacknowledged packets list
            if len(self.unackPackets) != 0:
                self.expectedAckID = self.unackPackets[0]   # update expected packet 

            self.dupAckCtr = 0                      # No duplicate acks

        else:                                       # Received the wrong packet
            # MAYBE want to check if packetID is in self.unackPackets
            # NOTE: this works primarily for TCP Reno, not entirely sure how duplicate ACKS are processed
            #   in Fast TCP, but maybe we can keep it the same?
            print("FLOW Received DUPLICATE acknowledgement %d" % packetID)
            print("FLOW Duplicate Ack Ctr %d" % self.dupAckCtr)
            self.dupAckCtr += 1                     # Consider this a duplicate ack
            
            if constants.cngstn_ctrl == constants.TCP_RENO:
                self.TCPReno_updateW()              # Update W for TCP Reno

            if self.dupAckCtr == 2:                 # If we've received 3 duplicate ACKS, packet was dropped
                self.unackPackets.remove(packetID)  # Remove this packet from unacknowledged packets
                self.packetsToSend.put_nowait(packetID)     # Move it to packets to send
                self.dupAckCtr = 0                  # Reset counter for duplicate ACKS

                if constants.cngstn_ctrl == constants.TCP_RENO:
                    # Update window size to half because we dropped packet
                    self.windowSize = max(float(self.windowSize)/2, 1)      
                    constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)       
                    self.sst = self.windowSize      # If TCP Reno, then update slow start threshold
            else:
                self.unackPackets.remove(packetID)  # If we haven't received 3 duplicate acks yet, consider the packet that we  
                                                    #   actually received ack for as acknowledged

        print("FLOW Unacknowledged packets")
        print(self.unackPackets)
        print("FLOW Window Size %d" % self.windowSize)

        lengthPktsToSend = self.windowSize - len(self.unackPackets)     # Find number of packets to send
        self.flowSendNPackets(int(lengthPktsToSend))     # Send this many packets

        if len(self.unackPackets) == 0 and self.packetsToSend.empty(): # We're done with this flow...YAY!
            self.done = True
            print("Flow %s is done at time %s" % (self.ID, constants.system_EQ.currentTime))
            flow_done_event = Event(Event.flow_done, constants.system_EQ.currentTime, [constants.system_EQ.currentTime])
            constants.system_EQ.enqueue(flow_done_event)
            return


    def updateRTTandLogRTD(self, packetID, ackTime):
        constants.system_analytics.log_packet_RTD(self.ID, self.pkt_entry_times[packetID], ackTime)
        
        RTT = ackTime - self.pkt_entry_times[packetID]
        constants.system_analytics.log_flow_rate(self.ID, constants.DATA_PKT_SIZE, RTT, ackTime)

        if self.minRTT == 0:        # Save minimum RTT time
            self.minRTT = RTT
        elif RTT < self.minRTT:
            self.minRTT = RTT
        # CHECK: is average only over current time period or over whole time
        self.sumRTT += RTT
        self.numRTT += 1

        del self.pkt_entry_times[packetID]




