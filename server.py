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
        data = b''
        while True:
            chunk = c.recv(4096)
            if not chunk:
                break
            data += chunk
        files = pickle.loads(data)
        c_ip, c_port = c.getpeername()
        peerInfo = str(c_ip) + ";" + str(c_port) + ";"
        print(f'Peer {c_ip}:{c_port} adicionado com arquivos', end = " ")
        for file in files:
            print(file, end = " ")
            peerInfo += file + ";"
        server.peerList.append(peerInfo)
        print(server.peerList)
        print()
        c.send("JOIN_OK".encode("utf-8"))

    def search(c, addr):
        resposta = "peers com arquivo solicitado: "
        query = c.recv(4096).decode("utf-8")
        c_ip, c_port = c.getpeername()
        print("Peer %s:%s solicitou arquivo %s" % c_ip, c_port, query)
        print()
        for peer in server.peerList:
            i = 2
            for i in range(len(peer)):
                if (peer == query):
                    resposta += str(peer[0]) + ":" + str(peer[1]) + " "
        c.sendall(resposta.encode("utf-8"))

    def handle_client(c, addr):
        server.join(c, addr)
        option = c.recv(4096).decode("utf-8")
        if option == "JOIN":
            c.send("JOIN".encode("utf-8"))
            server.join(c, addr)
        elif option == "SEARCH":
            c.send("SEARCH".encode("utf-8"))
            server.search(c, addr)

    def start_server():
        server.s.listen(5)
        while True:
            c, addr = server.s.accept()
            c_thread = threading.Thread(target=server.handle_client, args=(c, addr))
            c_thread.start()

IP = input()
port = int(input())
svr = server(IP, port)