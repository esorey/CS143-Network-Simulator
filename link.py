import constants
import queue
import analytics as Analytics
class Link:
    '''A uni-directional link. Data can only flow from A to B.'''

    def __init__(self, ID, rate, delay, A, B, buffer_cap):
        self.ID = ID
        self.in_use = False
        self.rate = rate
        self.delay = delay
        self.A = A
        self.B = B
        self.buffer_capacity = buffer_cap
        self.buffer = queue.Queue(maxsize=self.buffer_capacity)


    def handle_link_free(self):
        '''Respond to an event that frees the link. If there is something on the buffer, dequeue it and put a link free event
           on the EQ, along with a packet received event for the destination of this link. If the buffer is empty, mark the link
           as free.'''
        if self.buffer.empty():
            self.in_use = False

        else:
            pkt = self.buffer.get_no_wait() # Dequeue a packet
            travel_time = self.get_packet_travel_time(pkt)
            self.EQ_put_link_free(travel_time + curr_time) # TODO: compute the time for the packet to travel. Should be curr_time + transmission time
            self.EQ_put_pkt_recv(time, self.B, pkt) # TODO: same time as before


    def enqueue_packet(self, packet):
        '''Enqueue a packet to the buffer of this link. If the buffer is full, log a dropped packet in the analytics class.'''
        try:
            self.buffer.put_no_wait(packet)
        except queue.Full: # The buffer is full; this packet is dropped.
            Analytics.log_dropped_packet(self.ID, curr_time) # TODO: figure out global time/analytics objects. This logs that this link dropped a packet
                                                             # at the current time.
            

    def get_packet_travel_time(self, packet):
        '''Compute the travel time for a packet. Will involve the current time and the transmission time.'''
        # TODO: Is this the right way to compute travel time??
        return packet.size / (constants.MBTOBYTES * self.rate)
