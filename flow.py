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
        
        self.windowSize = 25        # set in congestion control algorithm, initialize to 1 for RENO and FAST
        self.currACK = -1            # the last acknowledged packet ID
        self.droppedPackets = []    # dropped packets (IDs)

        # Number of data packets the flow needs to send
        self.num_packets = math.ceil(data_amt * constants.MB_TO_BYTES / constants.DATA_PKT_SIZE)

        # Packet that we will send next, if this is equal to num_packets
        #   then we have attempted to send all packets. Packets should now be
        #   sent from dropped array, if there are no packets there, we are
        #   done. 
        self.currPCK = 0

        self.pkt_entry_times = {}

        self.minRTT = 0
        self.numRTT = 0
        self.sumRTT = 0
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



    def congestionControlAlg(pcktReceived, pcktSent): 
        # run congestion control alg
        # TCP Reno
        # FAST-TCP
        self.windowSize = 100
        constants.system_analytics.log_window_size(self.ID, constats.system_EQ.currentTime, self.windowSize)
        #return self.windowSize

    ''' Sends a list of packets depending on the windowSize to the host. The
        function sends packets from dropped packets and new packets (gives 
        dropped packets priority). If there are not enough packets, the
        function sends whatever packets it can. '''
    def flowSendPackets(self): 
        packets_to_send = []
        if constants.debug: 
            print("Currently in Flow send Packets: ")
            print("dropped Packets: %s, WindowSize: %s" % (self.droppedPackets, self.windowSize))

        if self.currACK == self.num_packets - 1 and self.droppedPackets == []: # We're done with this flow...YAY!
            return
        # Send ALL packets from dropped packets
        if len(self.droppedPackets) >= self.windowSize:
            packets_to_send = self.generateDataPackets(self.droppedPackets[:(self.windowSize)])

        # send SOME (could be 0) packets from dropped packets and SOME from new packets
        else:
            # Generate and get ready to send packets from dropped packets
            getPcktsToSend = self.generateDataPackets(self.droppedPackets)
            packets_to_send.extend(getPcktsToSend)

            # Generate and get ready to send new packets
            temp = self.windowSize - len(self.droppedPackets)

            # If we reach the end of all the packets to send
            if self.currPCK + temp >= self.num_packets:
                end_pckt_index = self.num_packets + 1   # Indicate we have sent all packets
            else:   # Otherwise
                end_pckt_index = self.currPCK + temp
            if constants.debug: print("Generating data packets in range: %s to %s" %(self.currPCK, end_pckt_index))
            getPcktsToSend = self.generateDataPackets(range(self.currPCK, end_pckt_index))
            packets_to_send.extend(getPcktsToSend)

            # Update the current packet we want to send
            self.currPCK = end_pckt_index

        # Enqueue event that will tell hosts to send packets
        if constants.debug: print("Event is getting enqueued...")
        event_to_send = Event(Event.flow_src_send_packets, constants.system_EQ.currentTime, [self.source, packets_to_send])
        constants.system_EQ.enqueue(event_to_send)
        if constants.debug: 
            print("\tevent type: %s" % event_to_send.event_type)
            print("\tevent time: %s" % event_to_send.time)
            print("\tevent data: %s" % event_to_send.data)
            print("\tLen of eventlist: %s" % len(constants.system_EQ.eventList))

        constants.system_analytics.log_flow_send_rate(self.ID, self.windowSize, constants.system_EQ.currentTime)

    ''' When a host receives an acknowledgement packet it will call this 
        function for the flow to update what packets have been received. The 
        flow deals with packet loss.'''
    def getACK(self, packetID, ackTime):

        self.updateRTTandLogRTD(packetID, ackTime)

        if packetID == 0:
        	print("First ack")
        	print(constants.system_EQ.currentTime)
        
        if packetID  > self.currACK+1:  # if we dropped a packet
            # Add the packets we dropped to the droppedPackets list
            self.droppedPackets.append(range(self.currACK+1, packetID))
            self.currACK += 1
        elif packetID < self.currACK:   # If we receive an ack for packet that was dropped
            # Remove this packet from list of dropped packets
            self.droppedPackets.remove(packetID)
        else:
            self.currACK += 1   # We received correct packet, increment currACK

        if (self.currACK - len(self.droppedPackets) + 1) % self.windowSize == 0: # We're finished with this window; send a new one
            self.flowSendPackets()

    ''' Generates data packets with the given IDs and returns a list of the 
        packets. '''
    def generateDataPackets(self, listPacketIDs):
        packets_list = []
        if constants.debug: print("Generating Data Packets...")
        for PID in listPacketIDs:
            pckt = DataPacket(PID, self.source, self.dest, self.ID)
            packets_list.append(pckt)
            if pckt.packet_id not in self.pkt_entry_times:
                self.pkt_entry_times[pckt.packet_id] = constants.system_EQ.currentTime

        return packets_list

