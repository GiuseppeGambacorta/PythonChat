import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")
        
        self.server_port = tk.Entry(master, width=40)
        self.server_port.grid(row=0, column=0, padx=10, pady=10)
        
        self.connect_button = tk.Button(master, text="Connect", command=self.ciao)
        self.connect_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.close_button = tk.Button(master, text="Close", command=self.ciao)
        self.close_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.chat_history = scrolledtext.ScrolledText(master, width=50, height=20)
        self.chat_history.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.chat_history.config(state='disabled')
        
        self.message_entry = tk.Entry(master, width=40)
        self.message_entry.grid(row=2, column=0, padx=10, pady=10)
        
        self.send_button = tk.Button(master, text="Send", command=self.ciao)
        self.send_button.grid(row=2, column=1, padx=10, pady=10)
      
      
    def ciao(self):
        print("ciao")
        
      
    
 
def main():
    root = tk.Tk()
    chat_client = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
