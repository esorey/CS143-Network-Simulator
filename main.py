import sys
from event_queue import EventQueue
import constants
import network_map as nwm
from eventhandler import EventHandler
from flow import Flow
from inp_network import inp_network
from event import Event
from analytics import Analytics
import BellmanFord

if __name__ == "__main__":
    # Need absolute path
    # Input file (system parameters)
    # Assume input file has links and flows in number order
    inFile = sys.argv[1]
    # Output file (analytics)
    outFile = open(sys.argv[2], 'w')
    validNetwork = False
    # Initialize arrays


    constants.cngstn_ctrl = 1

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
    BellmanFord.runBellmanFord()
    # Continue to dequeue events until it is empty
    while(not constants.system_EQ.isempty()):
        curr_event = constants.system_EQ.dequeue()
        EventHandler(curr_event)

    for r in nwm.routers.keys():
        router = nwm.get_router_from_id(r)
        print("--" + r + "--")
        print(str(router.routingTable))

    # Initialize global variable indicating when all flows are done
    constants.all_flows_done = False
    # Enqueue all the flows
    for flow_key, flow_obj in nwm.flows.items():
        flow_event = Event(Event.flow_start, flow_obj.start, [flow_key])
        outFile.write(str(flow_event.event_type) + "\n")
        constants.system_EQ.enqueue(flow_event)

    bellman_event = Event(Event.bellman_ford, constants.BELLMAN_PERIOD, None)
    constants.system_EQ.enqueue(bellman_event)
    bellman_event = Event(Event.bellman_ford, 300, None)
    constants.system_EQ.enqueue(bellman_event)
    # Continue to dequeue events until it is empty
    while((not constants.system_EQ.isempty()) and (not constants.all_flows_done)):
        curr_event = constants.system_EQ.dequeue()
        EventHandler(curr_event)

    # If done with while loop, have finished all events
    # Output analytics in a text file
    constants.system_analytics.writeOutput()
    constants.system_analytics.plotOutput()
    outFile.close()