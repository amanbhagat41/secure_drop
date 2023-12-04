import socket
import threading

HOST = '127.0.0.1'
PORT = 6969

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

client_info = {}  # Dictionary to store client information (email: (socket, address))

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")

    email = client_socket.recv(1024).decode('utf-8')
    client_info[email] = (client_socket, address)

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Received from {address}: {data}")

        # Send the message to the specified recipient
        recipient_email, message = data.split(':', 1)
        if recipient_email in client_info:
            recipient_socket, _ = client_info[recipient_email]
            recipient_socket.send(f"{address}: {message}".encode('utf-8'))
        else:
            print(f"Recipient {recipient_email} not found.")

    print(f"Connection from {address} closed.")
    del client_info[email]
    client_socket.close()

while True:
    client_socket, address = server_socket.accept()

    client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
    client_handler.start()
