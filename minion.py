# -*- coding: utf-8 -*-

from threading import Thread
import time


class ChatSender(Thread):

    def __init__(self, socket_cliente, hist, secuencia, usuario):
        self.socket_cliente = socket_cliente
        self.hist = hist
        self.usuario = usuario
        self.secuencia = secuencia
        Thread.__init__(self)

    def run(self):
        try:
            while True:
                #print(".")
                msg_array, self.secuencia = self.hist.obtener_historia(self.secuencia, self.usuario)
                for mensaje in msg_array:
                    self.socket_cliente.send(mensaje["nombre"] + ": " + mensaje["mensaje"]+"\n")
                time.sleep(1)
        except IOError:
            print("Socket cerrado")
        except BaseException as be:
            print("Error General"+str(be))
        finally:
            return 0


class ChatMinion(Thread):
    buff = 4096
    hist = None
    secuencia = 0
    nicks = None
    usuario = None

    def __init__(self, socket_cliente, socket_info, hist, usuarios):
        self.socket_cliente = socket_cliente
        self.socket_info = socket_info
        self.hist = hist
        self.nicks = usuarios
        Thread.__init__(self)

    def validar_nick(self, comando, nick):
        """
        :rtype : bool
        :param comando : Comando para establecer el nick
        :param nick: Nombre de usuario
        :return: True si es que se pudo validar y agregar el nick o False si ya se existe alguien con el mismo nick
        """
        # FIXME: Validar y añadir nick a la lista compartida
        nick = nick.strip()
        if comando != "NICK":
            return False

        if nick in self.nicks:
            print(nick + " ya existe")
            return False
        else:
            self.nicks.add(nick)
            self.usuario = nick
            print(nick + " Entró a la sala de chat")
            return True
    '''
    def enviar_historia(self):
        msg_array, self.secuencia = self.hist.obtener_historia(self.secuencia, self.usuario)
        for mensaje in msg_array:
            self.socket_cliente.send(mensaje["nombre"] + " : " + mensaje["mensaje"] + "\n")
    '''

    def run(self):
        print 'Conexión recibida: ' + self.socket_info[0] + ' puerto: ' + \
              str(self.socket_info[1])

        # Validar nombre de usuario
        respuesta = self.socket_cliente.recv(self.buff)
        comando, valor = parse_respuesta(respuesta)

        if self.validar_nick(comando, valor):
            ret_mens = ""
            self.socket_cliente.send("Bienvenido a la sala de Chat {0}\n".format(self.usuario))
            #self.enviar_historia()
            ChatSender(self.socket_cliente, self.hist, self.secuencia, self.usuario).start()
            respuesta = self.socket_cliente.recv(self.buff)
            comando, valor = parse_respuesta(respuesta)
            while comando:
                print "CMD : " + comando
                print "VAL : " + valor
                self.secuencia = self.hist.escribir_historia(self.usuario, valor)
                respuesta = self.socket_cliente.recv(self.buff)
                comando, valor = parse_respuesta(respuesta)
                #self.enviar_historia()
        else:
            if comando == "MENS":
                ret_mens = "Debe validar el nombre de usuario primero "
            else:
                ret_mens = "Comando no esperado "

        if self.usuario is not None:
            self.nicks.remove(self.usuario)
            print(self.usuario + " se desconectó")

        self.socket_cliente.send(ret_mens + "Conexión terminada\n")
        self.socket_cliente.close()


def parse_respuesta(cadena):
    if cadena == "EOF" or cadena is None:
        print("Cadena vacía")
        return None, "Fin de conexión"
    else:
        cmd, s, v = cadena.partition(" ")
        # print "cmd "+cmd
        # print "space "+s
        #print "value "+v
        if cmd == "MENS" or cmd == "NICK":
            return cmd, v.strip()
        else:
            return None, "Fin de conexión"