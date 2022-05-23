import socket
from threading import Thread

client = socket.socket(               
    socket.AF_INET,
    socket.SOCK_STREAM,   
)


client.connect(
    ("127.0.0.1", 8001)
)
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
