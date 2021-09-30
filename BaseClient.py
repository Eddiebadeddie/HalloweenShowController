class Client:
    def __init__(self, connection, address):
        self.address = address
        self.connection = connection
        self.messageCount = 0