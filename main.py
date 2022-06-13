import random
import socket
import threading
import time

from Classes.Server import Server
# Imports


sr = Server()
sr.set_up()
sr.main()
input()