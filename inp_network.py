from link import Link
from flow import Flow
from host import Host

def inp_network(file, L=[], F=[], H=[], R=[]):
    # Open relevant file
    f = open(file, 'r')
    # Initialize section count (each section has a specific format)
    sec_count = 0
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
        # Set list values based on the section we're in
        # Update link and host/router parameters
        # Return these instances in arrays: flows, links, hosts, routers
        if sec_count == 0:
            # Set up first link direction (a)
            temp_link = Link(params[0]+'a',float(params[3]),float(params[4]),params[1],params[2],float(params[5]))
            L.append(temp_link)
            # Set up other link direction (b)
            temp_link = Link(params[0]+'b',float(params[3]),float(params[4]),params[2],params[1],float(params[5]))
            L.append(temp_link)
            # Put hosts in array
            # Order by host number and then link number
            if params[1][0] == 'H':
                H[2*int(params[1][1])]= Host(params[1],params[0]+'a')
            # Put routers in array
            # Order by router number
            elif params[1][0] == 'R':
                pass
            if params[2][0] == 'H':
                H[2*int(params[2][1]+1)] = Host(params[2],params[0]+'b')
            elif params[2][0] == 'R':
                pass

        # Flow parameters
        # Assume input file puts flows in order
        if sec_count == 1:
            F.append(Flow(params[0],params[1],params[2],params[3],params[4]))
    f.close()

'''
# Test code
fil = 'C:\Users\Sophia\Documents\GitHub\CS143-Network-Simulator\inp2.txt'
links = []
flows = []
hosts = []
routers = []
l = {}
inp_network(fil,links,flows,hosts,routers)
print lnks
print flws
'''