import socket
import os
import json

class ChatClient:
    def __init__(self, myEmail):
        self.HOST = '127.0.0.1'
        self.PORT = 5555        
        self.FILEPORT = 5556
        self.command_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.command_socket.connect((self.HOST, self.PORT))
        self.command_socket.send(myEmail.encode('utf-8'))

        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_socket.connect((self.HOST, self.FILEPORT))

       
        self.myEmail = myEmail
    def receive_file(self, my_path):
        try:
            print("Waiting for File Request...")
            ack = self.file_socket.recv(1024).decode('utf-8')
            if(ack == "sendingInformation"):
                print("You have a transfer request...")
                self.file_socket.send(f'sendReady'.encode('utf-8'))
                sendersEmail = self.file_socket.recv(1024).decode('utf-8')
                self.file_socket.send(f'emailRecieved'.encode('utf-8'))
                fileName = self.file_socket.recv(1024).decode('utf-8')
                self.file_socket.send(f'fileNameRecieved'.encode('utf-8'))
                with open(my_path, "r") as file:
                    isContact = 0
                    dict = json.load(file)
                    i = 0
                    for i in range(len(dict)):
                        if(dict[i]['email'] == sendersEmail):
                            print("Contact Found")
                            isContact = 1
                file.close()
                if(isContact == 1):
                    self.file_socket.send(f'isContact'.encode('utf-8'))
                    print("Waiting for Receive of User Alert")
                    ack = self.file_socket.recv(1024).decode('utf-8')
                    if(ack == "AlertUser"):
                        print("Recieved User Alert Command")
                        response = input("Contact {} is sending a file '({})'\n Do you Accept? (y/n) ".format(sendersEmail, fileName))
                        if(response == 'y' or response =='Y'):
                            self.file_socket.send(f'Accepted'.encode('utf-8'))
                            with open(fileName + 'copy', "wb") as f:
                                while True:
                                    bytes_read = self.file_socket.recv(1024)

                                    if bytes_read == b"END_OF_FILE":
                                        print("End of file received")
                                        break

                                    # Check if bytes_read is empty and it's not just the sentinel value
                                    if not bytes_read: 
                                        # print("No longer bytes being read")
                                        break

                                    f.write(bytes_read)
                                f.close()    
                                # print("File Transferred to Recipient")
                            print("File Transferred Successfully")
                            return
                        elif(response == 'n' or response =='N'):
                            self.file_socket.send(f'Rejected'.encode('utf-8'))
                            return
                else:
                    print("Not a Contact")
                    self.file_socket.send(f'notContact'.encode('utf-8'))
        except KeyboardInterrupt:
            print("\n")
            return
    def send_file(self, recipient_email, file_path):
        # print("WIP")
        self.command_socket.send(b"send_user_file")
        file_name = os.path.basename(file_path)
        ack = self.file_socket.recv(1024).decode('utf-8')
        if(ack == 'fileTransferReady'):
            # print("WE ARE READY")
            self.file_socket.send(f'clientSideAcknowledge'.encode('utf-8'))
            ack = self.file_socket.recv(1024).decode('utf-8')
            if(ack == "initiate"):
                # print("KEEP GOING ITS WORKING!!!!")
                #Send to Server--------------------
                self.file_socket.send(f'sendingFileName'.encode('utf-8'))
                ack = self.file_socket.recv(1024).decode('utf-8')
                if(ack == "sendFileName"):
                    self.file_socket.send(f'{file_name}'.encode('utf-8'))
                    #file name
                        #senders email
                    ack = self.file_socket.recv(1024).decode('utf-8')
                    if ack == "sendSendersEmail":
                        # print("Sending sendersEmail {}".format(self.myEmail))
                        self.file_socket.send(f'{self.myEmail}'.encode('utf-8'))
                        ack = self.file_socket.recv(1024).decode('utf-8')
                        if ack == "sendRecipientEmail":
                            # print("Sending RecipientEmail")
                            self.file_socket.send(f'{recipient_email}'.encode('utf-8'))
                            ack = self.file_socket.recv(1024).decode('utf-8')
                            if ack == "serverSendingAlert":
                                # print("Sending Alert")
                                self.file_socket.send(f'sendAlert'.encode('utf-8'))
                                ack = self.file_socket.recv(1024).decode('utf-8')
                                if(ack == "UserNotOnline"):
                                    print("User is not a valid contact...")
                                    return
                                if(ack == "UserOnline"):
                                    ack = self.file_socket.recv(1024).decode('utf-8')
                                    print(ack + " message received")
                                    if(ack == "notAContact"):
                                        print("Recipient Doesnt Have You As A Contact!") 
                                        return   
                                    elif (ack == "RecipientAccepted"):
                                        # print("RECIPENTE ACCPETED WHOO")
                                        try:
                                            with open(file_path, "rb") as f:
                                                while True:
                                                    # read the bytes from the file
                                                    bytes_read = f.read(1024)
                                                    if not bytes_read:
                                                        # file transmitting is done
                                                        break
                                                    # we use sendall to assure transimission in 
                                                    # busy networks
                                                    self.file_socket.sendall(bytes_read)

                                        except KeyboardInterrupt:
                                            print("Force Closing...")
                                            
                                        # print("File Transferred to server")
                                        self.file_socket.sendall(b"END_OF_FILE")
                                        f.close()
                                        return
                                    elif (ack == "RecipientRejected"):
                                        print(recipient_email + " has rejected the file transfer")
                                        return    
    def getOnlineUsers(self):
        self.command_socket.send(b"get_online_users")
        try:
            response = self.command_socket.recv(1024).decode('utf-8')
        except Exception as e:
            print(f"Error receiving response: {e}")
        users = response.split(',')
        print("Fetched users online")
        return users