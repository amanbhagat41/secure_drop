import json
import os
from os import path
import maskpass
import bcrypt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def secureShell():
   while True:
    userInput = input("secure_drop> ")
    if userInput == "exit":
      exit()
    elif userInput == "help":
       print('  "add"  -> Add a new contact')
       print('  "list" -> List all online contacts')
       print('  "send" -> Transfer file to contact')
       print('  "exit" -> Exit SecureDrop')
    elif userInput == "add":
       cName = input("  Enter Full Name: ")
       cEmail = input("  Enter Email Address: ")
      #  salt = bcrypt.gensalt()
      #  cEmail = bcrypt.hashpw(cEmail, salt)
       contacts = [
          {"name": "",
          "email": "",
          }
       ]
       for contact in contacts:
        contact['name'] =  cName
        contact['email'] = cEmail
        my_path = 'contact.json'
        if path.exists(my_path):
          with open(my_path , 'r') as file:
           previous_json = json.load(file)
           contacts = previous_json + contacts
           with open(my_path , 'w') as file:
            json.dump(contacts, file, indent=4)
            print("Contact Added.")
        elif (not path.exists(my_path)):
           with open("contact.json", "w") as f:
            json.dump(contacts, f, indent=4)
            print("Contact Added.")
        with open(my_path, "r+") as file:
              # data = json.loads(open(my_path).read())
              # id_number = data[1]["email"]
              # if id_number in contacts:
              #    print("found")
              # print(id_number)
     
            content = file.read()
            file.seek(0)
            newC = content.replace("poop", "Pee")
            file.truncate(0)
            file.write(newC)
    elif userInput == "list":
      print("Work In Progress")
      with open("contact.json", "r") as outfile:
        data = json.load(outfile)
      print(data)
    elif userInput == "send":
       print("Work In Progress")

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
        # private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
        # print(private_key)
        #generate private key for authentication
        with open("users.json", "w") as outfile:
            outfile.write(json_file)
            