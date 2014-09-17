# -*- coding: utf-8 -*-

import socket
from minion import ChatMinion

class ChatDaemon(object):

    backlog = 5

    def __init__(self,direccion="",puerto=1234):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((direccion,puerto))
        
    def inicializar(self):
        self.server_socket.listen(self.backlog)
        
        while True:
            cliente, detalle = self.server_socket.accept()
            ChatMinion(cliente,detalle).start()
