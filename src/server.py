import sys
import socket
import threading
import signal


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
        
        with clients_lock:
            for client in clients:
                if client == clients[index]:
                    continue
                client.send(response)
                
                
def signal_handler(sig, frame):
    print('Exiting...')
    server.close()
    sys.exit(0)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))
server.listen(5)  # Accetta fino a 5 connessioni in sospeso
print("Server in ascolto su porta 8888...")

# Lista per tenere traccia dei client connessi
clients = []
clients_lock = threading.Lock()

print ('Ready to serve...')
thread = threading.Thread(target=addClients)
thread.daemon = True
thread.start()


print('Waiting for clients...')
#interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
    
    

