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

        Label(root, text='Сообщения: ').pack()
        self.message_area = scrolledtext.ScrolledText(root, width=50, height=15, state='disabled')
        self.message_area.pack()

        Label(root, text='Ваше сообщение:').pack()
        self.input_entry = Entry(root, width=50)
        self.input_entry.pack()
        self.input_entry.bind('<Return>', self.send_message)

        self.send_button = Button(root, text='Отправить', command=self.send_message, state='disabled')
        self.send_button.pack()

        self.client_socket = None
        self.connected = False

    def connect_to_server(self):
        server_ip = self.ip_entry.get()
        port = int(self.port_entry.get())
        self.username = self.name_entry.get()


        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((server_ip, port))
            self.connected = True

            self.connect_button.config(state='disabled')
            self.disconnect_button.config(state='normal')
            self.send_button.config(state='normal')
            self.ip_entry.config(state='disabled')
            self.port_entry.config(state='disabled')
            self.name_entry.config(state='disabled')

            self.add_message(f'Подключено к серверу {server_ip}:{port}')

            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось подключиться: {str(e)}')

    def receive_messages(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.add_message(data)
            except:
                if self.connected:
                    self.add_message('Ошибка при получении сообщения')
                    self.disconnect_from_server()
                break

    def add_message(self, message):
        self.message_area.config(state='normal')
        self.message_area.insert('end', message + '\n')
        self.message_area.config(state='disabled')
        self.message_area.see('end')

    def disconnect_from_server(self):

        if self.client_socket:
            self.connected = False
            self.client_socket.close()

            self.connect_button.config(state='normal')
            self.disconnect_button.config(state='disabled')
            self.send_button.config(state='disabled')
            self.ip_entry.config(state='normal')
            self.port_entry.config(state='normal')
            self.name_entry.config(state='normal')

            self.add_message('тключено от сервера')

    def send_message(self, event=None):
        if not self.connected:
            return
        message = self.input_entry.get()
        if message:
            full_name = f'{self.username}: {message}'
            try:
                self.client_socket.send(full_name.encode('utf-8'))
                self.input_entry.delete(0, 'end')
            except Exception as e:
                self.add_message(f'Ошибка при отправке: {e}')
                self.disconnect_from_server()




root = Tk()
server = ChatClient(root)
root.mainloop()