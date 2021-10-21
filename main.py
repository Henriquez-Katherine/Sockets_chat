import socket
import threading

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
id = "127.0.0.1"
server.bind(
    (id, 8001) # bind hosting port and adress
)

server.listen(5) #listen users
print ("[WARN] Server start listening!!!")

users = []

def listen(user):
    while True:
        data = user.recv(2048)
        print (data)
def start():
    Run = True
    while Run:
        user_socket, address = server.accept()
        user_socket.send(f"Connected! <{address[0]}!>".encode("utf-8")) # Send user data
        users.append(user_socket)
        listen_accept = threading.Thread(
                target=listen,
                args=(user_socket,)
        )
        listen_accept.start()
        print ("Succefuly!")
if __name__ == "__main__":    
    start()
