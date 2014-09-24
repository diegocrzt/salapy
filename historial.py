# -*- coding: utf-8 -*-


class Historial(object):
    def __init__(self):
        self.secuencia_max = 0
        self.historia = []

    def escribir_historia(self, sujeto, predicado):
        nueva_historia = {'nombre': sujeto, 'mensaje': predicado}
        self.historia.append(nueva_historia)
        self.secuencia_max += 1
        print "[historial] << " + nueva_historia['nombre'] \
              + ": " + nueva_historia['mensaje']
        return self.secuencia_max

    def obtener_historia(self, secuencia, excluir=""):
        ret = []
        if secuencia < self.secuencia_max:
            temp = self.historia[secuencia:self.secuencia_max - 1]
            for msg in temp:
                print(temp)
                if excluir not in msg.keys():
                    ret.append(msg)

        return ret, self.secuencia_max
