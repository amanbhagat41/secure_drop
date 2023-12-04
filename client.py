import socket
import threading

def start_client(email):
    HOST = '127.0.0.1'
    PORT = 6969

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send the email address to the server
    client_socket.send(email.encode('utf-8'))

    def receive_messages():
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            print(data)

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    recipient_email = input("Enter recipient's email: ")
    while True:
        message = input("Enter your message: ")
        client_socket.send(f"{recipient_email}:{message}".encode('utf-8'))
