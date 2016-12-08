from router import Router
import network_map as nwm
import constants

def runBellmanFord():
    ''' 
    Begin Bellman Ford by iterating through the routers and resetting the 
    weights of the necessary entries of the routers' routing tables. Then have
    every router broadcast routing table packets. 
    '''
    # broadcast RT packets from every router
    for ids in nwm.routers:
        curr_router = nwm.get_router_from_id(ids)
        # modify routing table to reset values
        curr_router.modify_routing_table()
        curr_router.broadcastRTPackets()