# client.py
import socket
import Comprador
import pickle

comprador = Comprador.Comprador()
picklestring = pickle.dumps(comprador)
# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))

#SERIALIZA EL OBJETO CLIENTE
s.send(picklestring)
# Receive no more than 1024 bytes
tm = s.recv(1024)

s.close()

print("The time got from the server is %s" % tm.decode('ascii'))