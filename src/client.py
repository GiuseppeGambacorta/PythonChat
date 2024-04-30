import sys
import socket
import threading


def printResponses():
    while True:
        response=client.recv(4096)
        print('\n'+ response.decode() )

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('localhost', 8888))
except Exception as e:
    print(f'Errore di connessione: {e}')
    sys.exit(0)


print('Connected to server')
threading.Thread(target=printResponses).start()
while True:
    message=input('Inserisci un messaggio: ')
    client.send(message.encode())
    if message=='exit':
        break




client.close()










