import constants
import queue
class Link:
    '''A uni-directional link. Data can only flow from the A_id host/router to the
       B_id host/router.'''

    def __init__(self, ID, rate, delay, A, B, buffer_cap):
        self.ID = ID
        self.in_use = False
        self.rate = rate
        self.delay = delay
        self.A = A_id
        self.B = B_id
        self.buffer_capacity = buffer_cap
        self.buffer = queue.Queue(maxsize=self.buffer_capacity)
        self.dropped_count = 0


    def send_packets(self, packet):
        '''Send a packet on this link. If the link is currently in use, put the packet
           on the buffer. If the buffer is full, the packet is dropped.'''
        if self.in_use:
            try:
                self.buffer.put_no_wait
            except queue.Full: # The buffer is full; this packet is dropped.
                # TODO: figure out who to tell about the dropped packet
                self.dropped_count += 1

        else:


    def get_packet_travel_time():

    def put_on_buffer(self, packet):
        self.buffer.put_no_wait(packet)



class LinkBuffer:
    '''A buffer of packets for a link.'''

    def __init__(self, from_id, to_id):
        self.from_id = from_id
        self.to_id = to_id
        self.capacity = constants.LINK_BUFFER_UNIDIR_CAPACITY
        self.queue = queue.Queue(maxsize = self.capacity)

    def put(self, pkt):
        '''Put a packet on the buffer. Return 0 for success, -1 for failure.'''
        try:
            self.queue.put_no_wait(pkt)
            return 0

        except queue.Full: # Queue is full; return error code -1.
            return -1

    def get(self):
        '''Get a packet from the buffer. Return None if the buffer is empty.'''
        try:
            return self.queue.get_no_wait()
        except queue.Empty:
            return None

    def size(self):
        '''Return the number of elements in the LinkBuffer.'''
        return self.queue.qsize()
