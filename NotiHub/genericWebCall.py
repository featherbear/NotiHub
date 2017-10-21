import socket
from threading import Thread
from socketserver import ThreadingMixIn
import urllib.parse

def handler(data: bytearray, callback: socket.socket):
    response = None
    print("GOT:", data)
    callback.send(b"\x32\x30\x31\x37\x30\x39\x32\x35\x2e\x34\x30\x35")
    print("SENT")
    data = [urllib.parse.unquote(part.decode("ascii")) for part in (data[5:data.index(b" HTTP/")].split(b"/") if data.startswith(b"GET /") else data.split(b'\x00'))]
    if len(data) == 3:
        APP, TITLE, CONTENT = data
        print(APP,TITLE,CONTENT)
    if response: callback.send(response)

class udpThread(Thread):
    def __init__(self,):
        Thread.__init__(self)
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 80))
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        print("Run UDP")
        while True:
            data = self.socket.recv(2048)
            #self.socket.send(b"\x00")
            #print("Receive UDP |",data)
            handler(data,self.socket)

class tcpThread(Thread):
    def __init__(self,):
        Thread.__init__(self)
        self.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 80))
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        print("Run TCP")
        self.socket.listen()
        while True:
            conn, addr = self.socket.accept()
            data = conn.recv(2048)
            #conn.send(b"\x00")
            #print("Receive TCP |", data)
            handler(data,conn)


tcpServer  = tcpThread()
udpServer = udpThread()

print("Call start")
tcpServer.start()
udpServer.start()
print("Call finish")
