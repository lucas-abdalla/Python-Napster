import socket
import os
import pickle

class peer:

    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path
        self.files = os.listdir(path)

    def printMenu():
        print("Escolha uma das opções digitando os números indicados:\n")
        print("1: Conectar ao servidor")
        print("2: Pesquisar arquivo")
        print("3: Baixar arquivo")
    
    def menu(self):
        peer.printMenu()
        option = int(input())
        if option == 1:
            self.join()
        elif option == 2:
            self.search()
        elif option == 3:
            self.download()

    def update():
        #conecta com o servidor e atualiza arquivos possuídos
        pass

    def join(self):
        s = socket.socket()
        s.connect((self.IP, self.port))
        data_string = pickle.dumps(self.files)
        s.sendall(data_string)
        resposta = s.recv(4096).decode()
        if (resposta == "JOIN_OK"):
            #print("Sou peer %s:%s, com arquivos " % (self.IP, s.getsockname()))
            print(f'Sou peer {s.getsockname()[0]}:{s.getsockname()[1]} com arquivos', end = " ")
            for file in self.files:
                #print(" %s" % file)
                print(file, end = " ")
        print()
        self.menu()

    def search(self):
        self.menu()

    def download(self):
        self.update()
        self.menu()
        
IP = input()
port = int(input())
path = input()
p = peer(IP, port, path)
p.menu()