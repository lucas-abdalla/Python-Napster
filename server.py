import socket
import threading
import pickle

class Servidor:
    
    #Cria o socket do servidor
    s = socket.socket()
    #Cria estrutura que armazenará peers e seus arquivos
    peerList = []
    
    #Inicializa o servidor com IP e porta lidos do teclado
    def __init__(self, IP, port):
        Servidor.IP = IP
        Servidor.port = port
        Servidor.s.bind((IP, port))
        Servidor.start_server()

    #Função JOIN do servidor
    def join(c, addr, data):
        #Reconverte a lista de arquivos do peer recebida em bytes para um array de strings
        files = pickle.loads(data)
        #Obtém IP e porta do peer conectado
        c_ip, c_port = c.getpeername()
        #Prepara formatação de string com IP e porta do peer
        peerInfo = str(c_ip) + ";" + str(c_port) + ";"
        #Printa conforme especificação
        print(f'Peer {c_ip}:{c_port} adicionado com arquivos', end = " ")
        for file in files:
            print(file, end = " ")
            #Continua formatação da string adicionando os arquivos do peer. Cada valor é separado por ;
            peerInfo += file + ";"
        #Adiciona as informações do peer na lista de peers do servidor
        Servidor.peerList.append(peerInfo)
        print()
        #Envia o JOIN_OK ao peer
        c.send("JOIN_OK".encode("utf-8"))
        #Volta a escutar as requisições do servidor
        Servidor.handle_client(c, addr)

    #Função SEARCH do servidor
    def search(c, addr, data):
        #Prepara formatação da resposta
        resposta = "peers com arquivo solicitado: "
        #Recebe arquivo pesquisado
        query = data.decode("utf-8")
        #Obtém IP e porta do peer solicitante
        c_ip, c_port = c.getpeername()
        #Printa conforme especificação
        print("Peer %s:%s solicitou arquivo %s" % (str(c_ip), str(c_port), query))
        #Percorre a lista de peers do servidor
        for peer in Servidor.peerList:
            #Faz o split da string nos ;
            peerArr = peer.split(';')
            i = 2
            #Percorre cada nome de arquivo do peer atual. Começa no 2 porque 0 e 1 guardam IP e porta do peer
            for i in range(len(peerArr)):
                #Se arquivo do peer da lista é o arquivo solicitado pelo peer conectado, adicionado peer da lista à resposta
                if (peerArr[i] == query):
                    resposta += str(peerArr[0]) + ":" + str(peerArr[1]) + " "
        #Envia resposta ao peer solicitante
        c.sendall(resposta.encode("utf-8"))
        Servidor.handle_client(c, addr)

    #Função UPDATE do servidor
    def update(c, addr):
        #Recebe os bytes utf-8 do nome do arquivo baixado
        data = c.recv(4096)
        #Decodifica os bytes e obtém a string do nome
        file = data.decode("utf-8")
        #Obtém IP e porta do peer que requisitou a atualização
        c_ip, c_port = c.getpeername()
        #Percorre lista de peers do servidor
        for i in range (len(Servidor.peerList)):
            #Faz o split
            peerArr = Servidor.peerList[i].split(';')
            #Se IP e porta do peer atual é o mesmo do peer requisitante, adiciona o arquivo baixado ao seu registro
            if (str(c_ip) == peerArr[0] and str(c_port) == peerArr[1]):
                Servidor.peerList[i] += file + ";"
        #Responde com UPDATE_OK
        c.sendall("UPDATE_OK".encode("utf-8"))
        Servidor.handle_client(c, addr)

    #Função que cuida das requisições dos peers. É chamada por diferentes threads para cada peer conectado
    def handle_client(c, addr):
        #Captura problemas de desconexão e outros erros que possam ocorrer
        try:
            #Recebe dados do peer em bytes
            data = c.recv(2097152)
            #Verifica se os dados são do tipo pickle verificando se a primeira posição é 0x80, que é o início da codificação pickle.
            #Se os dados são do tipo pickle significa que é uma requisição do tipo join
            if data[0] == 0x80:
                Servidor.join(c, addr, data)
            else:
                #Se não é pickle, caso tenha recebido uma string UPDATE, é uma requisição UPDATE
                aux = data.decode("utf-8")
                if aux == "UPDATE":
                    Servidor.update(c, addr)
                #Se não era uma requisição update era uma requisição SEARCH. Os bytes codificados são enviados à função SEARCH e são tratados nela
                else:
                    Servidor.search(c, addr, data)
        #Caso capture um erro não há prints para manter no console somente os prints especificados
        except Exception as e:
            pass

    #Função que inicia o servidor
    def start_server():
        #Começa a escutar por peers
        Servidor.s.listen(5)
        #Sempre escutando
        while True:
            #Aceita conexão
            c, addr = Servidor.s.accept()
            #Envia novas conexões para threads para poder cuidar de múltiplos peers ao mesmo tempo
            c_thread = threading.Thread(target=Servidor.handle_client, args=(c, addr))
            c_thread.start()

#Captura do teclado IP e porta do servidor
IP = input()
port = int(input())
#Instancia o servidor
svr = Servidor(IP, port)