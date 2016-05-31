# server.py
import socket
import time
import Subastador
import pickle
import copy
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
    print '\033[91m'+"Envio Hora"+'\033[1m'

print "Comenzando subasta"
pro = 1
numero_jugadores = []

bandera = 0
#Hace la subasta para todos los produvtos INCOMPLETO
while len(subastador.productos):
    print "---------------------------------------"
    print "Producto", subastador.productos[pro]
    print subastador.productos.values()[0]
    numero_jugadores = []
    for i in clientsockets:
        numero_jugadores.append(i)
    print numero_jugadores
    GANADOR = clientsockets[0]
    GASTO = 1
    BONO = 2
    subastador.nuevo_product(subastador.valores_estimados.values()[0], GANADOR)
    #Por cada cliente le manda el valor inicial, y pide la oferta y actualiza el valor, y le manda el nuevo max al cliente
    while (len(numero_jugadores) > 1):
        print "NUEVA RONDA"

        for clientsocket in clientsockets:
            print "NUMERO DE JUGADORES", len(numero_jugadores)
            print "MAXIMA OFRTA",subastador.max_puja
            print "Cliente en juego?", clientsocket in numero_jugadores
            if clientsocket in numero_jugadores:
                print '\033[91m' + "Envio Maximo "+str(subastador.max_puja)+ '\033[1m'
                clientsocket.send(str(subastador.max_puja)) #--->(3) actual
                #bandera = int(clientsocket.recv(1024)) #<------(4) Si juego
                #numero_jugadores -= bandera
                time.sleep(0.2)
                #Oferta del cliente
                #if bandera == 0:
                oferta = float(clientsocket.recv(1024))  # <---- (5) Oferta
                print '\033[94m'+"Recivo oferta " + str(oferta) + '\033[1m'
                print "Oferta cliente",clientsockets.index(clientsocket),": ", oferta
                #Cambia
                if(float(oferta) != 2.0):
                    subastador.nuevo_max(oferta,GANADOR)
                    GANADOR = clientsocket
                    print '\033[91m' + "Envio Maximo " + str(subastador.max_puja) + '\033[1m'
                    clientsocket.send(str(subastador.max_puja)) # ------> (6) Actual

                else:
                    numero_jugadores.remove(clientsocket)
                    #print "No envio valor" ,subastador.valores_estimados[pro]
                    print '\033[91m' + "Envio Maximo " + str(subastador.max_puja) + '\033[1m'
                    clientsocket.send(str(subastador.max_puja)) # ------> (6) Actual
                time.sleep(0.1)

                if(len(numero_jugadores)>1):
                    print '\033[91m' + "Envio No fin Producto 0 " + '\033[1m'
                    clientsocket.send(str("0"))
            else:
                clientsocket.send("NOJUEGO")  # --->(3) actual
                print '\033[91m' + "Envio  fin Producto NOJUEGO"+ '\033[1m'
    time.sleep(0.1)
    #clientsocket.send(str("FINPRO"))  # ------> (9) fin producto

    subastador.productos.pop(pro)
    subastador.valores_estimados.pop(pro)

    for clientsocket in clientsockets:
        clientsocket.send("NOJUEGO")  # --->(3) actual
        time.sleep(0.1)
        print '\033[91m' + "Envio  fin Producto NOJUEGO" + '\033[1m'
        if (clientsocket == GANADOR):
            print '\033[91m' + "Envio  ganador" + str(subastador.max_puja) + '\033[1m'
            clientsocket.send(str(subastador.max_puja))
        else:
            print '\033[91m' + "Envio  no Ganador " + str("NADA") + '\033[1m'
            clientsocket.send(str("NADA"))


    pro += 1
#Les informa a todos que acabo la subasta
for clientsocket in clientsockets:
    clientsocket.send("FINSUBASTA")
    print '\033[91m' + "Envio  fin subasta " + '\033[1m'
    time.sleep(0.1)
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