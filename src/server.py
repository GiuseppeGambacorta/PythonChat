import sys
import socket
import threading
import signal
import queue


class Client:

    def __init__(self, connectionSocket, addr):

        self.connectionSocket = connectionSocket
        self.addr = addr

        self.local_messages = queue.Queue()
        self.local_messages_lock = threading.Lock()

        
    def listenMessages(self):
         while True:
            response = self.connectionSocket.recv(4096)
            with self.local_messages_lock:
                self.local_messages.put(response)

    def send(self, message):
        self.connectionSocket.send(message)


def addClients():
    while True:
        connectionSocket, addr = server.accept() 
        client = Client(connectionSocket, addr)
        with clients_lock:
            clients.append(client)
            threading.Thread(target=client.listenMessages).start()
        print(f'Connected to {addr}')


            
def sendMessages():
    while True:
        if messages.empty():
            with clients_lock:
                for client in clients:
                    with client.local_messages_lock:
                        while not client.local_messages.empty():
                            response = client.local_messages.get()
                            messages.put((response, client))
        else:
                with clients_lock:
                    while not messages.empty():
                        message, client_from_queue = messages.get()
                        for client in clients:
                            if client != client_from_queue:
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
    
    

