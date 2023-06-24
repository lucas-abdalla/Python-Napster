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

    def join(c, addr, data):
        files = pickle.loads(data)
        c_ip, c_port = c.getpeername()
        peerInfo = str(c_ip) + ";" + str(c_port) + ";"
        print(f'Peer {c_ip}:{c_port} adicionado com arquivos', end = " ")
        for file in files:
            print(file, end = " ")
            peerInfo += file + ";"
        server.peerList.append(peerInfo)
        print()
        c.send("JOIN_OK".encode("utf-8"))
        server.handle_client(c, addr)

    def search(c, addr, data):
        resposta = "peers com arquivo solicitado: "
        query = data.decode("utf-8")
        c_ip, c_port = c.getpeername()
        print("Peer %s:%s solicitou arquivo %s" % (str(c_ip), str(c_port), query))
        for peer in server.peerList:
            peerArr = peer.split(';')
            i = 2
            for i in range(len(peerArr)):
                if (peerArr[i] == query):
                    resposta += str(peerArr[0]) + ":" + str(peerArr[1]) + " "
        c.sendall(resposta.encode("utf-8"))
        server.handle_client(c, addr)

    def handle_client(c, addr):
        data = c.recv(2097152)
        if data[0] == 0x80:
            server.join(c, addr, data)
        else:
            server.search(c, addr, data)

    def start_server():
        server.s.listen(5)
        while True:
            c, addr = server.s.accept()
            c_thread = threading.Thread(target=server.handle_client, args=(c, addr))
            c_thread.start()

IP = input()
port = int(input())
svr = server(IP, port)