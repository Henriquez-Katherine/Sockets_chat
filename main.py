import socket
import threading

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
id = "127.0.0.1"
while True:
    try:
        server.bind(
        (id, 8001) # bind hosting port and adress
        )
        break
    except OSError:
        print ("ERROR, Please change IP address at hosting config")

server.listen(5) #listen users
print ("[WARN] Server start listening!!!")
password = "1234"
users = [] # list with users
closing = False

def listen(user):
    global closing
    global password
    while True: # Wait for right password
        data = user.recv(2048)
        if data.decode("utf-8") == password:
            print ("Right password!")
            user.send("1".encode("utf-8"))
            break
        else:
            user.send("0".encode("utf-8"))
        if closing == True:
            break
    while True:
        if closing == True:
            break
        data = user.recv(2048)
        print (data) # Get data from user
    return
        
def cmd_cont(): # server control
    global password
    global closing
    while True:
        cmd = str(input(":::"))
        if cmd == "help":
            print ("* Control console ** help \n List with commands: \n help \n stop \n users \n password_change \n Write one command without any /! \n []")
        elif cmd == "stop":
            print ("Stopping server...")
            closing = True
            print ("Server stopped!")            
        elif cmd == "users":
            print ("Users list:")
            print (users)
        elif cmd == "password_change":
            print ("Write new password: ")
            password = str(input())
            print ("[WARN] Password was changed")
        else:
            print ("* Uncorrect command! Use help to get command list ///")
def start():
    global closing
    Run = True
    cmds  = threading.Thread(target=cmd_cont)
    cmds.start()
    while Run:
        user_socket, address = server.accept()
        user_socket.send(f"Connected! <{address[0]}!>".encode("utf-8")) # Send user data
        users.append(user_socket)
        listen_accept = threading.Thread( target=listen,  args=(user_socket,) )
        listen_accept.start() # User connected and now listening
        if closing == True:
            break
    return
if __name__ == "__main__":    
    start()


