import socket
import threading

HOST = "localhost"
PORT = 12345
MSG_SIZE = 560

class Server:
    chat_group = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lock = threading.Lock()

    def __init__(self):
        self.s.bind((HOST, PORT))
        self.s.listen(1)

    def handler(self, conn, addr):
        msgConnect = "{} joined the group".format(addr)
        msgDisconnect = "{} disconnected".format(addr)

        for connection in self.chat_group:
            if connection != conn:
                connection.send(msgConnect.encode())

        while True:
            data = conn.recv(MSG_SIZE).decode()

            if not data: 
                self.lock.acquire()
                self.chat_group.remove(conn)
                self.lock.release()
                for connection in self.chat_group:
                    connection.send(msgDisconnect.encode())
                conn.close()
                break
                
            for connection in self.chat_group:
                if connection != conn:
                    connection.send("{}: {}".format(addr,data).encode())
            


    def run(self):
        print("Chat application")
        while True:
            conn, addr = self.s.accept()
            connThread = threading.Thread(target=self.handler, args=(conn, addr))
            connThread.daemon = True
            connThread.start()
            self.lock.acquire()
            self.chat_group.append(conn)
            self.lock.release()
            print(self.chat_group)
    
    def drop(self):
        for connection in self.chat_group:
            connection.close()


server = Server()
try:
    server.run()
except KeyboardInterrupt:
    server.drop()
