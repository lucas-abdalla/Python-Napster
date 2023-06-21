import socket
import threading
import os
import pickle

class server:
    
    s = socket.socket()
    
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        server.s.bind((IP, port))
        server.start_server()

    def join(c, addr):
        files = pickle.loads(c.recv(4096))
        c_ip, c_port = c.getpeername()
        #files = []
        #while True:
        #    file = c.recv(4096).decode()
        #    if not file:
        #        break
        #    files.append(file)
        #print("Peer %s:%s adicionado com arquivos" % (addr, c.getsockname()))
        print(f'Peer {c_ip}:{c_port} adicionado com arquivos', end = " ")
        for file in files:
            #print("%s" % file)
            print(file, end = " ")
        print()
        c.send("JOIN_OK".encode())

    def handle_client(c, addr):
        server.join(c, addr)

    def start_server():
        server.s.listen(5)
        while True:
            c, addr = server.s.accept()
            c_thread = threading.Thread(target=server.handle_client, args=(c, addr))
            c_thread.start()

IP = input()
port = int(input())
svr = server(IP, port)