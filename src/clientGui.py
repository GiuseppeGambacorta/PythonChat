import tkinter as tk
from tkinter import scrolledtext
from classClient import Client
import threading
import time

class ChatClient:
    def __init__(self, master, client):
        self.master = master
        self.master.title("Client")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        
        self.client = client
        self.connected = False
        self.nickname_selected = False

        self.nickname_input = tk.Entry(master, width=40)
        self.nickname_input.grid(row=0, column=0, padx=0, pady=0)
        self.set_name_button = tk.Button(master, text="Set Nickname", command=self.set_nickname)
        self.set_name_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.server_port = tk.Entry(master, width=40)
        self.server_port.grid(row=1, column=0, padx=10, pady=10)
        
        self.connect_button = tk.Button(master, text="Connect", command=self.connect)
        self.connect_button.grid(row=1, column=1, padx=10, pady=10)
        
        self.close_button = tk.Button(master, text="Disconnect", command=self.disconnect)
        self.close_button.grid(row=1, column=2, padx=10, pady=10)


        self.status_text = scrolledtext.ScrolledText(master, width=70, height=10)
        self.status_text.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.status_text.config(state='disabled')
        
        self.chat_history = scrolledtext.ScrolledText(master, width=50, height=20)
        self.chat_history.grid(row=3, column=0, padx=10, pady=10)
        self.chat_history.config(state='disabled')

        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=4, column=0, padx=10, pady=10)

        self.send_button = tk.Button(master, text="Send", command=self.write_message_to_server)
        self.send_button.grid(row=4, column=1, padx=10, pady=10)


    def connect(self):
        if not self.connected:
            try:
                if self.nickname_selected:
                    port = self.server_port.get()
                    if len(port) > 0:
                        self.connected = self.client.connect("localhost", int(port))
                        if self.connected:
                            self.write_status('connected')
                            self.thread_response = threading.Thread(target=self.print_response)
                            self.thread_response.daemon = True
                            self.thread_response.start()
                        else:
                            self.write_status('connection failed')
                    else:
                        self.write_status('insert port')
                else:
                    self.write_status('set a nickname first')
            except Exception as e:
                self.write_status(f'Error: {e}')
        else:
            self.write_status('already connected')
       

    def disconnect(self):
        try:
            if self.connected:
                self.connected = False
                self.client.disconnect()
                self.write_status('disconnected')
                self.nickname_selected = False

        except Exception as e:
            self.write_status(f'Error: {e} ')
            
    def write_message_to_server(self):
        try:
            if self.connected:
                message=self.message_entry.get()
                self.message_entry.delete(0, tk.END)
                self.client.writeMessages(self.nickname, message)
            else:
                self.write_status('cant send messages if not connected')
        except Exception as e:
            self.write_status(f'Error: {e}')


    def write_status(self, message):
        self.status_text.config(state='normal')
        message = time.strftime('%H:%M:%S') + ": " + message
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)  
        self.status_text.config(state='disabled')

    def print_response(self):
        try:
            while self.connected:
                response = self.client.printResponses()
                self.chat_history.config(state='normal')
                self.chat_history.insert(tk.END, response.decode() + "\n")
                self.status_text.see(tk.END)  
                self.chat_history.config(state='disabled')
        except Exception as e:
            if self.connected:
                self.write_status(f'Error: {e}')

    def set_nickname(self):
        name = self.nickname_input.get().strip()
        name_len = len(name)
        if name_len > 0 and name_len< self.client.get_max_string_length():
            self.nickname = name
            self.nickname_selected = True
            self.nickname_input.config(textvariable=self.nickname)
        else:
            if name_len == 0:
                self.write_status('insert a nickname in the field')
            else:
                self.write_status('nickname too long')


    def on_closing(self):
        self.disconnect()
        self.master.destroy()
        
      
    
 
def main():
    root = tk.Tk()
    client = Client(guimode=True)
    chat_client = ChatClient(root, client)
    root.mainloop()

if __name__ == "__main__":
    main()
