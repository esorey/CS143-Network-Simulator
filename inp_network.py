from link import Link
from flow import Flow
from host import Host
from router import Router
import network_map as nwm
import constants
'''
# Test code
fil = 'C:\\Users\\Sophia\\Documents\\GitHub\\CS143-Network-Simulator\\inp2.txt'
links = []
flows = []
hosts = []
routers = []
l = {}
inp_network(fil,links,flows,hosts,routers)
print lnks
print flws
'''
# LFHR

def inp_network(file):
    test_case = 1
    # Open relevant file
    f = open(file, 'r')
    # Initialize section count (each section has a specific format)
    sec_count = 0
    # Temporary host dictionary to keep track of the links attached to a host
    temp_H = {}
    # Read each line in the file
    for line in f:
        # keep track of which section we're in
        # if there is a new line then we are in a new section
        if  line == '\n':
            sec_count += 1
            continue
        # Split up parameters
        params = line.split(' ')
        # Remove extra spaces
        while '' in params:
            params.remove('')
        if constants.debug: print(params[0] + " " + params[1])
        # Set list values based on the section we're in
        # Update link and host/router parameters
        # Return these instances in arrays: flows, links, hosts, routers
        if sec_count == 0:
            # Every line will be formatted like:
            #   params = linkID   source   destination   linkRate   linkDelay   linkBuffer

            # Set up first link direction (a)
            if constants.debug: print("creating a link %s from %s to %s" %(params[0]+'a', params[1],params[2]))
            temp_link = Link(params[0]+'a',float(params[3]),float(params[4]),params[1],params[2],float(params[5]))
            if (params[0]+'a') in nwm.links:
                print('Error: link {} defined twice'.format(params[0]))
                return False
            nwm.links[params[0]+'a'] = temp_link
            # Set up other link direction (b)
            if constants.debug: print("creating a link %s from %s to %s" %(params[0]+'b', params[2], params[1]))
            temp_link = Link(params[0]+'b',float(params[3]),float(params[4]),params[2],params[1],float(params[5]))
            if (params[0]+'b') in nwm.links:
                print('Error: link {} defined twice'.format(params[0]))
                return False
            nwm.links[params[0]+'b'] = temp_link
            # Put hosts in array
            # Order by host number and then link number
            if params[1][0] == 'H':
                if params[1] in nwm.hosts:
                    print('Error: host {} has two out links'.format(params[1]))
                    return False
                else:
                    nwm.hosts[params[1]] = Host(params[1], params[0]+'a')
            # Put routers in array
            # Order by router number
            elif params[1][0] == 'R':
                if test_case == 1:
                    if params[1]=='R1' or params[1]=='R2' or params[1]=='R4':
                        if params[1] not in nwm.routers:
                            nwm.routers[params[1]] = Router(params[1])
                        if params[0] == 'L1' or params[0] == 'L3' or params[0] == 'L5':
                            nwm.routers[params[1]].routingTable['H2'] = params[0]+'a'
                else:
                    pass

            if params[2][0] == 'H':
                if params[2] in nwm.hosts:
                    print('Error: host {} has two out links'.format(params[2]))
                else:
                    nwm.hosts[params[2]] = Host(params[2], params[0] + 'b')
            elif params[2][0] == 'R':
                if test_case == 1:
                    if params[2]=='R1' or params[2]=='R2' or params[2]=='R4':
                        if params[2] not in nwm.routers:
                            nwm.routers[params[2]] = Router(params[2])
                        if params[0] == 'L1' or params[0] == 'L3' or params[0] == 'L0':
                            nwm.routers[params[2]].routingTable['H1'] = params[0]+'b'
                else:
                    pass

        # Flow parameters
        # Assume input file puts flows in order
        if sec_count == 1:
            # Every line will be formatted like:
            #   params = flowID   source   dest   dataAmt   flowStart

            if constants.debug: print("TYPE: %s %s: %s" % (type(params[3]), type(params[4]), params[4]))
            if params[0] in nwm.flows:
                print('Error: flow {} defined twice'.format(params[0]))
                return False
            nwm.flows[params[0]] = Flow(params[0],params[1],params[2],float(params[3]), float(params[4]))
    f.close()
    return True
