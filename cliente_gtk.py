# -*- coding: utf-8 -*-
#import pygtk
#pygtk.require('2.0')
import gtk

#from libsalapy import ClienteConsola

class MyWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        #self.name = name
        #gtk.Window.__init__(self, title="Python+Git chat")
        self.set_title("Python+Git chat")
        # 400x600
        self.set_size_request(400, 600)

        # box
        #vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL, spacing=6)
        vbox = gtk.VBox()
        vbox.set_spacing(6)
        #vbox.set_border_width(6)
        self.add(vbox)

        # Mensajes
        self.messages = gtk.TextView()
        self.messages.set_editable(False)
        buffer = self.messages.get_buffer()
        tag = buffer.create_tag('username')

        vbox.pack_start(self.messages, True, True, 10)
        #vbox.add(self.messages)
        # Entrada
        self.entry = gtk.Entry()
        self.entry.set_text("")
        vbox.pack_start(self.entry, False, True, 0)
        #vbox.add(self.entry)

        # Enviar!
        self.button = gtk.Button(label="Enviar!")
        self.button.connect("clicked", self.send_message)
        vbox.pack_start(self.button, False, True, 0)
        #vbox.add(self.button)

        # Login
        self.log_in = gtk.Button(label="Iniciar Sesion")
        self.log_in.connect("clicked", self.do_login)
        vbox.pack_start(self.log_in, False, True, 0)
        #vbox.add(self.log_in)



    def send_message(self, widget):
        user = self.name
        message = self.entry.get_text()
        self.entry.set_text("")
        print "<{0}>".format(user), message
        #################################
        # Implementar envio de mensajes #
        #################################

    def do_login(self, widget):
        pass

def main():
    win = MyWindow()

    win.connect("destroy", gtk.main_quit)
    win.show_all()
    gtk.main()


if __name__ == '__main__':
    main()