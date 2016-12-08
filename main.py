import sys
import constants
import BellmanFord

from event_queue import EventQueue
from eventhandler import EventHandler
from flow import Flow
from inp_network import inp_network
from event import Event
from analytics import Analytics

import network_map as nwm

if __name__ == "__main__":
    # Need absolute path
    # Input file (system parameters)
    # Assume input file has links and flows in number order
    inFile = sys.argv[1]

    validNetwork = False
    validNetwork = inp_network(inFile)

    if not validNetwork:
        print("The network was not valid")
        exit(1)

    constants.system_EQ = EventQueue()
    constants.system_analytics = Analytics(nwm.links2plot, nwm.flows2plot)

    # Initial Bellman Ford to set up routing tables
    BellmanFord.runBellmanFord()   

    # Continue to dequeue events until it is empty (i.e. initial Bellman ford
    #   is finished and routing tables have initial paths)
    while(not constants.system_EQ.isempty()):
        curr_event = constants.system_EQ.dequeue()
        EventHandler(curr_event)

    if constants.debug:
        for r in nwm.routers.keys():
            router = nwm.get_router_from_id(r)
            print("--" + r + "--")
            print(str(router.routingTable))

    # Initialize global variable indicating when all flows are done
    constants.all_flows_done = False

    # Enqueue all the flows by enqueueing flow_start events
    for flow_key, flow_obj in nwm.flows.items():
        flow_event = Event(Event.flow_start, flow_obj.start, [flow_key])
        constants.system_EQ.enqueue(flow_event)

    # Enqueue a bellman ford routing table update event at BELLMAN_PERIOD
    bellman_event = Event(Event.bellman_ford, constants.BELLMAN_PERIOD, None)
    constants.system_EQ.enqueue(bellman_event)

    # Running the actual simulation
    # Continue to dequeue events from event queue until it is empty
    while((not constants.system_EQ.isempty()) and \
            (not constants.all_flows_done)):
        curr_event = constants.system_EQ.dequeue()
        EventHandler(curr_event)

    # If we have finished all the events, then plot the analytics
    constants.system_analytics.plotOutput()
