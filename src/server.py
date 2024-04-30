import sys
import socket
import threading


def addClients():
    while True:
        connectionSocket, addr = server.accept() 
        with clients_lock:
            clients.append(connectionSocket)
            threading.Thread(target=manageClient, args=(len(clients) - 1,)).start()
        print(f'Connected to {addr}')

def manageClient(index):
    while True:
        if len(clients) == 0:
            break

        response = clients[index].recv(4096)
        print(response.decode())
        
        for client in clients:
            if client == clients[index]:
                continue
            client.send(response)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen(5)  # Accetta fino a 5 connessioni in sospeso
print("Server in ascolto su porta 8888...")

# Lista per tenere traccia dei client connessi
clients = []
clients_lock = threading.Lock()

print ('Ready to serve...')
threading.Thread(target=addClients).start()


print('Waiting for clients...')
while True:
    pass



    
server.close()