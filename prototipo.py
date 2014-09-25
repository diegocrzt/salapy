# -*- coding: utf-8 -*-
from gi.repository import Gtk
#import gtk as Gtk
#from gtk import Gtk
#from daemon import ChatDaemon
import socket
from threading import Thread
import time

HOST = "127.0.0.1"
PUERTO = 1234


class HiloReceptor(Thread):
    socket_chat = None
    iter_texto = None
    buffer_texto = None

    def __init__(self, socket_chat, iter_texto, buffer_texto):
        self.socket_chat = socket_chat
        self.iter_texto = iter_texto
        self.buffer_texto = buffer_texto
        Thread.__init__(self)

    def run(self):
        try:
            while True:
                resp = self.socket_chat.recv(4096)
                self.buffer_texto.insert(self.iter_texto, resp)
                time.sleep(1)
        except IOError as io:
            print("Desconectado'\n" + str(io))
        except Exception as e:
            print("Error General\n" + str(e))
        finally:
            print("Hilo de recepción terminado")
            return -1


class MyWindow(Gtk.Window):
    def __init__(self, name="Anónimo"):
        self.socket_chat = None
        self.nombre = name
        self.logineable = True
        Gtk.Window.__init__(self, title="Python+Git chat")
        # 400x600
        self.set_size_request(400, 600)

        # box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Mensajes
        self.messages = Gtk.TextView()
        self.messages.set_editable(False)
        self.buffer = self.messages.get_buffer()
        tag = self.buffer.create_tag('username')
        self.iter = self.buffer.get_iter_at_offset(0)

        sw = Gtk.ScrolledWindow()
        #sw.set_shadow_type(Gtk.SHADOW_ETCHED_IN)
        #sw.set_policy(Gtk.POLICY_AUTOMATIC, Gtk.POLICY_AUTOMATIC)

        sw.add(self.messages)

        vbox.pack_start(sw, True, True, 10)

        #vbox.pack_start(self.messages, True, True, 10)

        # Entrada
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        vbox.pack_start(self.entry, False, True, 0)

        # Enviar!
        self.button = Gtk.Button(label="Enviar!")
        self.button.connect("clicked", self.send_message)
        self.login = Gtk.Button(label="Iniciar Sesion")
        self.login.connect("clicked", self.do_login)

        vbox.pack_start(self.login, False, True, 0)
        vbox.pack_start(self.button, False, True, 0)

    def do_login(self, widget):
        print("do_login")
        if not self.logineable:
            return

        login_ok = False
        entrada = self.entry.get_text()
        if entrada != "" and entrada is not None:

            self.socket_chat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_chat.connect((HOST, PUERTO))
            self.socket_chat.send("NICK"+" "+entrada)
            self.entry.set_text("")

            resp = self.socket_chat.recv(4096)

            if resp[:10] == "Bienvenido":
                login_ok = True
                # SI SALIO BIEN
                self.name = entrada

                self.login.set_label("Cerrar Sesión")
                self.login.connect("clicked", self.do_logout)
                self.logineable = False
            else:
                self.logineable = True

            self.buffer.insert(self.iter, resp)

            #self.socket_chat.close()
        else:
            self.buffer.insert(self.iter, "Ingrese un nombre de usuario antes\n")

        if login_ok:
            # Hilo para recibir sólo si se validó el inicio de sesión
            print("Arrancando Hilo de recepción")
            HiloReceptor(self.socket_chat, self.iter, self.buffer).start()


    def do_logout(self, widget):
        print("do_logout")
        if self.logineable:
            return

        self.socket_chat.send("DISC"+" ")
        self.socket_chat.close()
        self.login.set_label("Iniciar Sesion")
        self.login.connect("clicked", self.do_login)
        self.logineable = True

    def send_message(self, widget):
        user = self.name
        message = self.entry.get_text()
        self.entry.set_text("")
        print "<{0}>".format(user), message
        #################################
        # Implementar envio de mensajes #
        #################################
        try:
            self.socket_chat.send("MENS"+" "+message)
            self.entry.set_text("")
        except Exception as e:
            print("Falló al enviar\n"+str(e))

    def new_message(self, user, message):
        buffer = self.messages.get_buffer()

        buffer.set_text(
            buffer.get_text(
                buffer.get_start_iter(),
                buffer.get_end_iter(),
                False
            ) + "<{0}>: {1}\n".format(user, message)
        )


win = MyWindow()

win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()