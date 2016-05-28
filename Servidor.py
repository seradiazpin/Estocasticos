# servchat.py
# Creamos un servidor de chat.

import socket
import select

class agentAuctionner():
    states = {"":1}
    actions = {"informar":1}
    def program(self, buyer, offer):

        # percepciones:
        # * comprador (tipo socket)
        # * oferta obtenida por un comprador (tipo entero)

        global maximumOffer
        global agentList

        if(offer > maximumOffer):
            maximumOffer = offer


        action = self.actions["informar"]
        argument = maximumOffer

        return action,argument


def accept_new_connection():

 try:
     global server
     global agentList
     newsock, (remhost, remport) = server.accept()
     server.settimeout(.1)
     runAction(newsock, 0, maximumOffer)
     agentList.append(newsock)
 except:
     pass


def broadcast(msg, sock):

     global agentList
     global server
     host, port = sock.getpeername()
     msg = "%s:%s:%s" % (str(host), str(port), str(msg))
     for destsock in agentList:
         #if destsock != sock and destsock != server:
         if destsock != server:
             destsock.send(msg)

def get_msg(sock):

 try:
     msg = sock.recv(1024)
     sock.settimeout(.1)
     return msg
 except:
     global agentList
     host, port = sock.getpeername()
     print "[%s:%s] ha salido." % (str(host), str(port))
     agentList.remove(sock)
     return None




def runAction(agent, action, argument):

    if( action==0 ):
        #en esta accion el servidor envia
        # el valor maximo del elemento ofertado
        # a UN agente que se conecta por primera vez
        host, port = agent.getpeername()

        m = str(action)+ ":" + str(argument)
        msg = "%s:%s:%s" % (str(host), str(port), str(m))
        agent.send(msg)


    if( action==1 ):
        #en esta accion el servidor envia
        # el valor maximo del elemento ofertado
        # a TODOS los agentes clientes
        msg= str(action)+ ":" + argument
        broadcast(msg, agent)





global server
global agentList
global maximumOffer


auctionner =agentAuctionner()
maximumOffer=0

print("Soy el agente subastador")
# se configura el tipo de socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#se asigna la y IP y el puerto del servidor
#server.bind(("192.168.137.41", 8000))
server = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
server.bind((host, port))        # Bind to the port
#maximo 5 conexiones paralelo
server.listen(5)

agentList = [server]
while 1:
 accept_new_connection()
 (sread, swrite, sexc) = select.select(agentList, [], [])
 for agent in sread:
     if agent != server:
         flag = get_msg(agent)
         if flag:
             (action, argument) = auctionner.program(agent, flag)
             runAction(agent, int(action), argument)












