from link import Link
from flow import flow

def inp_network(file, L=[], F=[]):
    # Open relevant file
    f = open(file, 'r')
    # Dictionary of links and flows to hold data while reading from file
    links = {}
    flows = {}
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
        # Set dictionary values based on the section we're in
        # What link is connecting
        if sec_count == 0:
            links[params[1]] = [params[0],params[2][0:2]]
        # What the link parameters are
        if sec_count == 1:
            links[params[0]].append(float(params[1]))
            links[params[0]].append(float(params[2]))
            links[params[0]].append(float(params[3]))
        # Flow parameters
        if sec_count == 2:
            flows[params[0]] = [params[1], params[2], float(params[3]), float(params[4])]
    f.close()
    # Set class instances to the parameters from file
    # Return these instances in arrays, one for flow one for link
    for link in links:
        print link
        temp_link = Link(link+'a',links[link][2],links[link][3],links[link][0],links[link][1],links[link][4])
        L.append(temp_link)
        temp_link = Link(link+'b',links[link][2],links[link][3],links[link][0],links[link][1],links[link][4])
        L.append(temp_link)
    for fl in flows:
        temp_flow = flow(fl,flows[fl][0],flows[fl][1],flows[fl][2],flows[fl][3])
        F.append(temp_flow)

'''
# Test code
fil = 'C:\Users\Sophia\Documents\GitHub\CS143-Network-Simulator\inp2.txt'
lnks = []
flws = []
l = {}
inp_network(fil,lnks,flws,l)
print lnks
print flws
'''