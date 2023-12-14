import socket
import threading
import os

HOST = '127.0.0.1'
<<<<<<< Updated upstream
PORT = 5552
=======
PORT = 5555
FILEPORT = 5556
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
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
=======
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
                                    with open(file_name + 'copy', "wb") as f:
                                        while True:
                                            bytes_read = file_socket.recv(1024)

                                            if bytes_read == b"END_OF_FILE":
                                                print("End of file received")
                                                break

                                            # Check if bytes_read is empty and it's not just the sentinel value
                                            if not bytes_read: 
                                                print("No longer bytes being read")
                                                break

                                            f.write(bytes_read)
                                        f.close()
                                        print("File Transferred to Recipient")
                                    #Send the file to the recipient
                                    try:
                                        with open(file_name + 'copy', "rb") as f:
                                            while True:
                                                # read the bytes from the file
                                                bytes_read = f.read(1024)
                                                if not bytes_read:
                                                    # file transmitting is done
                                                    break
                                                # we use sendall to assure transimission in 
                                                # busy networks
                                                recipient_socket.sendall(bytes_read)

                                    except KeyboardInterrupt:
                                        print("Force Closing...")
                                        
                                    print("File Transferred to server")
                                    recipient_socket.sendall(b"END_OF_FILE")
                                    f.close()
                                    #delete temp file
                                    if os.path.exists(file_name + 'copy'):
                                        os.remove(file_name + 'copy')
                                        print("Removed Temporary file")
                                    else:
                                        print("This file does not exist")
                                        
                                elif(ack == "Rejected"):
                                    print("Recipient Denied Transfer")
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        server_socket.close()
=======
        server_socket.close()
>>>>>>> Stashed changes
