#localhost:5555
from tkinter import Tk, scrolledtext, Label, Entry, Button, messagebox
import socket
import threading

class ChatServer:
    def __init__(self, root):
        self.root = root
        self.root.title('Сервер чата')

        Label(root, text='Порт:').pack()
        self.port_entry = Entry(root)
        self.port_entry.pack()
        self.port_entry.insert(0, '5555')


        self.start_button = Button(root, text='Start server', command=self.start_server)
        self.start_button.pack()
        self.stop_button = Button(root, text='Stop server', command=self.stop_server, state='disabled')
        self.stop_button.pack()

        Label(root, text='Log server: ').pack()
        self.log_area = scrolledtext.ScrolledText(root, width=50, height=15, state='disabled')
        self.log_area.pack()

        self.clients = []
        self.server_socket = None
        self.running = False

    def start_server(self):
        port = int(self.port_entry.get())

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.port_entry.config(state='disabled')

        self.log_message(f'Сервер запущен на порту {port}')

        accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
        accept_thread.start()


    def accept_connections(self):
        while self.running:
            client_socket, address = self.server_socket.accept()
            client_socket = threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True)
            client_socket.start()

    def handle_client(self, client_socket, address):
        self.log_message(f'Новое подключение: {address}')
        self.clients.append(client_socket)
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                self.log_message(f'От {address}: {data}')

                for client in self.clients:
                    if client != client_socket:
                        try:
                            client.send(f'От {address[0]}: {data}'.encode('utf-8'))
                        except:
                            self.clients.remove(client)
        except Exception as e:
            self.log_message(f'Ошибка с клиентом {address}: {str(e)}')
        finally:
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            self.log_message(f'Клиент отключен: {address}')




    def stop_server(self):
        self.running = False
        for client in self.clients:
            client.close()
        self.clients = []

        if self.server_socket:
            temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            temp.connect(('localhost', int(self.port_entry.get())))
            temp.close()

            self.server_socket.close()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.port_entry.config(state='normal')
        self.log_message('Сервер остановлен')

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert('end', message + '\n')
        self.log_area.config(state='disabled')
        self.log_area.see('end')


root = Tk()
server = ChatServer(root)
root.mainloop()