class Event:
    # Event Types
    flow_start = 1      # Flow begins at some time
    pckt_rcv = 2        # Packet is received by host or router
    link_free = 3       # Link is available to send packets over
    flow_src_send_packets = 4       # Flow's source (host) is sending packets
    ack_rcv = 5         # Acknowledgement packet received by host
    pckt_send = 6       # Packet to be sent over a link
    update_FAST = 7     # Update FAST TCP window size
    pckt_timeout = 8    # Packet times out
    bellman_ford = 9    # Run bellman ford event
    flow_done = 10
    flow_rcv_data = 11  # Flow gets a data packet 

    def __init__(self, ev_type, time, data):
        '''
        event_type - enumerated type that indicates what sort of event 
                     this is 
        time - integer, when the event occurs
        data - information required for the events (list of varying size
               depending on event, see below for details).
        '''
        self.event_type = ev_type
        self.time = time
        self.data = data
        
        ''' 
        Event Type Details:
        flow_start:
            Description: tells the flow to send packets
            Data: [flowID]

        pckt_rcv:
            Description: Hands off packet to a host or router to deal with
            Data: [hostID/routerID, packet]

        link_free:
            Description: Frees the link (i.e. it is no longer sending a packet),
                and tells the link to send another packet if possible.
            Data: [linkID]

        flow_src_send_packets:
            Description: Enables the flow to tell the flow's source/dest (some host)
                to send packets.
            Data: [hostID, list of packets]

        ack_rcv:
            Description: Tells the flow an acknowledgement packet was received
            Data: [packetID, flowID, acknowledgement time]

        pckt_send:
            Description: Hands off the packet to the link to send, hold in buffer,
                or drop.
            Data: [linkID, packet]

        update_FAST:
            Description: Update the window size for Fast TCP congestion control 
                algorithm
            Data: [flowID]

        pckt_timeout:
            Description: Tells the flow that a packet with a certain ID has timed out
            Data: [packet, flowID]

        bellman_ford:
            Description: Enqueues another Bellman Ford event at a fixed time, and begins
                Bellman Ford algorithm to dynamically update routing tables.
            Data: None

        flow_done:
            Description: Checks if all the flows are finished, and updates the global
                constant that indicates all flows are finished.
            Data: None

        flow_rcv_data:
            Description: Flow receives a data packet and determines what ack to send
            Data: [flowID, packet]
        '''
