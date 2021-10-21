import socket
from tkinter import *
from threading import Thread


root  = Tk()


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
id = "127.0.0.1"
client.connect(
    (id, 8001) # bind hosting port and adress
)

def listen_server():
    while True:
        data = client.recv(2048) # receive from server
        print (data.decode("utf-8"))
def send_data():
    while True:
        ins = str(input()).encode("utf-8")
        client.send(ins)
def draw():
    root['bg'] = '#fafafa'
    root.title("ChunguZeta_client")
    root.wm_attributes('-alpha', 1)
    root.geometry('500x400')
    canvas = Canvas(root, height=500, width=400)
    canvas.pack()
    frame = Frame(root, bg='red')
    frame.place(relwidth=0.7, relheight=0.7)
    root.resizable(width=False, height=False)
    root.mainloop()
    
def start():
        print ("[WARN] Client started!")
        listen = Thread(target=listen_server)
        sends = Thread(target=send_data)
        listen.start()
        sends.start()
        draw()
        
if __name__ ==  "__main__":
    start()
