import json
import os
from os import path
import maskpass
import bcrypt
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.fernet import Fernet
import Crypto
import string
import random
import threading
import socket
# from secure_drop.server import server
import client as client


def secureShell():
   while True:
    #Start Socket
    userInput = input("secure_drop> ")
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
       print('  "exit" -> Exit SecureDrop')
    elif userInput == "add":
       alreadyAdded = 0
       cName = input("  Enter Full Name: ")
       cEmail = input("  Enter Email Address: ")
       for contact in contacts:
        # salt = bcrypt.gensalt()
        # cEmail = bcrypt.hashpw(cEmail, salt)
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
        if(alreadyAdded == 0):
         if path.exists(my_path):
           with open(my_path , 'r') as file:
            previous_json = json.load(file)
            contacts = previous_json + contacts
            with open(my_path , 'w') as file:
             json.dump(contacts, file, indent=4)
             print("Contact Added.")
    elif userInput == "list":
      print("Work In Progress")
      #Send a ping to all open ports to see who is online on the localhost
      #if it gets a response from someone, we know they are active
    elif userInput == "send":
       client.start_client()
       print("Work In Progress")
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
          print("Wrong Password")
      else:
        print("No Email Matches")
  else:
      print("No users are registered with this client.")  #register new user
      inp = input("Do you want to register a new user? (y/n)")
      if inp == 'y':
          # generate the key here
          res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=10))
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
          userInfo = [fullName, emailAdd, passwrd, res]
          json_file = json.dumps(userInfo)
          # private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
          # print(private_key)
          #generate private key for authentication
          with open("users.json", "w") as outfile:
              outfile.write(json_file)
main()