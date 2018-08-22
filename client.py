import socket
import threading
import sys

HOST = "localhost"
PORT = 12345
MSG_SIZE = 560


class Client:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        self.s.connect((HOST, PORT))

        inputThread = threading.Thread(target=self.sendMsg)
        inputThread.daemon = True
        inputThread.start()
    
    def sendMsg(self):
        while True:
            msg = input()
            self.s.send(msg.encode())
            

    def run(self):
        while True: 
            msg = self.s.recv(MSG_SIZE) 
            if not msg: 
                print("Server down...")
                break  
            print(msg.decode())  

    def drop(self):
        self.s.close()
            
client = Client()

try:
    client.run()
except KeyboardInterrupt:
    client.drop()
