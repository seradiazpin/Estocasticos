import Comprador as cmpr, time
class Subastador:
    states = {"": 1}
    actions = {"informar": 1}
    def __init__(self):
        self.productos = {1:"Cosa",2:"Cosa2"}#,3:"Cosa3",4:"Cosa4",5:"Cosa5",6:"Cosa6",7:"Cosa7",8:"Cosa8",9:"Cosa9",10:"Cosa10",11:"Cosa11",12:"Cosa12"}
        self.valores_estimados = {1:50,2:80}#,3:150,4:40,5:300,6:500,7:600,8:200,9:4,10:33,11:14,12:15}
        self.max_puja = self.valores_estimados.values()[0]
        self.ganador = -1
        self.numero_de_pujas = 0

    def iniciar_subasta(self):
        return self.productos[1]

    def terminar_puja(self,inicio,fin):
        return fin - inicio > 5;

    def nuevo_max(self, puj,ganadorIndex):
        if puj > self.max_puja:
            self.max_puja = puj
            self.ganador = ganadorIndex

    def nuevo_product(self,puj,ganadorIndex):
        self.max_puja = puj
        self.ganador = ganadorIndex

    def terminar_subasta(self):
        if (self.numero_de_pujas == 1 or self.numero_de_pujas==0)  and self.max_puja != 0:
            producto_key = self.productos.keys()[0]
            print '\033[94m'+"Usuario ", self.ganador+1
            print "Ganador de subasta" , self.max_puja , self.valores_estimados[producto_key], self.max_puja -self.valores_estimados[producto_key]
            para_retornar = self.ganador,self.max_puja, abs(self.max_puja - self.valores_estimados[producto_key])
            self.productos.pop(self.productos.keys()[0])
            self.max_puja = self.valores_estimados.values()[0]
            return para_retornar
        return 1

    def informar_puja(self):
        return self.max_puja

    def hacer_subasta(self,producto,compradores):
        print '\033[1m'+"----------------------------------"
        print '\033[92m'+"Producto", producto
        print '\033[1m'+"----------------------------------"
        para_retornar = None
        while(producto in self.productos.values()):
            self.numero_de_pujas = 0
            for com in compradores:
                if com.juega:
                    self.numero_de_pujas += 1
            if (self.numero_de_pujas != 1):
                for i in range(len(compradores)):
                    if (compradores[i].juega):
                        print "Comprador -", i + 1, "Numero de pujas", self.numero_de_pujas
                        print compradores[i]
                        start_time = time.time()
                        puj = compradores[i].hacer_puja(self.informar_puja())
                        end_time = time.time()
                        if (puj != -1):
                            if not self.terminar_puja(start_time, end_time):
                                self.nuevo_max(puj,i)
                            self.numero_de_pujas += 1
                        else:
                            compradores[i].juega = False
            para_retornar = self.terminar_subasta()
        for com in compradores:
            com.juega = True
        return para_retornar



def main():
    subastador = Subastador()
    compradores = []
    for i in range(5):
        compradores.append(cmpr.Comprador())
    fin = 1

    GANADOR = 0
    GASTO = 1
    BONO = 2

    for producto in subastador.productos.values():
        retorno = subastador.hacer_subasta(producto,compradores)
        compradores[retorno[GANADOR]].actualizar_datos(retorno[GASTO],retorno[BONO])
        subastador.ganador = -1