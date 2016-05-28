import sys,random as rnd, time
class Comprador:
    ariesgado = {0.7:1.2}
    moderado = {0.5:1.2}
    conservador = {0.3:1.2}
    def __init__(self):
        self.dinero = 1000
        self.bono = 0
        self.objetos_comprados = 0
        self.asociado = False
        self.juega = True
        prob = rnd.random()
        if(prob <=0.33):
            self.personalidad = self.ariesgado
            self.personalidad_str = "Ariesgado"
        elif(prob >=0.33 and prob <=0.66):
            self.personalidad = self.moderado
            self.personalidad_str = "Moderado"
        else:
            self.personalidad = self.conservador
            self.personalidad_str = "Conservador"

    def posible_puja(self,actual,value):
        if actual>= self.dinero+self.bono or value > self.dinero:
            return False , -1
        else:
            if actual >= value:
                return False, -1
            else:
                return True , value


    def hacer_puja(self,actual):
        print "Valor actual de la puja", actual

        prob = rnd.random()

        aries = self.personalidad.keys()[0]
        print "PROB", prob, "ARIES", aries
        if prob <= aries:
            value = self.personalidad.values()[0]*actual
            valido,valor = self.posible_puja(actual,value)
            print "Valor a pujar",valor
            if valido:
                print "-------------------------------------------------"
                return value
            else:
                print "Puja No posible"
                print "-------------------------------------------------"
                return valor
        else:
            print "-------------------------------------------------"
            return -1
    def actualizar_datos(self,gasto,bono):
        self.dinero -= gasto
        self.bono = bono

    def __str__(self):
        return '\033[91m'+"Dinero: "+str(self.dinero)+" Bono: "+str(self.bono)+" "+self.personalidad_str+'\033[1m'