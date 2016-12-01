import constants
import queue
import analytics
from event import Event
import network_map as nwm
from packet import Packet 
from packet import DataPacket
class Link:
    '''A uni-directional link. Data can only flow from A to B.'''

    def __init__(self, ID, rate, delay, A, B, buffer_cap):
        self.ID = ID
        self.in_use = False
        self.rate = rate
        self.delay = 0#delay
        self.A = A
        self.B = B
        self.buffer_capacity = buffer_cap * constants.KB_TO_BYTES # buffer_cap is in MB
        self.buffer_space_used = float(0)
        self.buffer = queue.Queue()

        self.pkt_entry_times = {}    # Key: packet ID, value: [entryTime]


    def handle_link_free(self):
        '''Respond to an event that frees the link. If there is something on the buffer, dequeue it and put a link free event
           on the EQ, along with a packet received event for the destination of this link. If the buffer is empty, mark the link
           as free.'''
        if self.buffer.empty():
            self.in_use = False

        else:
            pkt = self.buffer.get_nowait() # Dequeue a packet
            self.buffer_space_used -= pkt.size
            travel_time = float(constants.system_EQ.currentTime + self.get_packet_travel_time(pkt))
            
            self.packet_left_link(pkt, travel_time)     # Log that a packet left

            self.in_use = True              # Link is in use
            
            # Generate link free and packet receive events at the appropriate times
            link_free_event = Event(Event.link_free, travel_time, [self.ID])
            pkt_receive_event = Event(Event.pckt_rcv, travel_time, [self.B, pkt])

            # Enqueue these events in global Event Queue
            constants.system_EQ.enqueue(link_free_event)
            constants.system_EQ.enqueue(pkt_receive_event)

    def enqueue_packet(self, pkt):
        '''Enqueue a packet to the buffer of this link. If the buffer is full, log a dropped packet in the analytics class.
           If the buffer is empty then send the packet immediately across the link.'''
        
        # If the buffer is empty and the link is free, immediately send the packet over the link
        if self.buffer.empty() and self.in_use == False:
            self.buffer.put_nowait(pkt)        # Enqueue the packet
            self.buffer_space_used += pkt.size
            self.packet_entered_link(pkt)       # Record the time the packet entered the link
            # Log buffer occupancy for the whole link
            constants.system_analytics.log_buff_occupancy(self.ID[0:-1], constants.system_EQ.currentTime, self.get_buffer_occupancy())
            constants.system_analytics.log_dropped_packet(self.ID[0:-1], constants.system_EQ.currentTime, 0)
            self.handle_link_free()             # Handle the fact that the link is free by putting link in use

        # If buffer is full, log that we dropped a packet
        elif self.get_buffer_occupancy() + pkt.size > self.buffer_capacity:                
            constants.system_analytics.log_dropped_packet(self.ID[0:-1], constants.system_EQ.currentTime, 1)

        else:       # Otherwise either link is in use or buffer has some elements, so add pkt to buffer
            self.buffer.put_nowait(pkt)         # Enqueue the packet into link buffer
            self.buffer_space_used += pkt.size
            self.packet_entered_link(pkt)       # Record the time the packet entered the link
            # Log buffer occupancy for the whole link
            constants.system_analytics.log_buff_occupancy(self.ID[0:-1], constants.system_EQ.currentTime, self.get_buffer_occupancy())
            

    def get_packet_travel_time(self, pkt):
        '''Compute the travel time for a packet. Will involve the current time and the transmission time.'''
        travel_time = self.delay + constants.SEC_TO_MS * (pkt.size * constants.BYTES_TO_MBITS / self.rate)
        print("Travel Time:")
        print(travel_time)
        return travel_time

    def packet_entered_link(self, pkt):
        if pkt.packet_id not in self.pkt_entry_times:
            self.pkt_entry_times[pkt.packet_id] = [constants.system_EQ.currentTime]
        else:
            self.pkt_entry_times[pkt.packet_id].append(constants.system_EQ.currentTime)

    def packet_left_link(self, pkt, exit_time):
        entry_time = self.pkt_entry_times[pkt.packet_id][0]
        
        if len(self.pkt_entry_times[pkt.packet_id]) == 1:
            del self.pkt_entry_times[pkt.packet_id]
        else:
            del self.pkt_entry_times[pkt.packet_id][0]
        if type(pkt) is DataPacket:
        	constants.system_analytics.log_link_rate(self.ID, pkt.size, float(exit_time-entry_time), exit_time)

        
    def get_buffer_occupancy(self):
        '''
        Get the number of bytes in the bidirectional link that this link is a part of. This checks
        the number of bytes in the buffer of the link that runs opposite to this one.
        '''
        other_link_obj = self.get_opposite_link_obj()
        print(self.ID)
        print((self.buffer_space_used + other_link_obj.buffer_space_used)/float(1024))
        return self.buffer_space_used + other_link_obj.buffer_space_used


    def get_opposite_link_obj(self):
        '''
        Get the link object that runs opposite to this one.
        '''
        # Flip the link id
        if self.ID[-1] == 'a':
            other_link_id = self.ID[:-1] + 'b'
        elif self.ID[-1] == 'b':
            other_link_id  = self.ID[:-1] + 'a'
        else:
            raise ValueError('Malformed link id: %s' % self.ID)

        return nwm.get_link_from_id(other_link_id)

