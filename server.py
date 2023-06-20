import socket
import threading
import os

def join(c, addr):
    files = []
    while True:
        file = c.recv(4096).decode()
        if not file:
            break
        files.append(file)
    print("Peer %s:%s adicionado com arquivos" % (addr, c.getsockname()))
    for file in files:
        print(" %s" % file)
    c.send("JOIN_OK".encode())

def handle_client(c, addr):
    join(c, addr)
    #files = []
    #while True:
    #    file = c.recv(4096).decode()
    #    if not file:
    #        break
    #    files.append(file)
    #print("Peer %s:%s adicionado com arquivos" % (addr, c.getsockname()))
    #for file in files:
    #    print(" %s" % file)
    #c.send("JOIN_OK".encode())

s = socket.socket()
port = 1099

s.bind(('127.0.0.1', port))
s.listen(5)

while True:
    c, addr = s.accept()
    c_thread = threading.Thread(target=handle_client, args=(c, addr))
    c_thread.start()