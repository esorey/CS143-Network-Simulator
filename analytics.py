import constants
import matplotlib.pyplot as plt
import collections

class Analytics:

    def __init__(self, plot_links, plot_flows):
        '''
        Logs and plots the relevant analytics for the network simulation

        link_buff_occupancy (dictionary of lists) - key is the linkID (without 
            direction specifier), values are lists of (time, buffer_occupancy)
            tuples

        link_packet_lost (dictionary of dictionaries) - key is the linkID 
            (without direction specifier), second key is the time, value
            is the number of packets lost at this time

        link_flow_rate (dictionary of lists) - key is the linkID, values are
            lists of (time, packets sent) tuples.

        flow_send_rate (dictionary of lists) - key is the flowID, values are
            lists of (time, data sent) tuples. 

        flow_packet_RTD (dictionary of lists) - key is the flowID, values are
            lists of (time, packet RTD) tuples.

        flow_window_size (dictionary of lists) - key is the flowID, values are
            lists of (time, window size) tuples.

        '''
        self.link_buff_occupancy = {}
        self.link_packet_lost = {}
        self.link_flow_rate = {}

        self.flow_send_rate = {}
        self.flow_packet_RTD = {}
        self.flow_window_size = {}

        self.plotlinks = plot_links     # Links we care about logging/plotting
        self.plotflows = plot_flows     # Flows we care about logging/plotting


    def log_buff_occupancy(self, linkID, currTime, buffOccupancy):
        '''
        Log the buffer occupancy for this link.
        '''
        currTime = currTime * constants.MS_TO_SEC

        if linkID in self.plotlinks:
            if linkID in self.link_buff_occupancy:
                self.link_buff_occupancy[linkID].append((currTime, buffOccupancy))
            else:
                self.link_buff_occupancy[linkID] = [(currTime, buffOccupancy)]

    def log_dropped_packet(self, linkID, currTime, numPkts):
        '''
        Log that linkID dropped numPkts packets at currTime.
        '''
        currTime = round(currTime, constants.DEC_PLACES) * constants.MS_TO_SEC 

        if linkID in self.plotlinks:
            if linkID in self.link_packet_lost:
                if currTime in self.link_packet_lost[linkID]:
                    self.link_packet_lost[linkID][currTime] += numPkts
                else:
                    self.link_packet_lost[linkID][currTime] = numPkts
            else:
                self.link_packet_lost[linkID] = {}
                self.link_packet_lost[linkID][currTime] = numPkts

    def log_link_rate(self, linkID, pktsize, currTime):
        '''
        Log that pktsize packets were sent at currTime over this link. Check 
        if there's already data for link rate at this time, if there is then
        just update it.
        '''

        link_key = linkID[0:-1]
        currTime = round(currTime, constants.DEC_PLACES) * constants.MS_TO_SEC

        if link_key in self.plotlinks:
            if link_key in self.link_flow_rate:
                prev_pkts_sent = 0
                time_list = [pt[0] for pt in self.link_flow_rate[link_key]]

                # If we already have data for this time, then just update the data
                if currTime in time_list:
                    prev_ind = time_list.index(currTime)
                    prev_pkts_sent = self.link_flow_rate[link_key][prev_ind][1]
                    del self.link_flow_rate[link_key][prev_ind]     # Remove previous data

                self.link_flow_rate[link_key].append((currTime, pktsize+prev_pkts_sent))
            else:
                self.link_flow_rate[link_key] = [(currTime, pktsize)]
    
    def log_flow_send_rate(self, flowID, numBytes, currTime):
        '''
        Log how many packets a flow sends.
        '''
        if flowID in self.plotflows:
            currTime = round(currTime, constants.DEC_PLACES) * constants.MS_TO_SEC

            if flowID in self.flow_send_rate:
                prev_data_sent = 0
                time_list = [pt[0] for pt in self.flow_send_rate[flowID]]

                # if send rate has previously been logged at the current time
                if currTime in time_list:
                    prev_ind = time_list.index(currTime)
                    prev_data_sent = self.flow_send_rate[flowID][prev_ind][1]
                    del self.flow_send_rate[flowID][prev_ind]

                self.flow_send_rate[flowID].append((currTime, numBytes+prev_data_sent))
            else:
                self.flow_send_rate[flowID] = [(currTime, numBytes)]


    def log_packet_RTD(self, flowID, RTT, timeEnd):
        '''
        Log the packet round trip delay for this flow.
        '''
        timeEnd = timeEnd * constants.MS_TO_SEC

        if flowID in self.plotflows:
            if flowID in self.flow_packet_RTD:
                self.flow_packet_RTD[flowID].append((timeEnd, RTT))
            else:
                self.flow_packet_RTD[flowID] = [(timeEnd, RTT)]

    def log_window_size(self, flowID, currTime, windowSize):
        '''
        Log the flow's window size.
        '''
        currTime = currTime * constants.MS_TO_SEC

        if flowID in self.plotflows:
            if flowID in self.flow_window_size:
                self.flow_window_size[flowID].append((currTime, windowSize))
            else:
                self.flow_window_size[flowID] = [(currTime, windowSize)]

    def convertToWindow(self, times, data, numWindows=None):
        '''
        Converts the input times and data into numWindows discrete windows. The
        return value ret_times is a list of lists where each row represents the
        times in a particular window. Similarly ret_data is a list of lists
        where each row represents the data in that window.
        '''
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
        '''
        This function takes the times and data input and converts it to a rate
        by using the discrete windows.
        '''
        if numWindows == None:
            numWindows = constants.DEFAULT_NUM_WINDOWS

        window_size = max(times)/numWindows

        w_times, w_data = self.convertToWindow(times, data, numWindows)

        ret_times = [sum(a)*1.0/len(a) for a in w_times]
        ret_data = [sum(a)*1.0/window_size for a in w_data]

        return ret_times, ret_data

    def getAvg(self, times, data, numWindows=None):
        if numWindows == None:
            numWindows = constants.DEFAULT_NUM_WINDOWS

        window_size = max(times)/numWindows

        w_times, w_data = self.convertToWindow(times, data, numWindows)

        ret_times = [sum(a)*1.0/len(a) for a in w_times]
        ret_data = [sum(a)*1.0/len(a) for a in w_data]

        return ret_times, ret_data

    def plotOutput(self):
        colors = ['k', 'r', 'b', 'g', 'm', 'y', 'c', '0.5', '0.75', '#B62828',
        '#0F644D', '#87C41C']

        # Create figure 1: link rate
        color_ctr = 0
        plt.figure(num=1, figsize=(7,2))

        sorted_linkIDs = sorted(self.link_flow_rate.keys())

        for linkID in sorted_linkIDs:
            link_points = self.link_flow_rate[linkID]   # Get (time, value)
            link_points.sort(key=lambda x: x[0])        # Sort by time

            # Get the link rate times and data separately
            time = [elt[0] for elt in link_points]
            link_rate_data = [elt[1]*constants.BYTES_TO_MBITS \
                                for elt in link_points]

            # Convert into window averaged rates
            LFR_t, LFR_d = self.getRate(time, link_rate_data)

            plt.plot(LFR_t, LFR_d, label=linkID, marker='o', linestyle='--',
                        markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Link Rate (Mbps)')

        plt.savefig("./Figures/Figure1-LinkRate", additional_artists=[lgd],
                    bbox_inches="tight")


        # Create figure 2: buffer occupancy
        color_ctr = 0
        plt.figure(num=2, figsize=(7,2))

        sorted_linkIDs = sorted(self.link_buff_occupancy.keys())

        for linkID in sorted_linkIDs:
            # Get the link buffer occupancy times and data separately
            time = [elt[0] for elt in self.link_buff_occupancy[linkID]]
            buff_occ_data = [elt[1] for elt in self.link_buff_occupancy[linkID]]

            buff_occ_t, buff_occ_d = self.getAvg(time, buff_occ_data)
            plt.plot(buff_occ_t, buff_occ_d, label=linkID, marker='o',
                        linestyle='--', markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Buffer Occupancy (KB)')

        plt.savefig("./Figures/Figure2-BufferOccupancy",
                    additional_artists=[lgd], bbox_inches="tight")


        # Create figure 3: packet delay
        color_ctr = 0
        plt.figure(num=3, figsize=(7,2))

        sorted_flowIDs = sorted(self.flow_packet_RTD.keys())

        for flowID in sorted_flowIDs:
            # Get packet delay times and data separately
            time = [elt[0] for elt in self.flow_packet_RTD[flowID]]
            pkt_delay_data = [elt[1] for elt in self.flow_packet_RTD[flowID]]

            pd_t, pd_d = self.getAvg(time, pkt_delay_data)
            plt.plot(pd_t, pd_d, label=flowID, marker='o',
                        linestyle='--', markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Packet Delay (ms)')

        plt.savefig("./Figures/Figure3-PacketDelay", additional_artists=[lgd],
                    bbox_inches="tight")


        # Create figure 4: flow rate
        color_ctr = 0
        plt.figure(num=4, figsize=(7,2))
        
        sorted_flowIDs = sorted(self.flow_send_rate.keys())
        for flowID in sorted_flowIDs:
            flow_rate_points = self.flow_send_rate[flowID]  # Get (time, value)
            flow_rate_points.sort(key=lambda x: x[0])       # Sort by time

            # Get flow rate times and data separately
            time = [elt[0] for elt in flow_rate_points]
            flow_rate_data = [elt[1]*constants.BYTES_TO_MBITS \
                                for elt in flow_rate_points]

            # Convert to window averaged rates
            FR_t, FR_d = self.getRate(time, flow_rate_data)

            plt.plot(FR_t, FR_d, label=flowID, marker='o', linestyle='--',
                        markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Flow Rate (Mbps)')

        plt.savefig("./Figures/Figure4-FlowRate", additional_artists=[lgd],
                    bbox_inches="tight")


        # Create figure 5: packets dropped
        color_ctr = 0
        plt.figure(num=5, figsize=(7,2))

        sorted_linkIDs = sorted(self.link_packet_lost.keys())

        for linkID in sorted_linkIDs:
            link_dict = self.link_packet_lost[linkID]

            sorted_time = sorted(link_dict)     # Get sorted list of times

            l_pkt_lost = []                     # Create list of data  
            for time in sorted_time:
                l_pkt_lost.append(link_dict[time])

            plt.plot(sorted_time, l_pkt_lost, label=linkID, marker='o',
                        linestyle='--', markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Packets Dropped')

        plt.savefig("./Figures/Figure5-PacketsDropped",
                    additional_artists=[lgd], bbox_inches="tight")


        # Create figure 6: window size
        color_ctr = 0
        plt.figure(num=6, figsize=(7,2))

        sorted_flowIDs = sorted(self.flow_window_size.keys())

        for flowID in sorted_flowIDs:
            # Get time and data separately
            time = [elt[0] for elt in self.flow_window_size[flowID]]
            flow_ws = [elt[1] for elt in self.flow_window_size[flowID]]

            plt.plot(time, flow_ws, label=flowID, marker='o', linestyle='--',
                        markersize=1, color=colors[color_ctr],
                        markeredgecolor=colors[color_ctr])

            color_ctr += 1

        lgd = plt.legend(loc=7, bbox_to_anchor=(1.25,0.5))
        plt.xlabel('time (ms)')
        plt.ylabel('Window Size (pkts)')

        plt.savefig("./Figures/Figure6-WindowSize", additional_artists=[lgd],
                    bbox_inches="tight")

        plt.show()
