import socket
import threading
import hashlib
import time
import random

class Servers():

        def __init__(self):

                self.ip = 0
                self.port = 8000
                self.max = 99
                self.stopping = False

                self.chats = []  # [token, users, name, limit, owner]
                self.token_len = 8
                # token len for chats
                self.users = []
                self.users_data = ["bob 1234"] # User: login password rang(User, manager, admin)


                self.server = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,
                    )
                # Create socket for server

                self.letters = ["a", "b", "c", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                # For token generation


        def main(self):
                print ("[INFO] SERVER start listening.")
                Run = True
                cmds = threading.Thread(target=self.cmd) # Create thread for console commands
                cmds.start()
                while Run:
                        if self.stopping == True:
                            return
                        user_socket, address = self.server.accept() # Unknow user try to connect
                        user_socket.send(f"********************* \n".encode("utf-8")) # Send user data(check)
                        self.users.append(user_socket)
                        listen_accept = threading.Thread( target=self.listen,  args=(user_socket,) )
                        listen_accept.start() # User connected and now listening


        def cmd(self):
            print ("|| SERVER 0.1        CONTROL CMD||")
            while True:
                a = str(input()).split()
                if a[0] == "!help":
                    print ("* Control console ** help \n List with commands: \n !help \n !stop \n !users \n !stats \n !close \n []")
                if a[0] == "!stop":
                    print ("[WARN] Stopping SERVER!")
                    self.stopping = True
                    time.sleep(5)
                    print ("[INFO] SERVER stopped")
                    return
                if a[0] == "!users":
                    print ("[INFO] OUTPUT USERS: ")
                    for i in self.users:
                        print (f"USER: {i}")
                if a[0] == "!stats":
                    print ("SERVER v0.1: ")
                    print (f"ADDRESS: {self.ip}, PORT: {self.port}")


        def listen(self, user):
            # Start work with user
            Run = True
            token = "NULL"
            login = "NULL"
            while Run: # Wait for right password
                try:
                    user.send("* Write your login, then your password: (if haven't record print !create)".encode("utf-8"))
                    data = user.recv(2048)
                    data = data.decode("utf-8") 
                    entry = data.split()
                    if self.stopping == True:
                        return
                    if entry[0] == "!exit":
                        user.send("* You leave the server.".encode("utf-8"))
                        for i in self.users:
                            if i == user:
                                self.users.remove(i)
                        return
                    for i in self.users_data:
                        if i.split()[0] == entry[0]:
                                if i.split()[1] == entry[1]:
                                        login = entry[0]
                                        print (login)
                                        user.send("* Right answer! Acces greated!".encode("utf-8"))
                                        Run = False
                                        break
                        else:
                            user.send("Uncorrect data! User or password uncorrect.".encode("utf-8"))
                except ConnectionResetError:
                        print ("[ERROR] USER disconnected Error!")
                        break
            Run = True
            Run1 = False
            n = 0

            # Dont try to understand this shit

            # And....
            # First loop:
            # This loop connect user to the chat or create personal lobby
            # Second loop:
            # This loop sending messages, executing commands from owner and closing chats
            #
            # Here soo many 'if-else'
            while Run:
                try:
                    user.send("* Input chat token or write - !create lobby: ".encode("utf-8"))
                    data = user.recv(2048)
                    data = data.decode("utf-8") 
                    entry = data.split()
                    if self.stopping == True:
                        return
                    if entry[0] == "!exit":
                        user.send("* You leave the server.".encode("utf-8"))
                        for i in self.users:
                            if i == user:
                                self.users.remove(i)
                        return
                    if entry[0] == "!create" and entry[1] == "lobby":
                        token = ""
                        for i in range(self.token_len):
                            token = token + random.choice(self.letters)
                        self.chats.append([token, [user], "NO_NAME", 5, user])
                        user.send(f"Lobby created. token: {token}".encode("utf-8"))
                        user.send("| !help to get commands".encode("utf-8"))

                        Run1 = True    
                    for i in self.chats:
                        if i[0] == entry[0]:
                                user.send("* Joining to the chats...".encode("utf-8"))
                                token = i[0]
                                i[1].append(user)
                                user.send(f"| You connected to {i[2]} lobby! |".encode("utf-8"))
                                Run1 = True
                                break
                    if Run1 == True:
                        for i in self.chats:
                            if i[0] == token:
                                chat = n
                                break
                            n += 1
                        while Run1:
                                n =  0
                                for i in self.chats:
                                    if i == self.chats[chat]:
                                        pass
                                    else:
                                        n += 1
                                if n == len(self.chats):
                                    Run1 = False
                                    break
                                else:
                                    data = user.recv(2048)
                                    data = data.decode("utf-8") 
                                    ent = data.split()
                                    if self.stopping == True:
                                        return
                                    if ent[0] == "!exit":
                                        user.send("* You leave the server.".encode("utf-8"))
                                        for i in self.users:
                                            if i == user:
                                                self.users.remove(i)
                                                return
                                    if ent[0] == "!help" and self.chats[chat][4] == user:
                                        user.send("* Chat commands ** help \n List with commands: \n !help \n !kick \n !members \n !name \n !close \n []".encode("utf-8"))
                                    if ent[0] == "!kick" and self.chats[chat][4] == user:
                                        for u in self.users:
                                            if ent[1] == u:
                                                u.send("||||||||||||||||||||||||||||".encode("utf-8"))
                                                u.send("| You was kicked from lobby|".encode("utf-8"))
                                                for i in self.chats[chat][1]:
                                                    if i == u:
                                                        self.chats[chat][1].remove(i)
                                    if ent[0] == "!members" and self.chats[chat][4] == user:
                                        user.send(f"* Members: {self.chats[chat][1]}".encode("utf-8"))
                                    if ent[0] == "!name":
                                        self.chats[chat][2] = ent[1]
                                        user.send("* Name changed!".encode("utf-8"))
                                    if ent[0] == "!close":
                                        data = "### CHAT WAS CLOSED!"
                                        for i in self.chats:
                                            if i[0] == token:
                                                for u in self.users:
                                                    if u in i[1]:
                                                        u.send(data.encode("utf-8"))
                                                break
                                        self.chats.remove(self.chats[chat])
                                        Run1 = False
                                        print (self.chats)
                                    data = login + " : " + f"{data}"
                                    for i in self.chats:
                                        if i[0] == token:
                                            for u in self.users:
                                                if u in i[1]:
                                                    u.send(data.encode("utf-8"))
                                            break

                except ConnectionResetError:
                    print ("[ERROR] USER disconnected Error!")
                    break
            
            
        def set_up(self):
                print ("|||||||||||||||||||||||||")
                print ("| Start set_up  |")
                
                while True:
                    try:
                        print ("* Set ip and port. (Or write null: 127.0.0.1:8001)")
                        dat = str(input()).split()
                        if dat[0] != "null": # Skip
                            print ("* Write address: ")
                            id = str(input())
                            print ("* Write port: ")
                            port = str(input())
                        else:
                            id = "127.0.0.1"
                            port = 8001
                        self.server.bind(
                        (id, port) # bind hosting port and adress
                        )
                        self.ip = id
                        self.port = port
                        break
                    except:
                        print ("[ERROR] SET UP ERROR. Invalid ip or port or other error.")
                self.server.listen(self.max) #listen users  max
                print ("[INFO] SERVER set up.")
