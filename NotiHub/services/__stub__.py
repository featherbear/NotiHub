class Service():
    TYPE_API = 0
    TYPE_PASSWORD = 1
    _NAME = ""
    _AUTHMETHOD : int = None
    def __init__(self, login, password=None, *, send, receive):
        self.authorisation = (login, password) if password else login
        self.canSend = send
        self.canReceive = receive
        pass

    def connect(self):
        raise Exception("Not implemented")

    def send(self):
        raise Exception("Not implemented")

    def listen(self):
        raise Exception("Not implemented")

    def stopListen(self):
        raise Exception("Not implemented")

    def handler(self):
        raise Exception("Not implemented")
