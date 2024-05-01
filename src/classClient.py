import sys
import socket
import threading
import signal
import messages_struct
import struct
import time


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, address, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((address, port))
            return True
        except Exception as e:
            print(f'Errore di connessione: {e}')
            return False

    def disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            print(f'Errore di connessione: {e}')
            sys.exit(0)

    def printResponses(self):
        try:
            return self.client.recv(4096)
        except Exception as e:
            print(f'Errore di connessione: {e}')
            sys.exit(0)
          

    def writeMessages(self, message):
        try:
            name = 'Giuseppe'.ljust(20).encode()
            send=(True,time.time(),name)
            data = struct.pack(messages_struct.format, *send)
            data = data + message.encode()
            self.client.send(data)
        except Exception as e:
            print(f'Errore di connessione: {e}')
            sys.exit(0)

