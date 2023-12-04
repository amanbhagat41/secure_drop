import socket
import threading

HOST = '127.0.0.1'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

clients = []

def broadcast(message, sender_address):
    for client_socket, address in clients:
        if address != sender_address:
            try:
                client_socket.send(message.encode('utf-8'))
            except socket.error:
                # Handle disconnected client (optional)
                print(f"Connection from {address} closed.")
                clients.remove((client_socket, address))
                client_socket.close()

def handle_client(client_socket, address):
    print(f"Accepted connection from {address}")
    clients.append((client_socket, address))
    
    # Notify all clients about the new connection
    broadcast(f"{address} has joined the chat.", address)

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received from {address}: {data}")
            broadcast(f"{address}: {data}", address)

        except socket.error:
            # Handle disconnected client (optional)
            print(f"Connection from {address} closed.")
            clients.remove((client_socket, address))
            client_socket.close()
            break

    print(f"Connection from {address} closed.")
    clients.remove((client_socket, address))
    client_socket.close()
    # Notify all clients about the disconnection
    broadcast(f"{address} has left the chat.", address)

while True:
    client_socket, address = server_socket.accept()

    client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
    client_handler.start()
