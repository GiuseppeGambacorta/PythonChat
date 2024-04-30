import sys
import socket
import threading
import signal


def printResponses():
    while True:
        response=client.recv(4096)
        print('\n'+ response.decode() )
        
        
def writeMessages():
    while True:
        message=input('Inserisci un messaggio: ')
        client.send(message.encode())
        
def signal_handler(sig, frame):
    print('Exiting...')
    client.close()
    sys.exit(0)
        
        
               
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(('localhost', 8888))
except Exception as e:
    print(f'Errore di connessione: {e}')
    sys.exit(0)


print('Connected to server')

thread = threading.Thread(target=printResponses)
thread.daemon = True
thread.start()


thread2 = threading.Thread(target=writeMessages)
thread2.daemon = True
thread2.start()



signal.signal(signal.SIGINT, signal_handler)
signal.pause() 




    
   
  
    














