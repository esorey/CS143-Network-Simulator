import sys
from event_queue import EventQueue
import constants
import network_map as nwm
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
    outFile = open(sys.argv[2], 'w')
    validNetwork = False
    # Initialize arrays

    # Initialize event queue
    constants.system_EQ = EventQueue()
    # Initialize analytics
    constants.system_analytics = Analytics(outFile)
    # Set up network
    validNetwork = inp_network(inFile)
    if not validNetwork:
        print("The network was not valid")
        exit(1)
    # Should run Bellman Ford first
    
    # Enqueue all the flows
    for flow_key, flow_obj in nwm.flows.items():
        flow_event = Event(Event.flow_start, flow_obj.start, [flow_key])
        outFile.write(str(flow_event.event_type) + "\n")
        constants.system_EQ.enqueue(flow_event)
    # Continue to dequeue events until it is empty
    while(not constants.system_EQ.isempty()):
        curr_event = constants.system_EQ.dequeue()
        EventHandler(curr_event)
    # If done with while loop, have finished all events
    # Output analytics in a text file
    constants.system_analytics.writeOutput()
    constants.system_analytics.plotOutput()
    outFile.close()