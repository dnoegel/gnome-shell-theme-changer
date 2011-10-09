#!/usr/bin/env python
# coding:utf-8

## Simple script to change the theme in gnome-shell
# requires the user-theme extension

# http://www.micahcarrick.com/gsettings-python-gnome-3.html

import os

from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
from gi.repository import GdkPixbuf
from gi.repository import Gio as gio

SETTINGS_KEY = "org.gnome.shell.extensions.user-theme"

## List themes in ~/.themes
def get_themes():
    path = os.path.expanduser("~/.themes")
    
    return [d for d in os.listdir(path) if os.path.exists(os.path.join(path, d, "gnome-shell"))]
    

## Main class
# should be replaced, as it is a simple wrapper class
class Main(object):
    def __init__(self):
        self.settings = gio.Settings.new(SETTINGS_KEY)
        self.settings.get_string("name")
        self.gui = GUI(self)
        

## The actual user interface
class GUI(object): 
    def __init__(self, main):
        self.main = main
        
        self.window = gtk.Window()
        self.window.set_property("resizable", False)
        self.window.set_size_request(300, 250)
        self.window.set_title("GnomeShell Theme Selector v0.1")
        self.window.connect("destroy", gtk.main_quit)
        
        self.vbox = gtk.VBox()


        self.image = gtk.Image()
                
        self.combo = gtk.ComboBoxText()
        self._fill_combo()
        self.combo.connect("changed", self.combo_changed_cb)
        
        btn = gtk.Button(stock=gtk.STOCK_QUIT)
        btn.connect("clicked", self.btn_clicked_cb)
        
        self.vbox.pack_start(self.combo, False, True, 0)
        self.vbox.pack_start(self.image, False, True, 0)
        self.vbox.pack_start(btn, False, True, 0)
        self.window.add(self.vbox)
        
        self.window.show_all()
        
    def _fill_combo(self):
        cur_theme = self.main.settings.get_string("name")
        
        for i, t in enumerate(get_themes()):
            self.combo.append_text(t)
            if t == cur_theme:
                self.combo.set_active(i)
                self.set_image_from_theme_name(cur_theme)
                
    def set_image_from_theme_name(self, name):
        themes_path = os.path.expanduser("~/.themes")
        
        image_path = None
        
        path = os.path.join(themes_path, name, "gnome-shell")
        for fl in os.listdir(path):
            if fl.startswith("preview") and fl.endswith("png"):
                image_path = os.path.join(path, fl)
                break
        
        if image_path:
            pb =GdkPixbuf.Pixbuf().new_from_file_at_size(image_path, 320, 200)
            self.image.set_from_pixbuf(pb)
        else:
            self.image.set_from_stock(gtk.STOCK_MISSING_IMAGE, gtk.IconSize.DIALOG)
        
    #
    # Callbacks 
    #
    def btn_clicked_cb(self, widget):
        gtk.main_quit()
    def combo_changed_cb(self, widget):
        model = widget.get_model()
        iter = widget.get_active_iter()
        
        new_entry = model.get_value(iter, 0)
        self.main.settings.set_string("name", new_entry)
        self.set_image_from_theme_name(new_entry)

if __name__ == "__main__":
    Main()
    gtk.main()
