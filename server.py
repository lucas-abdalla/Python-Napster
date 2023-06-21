import socket
import threading
import os
import pickle

class server:
    
    s = socket.socket()
    peerList = []
    
    def __init__(self, IP, port):
        server.IP = IP
        server.port = port
        server.s.bind((IP, port))
        server.start_server()

    def join(c, addr):
        files = pickle.loads(c.recv(4096))
        c_ip, c_port = c.getpeername()
        peerInfo = str(c_ip) + ";" + str(c_port) + ";"
        print(f'Peer {c_ip}:{c_port} adicionado com arquivos', end = " ")
        for file in files:
            print(file, end = " ")
            peerInfo += file + ";"
        server.peerList.append(peerInfo)
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