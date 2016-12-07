import constants
import matplotlib.pyplot as plt
import collections

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
        self.pckts = 0

    '''This logs that this link dropped a packet at the current time.'''
    def log_dropped_packet(self, linkID, currTime, numPkts):
        if linkID in self.link_packet_lost:
            if currTime in self.link_packet_lost[linkID]:
                self.link_packet_lost[linkID][currTime] += numPkts
            else:
                self.link_packet_lost[linkID][currTime] = numPkts
        else:
            self.link_packet_lost[linkID] = {}
            self.link_packet_lost[linkID][currTime] = numPkts

    ''' Arrange dictionary by linkID followed by currTime'''
    def log_buff_occupancy(self, linkID, currTime, buffOccupancy):
        if linkID in self.link_buff_occupancy:
            self.link_buff_occupancy[linkID].append((currTime, buffOccupancy/constants.DATA_PKT_SIZE))
        else:
            self.link_buff_occupancy[linkID] = [(currTime, buffOccupancy/constants.DATA_PKT_SIZE)]

    ''' link flow rate calculation stores number of packets properly
    sent through flow in the span between current time to previous time'''
    # changed to flowID because I think this should be flow? i.e. when a flow
    # decides to put first packet in iink buffer to when host receives last
    # packet
    #def log_flow_rate(self, flowID, numBytes, currTime, prevTime):
    def log_flow_rate(self, flowID, numBytes, RTT, currTime): 
        #rate = numBytes*constants.BYTES_TO_MBITS/(RTT/constants.SEC_TO_MS)
        #if flowID in self.flow_rate:
        #    self.flow_rate[flowID].append((currTime, rate))
        #else:
        #    self.flow_rate[flowID] = [(currTime, rate)]
        #if constants.debug:
        #   print(rate)
        if flowID in self.flow_rate:
            self.flow_rate[flowID].append((currTime, numBytes))
        else:
            self.flow_rate[flowID] = [(currTime, numBytes)]

    '''flow send rate should read the updating window sizes, which
    decide the send rate of each flow, and update it to the relevant time'''
    def log_flow_send_rate(self, flowID, numBytes, currTime):
        currTime = round(currTime, constants.DEC_PLACES)
        prev_data_sent = 0

        if flowID in self.flow_send_rate:
            flow_send_rate_points = self.flow_send_rate[flowID]
            flow_send_rate_times = [pt[0] for pt in flow_send_rate_points]

            if currTime in flow_send_rate_times:
                prev_ind = flow_send_rate_times.index(currTime)
                prev_data_sent = flow_send_rate_points[prev_ind][1]
                del self.flow_send_rate[flowID][prev_ind]

            self.flow_send_rate[flowID].append((currTime, numBytes+prev_data_sent))
        else:
            self.flow_send_rate[flowID] = [(currTime, numBytes)]

    '''flow receive rate should read the time that the packet was received
    at the host and add it to the corresponding packet in the flow'''
    def log_flow_receive_rate(self, flowID, currTime, receive_order):
        self.pckts += 1
        if flowID in self.flow_send_rate:
            # If the number of the received packet is greater than window size,
            #   there is an issue
            if constants.debug: print(self.flow_send_rate[flowID])
            if receive_order <= self.flow_send_rate[flowID][-1][0]:
                pass
                # Log the flow rate
                #self.log_flow_rate(flowID, constants.DATA_PKT_SIZE, currTime, self.flow_send_rate[flowID][-1][1])

    # time start is queued in immediately
    # time end is when the ack with the right packetID is sent
    # get the time for that ack in event queue
    def log_packet_RTD(self, flowID, timeStart, timeEnd):
        if flowID in self.flow_packet_RTD:
            self.flow_packet_RTD[flowID].append((timeEnd, timeEnd - timeStart))
        else:
            self.flow_packet_RTD[flowID] = [(timeEnd, timeEnd - timeStart)]


    def log_host_send_rate():
        pass

    def log_host_receive_rate():
        pass
        
    '''link rate should read the time that this delay was calculated for the 
    link and update the relevant link delay'''
    def log_link_rate(self, linkID, pktsize, currTime):
        link_key = linkID[0:-1]
        currTime = round(currTime, constants.DEC_PLACES)
        prev_pkts_sent = 0

        if link_key in self.link_flow_rate:
            link_flow_rate_points = self.link_flow_rate[link_key]
            link_flow_rate_times = [pt[0] for pt in link_flow_rate_points]

            # If we already have data for this time, then just update the data
            if currTime in link_flow_rate_times:
                prev_ind = link_flow_rate_times.index(currTime)
                prev_pkts_sent = link_flow_rate_points[prev_ind][1]
                del self.link_flow_rate[link_key][prev_ind]     # Remove previous data

            self.link_flow_rate[link_key].append((currTime, pktsize+prev_pkts_sent))
        else:
            self.link_flow_rate[link_key] = [(currTime, pktsize)]

    def log_window_size(self, flowID, currTime, windowSize):
        if flowID in self.flow_window_size:
            self.flow_window_size[flowID].append((currTime, windowSize))
        else:
            self.flow_window_size[flowID] = [(currTime, windowSize)]

    def generatePlots():
        pass

    def writeOutput(self):
        self.outFile.write("link buff occupancy: ")
        self.outFile.write(str(self.link_buff_occupancy))
        self.outFile.write("link packet lost:  ")
        self.outFile.write(str(self.link_packet_lost))
        self.outFile.write("link flow rate: ")
        self.outFile.write(str(self.link_flow_rate))
        self.outFile.write("\n\n\n\n Total Number of Packets: %d" % self.pckts)

    def convertToWindow(self, times, data, numWindows=None):
        # times should be sorted
        if numWindows == None:
            numWindows = constants.DEFAULT_NUM_WINDOWS

        window_size = max(times)/numWindows
        window_start = 0
        ret_times = []
        ret_data = []
        cur_time_windows = []
        cur_data_windows = []

        for j in range(len(times)):
            if times[j] > window_start+window_size:
                if len(cur_time_windows) == 0:
                    cur_time_windows.append(window_start + window_size * 1.0/2)
                    cur_data_windows.append(0)
                
                window_start += window_size
                ret_times.append(cur_time_windows)
                ret_data.append(cur_data_windows)
                cur_time_windows = []
                cur_data_windows = []

            cur_time_windows.append(times[j])
            cur_data_windows.append(data[j])

        return ret_times, ret_data

    def convertToSlidingWindow(self, times, data, numWindows=None):
        # Might want to implement this to make the graph look more
        # like the test cases
        # To implement we would have to 
        pass


    def getRate(self, times, data, numWindows=None):
        if numWindows == None:
            numWindows = constants.DEFAULT_NUM_WINDOWS

        window_size = max(times)/numWindows

        w_times, w_data = self.convertToWindow(times, data, numWindows)

        ret_times = [sum(a)*1.0/len(a) for a in w_times]
        ret_data = [sum(a)*1.0/window_size for a in w_data]
        return ret_times, ret_data

    def plotOutput(self):
        fig, axes = plt.subplots(nrows=4, ncols=1)
        fig.tight_layout()
        colors = ['k', 'r', 'b', 'g', 'm', 'y', 'c', '0.5', '0.75', '#B62828',
        '#0F644D', '#87C41C']

        # Decide number of links to show based on test case number
        if constants.testcase in [0, 1]:
            num_plotted_links = 2
        else:
            num_plotted_links = 3

        color_ctr = 0
        plt.subplot(611)        # link rate plot
        sorted_linkIDs = sorted(self.link_flow_rate.keys())
        for linkID in sorted_linkIDs[1:1 + num_plotted_links]:
            if constants.debug:
                print("LINK FLOW RATE LINK ID:")
                print(linkID + " " + colors[color_ctr])
            #if list(self.link_flow_rate.keys()).index(linkID) is not 1:
            # Get time out of [time, rate] pairs
            link_points = self.link_flow_rate[linkID]
            link_points.sort(key=lambda x: x[0])
            time = [elt[0]*constants.MS_TO_SEC for elt in link_points]
            l_flow_rate_MBPS = [elt[1]*constants.BYTES_TO_MBITS for elt in link_points]

            LFR_t, LFR_d = self.getRate(time, l_flow_rate_MBPS)
            plt.plot(LFR_t, LFR_d, label=linkID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1

        plt.legend(bbox_to_anchor=(1,1))
        plt.xlabel('time (ms)')
        plt.ylabel('Link Rate (Mbps)')

        color_ctr = 0
        plt.subplot(612)        # buffer occupancy plot
        sorted_linkIDs = sorted(self.link_buff_occupancy.keys())
        for linkID in sorted_linkIDs[1:1 + num_plotted_links]:
            if constants.debug:
                print("LINK BUFF OCCUPANCY: ")
                print(linkID + " " + colors[color_ctr])
            time = [elt[0] for elt in self.link_buff_occupancy[linkID]]
            l_buff_occ_pkt = [elt[1] for elt in self.link_buff_occupancy[linkID]]
            plt.plot(time, l_buff_occ_pkt, label=linkID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1

        plt.legend(bbox_to_anchor=(1,1))
        plt.xlabel('time (ms)')
        plt.ylabel('Buffer Occupancy (KB)')


        color_ctr = 0
        plt.subplot(613)
        '''
        #old
        time_RTD_list = list(self.flow_packet_RTD.values())
        time = [tup[0] for tup in time_RTD_list]
        pkt_RTD = [tup[1] for tup in time_RTD_list]
        plt.plot(time, pkt_RTD, color='k')
        plt.xlabel('time (ms)')
        plt.ylabel('Packet Delay (ms)')
        '''
        #new
        sorted_flowIDs = sorted(self.flow_packet_RTD.keys())
        for flowID in sorted_flowIDs:
            if constants.debug:
                print("PACKET DELAY FLOW ID:")
                print(flowID + " " + colors[color_ctr])
            #if list(self.link_flow_rate.keys()).index(linkID) is not 1:
            # Get time out of [time, delay] pairs
            time = [elt[0] for elt in self.flow_packet_RTD[flowID]]
            # Get delay out of [time, delay] pairs
            pkt_delay_S = [elt[1] for elt in self.flow_packet_RTD[flowID]]
            plt.plot(time, pkt_delay_S, label=flowID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1

        plt.legend(bbox_to_anchor=(1,1))
        plt.xlabel('time (ms)')
        plt.ylabel('Packet Delay (ms)')

        plt.subplot(614)
        color_ctr = 0
        for flowID in self.flow_send_rate:
            flow_rate_points = self.flow_send_rate[flowID]
            flow_rate_points.sort(key=lambda x: x[0])

            time = [elt[0]*constants.MS_TO_SEC for elt in flow_rate_points]
            f_flow_rate = [elt[1]*constants.BYTES_TO_MBITS for elt in flow_rate_points]

            FR_t, FR_d = self.getRate(time, f_flow_rate)
            if constants.debug:
                print(time)
                print(f_flow_rate)

            plt.plot(FR_t, FR_d, label=flowID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1
        plt.xlabel('time (ms)')
        plt.ylabel('Flow Rate (Mbps)')

        color_ctr = 0
        plt.subplot(615)
        sorted_linkIDs = sorted(self.link_packet_lost.keys())
        for linkID in sorted_linkIDs[1:1 + num_plotted_links]:
            link_dict = self.link_packet_lost[linkID]
            sorted_time = sorted(link_dict)
            l_pkt_lost = []
            for time in sorted_time:
                l_pkt_lost.append(link_dict[time])
            plt.plot(sorted_time, l_pkt_lost, label=linkID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1
        plt.legend(bbox_to_anchor=(1,1))
        plt.xlabel('time (ms)')
        plt.ylabel('Packets Dropped')

        color_ctr = 0
        plt.subplot(616)        # link rate plot
        sorted_flowIDs = sorted(self.flow_window_size.keys())
        for flowID in sorted_flowIDs:
            if constants.debug:
                print("WINDOW SIZE FLOW ID:")
                print(flowID + " " + colors[color_ctr])
            #if list(self.link_flow_rate.keys()).index(linkID) is not 1:
            # Get time out of [time, rate] pairs
            time = [elt[0] for elt in self.flow_window_size[flowID]]
            # Get rate out of [time, rate] pairs
            flow_ws = [elt[1] for elt in self.flow_window_size[flowID]]
            plt.plot(time, flow_ws, label=flowID, marker='o', linestyle='--', markersize=1, color=colors[color_ctr], markeredgecolor=colors[color_ctr])
            color_ctr += 1
        plt.legend(bbox_to_anchor=(1,1))
        plt.xlabel('time (ms)')
        plt.ylabel('Window Size (pkts)')
        # ALSO FIX UNITS

        plt.show()
