import tkinter as tk
from tkinter import scrolledtext
from classClient import Client
import threading

class ChatClient:
    def __init__(self, master, client):
        self.master = master
        self.master.title("Client")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        
        self.client = client
        self.connected = False

        
        self.server_port = tk.Entry(master, width=40)
        self.server_port.grid(row=0, column=0, padx=10, pady=10)
        
        self.connect_button = tk.Button(master, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.close_button = tk.Button(master, text="Disconnect", command=self.disconnect)
        self.close_button.grid(row=0, column=2, padx=10, pady=10)


        self.status_text = tk.Label(master, text="Status:", bg="white", relief="sunken")
        self.status_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.chat_history = scrolledtext.ScrolledText(master, width=50, height=20)
        self.chat_history.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.chat_history.config(state='disabled')
        
        self.message_entry = tk.Entry(master, width=40)
        
        self.send_button = tk.Button(master, text="Send", command=self.write_message_to_server)
       


    def connect(self):
        port = self.server_port.get()
        if len(port) > 0:
            self.connected = self.client.connect("localhost", int(port))
            if self.connected:
                self.status_text.config(text='connected')  # Abilita la modifica del testo
                self.message_entry.grid(row=3, column=0, padx=10, pady=10)
                self.send_button.grid(row=3, column=1, padx=10, pady=10)
                thread = threading.Thread(target=self.print_response)
                thread.daemon = True
                thread.start()
            else:
                self.status_text.config(text='error with connection')  # Abilita la modifica del testo
       

    def disconnect(self):
        if self.connected:
            self.client.disconnect()
            self.status_text.config(text='disconnected')
            
    def write_message_to_server(self):
        message=self.message_entry.get()
        self.client.writeMessages(message)
        self.chat_history.config(state='normal')  # Abilita la modifica del testo
        self.chat_history.insert(tk.END, message+"\n")  # Aggiunge il messaggio alla fine della finestra di chat

    def print_response(self):
        while True:
            response = self.client.printResponses()
            self.chat_history.config(state='normal')
            self.chat_history.insert(tk.END, response.decode() + "\n")


    def on_closing(self):
        self.disconnect()
        self.master.destroy()
        
      
    
 
def main():
    root = tk.Tk()
    client = Client()
    chat_client = ChatClient(root, client)
    root.mainloop()

if __name__ == "__main__":
    main()
