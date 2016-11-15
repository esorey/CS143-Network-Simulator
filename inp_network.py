from link import Link
from flow import Flow
from host import Host
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

def inp_network(file, L=[], F=[], H={}, R={}):
    debug = True 
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
        if debug: print(params[0] + " " + params[1])
        # Set list values based on the section we're in
        # Update link and host/router parameters
        # Return these instances in arrays: flows, links, hosts, routers
        if sec_count == 0:
            # Set up first link direction (a)
            if debug: print("creating a link %s from %s to %s" %(params[0]+'a', params[1],params[2]))
            temp_link = Link(params[0]+'a',float(params[3]),float(params[4]),params[1],params[2],float(params[5]))
            L.append(temp_link)
            # Set up other link direction (b)
            if debug: print("creating a link %s from %s to %s" %(params[0]+'b', params[2], params[1]))
            temp_link = Link(params[0]+'b',float(params[3]),float(params[4]),params[2],params[1],float(params[5]))
            L.append(temp_link)
            # Put hosts in array
            # Order by host number and then link number
            if params[1][0] == 'H':
                if debug:
                    print(H)
                    # TODO: why 2*(int(params[1][1])-1)? 
                    print(2*(int(params[1][1])-1))
                H[2*(int(params[1][1])-1)]= Host(params[1], params[0]+'a')
            # Put routers in array
            # Order by router number
            elif params[1][0] == 'R':
                pass
            if params[2][0] == 'H':
                H[2*(int(params[2][1]-1)+1)] = Host(params[2],params[0]+'b')
            elif params[2][0] == 'R':
                pass

        # Flow parameters
        # Assume input file puts flows in order
        if sec_count == 1:
            if debug: print("TYPE: %s %s: %s" % (type(params[3]), type(params[4]), params[4]))
            F.append(Flow(params[0],params[1],params[2],float(params[3]), float(params[4])))
    f.close()

if __name__ == '__main__':
    inp_network("inp2.txt")