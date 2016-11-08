def inp_network(file, links={}, flows={}):
    f = open(file, 'r')
    sec_count = 0
    for line in f:
        # keep track of which section we're in
        if  line == '\n':
            sec_count += 1
            continue
        params = line.split(' ')
        while '' in params:
            params.remove('')
        if sec_count == 0:
            links[params[1]] = [params[0],params[2][0:2]]
        if sec_count == 1:
            links[params[0]].append(float(params[1]))
            links[params[0]].append(float(params[2]))
            links[params[0]].append(float(params[3]))
        if sec_count == 2:
            flows[params[0]] = [params[1], params[2], float(params[3]), float(params[4])]

'''
# Test code
fil = 'C:\Users\Sophia\Documents\GitHub\CS143-Network-Simulator\inp2.txt'
lnks = {}
flws = {}
inp_network(fil,lnks,flws)
print lnks
print flws
'''