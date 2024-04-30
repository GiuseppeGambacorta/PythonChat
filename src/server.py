import sys
import socket



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8887))
server.listen(5)  # Accetta fino a 5 connessioni in sospeso

print("Server in ascolto su porta 8888...")

# Lista per tenere traccia dei client connessi
clients = []


while True:

    print ('Ready to serve...')
    connectionSocket, addr = server.accept() # Si ferma qui in attesa di una connessione, mi rida indietro l'indirizzo del client
    print(connectionSocket,addr)
    clients.append(connectionSocket)
    print(f'Connected to {addr}')
    responde = clients[0].recv(4096)
    print(responde.decode())

    message=input('Inserisci un messaggio: ')
    clients[0].send(message.encode())



    
server.close()