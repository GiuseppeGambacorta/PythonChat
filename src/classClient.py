import sys
import socket
import threading
import signal


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
            self.client.send(message.encode())
        except Exception as e:
            print(f'Errore di connessione: {e}')
            sys.exit(0)

