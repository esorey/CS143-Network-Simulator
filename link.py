import constants
import queue
class Link:
    '''A uni-directional link. Data can only flow from the from_id host/router to the
       to_id host/router.'''

    def __init__(self, ID, rate, delay, from_id, to_id):
        self.ID = ID
        self.in_use = False
        self.rate = rate
        self.delay = delay
        self.from_id = from_id
        self.to_id = to_id
        self.buffer = LinkBuffer(from_id, to_id)
        self.dropped_count = 0



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
