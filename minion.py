# -*- coding: utf-8 -*-

from threading import Thread

class ChatMinion(Thread):

    buff = 4096
    hist = None
    secuencia = 0

    def __init__(self,socket_cliente,socket_info, hist):
        self.socket_cliente = socket_cliente
        self.socket_info = socket_info
        self.hist = hist
        Thread.__init__(self)
    
    def run(self):
		print 'Conexión recibida: '+self.socket_info[0]+' puerto: '+\
			str(self.socket_info[1])
		
		msg_array, self.secuencia = self.hist.obtener_historia(self.secuencia)
		for mensaje in msg_array:
			self.socket_cliente.send(mensaje["nombre"] + " : " + mensaje["mensaje"])
		
		respuesta = self.socket_cliente.recv(self.buff)
		comando, valor = parse_respuesta(respuesta)
		while comando:
			print "CMD : " + comando
			print "VAL : " + valor
			self.secuencia = self.hist.escribir_historia(comando,valor)
			respuesta = self.socket_cliente.recv(self.buff)
			comando, valor = parse_respuesta(respuesta)
		
		self.socket_cliente.send("Conexión terminada")
		self.socket_cliente.close


def parse_respuesta(cadena):
    if cadena == "EOF":
        return None , "Fin de conexión"
    else:
        return cadena, cadena
