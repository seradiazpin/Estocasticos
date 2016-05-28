import socket               # Import socket module
import Comprador as cmpr

class Cliente:
    def __init__(self):
        self.comprador = cmpr.Comprador()
        self.sk = socket.socket()
        self.host = socket.gethostname()
        self.port = 12345
        self.sk.connect((self.host, self.port))
        self.sk.recv(1024)


    def mandar_puja(self):
        self.comprador.hacer_puja()


    def mandar_mensaje(self,value):
        self.tmp = str(value)
        self.msg = ''
        for self.i in self.tmp:
            if self.i != '\n':
                self.msg += self.i
        self.client.send(self.msg)

    def coneccion(self):
        print "LOLOLOLO"
        while True:
            self.sk.recv(1024)

cliente = Cliente()
cliente.coneccion()