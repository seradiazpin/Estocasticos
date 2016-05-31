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
host = "127.0.0.1"#socket.gethostname()

port = 9999

# connection to hostname on the port.
s.connect((host, port))
#SERIALIZA EL OBJETO CLIENTE
s.send(picklestring) #-->>>>(1) Objeto
tm = s.recv(1024) #<----(2)  tiempo
print("The time got from the server is %s" % tm.decode('ascii'))
time.sleep(0.2)
if(comprador.juega):
    s.send("0") #-->>>>(4) si Juego
else:
    s.send("1")  # -->>>>(4) si Juego
actual = 0
fin_producto = 0
while actual != "FINSUBASTA":
    # Receive no more than 1024 bytes
    #comprador.hacer_puja(actual)
    print "Actual antes if", actual, fin_producto
    if(fin_producto == 0):
        actual = s.recv(1024)  # <-------(3) actual
        if(actual != "FINSUBASTA"):
            print actual
            oferta = comprador.hacer_puja(float(actual))
            if oferta != -1.0:
                s.send(str(oferta)) #------>(5) oferta
            else:
                s.send("2")
            actual = s.recv(1024)  # <-----(6) Actual
            fin_producto = s.recv(1024) #<------ fin producto(6)
            print "Nuevo " , actual ,fin_producto
    else:
        print "Nuevo fin", actual
        fin_producto = 0


s.close()

