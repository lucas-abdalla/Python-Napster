import socket
import os
import pickle

class peer:

    s = socket.socket()

    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path
        self.files = os.listdir(path)

    def update():
        #conecta com o servidor e atualiza arquivos possuídos
        pass

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

    def search(self):
        query = input()
        self.s.sendall(query.encode("utf-8"))
        resposta = self.s.recv(4096).decode()
        print(resposta)
        print()

    def download(self):
        self.update()

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