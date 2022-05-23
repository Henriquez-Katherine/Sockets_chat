import hashlib
import random
import socket
import threading
import time
#
#a = str(input()).encode("utf-8")
#sha = hashlib.sha1(a).hexdigest()
#print (sha)
users_data = [] # login password rang
users = []
chats = [] # [token, users, name, limit, owner]

token_len = 8

word = ["a", "b", "c", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

f = open("basa.txt", "r")
cou = f.readline() # Skip info
cou = f.readline() # Count of users
for i in range(int(cou)): # User: login password rang(User, manager, admin)
        users_data.append(str(f.readline()))
print (users_data)

# Create socket
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)

class Servers():
        def __init__(self):
                self.ip = 0
                self.port = 8000
                self.max = 99
                self.stopping = False
        def main(self):
                print ("[INFO] SERVER start listening.")
                Run = True
                cmds  = threading.Thread(target=self.cmd)
                cmds.start()
                while Run:
                        if self.stopping == True:
                            return
                        user_socket, address = server.accept() # Unknow user try to connect
                        user_socket.send(f"*********************".encode("utf-8")) # Send user data
                        users.append(user_socket)
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
                    for i in users:
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
                        for i in users:
                            if i == user:
                                users.remove(i)
                        return
                    for i in users_data:
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
                        for i in users:
                            if i == user:
                                users.remove(i)
                        return
                    if entry[0] == "!create" and entry[1] == "lobby":
                        token = ""
                        for i in range(token_len):
                            token = token + random.choice(word)
                        chats.append([token, [user], "NO_NAME", 5, user])
                        user.send(f"Lobby created. token: {token}".encode("utf-8"))
                        user.send("| !help to get commands".encode("utf-8"))

                        Run = False    
                    for i in chats:
                        if i[0] == entry[0]:
                                user.send("* Joining to the chats...".encode("utf-8"))
                                token = i[0]
                                i[1].append(user)
                                user.send(f"| You connected to {i[2]} lobby! |".encode("utf-8"))
                                Run = False
                                break
                except ConnectionResetError:
                        print ("[ERROR] USER disconnected Error!")
                        break
            Run = True
            n = 0
            for i in chats:
                if i[0] == token:
                    chat = n
                    break
                n += 1
            while Run:
                try:
                    data = user.recv(2048)
                    data = data.decode("utf-8") 
                    ent = data.split()
                    if self.stopping == True:
                        return
                    if ent[0] == "!exit":
                        user.send("* You leave the server.".encode("utf-8"))
                        for i in users:
                            if i == user:
                                users.remove(i)
                        return
                    if ent[0] == "!help" and chats[chat][4] == user:
                        user.send("* Chat commands ** help \n List with commands: \n !help \n !kick \n !members \n !name \n !close \n []".encode("utf-8"))
                    if ent[0] == "!kick" and chats[chat][4] == user:
                        for u in users:
                            if ent[1] == u:
                                u.send("||||||||||||||||||||||||||||".encode("utf-8"))
                                u.send("| You was kicked from lobby|".encode("utf-8"))
                                for i in chats[chat][1]:
                                    if i == u:
                                        chats[chat][1].remove(i)
                    if ent[0] == "!members" and chats[chat][4] == user:
                        user.send(f"* Members: {chats[chat][1]}".encode("utf-8"))
                    if ent[0] == "!name":
                        chats[chat][2] = ent[1]
                        user.send("* Name changed!".encode("utf-8"))
                    if ent[0] == "!close":
                        chats.remove(chats[chat])
                    data = login + " : " + f"{data}"
                    for i in chats:
                        if i[0] == token:
                            for u in users:
                                if u in i[1]:
                                    u.send(data.encode("utf-8"))
                            break
                except ConnectionResetError:
                        print ("[ERROR] USER disconnected Error!")
                        break

        def set_up(self):
                print ("|||||||||||||||||||||||||")
                print ("| Start set_uping       |")
                print ("* Set ip address and port. (Or write null)")
                dat = str(input()).split()
                if dat[0] != "null":
                    print ("* Write address: ")
                    id = str(input())
                    print ("* Write port: ")
                    port = str(input())
                else:
                    id = "127.0.0.1"
                    port = 8001
                while True:
                    try:
                        server.bind(
                        (id, port) # bind hosting port and adress
                        )
                        self.ip = id
                        self.port = port
                        break
                    except OSError:
                        print ("[ERROR] SET UP ERROR. Invalid ip or port or other error.")
                server.listen(self.max) #listen users  max
                print ("[INFO] SERVER set up.")


sr = Servers()
sr.set_up()
sr.main()
input()


class Client():
    def __init__(self):
        self.login = 0
        self.token = 0
        self.status = 0


