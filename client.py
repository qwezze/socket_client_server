#localhost:5555
from tkinter import Tk, scrolledtext, Label, Entry, Button, messagebox
import socket
import threading

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title('Клиент чата')

        Label(root, text='IP сервера:').pack()
        self.ip_entry = Entry(root)
        self.ip_entry.pack()
        self.ip_entry.insert(0, 'localhost')

        Label(root, text='Порт:').pack()
        self.port_entry = Entry(root)
        self.port_entry.pack()
        self.port_entry.insert(0, '5555')

        Label(root, text='Ваше имя:').pack()
        self.name_entry = Entry(root)
        self.name_entry.pack()
        self.name_entry.insert(0, 'Гость')


        self.connect_button = Button(root, text='Подключиться', command=self.connect_to_server)
        self.connect_button.pack()
        self.disconnect_button = Button(root, text='Отключиться', command=self.disconnect_from_server, state='disabled')
        self.disconnect_button.pack()

        Label(root, text='Ваше сообщение:').pack()
        self.input_entry = Entry(root, width=50)
        self.input_entry.pack()
        self.input_entry.bind('<Return>', self.send_message)

        self.send_button = Button(root, text='Отправить', command=self.send_message, state='disabled')
        self.send_button.pack()

        self.client_socket = None
        self.connected = False

    def connect_to_server(self):
       pass

    def disconnect_from_server(self):
        pass
    def send_message(self, event):
        pass



root = Tk()
server = ChatServer(root)
root.mainloop()