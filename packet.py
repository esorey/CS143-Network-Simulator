import constants

class Packet:
    def __init__(self, packet_id, origin_id, destination_id, size):
        self.packet_id = packet_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.size = size

class RoutingTablePacket(Packet):
    def __init__(self, packet_id, origin_id, size, link_id, routing_table):
        # No destination because it needs to go to all neighbors of the origin node
        super().__init__(packet_id, origin_id, None, size)
        self.link_id = link_id              # Link that the routing table packet arrived on
        self.routing_table = routing_table  # Routing table informaiton

class DataPacket(Packet):
    def __init__(self, packet_id, origin_id, destination_id, pkt_flow):
        super().__init__(packet_id, origin_id, destination_id, constants.DATA_PKT_SIZE)
        self.owner_flow = pkt_flow

class AckPacket(Packet):
    def __init__(self, packet_id, origin_id, destination_id, pkt_flow, ack_time):
        super().__init__(packet_id, origin_id, destination_id, constants.ACK_PKT_SIZE)
        self.owner_flow = pkt_flow
        self.ack_sent_time = ack_time
