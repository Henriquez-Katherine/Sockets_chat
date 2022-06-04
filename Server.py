
import socket
import threading
import hashlib
import time
import random


import sqlite3
from sqlite3 import Error


# Ranks
# user = 0
# room_owner = 1
# manager = 2
# admin = 3
# operator = 4

# Status
# ACTIVE - normal
# BANNED - banned
# FROZEN - freezed

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
                self.users_data = [] # User: login rang(User, manager, admin), socket, address
                self.server = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM,
                    )
                # Create socket for server

                self.letters = ["a", "b", "c", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
                # For token generation

        
        def main(self):
                print ("[INFO] SERVER start listening.")
                self.based()
                print ("[INFO] DATA BASE connected.")
                Run = True
                cmds = threading.Thread(target=self.cmd) # Create thread for console commands
                cmds.start()
                while Run:
                        if self.stopping == True:
                            return
                        user_socket, address = self.server.accept() # Unknow user try to connect
                        user_socket.send(f"********************* \n".encode("utf-8")) # Send user data(check)
                        self.users.append(user_socket)
                        listen_accept = threading.Thread( target=self.listen,  args=(user_socket, address,) )
                        listen_accept.start() # User connected and now listening


        def cmd(self):
            print ("|| SERVER 0.1        CONTROL CMD||")
            while True:
                for i in self.chats:
                    if len(i[1]) <= 0:
                        self.chats.remove(i)
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
                    for i in self.users_data:
                        print (f"USER: {i}")
                if a[0] == "!stats":
                    print ("SERVER v0.1: ")
                    print (f"ADDRESS: {self.ip}, PORT: {self.port}")


        def listen(self, user, adr):
            # Start work with user
            conn = sqlite3.connect('basa.bd')
            cursor = conn.cursor()
            Run = True
            token = "NULL"
            login = "NULL"
            while Run: # Wait for right password
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
                    if self.stopping == True:
                        return
                    try:    
                        if entry[0] == "!create" and len(entry) >= 3:
                            cursor.execute(f"SELECT * FROM users WHERE name = '{entry[1]}'")
                            buf = cursor.fetchall()
                            if len(buf) == 0:
                                cursor.execute("""INSERT INTO users(name, password, rank, bal, status, token, reg_date)
                                    VALUES('"""+ entry[1] + """', '"""+ self.hashing(entry[2]) + """', 0, 0, 'ACTIVE', '0', datetime(datetime())
                                    """)
                                conn.commit()
                            else:
                                user.send("* Error! The user already exists!".encode("utf-8"))
                        else:
                            if len(entry) >= 2:
                                cursor.execute(f"SELECT * FROM users WHERE name = '{entry[0]}' and password = '{self.hashing(entry[1])}'")
                                buf = cursor.fetchall()
                                if len(buf) > 0:
                                    if buf[0][4] == "BANNED" or buf[0][4] == "FROZEN":
                                        user.send("| YOUR ACCOUNT HAS BEEN BANNED |".encode("utf-8"))
                                        user.send("| DAYS OF THE END OF THE BAN: 99999 |".encode("utf-8"))
                                        user.send("* Acces denied!".encode("utf-8"))
                                        return
                                    else:
                                        user.send("* Acces greated!".encode("utf-8"))
                                        print (f"[INFO] User connected as: {buf[0][0]}")
                                        login = buf[0][0]
                                        Run = False
                                        print (buf)
                                        self.users_data.append((login, buf[0][2], user, adr))
                                else:
                                    user.send("Uncorrect data! User or password uncorrect.".encode("utf-8"))
                    except sqlite3.DatabaseError as err:
                        print (f"[ERROR] {err}")      
                except ConnectionResetError:
                        print ("[ERROR] USER disconnected Error!")
                        self.users.remove(user)
                        return
            Run = True
            Run1 = False
            n = 0
            rank = 0
            cursor.execute(f"SELECT * FROM users WHERE name = '{login}'")
            buf = cursor.fetchall()
            rank = buf[0][2]


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
                    if rank >= 3:
                        user.send("* Use !help to get commands".encode("utf-8"))
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

                    if self.stopping == True:
                        return

                    if len(entry) > 0:
                        if entry[0] == "!help":
                            user.send("* COMMNADS LIST: !help \n !ban \n !get_member \n !unban \n !ping \n []".encode("utf-8"))

                    # Ban in days: !ban name days reason
                    if len(entry) >= 4:
                        if entry[0] == "!ban":
                            cursor.execute(f"SELECT * FROM users WHERE name = '{entry[1]}'")
                            buf = cursor.fetchall()
                            if len(buf) > 0:
                                cursor.execute("""UPDATE users 
                                    SET status = 'BANNED'
                                    WHERE name = '""" + entry[1] + """' """)
                                cursor.execute(f"""INSERT INTO bans(name, reason, unban_date, ban_date)
                                    VALUES('{entry[1]}', '{entry[3]}', datetime(datetime(), '+{entry[2]} seconds'), datetime())
                                    """)
                                conn.commit()
                            else:
                                user.send("* Error! The user not exists!".encode("utf-8"))

                    if len(entry) >= 2:
                        if entry[0] == "!create" and entry[1] == "lobby":
                            token = ""
                            for i in range(self.token_len):
                                token = token + random.choice(self.letters)
                            self.chats.append([token, [[login, user]], "NO_NAME", 5, user])
                            user.send(f"Lobby created. token: {token}".encode("utf-8"))
                            user.send("| !help to get commands".encode("utf-8"))
                            cursor.execute("""
                                UPDATE users SET rank = 1
                                WHERE name = '""" + login + """' and rank = 0
                                """)
                            cursor.execute("""
                                UPDATE users SET token = '""" + token + """'
                                WHERE name = '""" + login + """'
                                """)
                            conn.commit()
                            Run1 = True    

                    for i in self.chats:
                        if i[0] == entry[0]:
                                user.send("* Joining to the chats...".encode("utf-8"))
                                token = i[0]
                                i[1].append([login, user])
                                user.send(f"| You connected to {i[2]} lobby! |".encode("utf-8"))
                                Run1 = True
                                cursor.execute("""
                                    UPDATE users SET token = '""" + token + """'
                                    WHERE name = '""" + login + """'
                                    """)
                                conn.commit()
                                break

                    if Run1 == True:
                        for i in self.chats:
                            if i[0] == token:
                                chat = n # chat Id
                                break
                            n += 1

                        while Run1:  
                                # This is chat
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
                                    buf0 = ""
                                    for i in data:
                                        if i == "'":
                                            buf0 = buf0 + "@"
                                        else:
                                            buf0 = buf0 + i
                                    data = buf0
                                    ent = data.split()

                                    if self.stopping == True:
                                        return

                                    if ent[0] == "!help" and self.chats[chat][4] == user:
                                        user.send("* Chat commands ** help \n List with commands: \n !help \n !kick \n !members \n !name \n !close \n []".encode("utf-8"))

                                    if ent[0] == "!kick" and self.chats[chat][4] == user and len(ent) >= 2:
                                        for u in self.chats[chat][1]:
                                            if ent[1] == u[0]:
                                                u[1].send("||||||||||||||||||||||||||||".encode("utf-8"))
                                                u[1].send("| You was kicked from lobby|".encode("utf-8"))
                                                self.chats[chat][1].remove(u)
                                                cursor.execute("""
                                                    UPDATE users SET token = '0'
                                                    WHERE name = '""" + u[0] + """'
                                                    """)
                                                conn.commit()
                                    if ent[0] == "!members" and self.chats[chat][4] == user:
                                        cursor.execute(f"SELECT * FROM users WHERE token = '{token}'")
                                        buf = cursor.fetchall()
                                        buf2 = []
                                        for i in buf:
                                            buf2.append(i[0])
                                        user.send(f"* Members: {buf2}".encode("utf-8"))
                                    if ent[0] == "!name" and self.chats[chat][4] == user and len(ent) >= 2:
                                        self.chats[chat][2] = ent[1]
                                        user.send("* Name changed!".encode("utf-8"))
                                    if ent[0] == "!close" and self.chats[chat][4] == user:
                                        data = "### CHAT WAS CLOSED!"
                                        for i in self.chats:
                                            if i[0] == token:
                                                for i1 in i[1]:
                                                    i1[1].send(data.encode("utf-8"))
                                                    cursor.execute("""
                                                        UPDATE users SET token = '0'
                                                        WHERE name = '""" + i1[0] + """'
                                                        """)
                                                    cursor.execute("""
                                                        UPDATE users SET rank = 0
                                                        WHERE name = '""" + i1[0] + """' and rank = 1
                                                        """)
                                                    conn.commit()
                                                break
                                        self.chats.remove(self.chats[chat])
                                        Run1 = False
                                        print (self.chats)
                                    data = login + " : " + f"{data}"
                                    cursor.execute(f"SELECT * FROM users WHERE name = '{login}' and token != '0'")
                                    if len(cursor.fetchall()) < 1:
                                        Run1 = False
                                    for i in self.chats:
                                        if i[0] == token:
                                            for i1 in i[1]:
                                                if i1[1] != user:
                                                    i1[1].send(data.encode("utf-8"))
                                            break

                except ConnectionResetError:
                    print ("[ERROR] USER disconnected Error!")
                    self.users.remove(user)
                    cursor.execute("""
                        UPDATE users SET rank = 0
                        WHERE name = '""" + login + """' and rank = 1
                        """)
                    cursor.execute("""
                        UPDATE users SET token = '0'
                        WHERE name = '""" + login + """'
                        """)
                    conn.commit()
                    return
            
            
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
                            port = int(input())
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

        def hashing(self, x): # here we create hash
            x = str(x).encode("utf-8")
            sha = hashlib.sha1(x).hexdigest()
            return sha

        def based(self):
            conn = sqlite3.connect('basa.bd')
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                password TEXT,
                rank INTEGER,
                bal INTEGER,
                status TEXT,
                token TEXT,
                reg_date DATE
                );
                """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bans(
                name TEXT,
                reason TEXT,
                unban_date DATE,
                ban_date DATE
                );
                """)
            conn.commit()
            #

            cursor.execute("SELECT * FROM bans WHERE unban_date >= ban_date")
            buf = cursor.fetchall()
            for i in buf:
                cursor.execute(f"SELECT * FROM users WHERE name = '{i[0]}'")
                buf1 = cursor.fetchall()
                if len(buf1) > 0:
                    print (buf1)
                    cursor.execute("""
                                UPDATE users SET status = "ACTIVE"
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
                    cursor.execute("""
                                DELETE FROM bans
                                WHERE name = '""" + buf1[0][0] + """'
                                """)
            cursor.execute("""
                UPDATE users SET rank = 0
                WHERE rank = 1
                """)
            cursor.execute("""
                UPDATE users SET token = '0'
                """)

            conn.commit()


