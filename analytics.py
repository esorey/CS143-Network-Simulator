class Analytics:

    def __init__(self):
        time_step = []      # Holds the time step (from global time variable)
                            #   at which data was recorded

        '''
        The data types below are dictionaries with:
            keys: Link IDs (strings)
            values: list of tuples containing link information specific to
                the dictionary and the associated time
        '''
        link_buff_occupancy = {}    # Stores buffer occupancy (number of
                                    #   packes in the buffer at the time).
                                    #   Updated any time packet is added to
                                    #   any link buffer
        link_packet_lost = {}       # Stores number of packets lost. Updated
                                    #   every time a packet is added to a
                                    #   full buffer
        link_flow_rate = {}         # Stores number of packets sent over a
                                    #   link. Updates every time a packet 
                                    #   receive event occurs.

        # Still need per flow: send/receive rate, packet round trip delay
        flow_send_rate = {}
        flow_receive_rate = {}
        flow_packet_RTD = {}

        # and per host: send/receive rate
        host_send_rate = {}
        host_receive_rate = {}
        # not sure how to implement/compute these

    '''This logs that this link dropped a packet at the current time.'''
    def log_dropped_packet(linkID, currTime):
        if linkID in link_packet_lost:
            link_packet_lost[linkID].append(currTime)
        else:
            link_packet_lost[linkID] = [currTime]

    ''' Arrange dictionary by linkID followed by currTime'''
    def log_buff_occupancy(linkID, currTime, buffOccupancy):
        if linkID in link_buff_occupancy:
            link_buff_occupancy[linkID].append((currTime, buffOccupancy))
        else:
            link_buff_occupancy[linkID] = [(currTime, buffOccupancy)]

    ''' link flow rate calculation stores number of packets properly
    sent through flow in the span between current time to previous time'''
    def log_flow_rate(linkID, numBytes, currTime, prevTime): 
        rate = numBytes/(currTime - prevTime)
        if linkID in link_flow_rate:
            link_flow_rate[linkID].append((currTime, rate))
        else:
            link_flow_rate[linkID] = [(currTime, rate)]

    '''flow send rate should read the updating window sizes, which
    decide the send rate of each flow, and update it to the relevant time'''
    def log_flow_send_rate(linkID, windowSize, currTime):
        if linkID in flow_send_rate:
            flow_send_rate[linkID].append((windowSize, currTime))
        else:
            flow_send_rate[linkID] = [(windowSize, currTime)]

    # TODO: what is receive rate?
    def log_flow_receive_rate(linkID, currTime, receive):
        pass

    # time start is queued in immediately
    # time end is when the ack with the right packetID is sent
    # get the time for that ack in event queue
    def log_packet_RTD(packetID, timeStart, timeEnd):
        flow_packet_RTD[packetID] = timeEnd - timeStart


    def log_host_send_rate():
        pass

    def log_host_receive_rate():
        pass