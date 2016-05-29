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
clientsockets = []

#Consigue la coneccion de cada uno de los clientes, mas sus datos como objeto
while len(compradores)<1:
    # establish a connection
    clientsocket,addr = serversocket.accept()
    clientsockets.append(clientsocket)
    print("Got a connection from %s" % str(addr))
    data = clientsocket.recv(1024)
    comprador = pickle.loads(data)
    compradores.append(comprador)
    print comprador
    currentTime = time.ctime(time.time()) + "\r\n Cliente:"+str(len(compradores))
    clientsocket.send(currentTime.encode('ascii'))

print "Comenzando subasta"
pro = 1
#Hace la subasta para todos los produvtos INCOMPLETO
while len(subastador.productos):
    print subastador.productos.values()[0]
    GANADOR = 0
    GASTO = 1
    BONO = 2
    #Por cada cliente le manda el valor inicial, y pide la oferta y actualiza el valor, y le manda el nuevo max al cliente
    for clientsocket in clientsockets:
        clientsocket.send(str(subastador.valores_estimados[pro]))
        time.sleep(0.2)
        #Oferta del cliente
        oferta = float(clientsocket.recv(1024))
        print "Oferta cliente: ", oferta
        #Cambia
        if(float(oferta) != -1.0):
            subastador.nuevo_max(oferta,GANADOR)
            GANADOR +=1
            clientsocket.send(str(subastador.valores_estimados[pro]))
        else:
            GANADOR += 1
            clientsocket.send(str(subastador.valores_estimados[pro]))
    subastador.productos.pop(pro)
    pro += 1
#Les informa a todos que acabo la subasta
for clientsocket in clientsockets:
    clientsocket.send("FINSUBASTA")
serversocket.close()
"""
#DESERIALIZA EL OBJETO
comprador = pickle.loads(data)
compradores.append(comprador)
print comprador
currentTime = time.ctime(time.time()) + "\r\n"
clientsocket.send(currentTime.encode('ascii'))
clientsocket.send(str(-1))
clientsocket.close()"""