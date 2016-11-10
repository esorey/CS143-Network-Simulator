class analytics:

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
        # and per host: send/receive rate
        # not sure how to implement/compute these
