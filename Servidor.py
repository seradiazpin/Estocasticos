# server.py
import socket
import time
import Subastador
import pickle
# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = "127.0.0.1"#socket.gethostname()

port = 9999

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

subastador = Subastador.Subastador()
compradores = []
clientsockets = []

#Consigue la coneccion de cada uno de los clientes, mas sus datos como objeto
while len(compradores)<2:
    # establish a connection
    clientsocket,addr = serversocket.accept()
    clientsockets.append(clientsocket)
    print("Got a connection from %s" % str(addr))
    data = clientsocket.recv(1024) #<<<<------(1)  objeto
    comprador = pickle.loads(data)
    compradores.append(comprador)
    print comprador
    currentTime = time.ctime(time.time()) + "\r\n Cliente:"+str(len(compradores))
    clientsocket.send(currentTime.encode('ascii'))#--->>>(2) tiempo

print "Comenzando subasta"
pro = 1
numero_jugadores = 0
bandera = 0
#Hace la subasta para todos los produvtos INCOMPLETO
while len(subastador.productos):
    for com in compradores:
        if com.juega:
            numero_jugadores += 1
    print subastador.productos.values()[0]

    GANADOR = 0
    GASTO = 1
    BONO = 2
    subastador.nuevo_max(subastador.valores_estimados.values()[0], GANADOR)
    #Por cada cliente le manda el valor inicial, y pide la oferta y actualiza el valor, y le manda el nuevo max al cliente
    #while (numero_jugadores > 1):
    for clientsocket in clientsockets:
        print subastador.max_puja
        clientsocket.send(str(subastador.max_puja)) #--->(3) actual
        #bandera = int(clientsocket.recv(1024)) #<------(4) Si juego
        #numero_jugadores -= bandera
        time.sleep(0.2)
        #Oferta del cliente
        #if bandera == 0:
        oferta = float(clientsocket.recv(1024))  # <---- (5) Oferta
        print "Oferta cliente",GANADOR,": ", oferta
        #Cambia
        if(float(oferta) != 2.0):
            subastador.nuevo_max(oferta,GANADOR)
            GANADOR += 1
            clientsocket.send(str(subastador.max_puja)) # ------> (6) Actual

        else:
            GANADOR += 1
            print "No envio valor" ,subastador.valores_estimados[pro]
            clientsocket.send(str(subastador.max_puja)) # ------> (6) Actual
        time.sleep(0.2)
        clientsocket.send(str("1"))  # ------> (9) fin producto

    subastador.productos.pop(pro)
    subastador.valores_estimados.pop(pro)

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