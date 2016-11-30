from link import Link
from flow import Flow
from event import Event
from event_queue import EventQueue
import network_map as nwm

import constants
class Router:
    """Router: end points of the network"""
    def __init__(self, id):
        self.id = id
        self.routingTable = {}
        self.links = []
        
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
                     

    def receivePackets(self, pckt):
        next_link = self.routingTable[pckt.destination_id]
        send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [next_link, pckt])
        constants.system_EQ.enqueue(send_pckt_event)