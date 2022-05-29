

class ClientPacket:
    def __init__(self, id, code, data):
        self.id : int = id
        self.code : bytes = code
        self.data = data