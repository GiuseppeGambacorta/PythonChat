import sys
import socket
import threading
import signal
import queue
import messages_struct
import struct
import time
from datetime import datetime

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
                threading.Thread(target=client.listenMessages).start()
            print(f'Connected to {addr}')

    def sendMessages(self):
        while True:
            if self.messages.empty():
                time.sleep(0.1)
                with self.clients_lock:
                    for client in self.clients:
                        with client.local_messages_lock:
                            while not client.local_messages.empty():
                                response = client.local_messages.get()
                                self.messages.put((response, client))
            else:
                with self.clients_lock:
                    while not self.messages.empty():
                        message, client_that_writed_message = self.messages.get()
                        structure_data, message= self.structure_manager.read(message)
                        print(f'structure data: {structure_data}')
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

    

