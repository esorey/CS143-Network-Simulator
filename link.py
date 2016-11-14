import constants
import queue
import analytics
class Link:
    '''A uni-directional link. Data can only flow from A to B.'''

    def __init__(self, ID, rate, delay, A, B, buffer_cap):
        self.ID = ID
        self.in_use = False
        self.rate = rate
        self.delay = delay
        self.A = A
        self.B = B
        self.buffer_capacity = buffer_cap * constants.MB_TO_BYTES # buffer_cap is in MB
        self.buffer_space_used = 0
        self.buffer = queue.Queue()


    def handle_link_free(self):
        '''Respond to an event that frees the link. If there is something on the buffer, dequeue it and put a link free event
           on the EQ, along with a packet received event for the destination of this link. If the buffer is empty, mark the link
           as free.'''
        if self.buffer.Empty():
            self.in_use = False

        else:
            pkt = self.buffer.get_no_wait() # Dequeue a packet
            self.buffer_space_used -= pkt.size
            travel_time = constants.system_EQ.currentTime + self.get_packet_travel_time(pkt)
            self.in_use = True              # Link is in use
            
            # Generate link free and packet receive events at the appropriate times
            link_free_event = Event(Event.link_free, travel_time, [self])
            pkt_receive_event = Event(Event.pckt_rcv, travel_time, [self.B, pkt])

            # Enqueue these events in global Event Queue
            constants.system_EQ.enqueue(link_free_event)
            constants.system_EQ.enqueue(pkt_receive_event)

            # not sure what this is trying to log? doesn't have corresponding analytic on file
            constants.system_analytics.log(self.ID, pkt.size, constants.system_EQ.currentTime, travel_time)

    def enqueue_packet(self, pkt):
        '''Enqueue a packet to the buffer of this link. If the buffer is full, log a dropped packet in the analytics class.
           If the buffer is empty then send the packet immediately across the link.'''
        # If the buffer is empty and the link is free, immediately send the packet over the link
        if self.buffer.empty() and self.in_use == False:
            self.buffer.put_no_wait(pkt)        # Enqueue the packet
            self.buffer_space_used += pkt.size
            self.handle_link_free()             # Handle the fact that the link is free by putting link in use

        # If buffer is full, log that we dropped a packet
        elif self.buffer_space_used + pkt.size > self.buffer_capacity:                
            constants.system_analytics.log_dropped_packet(self.ID, constants.system_EQ.currentTime)

        else:       # Otherwise either link is in use or buffer has some elements, so add pkt to buffer
            self.buffer.put_nowait(pkt)         # Enqueue the packet into link buffer
            self.buffer_space_used += pkt.size
            # Log the buffer space used for this link.
            constants.system_analytics.log_buff_occupancy(self.ID, constants.system_EQ.currentTime, self.buffer_space_used)
            

    def get_packet_travel_time(self, packet):
        '''Compute the travel time for a packet. Will involve the current time and the transmission time.'''
        travel_time = self.delay + constants.SEC_TO_MS * (packet.size / (constants.MB_TO_BYTES * self.rate))
        link_rate = float(constants.DATA_PKT_SIZE / travel_time)
        constants.system_analytics.log_link_rate(self.ID, constants.system_EQ.currentTime, link_rate)
        return travel_time
        
