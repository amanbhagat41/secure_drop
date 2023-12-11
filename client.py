import socket
import os
class ChatClient:
    def __init__(self, myEmail):
        self.HOST = '127.0.0.1'
        self.PORT = 5552
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.send(myEmail.encode('utf-8'))
        self.myEmail = myEmail
    def receive_file(self):
        print("Waiting for File Request")
        received_data = b''
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data or data == b"FileTransferComplete":
                    break
                received_data += data
        except Exception as e:
            print(f"Error receiving file data: {e}")
        folder_name = "download"
        file_name = input("Enter the name for the received file with extension: ")
        file_path = os.path.join(folder_name, file_name)

        # Create the download folder if it doesn't exist
        os.makedirs(folder_name, exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(received_data)

        print(f"File received and saved to {file_path}")

    def send_file(self, recipient_email, file_path):
        try:
            # Notify the server that a file will be sent
            self.client_socket.send(b"send_user_file")
            ack = self.client_socket.recv(1024).decode('utf-8')
            if(ack == "SendingInitated"):
                print("Server Acknowledge Handshake")
                # Send the recipient's email to the server
                self.client_socket.send(recipient_email.encode('utf-8'))
                # Open the file and send its content
                with open(file_path, 'rb') as file:
                    file_data = file.read(1024)  # Read 1024 bytes at a time
                    while file_data:
                        self.client_socket.send(file_data)
                        file_data = file.read(1024)
                print("File sent successfully")
        except Exception as e:
            print(f"Error sending file: {e}")
    def getOnlineUsers(self):
        self.client_socket.send(b"get_online_users")
        try:
            response = self.client_socket.recv(1024).decode('utf-8')
        except Exception as e:
            print(f"Error receiving response: {e}")
        users = response.split(',')
        return users
