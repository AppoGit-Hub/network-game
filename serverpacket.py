
class ServerPacket:
    def __init__(self, packet_id, validation, correction) -> None:
        self.packet_id : int = packet_id
        self.validation : bool = validation
        self.correction = correction