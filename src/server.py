import sys
import socket
import threading
import signal
import queue
import messages_struct
import time
from datetime import datetime

class Client:

    def __init__(self, connectionSocket, addr):

        self.connectionSocket = connectionSocket
        self.addr = addr

        self.local_messages = queue.Queue()
        self.local_messages_lock = threading.Lock()

        
    def listenMessages(self, clients, clients_lock):
        while True:
            try:
                response = self.connectionSocket.recv(4096)
            except Exception as e:  
                with clients_lock:
                    print(f'Disconnected from {self.addr}')
                    clients.remove(self)  # rimuove se stesso dalla lista dei client
                    print(f'Number of Clients: {len(clients)}')
                break
              
            with self.local_messages_lock:
                self.local_messages.put(response)

    def send(self, message):
        try:
            self.connectionSocket.send(message)
        except Exception as e:
            print(f'Error: {e}')


class Server:

    def __init__(self,ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip_address, port))
        self.server.listen(5)  # Accetta fino a 5 connessioni in sospeso
        

        self.clients = []
        self.clients_lock = threading.Lock()
        self.messages = queue.Queue()

        self.structure_manager = messages_struct.structManager()

        print(f"Server listening on port {port}...")

    def addClients(self):
        while True:
            connectionSocket, addr = self.server.accept()
            client = Client(connectionSocket, addr)
            with self.clients_lock:
                self.clients.append(client)
                threading.Thread(target=client.listenMessages, args=(self.clients, self.clients_lock)).start()
            print(f'Connected to {addr}')
            print(f'Number of Clients: {len(self.clients)}')

    def sendMessages(self):
        while True:
            if self.messages.empty():
                time.sleep(0.1)
                with self.clients_lock:
                    for client in self.clients:
                        with client.local_messages_lock:
                            while not client.local_messages.empty():
                                response = client.local_messages.get()
                                self.messages.put(response)
            else:
                with self.clients_lock:             
                    datastore =[]       
                    while not self.messages.empty():
                        message = self.messages.get()
                        data_structure,data = self.structure_manager.unpack(message)
                        datastore.append((data_structure[1], message))
                    datastore.sort(key=lambda x: x[0])

                    for time_stamp, message in datastore:
                        for client in self.clients:
                            client.send(message)

    def start(self):
        print('Waiting for clients...')
        # interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C)
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            time.sleep(1)

    def signal_handler(self, sig, frame):
        print('Exiting...')
        self.server.close()
        sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    server = Server('localhost',port)
    thread = threading.Thread(target=server.addClients)
    thread.daemon = True
    thread.start()

    thread2 = threading.Thread(target=server.sendMessages)
    thread2.daemon = True
    thread2.start()

    server.start()

    

