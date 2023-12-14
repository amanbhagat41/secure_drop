import socket
import threading

HOST = '127.0.0.1'
PORT = 5552
FILEPORT = 5553
client_info = {}  # Dictionary to store client information (email: (socket, address))

def handle_client(command_socket, address, file_socket, faddress):
    print(f"Accepted connection from {address}")

    email = command_socket.recv(1024).decode('utf-8')
    client_info[email] = (file_socket, faddress)

    while True:
        data = command_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Received from {address}: {data}")

        #print(data)
        # Check for the special command to get online users
        split_result = data.split('#')
        # Extract the second and third elements
        #print(split_result)
        selection = split_result[0]
        if selection == "get_online_users":
            online_users = [email for email in client_info]
            online_users_str = ','.join(online_users)

            try:
                command_socket.send(f'{online_users_str}'.encode('utf-8'))
            except Exception as e:
                print(f"Error sending response to {address}: {e}")
            return
        elif selection == "send_user_file":
            print("WIP")
            fileTransfer(file_socket, faddress)
            # file_socket_handler = threading.Thread(target=fileTransfer, args=(file_socket, faddress))
            # file_socket_handler.start()
            

    del client_info[email]
    command_socket.close()
def fileTransfer(file_socket, faddress):
    print("I am being called for a file transfer")
    print(f"file connection established from {faddress}")
    file_socket.send(f'fileTransferReady'.encode('utf-8'))
    ack = file_socket.recv(1024).decode('utf-8')
    if(ack == 'clientSideAcknowledge'):
        file_socket.send(f'initiate'.encode('utf-8'))
        print("Are we working???")
        ack = file_socket.recv(1024).decode('utf-8') #recieves sendingFileName
        if(ack == 'sendingFileName'):
            file_socket.send(f'sendFileName'.encode('utf-8'))
            file_name = file_socket.recv(1024).decode('utf-8')
            print("Server Recieved File Name: {}".format(file_name))
            file_socket.send(f'sendSendersEmail'.encode('utf-8'))
            sendersEmail = file_socket.recv(1024).decode('utf-8')
            print("Server Recieved Senders Email: {}".format(sendersEmail))
            file_socket.send(f'sendRecipientEmail'.encode('utf-8'))
            recipient_email = file_socket.recv(1024).decode('utf-8')
            print("Server Recieved Recipient: {}".format(recipient_email))
            file_socket.send(f'serverSendingAlert'.encode('utf-8'))
            ack = file_socket.recv(1024).decode('utf-8')
            if(ack == "sendAlert"):
                print("Sending Alert to Recipient (WIP)")
                if recipient_email in client_info:
                    recipient_socket, _ = client_info[recipient_email]
                    print("Found Recipient")
                    recipient_socket.send(f'sendingInformation'.encode('utf-8'))
                    ack = recipient_socket.recv(1024).decode('utf-8')
                    if(ack == "sendReady"):
                        recipient_socket.send(f'{sendersEmail}'.encode('utf-8'))
                        ack = recipient_socket.recv(1024).decode('utf-8')
                        if(ack == "emailRecieved"):
                            recipient_socket.send(f'{file_name}'.encode('utf-8'))
                            ack = recipient_socket.recv(1024).decode('utf-8')
                            if(ack == "fileNameRecieved"):
                                recipient_socket.send(f'AlertUser'.encode('utf-8'))
                                ack = recipient_socket.recv(1024).decode('utf-8')
                                if(ack == "Accepted"):
                                    print("Recipient Accepted Request")
                                    file_socket.send(f'RecipientAccepted'.encode('utf-8'))
                                    with open("fileTransfer.txt", "wb") as f:
                                        while True:
                                            # read 1024 bytes from the socket (receive)
                                            bytes_read = file_socket.recv(1024)
                                            if not bytes_read:    
                                                # nothing is received
                                                # file transmitting is done
                                                f.close()
                                                break
                                            # write to the file the bytes we just received
                                            f.write(bytes_read)
                                        
                                        print("File Transferred to Recipient")
                                elif(ack == "Rejected"):
                                    print("Recipient Denied Transfer")

if __name__ == '__main__':
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Server is listening on {HOST}:{PORT}")

        file_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_command.bind((HOST, FILEPORT))
        file_command.listen()
                
        while True:
            command_socket, address = server_socket.accept()
            file_socket, faddress = file_command.accept()
            client_handler = threading.Thread(target=handle_client, args=(command_socket, address, file_socket, faddress))
            client_handler.start()
    except KeyboardInterrupt:
        print("\nTurning Off Server.........")
    finally:
        server_socket.close()
        file_command.close()