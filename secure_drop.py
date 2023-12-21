import json
import sys
import os
from os import path
import maskpass
import bcrypt
from client import ChatClient

def secureShell():
   #Start Client
  with open('users.json', "r") as openfile:
    json_object = json.load(openfile)
  myChat = ChatClient(json_object[1])
  while True:
    selection = input("secure_drop> ")
    userInput = selection.split(' ', 1)[0]
    my_path = 'contact.json'
    contacts = [
          {"name": "EMPTY",
          "email": "EMPTY",
          }
       ]
    if (not path.exists(my_path)):
      with open("contact.json", "w") as f:
        json.dump(contacts, f, indent=4)
        print("Contact Added.")
    if userInput == "exit":
      exit()
    elif userInput == "help":
       print('  "add"  -> Add a new contact')
       print('  "list" -> List all online contacts')
       print('  "send" -> Transfer file to contact')
       print('  "recv" -> Recieve a file from a contact')
       print('  "exit" -> Exit SecureDrop')
    elif userInput == "add":
       alreadyAdded = 0
       cName = input("  Enter Full Name: ")
       cEmail = input("  Enter Email Address: ")
       for contact in contacts:
        contact['name'] =  cName
        contact['email'] = cEmail

        with open(my_path, "r+") as file:
          dict = json.load(file)
          i = 0
          for i in range(len(dict)):
            if(dict[i]['email'] == cEmail):
              alreadyAdded = 1
              print("Email Exists, Overwriting Name")
              dict[i]['name'] = cName
              with open(my_path, 'w') as json_file:
                json.dump(dict, json_file, indent = 4)
                json_file.close()
        file.close()
        if(alreadyAdded == 0):
         if path.exists(my_path):
           with open(my_path , 'r') as file:
            previous_json = json.load(file)
            contacts = previous_json + contacts
            with open(my_path , 'w') as file:
             json.dump(contacts, file, indent=4)
             print("Contact Added.")
    elif userInput == "list":
      allOnlineUsers = myChat.getOnlineUsers()
      with open(my_path, 'r') as file:
        data = json.load(file)
      with open("users.json", 'r') as file:
        userData = json.load(file)
      userEmail = userData[1]
      for item in data:
        if item['email'] != userEmail and item['email'] in allOnlineUsers:
          print(f"[ONLINE] Name: {item['name']}, Email: {item['email']}")
      #Send a ping to all open ports to see who is online on the localhost
      #if it gets a response from someone, we know they are active
    elif userInput == "send":
      recipient_emailSend = selection.split(' ', 2)[1]
      file_path = selection.split(' ', 2)[2]
      myChat.send_file(recipient_emailSend, file_path)
      # recipient_email = input("Enter recipient's email: ")
      #sending file logic here, might be myChat.send_file(parameters)
    elif userInput == "recv":
      myChat.receive_file(my_path)
       #once we know whos online and who is not, we will establish a connection for file sharing.

#main--------------------------------------------------------------------------------------------
def main():
  if os.path.exists("users.json"): #returning users
      retUserEmail = input("Enter Email Address: ")
      retUserPassword = maskpass.askpass()
      with open('users.json', "r") as openfile:
        json_object = json.load(openfile)
      userEmail = json_object[1]
      userPassword = json_object[2]
      if userEmail == retUserEmail:   #if user is a returning user check if passwords match
        if bcrypt.checkpw(retUserPassword, userPassword):
          print("Welcome to SecureDrop.")
          print('Type "help" For Commands.')
          secureShell()
        else:
          print("Email and Password Combination Invalid.")
      else:
        print("Email and Password Combination Invalid.")
  else:
      print("No users are registered with this client.")  #register new user
      inp = input("Do you want to register a new user? (y/n)")
      if inp == 'y':
          # generate the key here
          # print(res)
          #now write it to the users.json
          fullName = input("Enter Full Name: ")
          emailAdd = input("Enter Email Address: ")
          while(True):
              passwrd = maskpass.askpass()
              passwrdCheck = maskpass.askpass()
              if passwrd != passwrdCheck:
                  print("Passwords Do Not Match! Try Again")
              if passwrd == passwrdCheck:
                  break
          salt = bcrypt.gensalt()
          passwrd = bcrypt.hashpw(passwrd, salt)  #encrypt password   
          print("Passwords Matched")
          print("User Registered")
          print("Exiting SecureDrop.")
          userInfo = [fullName, emailAdd, passwrd]
          json_file = json.dumps(userInfo)
          with open("users.json", "w") as outfile:
              outfile.write(json_file)
main()