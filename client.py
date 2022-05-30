import socket
from threading import Thread

client = socket.socket(               
    socket.AF_INET,
    socket.SOCK_STREAM,   
)


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
                client.connect(
                        (id, port) # bind hosting port and adress
                        )
                break
        except:
                print ("[ERROR] SET UP ERROR. Invalid ip or port or other error.")

def listen():
    while True:
        data = client.recv(2048)
        print (data.decode("utf-8"))   

def send_client():
    print ("STARTED")
    listen_thr = Thread(target=listen)
    listen_thr.start()
    while True:
        client.send(input("").encode("utf-8"))

send_client()
