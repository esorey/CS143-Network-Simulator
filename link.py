import constants
import queue
import analytics
import util
import network_map as nwm
from event import Event
from packet import Packet 
from packet import DataPacket


class Link:
    '''A uni-directional link. Data can only flow from A to B.'''

    def __init__(self, ID, rate, delay, A, B, buffer_cap):
        self.ID = ID
        self.rate = rate            # Link rate in megabits per second
        self.delay = 0              # Link delay in ms
        self.A = A                  # Link source
        self.B = B                  # Link destination
        self.buffer_capacity = buffer_cap * constants.KB_TO_BYTES       # Buffer capacity in bytes

        self.in_use = False         # Indicates if a packet is being sent over the link
        self.buffer_space_used = float(0)       # Space used in link buffer
        self.buffer = queue.Queue()             # Link buffer is a queue


    def handle_link_free(self):
        '''
        Respond to an event that frees the link. If there is something on the buffer,
        dequeue it and send it across the link (i.e. put link free event on the EQ,
        along with a packet received event for the destination of this link). If the buffer
        is empty, mark the link as free.
        '''

        if self.buffer.empty():         # No more packets to send
            self.in_use = False

        else:
            pkt = self.buffer.get_nowait()      # Get a packet to send
            self.buffer_space_used -= pkt.size  # Update buffer space

            # Calculate time it takes packet to travel over link
            travel_time = float(constants.system_EQ.currentTime + self.get_packet_travel_time(pkt))
            
            self.log_buffer_occupancy()                 # Log buffer size
            self.log_link_rate(pkt.size, travel_time)   # Log link rate
            
            self.in_use = True              # Indicate that the link is in use
            
            # Generate link free and packet receive events at the appropriate times
            link_free_event = Event(Event.link_free, travel_time, [self.ID])
            pkt_receive_event = Event(Event.pckt_rcv, travel_time, [self.B, pkt])

            # Enqueue these events in global Event Queue
            constants.system_EQ.enqueue(link_free_event)
            constants.system_EQ.enqueue(pkt_receive_event)

    def enqueue_packet(self, pkt):
        '''
        Enqueue a packet to the buffer of this link. If the buffer is full, log a dropped
        packet in the analytics class. If the buffer is empty then send the packet immediately
        across the link.
        '''
        
        # If the buffer is empty and the link is free, immediately send the packet over the link
        if self.buffer.empty() and self.in_use == False:
            self.buffer.put_nowait(pkt)             # Enqueue the packet
            self.buffer_space_used += pkt.size      # Update buffer size
  
            self.log_buffer_occupancy()               # Log buffer occupancy
            self.log_packet_dropped(0)              # Log that no packets were dropped

            self.handle_link_free()                 # Handle the fact that link is free by putting link in use

        # If buffer is full, log that we dropped a packet
        elif self.get_buffer_occupancy() + pkt.size > self.buffer_capacity: 
            print(self.ID)
            print("Packet dropped, buffer occupancy is %s" % self.get_buffer_occupancy())
            print("buffer capacity is %s" % self.buffer_capacity)   

            self.log_packet_dropped(1)              # Log that a packet was dropped

        # Otherwise either link is in use and/or buffer has some elements, so add packet to buffer
        else:       
            self.buffer.put_nowait(pkt)             # Enqueue the packet into link buffer
            self.buffer_space_used += pkt.size      # Update buffer size
            
            self.log_buffer_occupancy()             # Log the buffer occupancy
            self.log_packet_dropped(0)              # Log that no packets were dropped

    def get_packet_travel_time(self, pkt):
        '''
        Compute the travel time for a packet. Will involve the current time and the transmission
        time.
        '''
        travel_time = self.delay + constants.SEC_TO_MS * (pkt.size * constants.BYTES_TO_MBITS * 1.0 / self.rate)
        
        if constants.debug:
            print("Travel Time:")
            print(travel_time)

        return travel_time

    def get_buffer_occupancy(self):
        '''
        Get the number of bytes in the bidirectional link that this link is a part of. This checks
        the number of bytes in the buffer of the link that runs opposite to this one.
        '''
        other_link_obj = self.get_opposite_link_obj()
        if constants.debug:
            print(self.ID)
            print((self.buffer_space_used + other_link_obj.buffer_space_used)/float(1024))
        return self.buffer_space_used + other_link_obj.buffer_space_used


    def get_opposite_link_obj(self):
        '''
        Get the link object that runs opposite to this one.
        '''
        other_link_id = util.flip_link_id(self.ID)

        return nwm.get_link_from_id(other_link_id)

    def log_buffer_occupancy(self):
        '''
        Log the total buffer occupancy for system analytics.
        '''
        constants.system_analytics.log_buff_occupancy(self.ID[0:-1], constants.system_EQ.currentTime, self.get_buffer_occupancy())

    def log_packet_dropped(self, num_packets):
        '''
        Log that num_packets were dropped for system analytics.
        '''
        constants.system_analytics.log_dropped_packet(self.ID[0:-1], constants.system_EQ.currentTime, num_packets)

    def log_link_rate(self, pktsize, time):
        '''
        Log the link rate by logging the number of bytes sent over at this time.
        '''
        constants.system_analytics.log_link_rate(self.ID, pktsize, time)
