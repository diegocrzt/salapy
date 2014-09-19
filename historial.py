# -*- coding: utf-8 -*-

class Historial(object):
	
	def __init__(self):
		self.secuencia_max = 0
		self.historia = []
		
	def escribir_historia(self, sujeto, predicado):
		nueva_historia = {'nombre': sujeto, 'mensaje' : predicado}
		self.historia.append(nueva_historia)
		self.secuencia_max += 1
	
	def obtener_historia(self,secuencia):
		ret = []
		if(secuencia < self.secuencia_max):
			ret = self.historia[secuencia:self.secuencia_max-1]
		
		return ret
