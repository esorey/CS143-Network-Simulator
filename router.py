from link import Link
from flow import Flow
from event import Event
from packet import Packet
from event_queue import EventQueue
import network_map as nwm
import util
from packet import RoutingTablePacket


import constants
class Router:
    """Router: end points of the network"""
    def __init__(self, id):
        self.id = id
        self.links = [] # All links are outgoing from this router
        self.routingTable = None
        self.changeCurr = True
        self.changePrev = True

    def init_routing_table(self):
        '''Initialize the routing table.'''
        # Get dict of hosts
        routing_table = {}
        hosts_dict = nwm.hosts
        print(nwm.hosts)
        for host_id in hosts_dict.keys():
            host_obj = nwm.get_host_from_id(host_id)
            host_link_id = host_obj.out_link

            flipped_link_id = util.flip_link_id(host_link_id)

            host_link_obj = nwm.get_link_from_id(flipped_link_id)
            link_dest = host_link_obj.A
            # If the link connects to this router, add the host and weights to the routing table
            if link_dest == self.id:
                routing_table[host_id] = [flipped_link_id, host_link_obj.get_buffer_occupancy()]

            # If not, mark the host as link unknown, distance infinity
            else:
                routing_table[host_id] = [None, float("Inf"), self.id]

        print("Routing table for " + self.id + " is " + str(routing_table))
        self.routingTable = routing_table

    def modify_routing_table(self):
        '''modify the routing table.'''
        # Get dict of hosts
        routing_table = {}
        hosts_dict = nwm.hosts
        print(nwm.hosts)
        for host_id in hosts_dict.keys():
            host_obj = nwm.get_host_from_id(host_id)
            host_link_id = host_obj.out_link

            flipped_link_id = util.flip_link_id(host_link_id)

            host_link_obj = nwm.get_link_from_id(flipped_link_id)
            link_dest = host_link_obj.A
            # If the link connects to this router, add the host and weights to the routing table
            if link_dest == self.id:
                routing_table[host_id] = [flipped_link_id, host_link_obj.get_buffer_occupancy()]

            # If not, mark the host as link unknown, distance infinity
            else:
                routing_table[host_id] = [flipped_link_id, float("Inf"), self.id]

        print("Routing table for " + self.id + " is " + str(routing_table))
        self.routingTable = routing_table
        
    '''Bellman-Ford Algorithm: Update routing tables based
    on congestion information'''
 # The main function that finds shortest distances from src to
    # all other vertices using Bellman-Ford algorithm.  The function
    # also detects negative weight cycle
    def BellmanFord(self):
        src = self.id
        bufTable = {}
        # Step 1: Initialize buffer occupancy from src to all other vertices
        # as INFINITE
        for i in self.links:
            self.bufTable[i] = float('Inf')
        bufTable[src] = 0
 
 
        # Step 2: Relax all edges |V| - 1 times. A simple shortest 
        # path from src to any other vertex can have at-most |V| - 1 
        # edges
        for i in range(self.routingTable - 1):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            for u, v, w in self.graph:
                if bufTable[u] != float("Inf") and dist[u] + w < dist[v]:
                    bufTable[v] = bufTable[u] + w
 
        # Step 3: check for negative-weight cycles.  The above step 
        # guarantees shortest distances if graph doesn't contain 
        # negative weight cycle.  If we get a shorter path, then there
        # is a cycle.
 
        for u, v, w in self.graph:
            if bufTable[u] != float('Inf') and bufTable[u] + w < bufTable[v]:
                print("!--Graph contains negative weight cycle--!")
                return

    # starts bellman ford             
    def broadcastRTPackets(self):
        for link in self.links:
            # make routing table packets
            # format of routing table: packet_id, origin_id, size, link_id, routing_table
            pckt = RoutingTablePacket(None, self.id, constants.RTABLE_PKT_SIZE, link, self.routingTable)
            # enqueue each routing table packet and send it down each link that the
            # router is attached to
            send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [link, pckt])
            constants.system_EQ.enqueue(send_pckt_event)


    def receivePackets(self, pckt):
        self.changePrev = self.changeCurr
        self.changeCurr = False
        if type(pckt) is RoutingTablePacket:
            print("Routing table for " + self.id + " is " + str(self.routingTable))

            # do bellman Ford
            # check the routing table of the packet
            # format is hostID: [link_id, bufferOccupancy]
            origin_link = nwm.get_link_from_id(pckt.link_id)
            link_cost = origin_link.get_buffer_occupancy()
            # is curr occupancy + value  in the routing table from the other guy
            for hosts in pckt.routing_table.keys():
                new_cost = pckt.routing_table[hosts][1] + link_cost
                print("New Cost: " + str(new_cost))
                print("original cost: " + str(self.routingTable[hosts][1]))
                if new_cost < self.routingTable[hosts][1]:
                    self.routingTable[hosts][1] = new_cost
                    # want to flip the ID because direction is reversed
                    self.routingTable[hosts][0] = util.flip_link_id(pckt.link_id)
                    self.changeCurr = True

            if self.changeCurr == True:
                print("CHECK: " + str(self.routingTable))
                self.broadcastRTPackets()
            if self.changePrev == True and self.changeCurr == False:
                constants.Bellman_not_done -= 1
            elif self.changePrev == False and self.changeCurr == True:
                constants.Bellman_not_done += 1
        else:
            next_link = self.routingTable[pckt.destination_id][0]
            send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [next_link, pckt])
            constants.system_EQ.enqueue(send_pckt_event)
