# network_maps.py
links = {}
flows = {}
hosts = {}
routers = {}



####################################
### Getters for the object maps ####
####################################

def get_link_from_id(link_id):
    return links[link_id]

def get_flow_from_id(flow_id):
    return flows[flow_id]

def get_host_from_id(host_id):
    return hosts[host_id]

def get_router_from_id(router_id):
    return routers[router_id]
