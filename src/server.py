import sys
import socket
import threading
import signal
import queue


def addClients():
    while True:
        connectionSocket, addr = server.accept() 
        with clients_lock:
            clients.append(connectionSocket)
            threading.Thread(target=manageClient, args=(connectionSocket,)).start()
        print(f'Connected to {addr}')

def manageClient(client):

   addMessages(client)


        
       

def addMessages(client):
    while True:
        response = client.recv(4096)
        print(response.decode())
        with messages_lock:
            messages.put((response, client))
            


def sendMessages():
    while True:
        with messages_lock:
            if not messages.empty() and  len(clients) > 0:
                with clients_lock:
                    while not messages.empty():
                        message, client_from_queue = messages.get()
                        for client in clients:
                            if client == client_from_queue:
                                continue
                            client.send(message)

                
                
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

messages = queue.Queue()
messages_lock = threading.Lock()

print ('Ready to serve...')
thread = threading.Thread(target=addClients)
thread.daemon = True
thread.start()


thread2 = threading.Thread(target=sendMessages)
thread2.daemon = True
thread2.start()

print('Waiting for clients...')
#interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
    
    

