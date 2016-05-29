# client.py
import socket
import Comprador
import pickle
import time

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
tm = s.recv(1024)
print("The time got from the server is %s" % tm.decode('ascii'))
time.sleep(0.2)
actual = s.recv(1024)

while actual != "FINSUBASTA":
    # Receive no more than 1024 bytes
    #comprador.hacer_puja(actual)
    print actual
    oferta = comprador.hacer_puja(float(actual))
    if oferta != -1.0:
        s.send(str(oferta))
    else:
        s.send(str(-1))
    actual = s.recv(1024)


s.close()

