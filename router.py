from link import Link
from flow import Flow
from event import Event
from packet import Packet
from event_queue import EventQueue
import network_map as nwm
from packet import RoutingTablePacket
import util
import constants

class Router:
    '''Router: end points of the network'''
    def __init__(self, id):
        self.id = id
        self.links = [] # All links are outgoing from this router
        self.routingTable = None
        self.changeCurr = True

    def init_routing_table(self):
        '''
        Initialize the routing table. hosts that are not directly connected
        to the router have their links set to unknown, distance infinity.
        '''
        self.modify_routing_table(False)

    def modify_routing_table(self, setLink=True):
        '''
        modify the routing table. Hosts not directly connected to the router
        retain the pre-set link ID to travel down but have distances reset to
        infinity. 
        '''

        routing_table = {}
        hosts_dict = nwm.hosts
        for host_id in hosts_dict.keys():
            host_obj = nwm.get_host_from_id(host_id)
            host_link_id = host_obj.out_link
            flipped_link_id = util.flip_link_id(host_link_id)

            host_link_obj = nwm.get_link_from_id(flipped_link_id)
            link_dest = host_link_obj.A
            # If the link connects to this router, add the host 
            # and weights to the routing table
            if link_dest == self.id:
                routing_table[host_id] = [flipped_link_id, 
                    host_link_obj.get_buffer_occupancy()]

            else:
                if setLink==False:
                    routing_table[host_id] = [None, float("Inf"), self.id]
                else:
                    # mark the host as link unknown, distance infinity
                    routing_table[host_id] = [flipped_link_id, float("Inf"), 
                        self.id]

        #print("Routing table for " + self.id + " is " + str(routing_table))
        self.routingTable = routing_table
        
    def broadcastRTPackets(self):
        '''
        Router begins broadcasting packets down all of its neighboring links 
        for Bellman Ford
        '''
        for link in self.links:
            # make routing table packets
            # format of routing table: packet_id, origin_id, size, link_id, routing_table
            pckt = RoutingTablePacket(None, self.id, constants.RTABLE_PKT_SIZE, link, self.routingTable)
            # enqueue each routing table packet and send it down each link that the
            # router is attached to
            send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [link, pckt])
            constants.system_EQ.enqueue(send_pckt_event)


    def receivePackets(self, pckt):
        '''
        When a router receives a packet, a new weight is calculated from
        the packet's routing table packet and current link cost. If the new 
        weight is less than the corresponding stored weight in the router, the
        entry is over-written. The router then logs a change and broadcasts 
        another round of routing table packets. Bellman Ford will continue to
        run until there are no changes to be made.
        '''
        self.changeCurr = False
        if type(pckt) is RoutingTablePacket:
            #print("Routing table for "+self.id+" is "+str(self.routingTable))

            # Check the routing table of the packet
            origin_link = nwm.get_link_from_id(pckt.link_id)
            link_cost = origin_link.get_buffer_occupancy()
            for hosts in pckt.routing_table.keys():
                new_cost = pckt.routing_table[hosts][1] + link_cost
                #print("New Cost: " + str(new_cost))
                #print("original cost: " + str(self.routingTable[hosts][1]))
                if new_cost < self.routingTable[hosts][1]:
                    self.routingTable[hosts][1] = new_cost
                    # want to flip the ID because direction is reversed
                    self.routingTable[hosts][0] = util.flip_link_id(pckt.link_id)
                    self.changeCurr = True

            # A change has been made to the routing table
            if self.changeCurr == True:
                #print("CHECK: " + str(self.routingTable))
                self.broadcastRTPackets()
        else:
            next_link = self.routingTable[pckt.destination_id][0]
            send_pckt_event = Event(Event.pckt_send, 
                constants.system_EQ.currentTime, [next_link, pckt])
            constants.system_EQ.enqueue(send_pckt_event)
