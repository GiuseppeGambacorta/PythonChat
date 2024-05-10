import sys
import socket
import threading
import signal
import messages_struct
import struct
import time


class Client:
    def __init__(self,guimode : bool = False):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.structure_manager = messages_struct.structManager()
        self.guimode = guimode
        
    def connect(self, address, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((address, port))
            return True
        except Exception as e:
            if self.guimode:
                raise
            else:
                print(f'Errore di connessione: {e}')
                return False

    def disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            if self.guimode:
                raise
            else:
                print(f'Errore di connessione: {e}')
                return False

    def readResponses(self):
        try:
            data = self.client.recv(4096)
            return self.structure_manager.unpack_structure(data)   
        except Exception as e:
            if self.guimode:
                raise
            else:
                print(f'Errore di connessione: {e}')
                return False
          

    def writeMessages(self, nickname,message):
        try:
            name = nickname.ljust(self.structure_manager.get_max_string_length()).encode()
            structure_to_send=(time.time(),name)
            data = self.structure_manager.pack_structure(structure_to_send, message)
            self.client.send(data)
        except Exception as e:
            if self.guimode:
                raise
            else:
                print(f'Errore di connessione: {e}')
                return False
            
    def get_max_string_length(self):
        return self.structure_manager.get_max_string_length()



