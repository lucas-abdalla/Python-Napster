import socket

s = socket.socket();
print("Socket succesfully created")

port = 12345

s.connect(('127.0.0.1', port))

print(s.recv(1024).decode())

s.close()