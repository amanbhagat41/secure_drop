import socket
import os
import json

class ChatClient:
    def __init__(self, myEmail):
        self.HOST = '127.0.0.1'
        self.PORT = 5555
        self.MOTHERSHIP = 5557

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.connect((self.HOST, self.MOTHERSHIP))

        self.client_socket.send(myEmail.encode('utf-8'))
        self.myEmail = myEmail
    
    def receive_file(self):
        try:
            with open('contact.json', 'r') as file:
                contacts = json.load(file)
            #Get the alert, contains the sender email
            #We are gonna look up and see if the sender email is in contacts first

            #if it is, ask if it wants it, if not discard
            print("Expecting a file transfer.....")
            ack = self.client_socket.recv(1024).decode('utf-8')
            if ack == "incomingRequest":
                print("Request inbound")
                self.client_socket.send(f"sendSenderEmail".encode('utf-8'))
                senderEmail = self.client_socket.recv(1024).decode('utf-8')
                if is_email_a_contact(senderEmail, contacts):
                    print("Checking if email is contact")
                    self.client_socket.send(f'isContact'.encode('utf-8'))
                    #Prompt user for incoming request
                    isAccepted = input("Contact {senderEmail} is sending a file. Accept (y/n)?")
                    if(isAccepted == 'y' or isAccepted == 'Y'):
                        print("Accepted File")
                        self.client_socket.send(f'accepted'.encode('utf-8'))
                        ack = self.client_socket.recv(1024).decode('utf-8')
                        if(ack == "acceptedSeen"):
                            print("STARTING FILE TRANSFER")
                            print("WIP")
                    else:
                        self.client_socket.send(f'rejected'.encode('utf-8'))
                        print("Rejected File")

                else:
                    self.client_socket.send(f'notContact'.encode('utf-8'))
                    print("Email not a contact")
        except KeyboardInterrupt:
            print("exiting....")
            return
        
        
                


        
        # folder_name = "download"
        # file_name = input("Enter the name for the received file with extension: ")
        # file_path = os.path.join(folder_name, file_name)

        # # Create the download folder if it doesn't exist
        # os.makedirs(folder_name, exist_ok=True)
        

        # print(f"File received and saved to {file_path}")

    def send_file(self, recipient_email, file_path):
        try:
            # Notify the server that a file will be sent
            self.command_socket.send(f"send_user_file#{recipient_email}".encode('utf-8'))

            # Wait for server's response to initiate file transfer
            ack = self.command_socket.recv(1024).decode('utf-8')
            if ack == "SendingInitated":
                print("Server Acknowledge Handshake")
                # Open the file and send its size first
                file_size = os.path.getsize(file_path)
                self.client_socket.send(str(file_size).encode('utf-8'))
                ack = self.client_socket.recv(1024).decode('utf-8')
                if(ack == "ReceivedFileSize"):
                    print("Received File Size")
                    #self.client_socket.send(f"{self.myEmail}".encode('utf-8'))
                    self.client_socket.send(f'sendingInfo'.encode('utf-8'))
                    ack = self.client_socket.recv(1024).decode('utf-8')
                    if(ack == "sendEmail"):
                        print("Sending Email to Server")
                        self.client_socket.send(f'{self.myEmail}'.encode('utf-8'))
                        ack = self.client_socket.recv(1024).decode('utf-8')
                        if (ack == "ReceivedSenderEmail"):
                            print("Received sender Email")
                            self.client_socket.send(f'sendUserAlert'.encode('utf-8'))
                        
               
        except Exception as e:
            print(f"Error sending file: {e}")

    def getOnlineUsers(self):
        self.command_socket.send(b"get_online_users")
        try:
            response = self.command_socket.recv(1024).decode('utf-8')
        except Exception as e:
            print(f"Error receiving response: {e}")
        return response.split(',')
def is_email_a_contact(email, contacts):
        for contact in contacts:
            if contact['email'] == email:
                return True
        return False