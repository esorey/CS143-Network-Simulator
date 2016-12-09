from link import Link
from flow import Flow
from flowReno import FlowReno
from flowFast import FlowFast
from host import Host
from router import Router
import network_map as nwm
import constants

def inp_network(file):
    f = open(file, 'r')
    
    sec_count = 0       # Count what section we're in
    
    temp_H = {}         # Temporary host dictionary to keep track of the links
                        #   attached to a host
    
    plot_line = 0       # Keep track of which line in plot section we are on

    for line in f:
        if  line == '\n':       # If a line contains only a new line, then 
            sec_count += 1      #   we're in a new section
            continue

        params = line.split(' ')    # Split up parameters
        
        while '' in params:         # Remove extra spaces
            params.remove('')

        # Set list values based on the section we're in
        # Update link and host/router parameters
        # Return these instances in arrays: flows, links, hosts, routers
        # Section: Link Definitions
        if sec_count == 0:
            # Every link descriptor line will be formatted like:
            #   params = linkID  src  dest  rate  delay  buffer_cap

            # Set up first link (direction a)
            temp_link = Link(params[0]+'a', float(params[3]),
                        float(params[4]), params[1], params[2], 
                        float(params[5]))

            if (params[0]+'a') in nwm.links:
                raise ValueError('Link {} defined twice'.format(params[0]))
                return False

            nwm.links[params[0]+'a'] = temp_link
            
            # Set up second link, (direction b)
            temp_link = Link(params[0]+'b', float(params[3]), 
                        float(params[4]), params[2], params[1],
                        float(params[5]))
            
            if (params[0]+'b') in nwm.links:
                raise ValueError('Link {} defined twice'.format(params[0]))
                return False

            nwm.links[params[0]+'b'] = temp_link


            # If the source parameter is a host, put host in dictionary
            # Order by host number and then link number
            if params[1][0] == 'H':
                if params[1] in nwm.hosts:
                    raise ValueError('Host {} has two out links'.format(params[1]))
                    return False
                else:
                    nwm.hosts[params[1]] = Host(params[1], params[0]+'a')

            # If the source parameter is a router, put router in dictionary
            # Order by router number
            elif params[1][0] == 'R':
                if params[1] in nwm.routers:
                    nwm.routers[params[1]].links.append(params[0]+'a')
                else:
                    nwm.routers[params[1]] = Router(params[1])
                    nwm.routers[params[1]].links.append(params[0]+'a')

            # If the destination parameter is a host, put host in dictionary
            if params[2][0] == 'H':
                if params[2] in nwm.hosts:
                    raise ValueError('Host {} has two out links'.format(params[2]))
                else:
                    nwm.hosts[params[2]] = Host(params[2], params[0]+'b')

            # If the destination parameter is a router, put router in
            #   dictionary
            elif params[2][0] == 'R':
                if params[2] in nwm.routers:
                    nwm.routers[params[2]].links.append(params[0]+'b')
                else:
                    nwm.routers[params[2]] = Router(params[2])
                    nwm.routers[params[2]].links.append(params[0]+'b')

        # Flow parameters
        # Assume input file puts flows in order
        # Section: Flow Definitions
        if sec_count == 1:
            # Every line will be formatted like:
            #   params = flowID   source   dest   dataAmt   flowStart

            if params[0] in nwm.flows:
                raise ValueError('Flow {} defined twice'.format(params[0]))
                return False

            # Set up the flow based on the congestion control we will use 
            #   for it
            if params[5] == 0:          # No congestion Control
                nwm.flows[params[0]] = Flow(params[0], params[1], params[2],
                                        float(params[3]), 
                                        float(params[4])*constants.SEC_TO_MS)

            elif params[5] == 'R\n':    # TCP Reno
                nwm.flows[params[0]] = FlowReno(params[0], params[1], 
                                        params[2], float(params[3]),
                                        float(params[4])*constants.SEC_TO_MS)

            elif params[5] == 'F\n':    # FAST TCP
                nwm.flows[params[0]] = FlowFast(params[0], params[1],
                                        params[2], float(params[3]), 
                                        float(params[4])*constants.SEC_TO_MS)

        # Plot Output Section
        if sec_count == 2:
            params[-1] = params[-1][:2]

            if plot_line == 0:          # First line is links to plot
                nwm.links2plot = params
            elif plot_line == 1:        # Second is flows to plot
                nwm.flows2plot = params

            plot_line += 1

    f.close()

    # Set up the router's routing tables
    for router_id in nwm.routers:
        router = nwm.get_router_from_id(router_id)
        router.init_routing_table()

    return True
