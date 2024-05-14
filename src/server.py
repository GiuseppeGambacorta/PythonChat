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
        
        self.structure_manager = messages_struct.structManager()
    
    def listenMessages(self):
            
        while True:
            try:
                response = self.connectionSocket.recv(4096)
            except Exception as e:  
                print(f'Error: {e} on client {self.connectionSocket} {self.addr}')
                break
                
            with self.local_messages_lock:
                self.local_messages.put(response)

    
    def send(self, message):
        try:
            self.connectionSocket.send(message)
        except Exception as e:
            print(f'Error: {e}')
            
    
    def close_socket(self):
        self.connectionSocket.close()





class Server:

    def __init__(self,ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(1)  # Imposta un timeout di 1 secondo
        self.server.bind((ip_address, port))
        self.server.listen(5)  
        
        self.clients = []
        self.clients_lock = threading.Lock()
        self.client_threads = []
        
        self.messages = queue.Queue()

        self.structure_manager = messages_struct.structManager()
        
        self.server_on = True
        self.thread_listen = threading.Thread(target=self.listen_for_new_clients)
        self.thread_check_client = threading.Thread(target=self.check_clients_connection)
        self.thread_send = threading.Thread(target=self.send_messages)
        
        self.thread_listen.start()
        self.thread_check_client.start()
        self.thread_send.start()
        
        print(f"Server listening on port {port}...")
        
    # Method to listen for new clients, it creates a new client object and a new thread for each client
    def listen_for_new_clients(self):
        while self.server_on:
            try:
                connectionSocket, addr = self.server.accept()
            except socket.timeout: #Added a timeout for the accept method, so that the server can check if it is still running and stop the thread
                continue
            client = Client(connectionSocket, addr)
            thread = threading.Thread(target=client.listenMessages)
            thread.start()
            with self.clients_lock:
                self.clients.append(client)
                self.client_threads.append((client, thread))
                
            print(f'Connected to {addr}')
            print(f'Number of Clients: {len(self.clients)}')
        
        print("listening for new clients thread  stopped")    
            
    # Method to check if the clients are still connected, if not it closes the socket and removes the client from the list
    def check_clients_connection(self):
        while self.server_on:
            with self.clients_lock:
                for client, thread in self.client_threads:
                    if not thread.is_alive():
                        client.close_socket()
                        self.client_threads.remove((client, thread))
                        self.clients.remove(client)
                        print(f'Disconnected from {client.addr}')
                        print(f'Number of Clients: {len(self.clients)}')
            time.sleep(1)
            
        print("check client connection thred stopped")    
            
    # Method to send messages to the clients, it checks if there are messages in the queue and sends them to the clients
    def send_messages(self):
        while self.server_on:
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
                    data_store = []       
                    while not self.messages.empty():
                        message = self.messages.get()
                        data_structure,data = self.structure_manager.unpack_structure(message)
                        data_store.append((data_structure[0], message)) #in index 0 there is the timestamp
                    data_store.sort(key=lambda x: x[0]) #sort the messages by timestamp

                    for time_stamp, message in data_store:
                        for client in self.clients:
                            client.send(message)
        
        print("send messages thread stopped") 


    def wait(self):
        print('Waiting for clients...')
        signal.signal(signal.SIGINT, self.signal_handler)
        while True:
            time.sleep(1)
    
           
    def signal_handler(self, sig, frame):
        if self.server_on:
            print('Exiting...')
            self.server_on = False
            self.thread_listen.join()
            self.thread_check_client.join()
            self.thread_send.join()
            with self.clients_lock:
                for client in self.clients:
                        client.close_socket()

            sys.exit(0)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8888
    server = Server('localhost',port)
   
    server.wait()

    

