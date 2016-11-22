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

    ''' Pseudo code below change later'''
    def initialize(self, graph, source):
        dest = {} # destination
        pred = {} # predecessor
        for node in graph:
            dest[node] = float('Inf')
            pred[node] = None
        dest[node] = 0 # for the source we can reach
        return dest, pred
        
    '''Bellman-Ford Algorithm: Update routing tables based
    on congestion information'''
    def bellmanFord(self, graph, source):
        # run bellman ford
        '''
        def relax(node, neighbour, graph, d, p):
        # If the distance between the node and the neighbour is lower than the one I have now
        if d[neighbour] > d[node] + graph[node][neighbour]:
            # Record this lower distance
            d[neighbour]  = d[node] + graph[node][neighbour]
            p[neighbour] = node

        def bellman_ford(graph, source):
            d, p = initialize(graph, source)
            for i in range(len(graph)-1): #Run this until is converges
                for u in graph:
                    for v in graph[u]: #For each neighbour of u
                        relax(u, v, graph, d, p) #Lets relax it

            # Step 3: check for negative-weight cycles
            for u in graph:
                for v in graph[u]:
                    assert d[v] <= d[u] + graph[u][v]

            return d, p

        '''
        pass
    def receivePackets(self, pckt):
        next_link = self.routingTable[pckt.destination_id]
        send_pckt_event = Event(Event.pckt_send, constants.system_EQ.currentTime, [next_link, pckt])
        constants.system_EQ.enqueue(send_pckt_event)