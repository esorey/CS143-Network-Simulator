from link import link
from flow import flow
class router:
	"""Router: end points of the network"""
	def __init__(self, id):
		super(Host, self).__init__()
		self.id = id
		self.routingTable = []

''' Pseudo code below change later'''
	def initialize(graph, source):
		dest = {} # destination
		pred = {} # predecessor
		for node in graph:
			dest[node] = float('Inf')
			pred[node] = None
		dest[node] = 0 # for the source we can reach
		return dest, pred
		
	'''Bellman-Ford Algorithm: Update routing tables based
	on congestion information'''
	def bellmanFord(graph, source):
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