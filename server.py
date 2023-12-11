import socket
import threading

HOST = '127.0.0.1'
PORT = 5552
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

        #print(data)
        # Check for the special command to get online users
        split_result = data.split('#')
        # Extract the second and third elements
        print(split_result)
        selection = split_result[0]
        if selection == "get_online_users":
            online_users = [email for email in client_info]
            online_users_str = ','.join(online_users)

            try:
                client_socket.send(f'{online_users_str}'.encode('utf-8'))
            except Exception as e:
                print(f"Error sending response to {address}: {e}")
            return
        elif selection == "send_user_file":
            print(f"Server is expecting a file transfer")
            client_socket.send(f'SendingInitated'.encode('utf-8'))
            recipient_email = client_socket.recv(1024).decode('utf-8')
            try:
                #Receive the recipient's email
                print("We entered sending file")
                print(f"Recipient Email: {recipient_email}")
                # Find the recipient's socket in client_info
                if recipient_email in client_info:
                    recipient_socket, _ = client_info[recipient_email]
                    print("Found Recipient")

                    # Forward the file data to the recipient
                    while True:
                        file_data = data.read(1024)
                        if not file_data:
                            break
                        recipient_socket.send(file_data)

                    # Add a signal to indicate the end of file transfer
                    recipient_socket.send(b"FileTransferComplete")

                    print("File transfer completed or error occurred.")
                else:
                    print(f"Recipient {recipient_email} not found.")
            except Exception as e:
                print(f"Error forwarding file: {e}")
            print(f"Connection from {address} closed.")
    del client_info[email]
    client_socket.close()
if __name__ == '__main__':
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server is listening on {HOST}:{PORT}")
        while True:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
            client_handler.start()
    except KeyboardInterrupt:
        print("\nTurning Off Server.........")
    finally:
        server_socket.close()
