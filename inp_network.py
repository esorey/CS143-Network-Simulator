from link import Link
from flow import flow
from host import host

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
            temp_link = Link(params[0]+'a',float(params[3]),float(params[4]),params[1],params[2],float(params[5]))
            L.append(temp_link)
            temp_link = Link(params[0]+'b',float(params[3]),float(params[4]),params[2]),params[1],float(params[5]))
            L.append(temp_link)
            if params[1][0] == 'H':
                H.append(host(params[1],params[0]+'a'))
            elif params[1][0] == 'R':
                pass
            if params[2][0] == 'H':
                H.append(host(params[2],params[0]+'b'))
            elif params[2][0] == 'R':
                pass

        # Flow parameters
        if sec_count == 1:
            F.append(flow(params[0],params[1],params[2],params[3],params[4]))
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