import socket
import threading

HOST = '127.0.0.1'
PORT = 5555
MOTHERSHIP = 5557
client_info = {}  # Dictionary to store client information (email: (socket, address))
def handle_client(client_socket, address, listen, command_socket):
    
    print(f"Server Accepted connection from {address}")

    email = command_socket.recv(1024).decode('utf-8')#
    client_info[email] = (command_socket, address)#

    while True:
        if(listen == True):
            
            data = command_socket.recv(1024).decode('utf-8')#
            print("Command: {}".format(data))
            if not data:
                break

            print(f"Received from {address}: {data}")

            # Check for the special command to get online users
            command, *args = data.split('#')
            
            if command == "get_online_users":
                listen = False
                handle_get_online_users(client_socket, address)
                listen = True
            elif command == "send_user_file":
                listen = False
                print("Command Sent")
                handle_send_user_file(client_socket, args)
                print("Im a pussy exiting when I shouldn't")

    # Remove the client from the dictionary and close the connection
    del client_info[email]
    client_socket.close()
    command_socket.close()

def handle_get_online_users(client_socket, address):
    try:
        online_users = ','.join(client_info)
        client_socket.send(online_users.encode('utf-8'))
    except Exception as e:
        print(f"Error sending response to {address}: {e}")

def handle_send_user_file(client_socket, args):
    if len(args) < 1:
        return

    recipient_email = args[0]
    if recipient_email in client_info:
        recipient_socket, _ = client_info[recipient_email]
        try:
            print("Sending has Initiated")
            command_socket.send(f'SendingInitated'.encode('utf-8'))
            file_size = int(client_socket.recv(1024).decode('utf-8'))
            print("Server Received file size {}".format(file_size))
            client_socket.send(f'ReceivedFileSize'.encode('utf-8'))
            ack = client_socket.recv(1024).decode('utf-8')
            if (ack == "sendingInfo"):
                print("Sending Info")
                client_socket.send(f'sendEmail'.encode('utf-8'))
                senderEmail = client_socket.recv(1024).decode('utf-8')
                print("Received Sender email {}".format(senderEmail))
                client_socket.send(f'ReceivedSenderEmail'.encode('utf-8'))
                ack = client_socket.recv(1024).decode('utf-8')
                if(ack == "sendUserAlert"):
                    print("Sending User Alert")
                    #Send Recipient Alert
                    recipient_socket.send(f'incomingRequest'.encode('utf-8'))
                    ack = client_socket.recv(1024).decode('utf-8')
                    if (ack == "sendSenderEmail"):
                        print("sender email Received")
                        recipient_socket.send(f'{senderEmail}'.encode('utf-8'))
                        ack = client_socket.recv(1024).decode('utf-8')
                        if(ack == "isContact"):
                            #Continue
                            print("User is a contact")
                            ack = client_socket.recv(1024).decode('utf-8')
                            if(ack == "accepted"):
                                recipient_socket.send(f'acceptedSeen'.encode('utf-8'))
                                print("Recipient Accepted Transfer")
                                print("STARTING FILE TRANSFER")
                                #Start FILE TRANSFER
                            elif(ack == "rejected"):
                                print("Recipient has rejected your transfer request")
                            
                        elif (ack == "notContact"):
                            print("This user has not added you as a contact yet...")
                            return
            #recipient_socket.send(b"FileTransferComplete")
        except Exception as e:
            print(f"Error forwarding file to {recipient_email}: {e}")
    else:
        print(f"Recipient {recipient_email} not found.")

if __name__ == '__main__':
    listen = True
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        mothership_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mothership_socket.bind((HOST, MOTHERSHIP))
        mothership_socket.listen()

        print(f"Server is listening on {HOST}:{PORT}")
        print(f"Mothership is listening on {HOST}:{MOTHERSHIP}")

        while True:
            client_socket, address = server_socket.accept()
            command_socket, faddress = mothership_socket.accept()

            client_handler = threading.Thread(target=handle_client, args=(client_socket, address, listen,command_socket))
            client_handler.start()
    except KeyboardInterrupt:
        print("\nTurning Off Server.........")
    finally:
        server_socket.close()
        mothership_socket.close()
