import sys
import socket


client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('localhost', 8887))
except Exception as e:
    print(f'Errore di connessione: {e}')
    sys.exit(0)


print('Connected to server')

while True:
    message=input('Inserisci un messaggio: ')
    client.send(message.encode())
    if message=='exit':
        break

    response=client.recv(4096)
    print(response.decode())









