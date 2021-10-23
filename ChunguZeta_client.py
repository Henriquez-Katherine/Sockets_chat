import socket
from tkinter import *
from threading import Thread
from tkinter import messagebox
import time

root  = Tk()
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM,
)
while True:
    try:
        id = "127.0.0.1"
        client.connect(
            (id, 8001) # connect to port and adress
        )
        break
    except ConnectionRefusedError:
        print ("IP not finded.. Please wait")
        time.sleep(5)
data = ""
root['bg'] = '#fafafa'
root.title("ChunguZeta_client")
root.wm_attributes('-alpha', 1)
root.geometry('700x600')
canvas = Canvas(root, height=600, width=700)
canvas.pack()
frame = Frame(root, bg='grey')
frame.place(relwidth=1, relheight=1)




def profiles(title2, title3, btn2, btn3, btn4, btn5):
    title2.destroy()
    title3.destroy()
    btn2.destroy()
    btn3.destroy()
    btn4.destroy()
    btn5.destroy()
    title4 = Label(frame, text='ChunguZeta v0.0.1', bg='white', font=100)
    title4.pack()
    title5 = Label(frame, text='Profiles', bg='white', font=40)
    title5.pack()
    
    
def listen_server():
    global data
    while True:
        data = client.recv(2048) # receive from server
        print (data.decode("utf-8"))
        data = data.decode("utf-8")
        if data == "1":
            print ("ENTERED!")
        if data == "0":
            print ("Error!")
def send_data():
    while True:
        ins = str(input()).encode("utf-8")
        client.send(ins)
def entered():
    title2 = Label(frame, text='ChunguZeta v0.0.1', bg='white', font=100)
    title2.pack()
    title3 = Label(frame, text='Welcome!', bg='white', font=40)
    title3.pack()
    btn2 = Button(frame, text='Profile', bg='yellow', font=40, command= lambda : profiles(title2, title3, btn2, btn3, btn4, btn5))
    btn2.place(relx=0, y = 60)
    btn3 = Button(frame, text='Chats', bg='yellow', font=40)
    btn3.place(relx=0, y = 100)
    btn4 = Button(frame, text='Data', bg='yellow', font=40)
    btn4.place(relx=0, y = 140)
    btn5 = Button(frame, text='Settings', bg='yellow', font=40)
    btn5.place(relx=0, y = 180)
    
def send(search):
        search1 = search.get()
        client.send(str(search1).encode("utf-8"))

    
def enter_in_system(user_login, user_password, title1, btn): # Send password and login at server for check
    global data
    login = user_login.get()
    password = user_password.get()
    if password  == "":
        password = "0"
    info = f"Data: {str(login)}, {str(password)}"
    messagebox.showinfo(title="INFO", message=info)
    client.send(password.encode("utf-8"))
    while True:
        if data  == "1":
            user_login.destroy()
            user_password.destroy()
            title1.destroy()
            btn.destroy()
            entered()
            break
        if data == "0":
            break        
def draw():

    title1 = Label(frame, text='ChunguZeta v0.0.1', bg='white', font=100)
    title1.pack()
    user_login = Entry(frame, bg='white')
    user_password = Entry(frame, bg='white', show='*')
    user_login.pack()
    user_password.pack()
    btn = Button(frame, text='Send', bg='yellow', font=100, command=lambda : enter_in_system(user_login, user_password, title1, btn))
    btn.pack()
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

