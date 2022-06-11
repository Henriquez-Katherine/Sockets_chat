
import socket
import threading
import time
import random

from Database import Database
from Logger import Logger
from SocketX import SocketX
from Chat import Chat
from Hasher import Hasher

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



class Message():

    def __init__(self, author, time, content):
        self.author = author
        self.time = time
        self.content = content



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

        self.request = ()
        self.answer = 0
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
        bds = threading.Thread(target=self.bd) # Create thread
        bds.start()
        while True:
            user, address = self._SocketX__connect(self.server) 
            user.send(f"********************* \n".encode("utf-8")) # Send user data(check)
            self.users.append(address)
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
                                self.request = (3, entry[1], entry[2])
                                if self.answer == 1:
                                    user.send("* Created!".encode("utf-8"))
                                else:
                                    user.send("* Error! The user already exists!".encode("utf-8"))
                            else:
                                if len(entry) >= 2:
                                    self.request = (10, entry[0], entry[1])
                                    if self.answer == 1:
                                            user.send("* Acces greated!".encode("utf-8"))
                                            print (f"[INFO] User connected")
                                            break
                                    else:
                                        user.send("Uncorrect data! User or password uncorrect.".encode("utf-8"))    
                except Exception as er:
                        print (f"[ERROR] {er}!")
                        self.users.remove(user)
                        return
    
    def bd(self):
        if len(self.request) > 0:
            self.answer = 0
            if self.request[0] == 1:
                self.answer = Database.check_init()
            if self.request[0] == 2:
                Database.init()
            if self.request[0] == 3:
                self.answer = Database.new_user(self.request[1], self.request[2])
            if self.request[0] == 4:
                self.answer = Database.del_user(self.request[1])
            if self.request[0] == 5:
                self.answer = Database.find_with_name(self.request[1])
            if self.request[0] == 6:
                self.answer = Database.ban_user(self.request[1], self.request[2], self.request[3])
            if self.request[0] == 7:
                self.answer = Database.set_token(self.request[1], self.request[2])
            if self.request[0] == 8:
                self.answer = Database.clear_token(self.request[1])
            if self.request[0] == 9:
                self.answer = Database.find_with_token(self.request[1])
            if self.request[0] == 10:
                self.answer = Database.check_name_password(self.request[1], self.request[2])
            self.request = ()

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




                            

               

    