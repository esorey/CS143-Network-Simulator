import constants
import matplotlib.pyplot as plt
import collections

debug = False
class Analytics:

    def __init__(self, outFile):
        time_step = []      # Holds the time step (from global time variable)
                            #   at which data was recorded
                            # Do we need this?

        '''
        The data types below are dictionaries with:
            keys: Link IDs (strings)
            values: list of tuples containing link information specific to
                the dictionary and the associated time
        '''
        self.link_buff_occupancy = {}    # Stores buffer occupancy (number of
                                    #   packes in the buffer at the time).
                                    #   Updated any time packet is added to
                                    #   any link buffer
        self.link_packet_lost = {}       # Stores number of packets lost. Updated
                                    #   every time a packet is added to a
                                    #   full buffer
        self.link_flow_rate = {}         # Stores number of packets sent over a
                                    #   link. Updates every time a packet 
                                    #   receive event occurs.

        # Still need per flow: send/receive rate, packet round trip delay
        self.flow_rate = {}
        self.flow_send_rate = {}
        self.flow_packet_RTD = {}
        self.flow_window_size = {}

        # and per host: send/receive rate
        self.host_send_rate = {}
        self.host_receive_rate = {}

        # not sure how to implement/compute these
        # file that we are writing to
        self.outFile = outFile

    '''This logs that this link dropped a packet at the current time.'''
    def log_dropped_packet(self, linkID, currTime):
        if linkID in self.link_packet_lost:
            self.link_packet_lost[linkID].append(currTime)
        else:
            self.link_packet_lost[linkID] = [currTime]

    ''' Arrange dictionary by linkID followed by currTime'''
    def log_buff_occupancy(self, linkID, currTime, buffOccupancy):
        if linkID in self.link_buff_occupancy:
            self.link_buff_occupancy[linkID].append((currTime, buffOccupancy))
        else:
            self.link_buff_occupancy[linkID] = [(currTime, buffOccupancy)]

    ''' link flow rate calculation stores number of packets properly
    sent through flow in the span between current time to previous time'''
    # changed to flowID because I think this should be flow? i.e. when a flow
    # decides to put first packet in iink buffer to when host receives last
    # packet
    def log_flow_rate(self, flowID, numBytes, currTime, prevTime): 
        rate = numBytes/((currTime - prevTime) * constants.MB_TO_BYTES)
        if flowID in self.flow_rate:
            self.flow_rate[flowID].append((currTime, rate))
        else:
            self.flow_rate[flowID] = [(currTime, rate)]
        if debug:
            print(rate)


    '''flow send rate should read the updating window sizes, which
    decide the send rate of each flow, and update it to the relevant time'''
    def log_flow_send_rate(self, flowID, windowSize, currTime):
        if flowID in self.flow_send_rate:
            self.flow_send_rate[flowID].append((windowSize, currTime))
        else:
            self.flow_send_rate[flowID] = [(windowSize, currTime)]

    '''flow receive rate should read the time that the packet was received
    at the host and add it to the corresponding packet in the flow'''
    def log_flow_receive_rate(self, flowID, currTime, receive_order):
        if flowID in self.flow_send_rate:
            # If the number of the received packet is greater than window size,
            #   there is an issue
            if debug: print(self.flow_send_rate[flowID])
            if receive_order <= self.flow_send_rate[flowID][-1][0]:
                # Log the flow rate
                self.log_flow_rate(flowID, constants.DATA_PKT_SIZE, currTime, self.flow_send_rate[flowID][-1][1])

    # time start is queued in immediately
    # time end is when the ack with the right packetID is sent
    # get the time for that ack in event queue
    def log_packet_RTD(self, packetID, timeStart, timeEnd):
        self.flow_packet_RTD[packetID] = (timeEnd, timeEnd - timeStart)


    def log_host_send_rate():
        pass

    def log_host_receive_rate():
        pass
        
    '''link rate should read the time that this delay was calculated for the 
    link and update the relevant link delay'''
    def log_link_rate(self, linkID, pktsize, duration, currTime):
        rate = (pktsize/constants.MB_TO_BYTES)/duration

        if linkID in self.link_flow_rate:
            self.link_flow_rate[linkID].append((currTime, rate))
        else:
            self.link_flow_rate[linkID] = [(currTime, rate)]

    def log_window_size(self, flowID, currTime, windowSize):
        if flowID in self.flow_window_size:
            self.flow_window_size[flowID].append((currTime, windowSize))
        else:
            self.flow_window_size[flowID] = [(currTime, delay)]

    def generatePlots():
        pass

    def writeOutput(self):
        self.outFile.write("link buff occupancy: ")
        self.outFile.write(str(self.link_buff_occupancy))
        self.outFile.write("link packet lost:  ")
        self.outFile.write(str(self.link_packet_lost))
        self.outFile.write("link flow rate: ")
        self.outFile.write(str(self.link_flow_rate))

    def plotOutput(self):
        plt.figure(1)

        colors = ['k', 'r', 'b', 'g', 'm', 'y']
        color_ctr = 0
        plt.subplot(611)        # link rate plot
        for linkID in self.link_flow_rate:
            time = [elt[0] for elt in self.link_flow_rate[linkID]]
            l_flow_rate_MBPS = [elt[1] for elt in self.link_flow_rate[linkID]]
            plt.plot(time, l_flow_rate_MBPS, color=colors[color_ctr])
            color_ctr += 1


        plt.subplot(612)        # buffer occupancy plot
        color_ctr = 0
        for linkID in self.link_buff_occupancy:
            time = [elt[0] for elt in self.link_buff_occupancy[linkID]]
            l_buff_occ_pkt = [elt[1] for elt in self.link_buff_occupancy[linkID]]
            plt.plot(time, l_buff_occ_pkt, color=colors[color_ctr])
            color_ctr += 1

        plt.subplot(613)
        color_ctr = 0
        lost_packet_link_dict = {linkID: collections.Counter(self.link_packet_lost[linkID] for linkID in self.link_packet_lost)}
        for linkID in lost_packet_link_dict:
            time = lost_packet_link_dict[linkID].keys()
            l_pkt_lost = lost_packet_link_dict.values()
            plt.plot(time, l_pkt_lost, color=colors[color_ctr])
            color_ctr += 1

        plt.subplot(614)
        color_ctr = 0
        for flowID in self.flow_rate:
            time = [elt[0] for elt in self.flow_rate[flowID]]
            f_flow_rate = [elt[1] for elt in self.flow_rate[flowID]]
            plt.plot(time, f_flow_rate, color=colors[color_ctr])
            color_ctr += 1

        plt.subplot(615)
        clor_ctr = 0

        plt.show()
