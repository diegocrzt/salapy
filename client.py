# -*- coding: utf-8 -*-
from gi.repository import Gtk
from daemon import ChatDaemon



class MyWindow(Gtk.Window):
    def __init__(self, name="Anónimo"):
        self.name = name
        Gtk.Window.__init__(self, title="Python+Git chat")
        # 400x600
        self.set_size_request(400, 600)

        # box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Mensajes
        self.messages = Gtk.TextView()
        self.messages.set_editable(False)
        buffer = self.messages.get_buffer()
        tag = buffer.create_tag('username')

        vbox.pack_start(self.messages, True, True, 10)

        # Entrada
        self.entry = Gtk.Entry()
        self.entry.set_text("")
        vbox.pack_start(self.entry, False, True, 0)

        # Enviar!
        self.button = Gtk.Button(label="Enviar!")
        self.button.connect("clicked", self.send_message)

        vbox.pack_start(self.button, False, True, 0)

    def send_message(self, widget):
        user = self.name
        message = self.entry.get_text()
        self.entry.set_text("")
        print "<{0}>".format(user), message
        #################################
        # Implementar envio de mensajes #
        #################################


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