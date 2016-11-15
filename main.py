import sys
from event_queue import EventQueue
import constants
from eventhandler import EventHandler
from flow import Flow
from inp_network import inp_network
from event import Event
from analytics import Analytics

if __name__ == "__main__":
    # Need absolute path
    # Input file (system parameters)
    # Assume input file has links and flows in number order
    inFile = sys.argv[1]
    # Output file (analytics)
    outFile = sys.argv[2]
    # Initialize arrays
    links = {}
    flows = {}
    hosts = {}
    routers = {}

    # Initialize event queue
    constants.system_EQ = EventQueue()
    # Initialize analytics
    constants.system_analytics = Analytics()
    # Set up network
    inp_network(inFile,links,flows,hosts,routers)
    # Enqueue all the flows
    for flow_obj in flows:
        flow_event = Event(Event.flow_start, flow_obj.start, [flow_obj])
        constants.system_eq.enqueue(flow_event)
    # Continue to dequeue events until it is empty
    while(not constants.system_eq.isempty()):
        curr_event = constants.system_eq.dequeue()
        EventHandler(curr_event)
    # If done with while loop, have finished all events
    # Output analytics in a text file
