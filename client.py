import socket
import threading
import os
def start_client():
    HOST = '127.0.0.1'
    PORT = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    def receive_messages():
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        message = input("Enter your message: ")
        client_socket.send(message.encode('utf-8'))
