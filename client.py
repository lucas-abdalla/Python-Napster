import socket
import os
import pickle
import threading

class peer:

    s = socket.socket()

    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path
        self.files = os.listdir(path)

    def update(self):
        #conecta com o servidor e atualiza arquivos possuídos
        self.s.sendall("UPDATE".encode("utf-8"))
        self.s.sendall(query.encode("utf-8"))
        resposta = self.s.recv(4096).decode("utf-8")
        while True:
            if resposta == "UPDATE_OK":
                break

    def join(self):
        self.s.connect((self.IP, self.port))
        data_string = pickle.dumps(self.files)
        self.s.sendall(data_string)
        resposta = self.s.recv(4096).decode()
        if resposta == "JOIN_OK":
            print(f'Sou peer {self.s.getsockname()[0]}:{self.s.getsockname()[1]} com arquivos', end = " ")
            for file in self.files:
                print(file, end = " ")
        print()
        standby_thread = threading.Thread(target=self.standbyD, args=())
        standby_thread.start()

    def search(self):
        global query
        query = input()
        self.s.sendall(query.encode("utf-8"))
        resposta = self.s.recv(4096).decode()
        print(resposta)
        print()

    def download(self):
        IP = input()
        port = int(input())
        d = socket.socket()
        d.connect((IP, port))
        if query:
            d.sendall(query.encode("utf-8"))
            file_size = int(d.recv(4096).decode("utf-8"))
            with open(self.path + "\\" + query, "wb") as f:
                i = 0
                while i < file_size:
                    data = d.recv(1024 * 1024)
                    i += 1024 * 1024
                    f.write(data)
                f.close()
            d.close()
            print("Arquivo %s baixado com sucesso na pasta %s" % (query, self.path))
            print()
            self.update()
        else:
            print("Não foi possível baixar pois uma pesquisa por arquivo não foi feita")
    
    def standbyD(self):
        sbD = socket.socket()
        sbD.bind((self.s.getsockname()[0], self.s.getsockname()[1]))
        sbD.listen(5)
        while True:
            c, addr = sbD.accept()
            request = c.recv(4096).decode()
            if request in self.files:
                file_path = os.path.join(self.path, request)
                file_size = os.path.getsize(file_path)
                c.sendall(str(file_size).encode("utf-8"))
                with open(file_path, "rb") as f:
                    i = 0
                    while i < file_size:
                        c.sendall(f.read(1024 * 1024))
                        i += 1024 * 1024
                    f.close()
                c.close()

def printMenu():
        print("Escolha uma das opções digitando os números indicados:\n")
        print("1: Conectar ao servidor (JOIN)")
        print("2: Pesquisar arquivo (SEARCH)")
        print("3: Baixar arquivo (DOWNLOAD)")
    
def menu(p):
    printMenu()
    option = int(input())
    if option == 1:
        IP = input()
        port = int(input())
        path = input()
        p = peer(IP, port, path)
        p.join()
        menu(p)
    elif option == 2:
        p.search()
        menu(p)
    elif option == 3:
        p.download()
        menu(p)

global p
p = None
menu(p)