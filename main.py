import hashlib
import random
import socket
import threading
import time


#a = str(input()).encode("utf-8")
#sha = hashlib.sha1(a).hexdigest()
#print (sha)

from Server import Servers



sr = Servers()
sr.set_up()
sr.main()
input()

# Class for server operations
#
class Client():
    def __init__(self):
        self.login = 0
        self.token = 0
        self.status = 0
