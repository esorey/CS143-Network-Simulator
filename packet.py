import constants

class Packet:
    def __init__(self, packet_id, origin_id, destination_id, size):
        self.packet_id = packet_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.size = size

class RoutingTablePacket(Packet):
    def __init__(self, packet_id, origin_id, size):
        # No destination because it needs to go to all neighbors of the origin node
        super().__init__(packet_id, origin_id, None, size)


class DataPacket(Packet):
    def __init__(self, packet_id, origin_id, destination_id, flow_id):
        super().__init__(packet_id, origin_id, destination_id, constants.DATA_PKT_SIZE)
        self.flow_id = flow_id

class AckPacket(Packet):
    def __init__(self, packet_id, origin_id, destination_id, flow_id):
        super().__init__(packet_id, origin_id, destination_id, constants.ACK_PKT_SIZE)
        self.flow_id = flow_id
