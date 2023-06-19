import socket
import os

def printMenu():
    print("Escolha uma das opções digitando os números indicados:\n\n")
    print("1: Conectar ao servidor\n")
    print("2: Pesquisar arquivo\n")
    print("3: Baixar arquivo\n")
    print("Aperte qualquer tecla para sair\n")

def update():
    #conecta com o servidor e atualiza arquivos possuídos
    placeholder = 0

def join():
    menu()

def search():
    menu()

def download():
    update()
    menu()

def menu():
    printMenu()
    option = int(input())
    if option == 1:
        join()
    elif option == 2:
        search()
    elif option == 3:
        download()
    else:
        s.close()
        

s = socket.socket()
print("Peer aberto!\n")
print("Insira o IP do peer:\n")
IP = input()
print("Insira a porta do peer:\n")
port = int(input())
print("Insira a pasta onde quer compartilhar (enviar e baixar) arquivos:\n")
path = input()
print("Informações obtidas com sucesso!\n\n")

menu()

s.connect(('127.0.0.1', port))

print(s.recv(1024).decode())

s.close()