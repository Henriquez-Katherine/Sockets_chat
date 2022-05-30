import hashlib
import random
import socket
import threading
import time


#a = str(input()).encode("utf-8")
#sha = hashlib.sha1(a).hexdigest()
#print (sha)

from Server import Servers
# Imports


sr = Servers()
sr.set_up()
sr.main()
input()