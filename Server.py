
import socket
import threading
import time
import random

from Database import Database
from Logger import Logger
from SocketX import SocketX
from Chat import Chat
from Hasher import Hasher
from User import User
from Message import Message

# Ranks
# user = 0
# NONE = 1
# manager = 2
# admin = 3
# operator = 4

# Status
# ACTIVE - normal
# BANNED - banned
# FROZEN - freezed



class Cmd(): # Commands for server
    
    @staticmethod 
    def get_commands():
        print ("* Control console ** help \n List with commands: \n !help \n !stop \n !users \n !stats \n !close \n []")



class Server(SocketX, Cmd):

    def __init__(self):
        self.ip = 0
        self.port = 8001
        self.server = 0
        self.max = 99
        self.chats = []
        self.users = []

        self.token_len = 8
        self.letters = ["a", "b", "c", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        # For token generation

    def set_up(self):
            print ("|||||||||||||||||||||||||")
            print ("|      Start set_up     |")
            print ("|||||||||||||||||||||||||")
            print ("[LOG] Create socket...")
            self.server = self._SocketX__create_socket()
            print ("\n * Write y/n. Start localhost? (127.0.0.1:8001)")
            while True:
                try:
                    buf = str(input())
                    if buf == "y":
                        self.ip = "127.0.0.1"
                        self.port = 8001
                    else:
                        print ("* Write address: ")
                        self.ip = str(input())
                        print ("* Write port: ")
                        self.port = int(input())
                    self._SocketX__bind(self.server, self.ip, self.port)
                    self._SocketX__setListen(self.server, self.max)
                    return
                except Exception as error:
                    print (f"[ERROR] Error: {error}")

    def main(self):
        print ("[INFO] Starting...")
#        print (Database.check_init())
        consoles = threading.Thread(target=self.console) # Create thread for console commands
        consoles.start()
        print ("[INFO] Database connected...")
        Database.init()
#        bds = threading.Thread(target=self.bd) # Create thread
#        bds.start()
        while True:
            user, address = self._SocketX__connect(self.server) 
            user.send(f"********************* \n".encode("utf-8")) # Send user data(check)
            listen_accept = threading.Thread( target=self.listen,  args=(user, address,) )
            listen_accept.start() # User connected and now listening


    def listen(self, user, adr):
            while True: # Wait for right password
                try:
                    user.send("* Write your login, then your password: (if haven't record print !create name password )".encode("utf-8"))
                    data = user.recv(2048)
                    data = data.decode("utf-8")
                    buf0 = ""
                    for i in data:
                        if i == "'":
                            buf0 = buf0 + "@"
                        else:
                            buf0 = buf0 + i
                    data = buf0
                    entry = data.split()
                    if len(entry) > 0:    
                            if entry[0] == "!create" and len(entry) >= 3:  
                                if self.bd(3, entry[1], entry[2]) == True:
                                    user.send("* Created!".encode("utf-8"))
                                else:
                                    user.send("* Error! The user already exists!".encode("utf-8"))
                            else:
                                if len(entry) >= 2:
                                    if self.bd(10, entry[0], entry[1]) == True:
                                            user.send("* Acces greated!".encode("utf-8"))
                                            print (f"[INFO] User connected")
                                            break
                                    else:
                                        user.send("Uncorrect data! User or password uncorrect.".encode("utf-8"))    
                except Exception as er:
                        print (f"[ERROR] {er}!")
                        return
            # Create user
            buf = self.bd(5, entry[0])[0]
            self.users.append(User(buf[0], buf[2], buf[4]))
            num = len(self.users) - 1
            
            Run = False
            while True:
                ##
                user.send("* Write !connect 'token' or !create chat !".encode("utf-8"))
                data = user.recv(2048)
                data = data.decode("utf-8")
                buf0 = ""
                for i in data:
                        if i == "'":
                            buf0 = buf0 + "@"
                        else:
                            buf0 = buf0 + i
                data = buf0
                entry = data.split()
                if entry[0] == "!create" and entry[1] == "chat":
                        token = ""
                        for i in range(self.token_len):
                            token = token + random.choice(self.letters)
                        self.chats.append(Chat(token, self.users[num].get_name()))
                        self.users[num].token = token
                        user.send(f"Chat created. token: {token}".encode("utf-8"))
                        user.send("| !help to get commands".encode("utf-8"))
                        Run = True    



    def bd(self, *request):
            print ("REQ")
            if len(request) > 0:
                answer = False
                if request[0] == 1:
                    answer = Database.check_init()
                if request[0] == 2:
                    Database.init()
                if request[0] == 3:
                    answer = Database.new_user(request[1], request[2])
                if request[0] == 4:
                    answer = Database.del_user(request[1])
                if request[0] == 5:
                    answer = Database.find_with_name(request[1])
                if request[0] == 6:
                    answer = Database.ban_user(request[1], request[2], request[3])
                if request[0] == 7:
                    answer = Database.set_token(request[1], request[2])
                if request[0] == 8:
                    answer = Database.clear_token(request[1])
                if request[0] == 9:
                    answer = Database.find_with_token(request[1])
                if request[0] == 10:
                    answer = Database.check_name_password(request[1], request[2])
                return answer

    def console(self):
        print ("|| SERVER v0.5             ||")
        while True:
                buf = str(input()).split()
                if buf[0] == "!help":
                    self.get_commands()
                if buf[0] == "!stop":
                    print ("[WARN] Stopping SERVER!")
                    time.sleep(5)
                    print ("[INFO] SERVER stopped")
                    self.server.close()
                    return
                if buf[0] == "!stats":
                    print ("SERVER v0.5: ")
                    print (f"ADDRESS: {self.ip}, PORT: {self.port}")




                            

               

    