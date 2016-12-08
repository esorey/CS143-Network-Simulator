from router import Router
import network_map as nwm
import constants

def runBellmanFord():
    # broadcast RT packets from every router
    for ids in nwm.routers:
        curr_router = nwm.get_router_from_id(ids)
        # modify routing table to reset values
        curr_router.modify_routing_table()
        curr_router.broadcastRTPackets()