''' Functions for TCP Congestion Control ''' 
# TODO: Some small TODOs listed below

    def flowStartTCP(self):
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
            pkt = DataPacket(pktID, self.source, self.dest, self.ID)    # Create data packet
            pkt_list.append(pkt)                        # Add to list of packets to send to host
            self.unackPackets.append(pktID)             # Add to list of packets in pipeline

            # Calculate the time at which to timeout
            if self.sumRTT == 0:
                timeout_time = constants.system_EQ.currentTime + constants.TIMEOUT_TIME
            else:
                timeout_time = constants.system_EQ.currentTime + 1.5 * float(self.sumRTT)/self.minRTT

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
        constants.system_analytics.log_flow_send_rate(self.ID, self.windowSize, constants.system_EQ.currentTime)



    # This will be called by event handler in the case of a packet timeout
    def handlePacketTimeout(self, packetID):
        if packetID in self.unackPackets:               # If packet is unacknowledged
            self.unackPackets.remove(packetID)          # Remove packet from unacknowledged packets
            self.packetsToSend.put_nowait(packetID)     # Send packet again

            self.windowSize = 1                         # Update window size
            constants.system_analytics.log_window_size(self.ID, constants.system_EQ.currentTime, self.windowSize)

            if constants.cngstn_ctrl == constants.TCP_RENO:     # Update slow start threshold if necessary
                self.sst = max(float(self.windowSize)/2, 1)

    def fastTCP_updateW(self):
        # TODO: remove slow start threshold and confirm if average RTT or last RTT
        #       also fix potential divide by 0
        # Update self.windowSize based on Fast TCP 
        if self.windowSize <= self.sst:
        	self.windowSize += 1
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
            if constants.cngstn_ctrl == constants.TCP_RENO:
                self.TCPReno_updateW()              # For TCP Reno, update W

            self.unackPackets.remove(packetID)          # Remove packet from unacknowledged packets list
            self.expectedAckID = self.unackPackets[0]   # update expected packet 
            self.dupAckCtr = 0                      # No duplicate acks

        else:                                       # Received the wrong packet
            # NOTE: this works primarily for TCP Reno, not entirely sure how duplicate ACKS are processed
            #   in Fast TCP, but maybe we can keep it the same?
            self.dupAckCtr += 1                     # Consider this a duplicate ack
            
            if constants.cngstn_ctrl == constants.TCP_RENO:
                self.TCPReno_updateW()              # Update W for TCP Reno

            if self.dupAckCtr == 3:                 # If we've received 3 duplicate ACKS
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

        lengthPktsToSend = self.windowSize - len(self.unackPackets)     # Find number of packets to send
        self.flowSendNPackets(lengthPktsToSend)     # Send this many packets

    def updateRTTandLogRTD(self, packetID, ackTime):
        constants.system_analytics.log_packet_RTD(self.ID, self.pkt_entry_times[packetID], ackTime)
        
        RTT = ackTime - self.pkt_entry_times[packetID]

        if self.minRTT == 0:        # Save minimum RTT time
            self.minRTT = RTT
        elif RTT < minRTT:
            self.minRTT = RTT
        # CHECK: is average only over current time period or over whole time
        self.sumRTT += RTT
        self.numRTT += 1

        del self.pkt_entry_times[packetID]




