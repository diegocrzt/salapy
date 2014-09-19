# -*- coding: utf-8 -*-

from threading import Thread

class ChatMinion(Thread):

    buff = 4096

    def __init__(self,socket_cliente,socket_info):
        self.socket_cliente = socket_cliente
        self.socket_info = socket_info
        Thread.__init__(self)
    
    def run(self):
        print 'Conexión recibida: '+self.socket_info[0]+' puerto: '+\
            str(self.socket_info[1])
        respuesta = self.socket_cliente.recv(self.buff)
        comando, valor = parse_respuesta(respuesta)
        while comando:
            print "CMD : " + comando
            print "VAL : " + valor
            respuesta = self.socket_cliente.recv(self.buff)
            comando, valor = parse_respuesta(respuesta)
        
        socket_cliente.send("Conexión terminada")
        socket_cliente.close


def parse_respuesta(cadena):
    if cadena == "EOF":
        return None , "Fin de conexión"
    else:
        return cadena, cadena
