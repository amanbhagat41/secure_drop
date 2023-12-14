import socket
import os
class ChatClient:
    def __init__(self, myEmail):
        self.HOST = '127.0.0.1'
        self.PORT = 5552
        self.FILEPORT = 5553
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.connect((self.HOST, self.PORT))
        self.command_socket.send(myEmail.encode('utf-8'))

        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_socket.connect((self.HOST, self.FILEPORT))

       
        self.myEmail = myEmail
    def receive_file(self):
        print("Waiting for File Request")

    def send_file(self, recipient_email, file_path):
        print("WIP")
        self.command_socket.send(b"send_user_file")
        file_name = os.path.basename(file_path)
        ack = self.file_socket.recv(1024).decode('utf-8')
        if(ack == 'fileTransferReady'):
            print("WE ARE READY")
            self.file_socket.send(f'clientSideAcknowledge'.encode('utf-8'))
            ack = self.file_socket.recv(1024).decode('utf-8')
            if(ack == "initiate"):
                print("KEEP GOING ITS WORKING!!!!")
                #Send to Server--------------------
                self.file_socket.send(f'sendingFileName'.encode('utf-8'))
                ack = self.file_socket.recv(1024).decode('utf-8')
                if(ack == "sendFileName"):
                    self.file_socket.send(f'{file_name}'.encode('utf-8'))
                    #file name
                        #senders email
                

    def getOnlineUsers(self):
        self.command_socket.send(b"get_online_users")
        try:
            response = self.command_socket.recv(1024).decode('utf-8')
        except Exception as e:
            print(f"Error receiving response: {e}")
        users = response.split(',')
        return users