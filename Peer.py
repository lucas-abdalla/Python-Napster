import socket
import os
import pickle
import threading

class Peer:

    #Cria um socket para a classe Peer
    s = socket.socket()
    #Global para poder ser utilizada no download e update futuramente
    global query
    query = ""

    #Inicializa o peer com as informações capturadas do teclado e obtem sua lista de arquivos
    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path
        #Obtém todos os arquivos no diretório em path
        self.files = os.listdir(path)

    #Faz requisição de atualização ao servidor e atualiza sua própria lista de arquivos
    #Função UPDATE do peer
    def update(self):
        self.files.append(query)
        #Diz ao servidor que é uma requisição de update
        self.s.sendall("UPDATE".encode("utf-8"))
        #Envia ao servidor arquivo adicionado
        self.s.sendall(query.encode("utf-8"))
        #Agurada o UPDATE_OK
        resposta = self.s.recv(4096).decode("utf-8")
        while True:
            #Se UPDATE_OK, libera o peer
            if resposta == "UPDATE_OK":
                break

    #Função JOIN do peer
    def join(self):
        #Tenta se conectar ao servidor
        try:
            #Conecta ao servidor
            self.s.connect((self.IP, self.port))
            #Usa módulo pickle do Python para codificar o vetor de arquivos do peer em bytes
            data_string = pickle.dumps(self.files)
            #Envia o vetor de arquivos em bytes
            self.s.sendall(data_string)
            #Recebe o JOIN_OK
            resposta = self.s.recv(4096).decode()
            if resposta == "JOIN_OK":
                #Printa conforme especificação
                print(f'Sou peer {self.s.getsockname()[0]}:{self.s.getsockname()[1]} com arquivos', end = " ")
                for file in self.files:
                    print(file, end = " ")
            print()
            #Após dar JOIN no servidor, cria uma thread que escutará requisições de download vindas de outros peers
            standby_thread = threading.Thread(target=self.standbyD, args=())
            standby_thread.start()
        #Acusa o erro caso não tenha sido possível se conectar
        except Exception:
            print("Não foi possível se conectar ao servidor. Ele pode estar offline ou os dados foram digitados incorretamente")

    #Função SEARCH do peer
    def search(self):
        query = input()
        #Envia query ao servidor
        self.s.sendall(query.encode("utf-8"))
        #Recebe resposta do SEARCH já formatada conforme especificação pelo servidor
        resposta = self.s.recv(4096).decode()
        print(resposta)
        print()

    #Função DOWNLOAD do peer
    def download(self):
        #Verifica se foi feita uma pesquisa antes de baixar
        #Recebe IP e porta do peer ao qual fará a requisição
        IP = input()
        port = int(input())
        #Abre um novo socket para fazer a requisição de download
        d = socket.socket()
        #Tenta se conectar ao peer
        try:
            d.connect((IP, port))
            #Envia o nome do arquivo requisitado ao outro peer
            d.sendall(query.encode("utf-8"))
            ans = d.recv(4096).decode("utf-8")
            #Verifica se o peer possui mesmo o arquivo solicitado
            if ans == "FILE_FOUND":
            #Recebe o tamanho do arquivo requisitado
                file_size = int(d.recv(4096).decode("utf-8"))
                #Abre arquivo no modo escrita na pasta path do peer
                with open(self.path + "\\" + query, "wb") as f:
                    i = 0
                    #Recebe os dados em pedaços de 1MB até que atinge o tamanho do arquivo
                    while i < file_size:
                        data = d.recv(1024 * 1024)
                        #Usado para controlar quantos bytes já foram recebidos
                        i += (1024 * 1024)
                        f.write(data)
                    #Fecha o arquivo
                    f.close()
                #Fecha a conexão com o peer requisitado
                d.close()
                #Print conforme especificação
                print("Arquivo %s baixado com sucesso na pasta %s" % (query, self.path))
                print()
                #Chama a função update
                self.update()
            else:
                print("O peer requisitado não possui o último arquivo pesquisado")
        #Caso não consiga se conectar
        except Exception:
            print("Não foi possível se conectar ao peer digitado. O peer pode estar offline ou os dados foram digitados incorretamente")
    
    #Função stand by download, que escuta requisições de downloads vindas de outros peers. Funciona numa thread separada criada no JOIN
    def standbyD(self):
        #Cria e liga um socket ao host e porta desse peer
        sbD = socket.socket()
        sbD.bind((self.s.getsockname()[0], self.s.getsockname()[1]))
        sbD.listen(5)
        #Espera requisições de downloads em looping infinito
        while True:
            #Aceita conexão e recebe a requisição
            c, addr = sbD.accept()
            #Manda a requisição para uma thread nova para poder receber requisições de outros peers
            sendfile_thread = threading.Thread(target=self.sendFile, args=(c, addr))
            sendfile_thread.start()

    def sendFile(self, c, addr):
        request = c.recv(4096).decode()
        #Se possui o arquivo requisitado...
        if request in self.files:
            c.sendall("FILE_FOUND".encode("utf-8"))
            #Cria um path com o nome do arquivo solicitado
            file_path = os.path.join(self.path, request)
            #Utiliza o path criado acima para obter tamanho do arquivo solicitado
            file_size = os.path.getsize(file_path)
            #Manda o tamanho do arquivo solicitado ao outro peer
            c.sendall(str(file_size).encode("utf-8"))
            #Abre arquivo no modo read
            with open(file_path, "rb") as f:
                i = 0
                #Similar ao download, envia o arquivo solicitado em pedações de 1MB
                while i < file_size:
                    c.sendall(f.read(1024 * 1024))
                    i += (1024 * 1024)
                #Fecha arquivo
                f.close()
            #Fecha conexão com o outro peer
            c.close()
        else:
            c.sendall("NO_SUCH_FILE".encode("utf-8"))

#Função simples que printa o menu interativo no console
def printMenu():
        print("Escolha uma das opções digitando os números indicados:\n")
        print("1: Conectar ao servidor (JOIN)")
        print("2: Pesquisar arquivo (SEARCH)")
        print("3: Baixar arquivo (DOWNLOAD)")

#Funcionamento lógico do menu interativo
def menu(p):
    printMenu()
    #Obtem ocção selecionada
    option = int(input())
    if option == 1:
        #Obtém a inicialização do peer pelo teclado no console
        IP = input()
        port = int(input())
        path = input()
        #Tenta criar o peer
        try:
            #Inicializa peer
            p = Peer(IP, port, path)
        #Nesse ponto a única exception possível é um path errado
        except Exception:
            print("Não foi possível criar o peer. Verifique se o caminho da pasta foi digitado corretamente")
            menu(p)
        #Chama função JOIN
        p.join()
        menu(p)
    #Chama função SEARCH
    elif option == 2:
        p.search()
        menu(p)
    #Chama função DOWNLOAD
    elif option == 3:
        p.download()
        menu(p)

#Cria variável global p para ser instância de peer após o join e manter mesma instância ao chamar o menu repetidamente
global p
p = None
menu(p)