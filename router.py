from link import Link
from flow import Flow
from event import Event
from event_queue import EventQueue
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
    def BellmanFord(self, src):
 
        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE
        for i in self.links:
            self.routingTable[i] = float('Inf')
        routingTable[src] = 0
 
 
        # Step 2: Relax all edges |V| - 1 times. A simple shortest 
        # path from src to any other vertex can have at-most |V| - 1 
        # edges
        for i in range(self.V - 1):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            for u, v, w in self.graph:
                if routingTable[u] != float("Inf") and dist[u] + w < dist[v]:
                    routingTable[v] = routingTable[u] + w
 
        # Step 3: check for negative-weight cycles.  The above step 
        # guarantees shortest distances if graph doesn't contain 
        # negative weight cycle.  If we get a shorter path, then there
        # is a cycle.
 
        for u, v, w in self.graph:
            if routingTable[u] != float('Inf') and routingTable[u] + w < routingTable[v]:
                print("!--Graph contains negative weight cycle--!")
                return
                     

    def receivePackets(self, pckt):
        next_link = self.routingTable[pckt.destination_id]
        send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [next_link, pckt])
        constants.system_EQ.enqueue(send_pckt_event)