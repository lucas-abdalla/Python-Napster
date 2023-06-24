import socket
import threading
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

    def update(c, addr):
        data = c.recv(4096)
        file = data.decode("utf-8")
        c_ip, c_port = c.getpeername()
        for i in range (len(server.peerList)):
            peerArr = server.peerList[i].split(';')
            if (str(c_ip) == peerArr[0] and str(c_port) == peerArr[1]):
                server.peerList[i] += file + ";"
            #if str(c_ip) + ";" + str(c_port) in peer:
            #    peer += file + ";"
        c.sendall("UPDATE_OK".encode("utf-8"))
        server.handle_client(c, addr)

    def handle_client(c, addr):
        try:
            data = c.recv(2097152)
            if data[0] == 0x80:
                server.join(c, addr, data)
            else:
                aux = data.decode("utf-8")
                if aux == "UPDATE":
                    server.update(c, addr)
                else:
                    server.search(c, addr, data)
        except Exception as e:
            pass
        #elif data.decode("utf-8") == "UPDATE":
        #    server.update(c, addr, data)
        #else:
        #    server.search(c, addr, data)

    def start_server():
        server.s.listen(5)
        while True:
            c, addr = server.s.accept()
            c_thread = threading.Thread(target=server.handle_client, args=(c, addr))
            c_thread.start()

IP = input()
port = int(input())
svr = server(IP, port)