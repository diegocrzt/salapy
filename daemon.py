# -*- coding: utf-8 -*-

import socket

from minion import ChatMinion
from historial import Historial


class ChatDaemon(object):
    backlog = 5
    hist = None
    usuarios = None

    def __init__(self, direccion="", puerto=1234):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((direccion, puerto))
        self.hist = Historial()
        self.usuarios = set()

    def inicializar(self):
        self.server_socket.listen(self.backlog)

        print "[salapy] Iniciando Servidor"
        print "[salapy] Esperando conexiones"

        while True:
            try:
                cliente, detalle = self.server_socket.accept()
                ChatMinion(cliente, detalle, self.hist, self.usuarios).start()
            except KeyboardInterrupt:
                self.server_socket.close()
                print("Terminó a pedido del usuario ")
                exit(0)