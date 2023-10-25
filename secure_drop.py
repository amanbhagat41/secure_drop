import io
import json
import os
import maskpass
import pwd
import crypt
import bcrypt
import random, string
import getpass

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
       contactAdd = [cName, cEmail]
       text_file = json.dumps(contactAdd)
       with open("contact.json", "a") as outfile:
        outfile.write(text_file +  "\n")
        print("Contact Added.")
    elif userInput == "list":
      print("Work In Progress")
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
        with open("users.json", "w") as outfile:
            outfile.write(json_file)



