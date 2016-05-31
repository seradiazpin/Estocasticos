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
s.send(picklestring) #-->>>>(1) Objeto
tm = s.recv(1024) #<----(2)  tiempo
print("The time got from the server is %s" % tm.decode('ascii'))
actual = 0
fin_producto = "0"
while actual != "FINSUBASTA":
    # Receive no more than 1024 bytes
    #comprador.hacer_puja(actual)
    #print "Actual antes if", actual, fin_producto
    if(fin_producto == "0"):
        actual = s.recv(1024)  # <-------(3) actual
        print '\033[94m' + "Recivo actual " + str(actual) + '\033[1m'
        if(actual != "NOJUEGO"):
            if(actual != "FINSUBASTA" and actual != "NADA" and actual != ""):
                print actual
                oferta = comprador.hacer_puja(float(actual))
                if oferta != -1.0:
                    s.send(str(oferta)) #------>(5) oferta
                    #print "OFERTA: ", str(oferta)
                    print '\033[91m' + "Envio  oferta "+str(oferta)+ '\033[1m'
                else:
                    s.send("2")
                    #print "OFRETA: NADA"
                    print '\033[91m' + "Envio  oferta 2"+'\033[1m'
                actual = s.recv(1024)  # <-----(6) Actual
                #print '\033[94m' + "Recivo actual " + str(actual) + '\033[1m'
                time.sleep(0.1)
                fin_producto = str(s.recv(1024)) #<------ fin producto(6)
                print '\033[94m' + "Recivo fin producto " + str(fin_producto) + '\033[1m'
            else:
                fin_producto = s.recv(1024)
                print '\033[94m' + "Recivo fin producto " + str(fin_producto) + '\033[1m'
    else:
        #print "Nuevo fin", actual
        fin_producto = "0"
        ganador = s.recv(1024)  # <-------(3) actual
        print '\033[94m' + "Recivo ganador " + str(ganador) + '\033[1m'
        if(ganador != "NADA" and ganador != "" and ganador != "NOJUEGO"):
            comprador.dinero -= float(ganador)
            comprador.objetos_comprados += 1

s.close()

print comprador