# -*- coding: utf-8 -*-

import socket
from threading import Thread
import time


class HiloReceptor(Thread):
    socket_chat = None
    #iter_texto = None
    #buffer_texto = None

    #def __init__(self, socket_chat, iter_texto, buffer_texto):
    def __init__(self, socket_chat, dispose_resp):
        self.socket_chat = socket_chat
        #self.iter_texto = iter_texto
        #self.buffer_texto = buffer_texto
        self.dipose_resp_function = dispose_resp
        Thread.__init__(self)

    def run(self):
        try:
            while True:
                resp = self.socket_chat.recv(4096)

                #self.buffer_texto.insert(self.iter_texto, resp)
                try:
                    self.dipose_resp_function(resp)
                except Exception as e:
                    print("No se pudo llamar la función de salida de texto\n" + str(e))
                    print(resp)

                time.sleep(1)
        except IOError as io:
            print("Desconectado'\n" + str(io))
        except Exception as e:
            print("Error General\n" + str(e))
        finally:
            print("Hilo de recepción terminado")
            return -1


class ClienteConsola(Thread):

    sock_buff = 4096
    dispose_resp_function = None

    def __init__(self, direccion="127.0.0.1", puerto=1234, dispose_resp=None):
        self.socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tupla_server = (direccion, puerto)
        self.receptor = None
        self.dispose_resp_function = dispose_resp

        Thread.__init__(self)

    def login(self, usuario="Anonimo"):

        login_ok = False
        entrada = usuario
        if entrada != "" and entrada is not None:

            self.socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_chat.connect(self.tupla_server)
            self.socket_chat.send("NICK"+" "+entrada)

            resp = self.socket_chat.recv(self.sock_buff)

            if resp[:10] == "Bienvenido":
                login_ok = True
                # SI SALIO BIEN
                self.name = entrada

                #self.login.set_label("Cerrar Sesión")
                #self.login.connect("clicked", self.do_logout)
                #self.logineable = False

            #else:
                #self.logineable = True

            #self.buffer.insert(self.iter, resp)
            self.dispose_resp_function(resp)

            #self.socket_chat.close()
        else:
            self.dispose_resp_function("Ingrese un nombre de usuario antes\n")
            #self.buffer.insert(self.iter, "Ingrese un nombre de usuario antes\n")

        if login_ok:
            # Hilo para recibir sólo si se validó el inicio de sesión
            print("Arrancando Hilo de recepción")
            self.receptor = HiloReceptor(self.socket_chat, self.dispose_resp_function)
            self.receptor.start()

        return login_ok

    def logout(self):

        self.socket_chat.send("DISC"+" ")
        self.socket_chat.close()
        #self.logineable = True