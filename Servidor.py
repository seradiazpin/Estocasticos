# server.py
import socket
import time
import Subastador
import pickle
# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

subastador = Subastador.Subastador()
compradores = []

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    data = clientsocket.recv(1024)
    #DESERIALIZA EL OBJETO
    comprador = pickle.loads(data)
    compradores.append(comprador)
    print comprador
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()