import sys
import event_queue
from event import Event
from flow import Flow
from inp_network import inp_network

if __name__ == "__main__":
	# Need absolute path
	# Input file (system parameters)
	# Assume input file has links and flows in number order
	inFile = sys.argv[1]
	# Output file (analytics)
	outFile = sys.argv[2]
	# Initialize arrays
	links = []
	flows = []
	hosts = []
	routers = []
	# Set up network
	inp_network(inFile,links,flows,hosts,routers)
	# Enqueue all the flows
	for flow in flows:
		start = Event(flow_start,flow.start)
		EventQueue.enqueue(start)
	# Continue to dequeue events until it is empty
	while (EventQueue.isempty()):
		curr_event = EventQueue.dequeue
		Event.handleEvent(curr_event)
	# If done with while loop, have finished all events
	# Output analytics in a text file

