#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk
import pango
import freedometer

class MainWindow:
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def scan(self, widget):
        self.liststore.clear()
        packages = self.free.scan_system()
        for i in packages:
            self.liststore.append(i)
        if (len(packages) == 0):
            dialog = gtk.Dialog("My dialog", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_DELETE_EVENT))
            label = gtk.Label(self.free.no_nonfree())
            dialog.vbox.pack_start(label,True,True,10)
            label.show()
            dialog.run()
            dialog.destroy()

    def __init__(self):
        self.free = freedometer.Freedometer()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(10)
        self.window.set_default_size(400,-1)
    
        self.box1 = gtk.VBox()

        self.system = self.free.system_summary()

        self.header = gtk.Label(self.system)
        self.header.set_line_wrap(True)
        self.box1.pack_start(self.header, True, True, 0)
        self.header.show()

        self.liststore = gtk.ListStore(str,str,str,str)
        self.tree = gtk.TreeView(self.liststore)
        self.textrenderer = gtk.CellRendererText()
        self.columns = []
        self.cells = []
        self.titles = self.free.get_package_fieldnames()
        for i in range (0,len(self.titles)):
            self.columns.append(gtk.TreeViewColumn(self.titles[i], self.textrenderer, text=i))
            self.tree.append_column(self.columns[i])
        self.tree.set_size_request(-1, 200)
        self.tree.show()
        self.scroll_tree = gtk.ScrolledWindow()
        self.scroll_tree.add(self.tree)
        self.scroll_tree.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.box1.pack_start(self.scroll_tree, True, True, 10)
        self.scroll_tree.show()

        self.box2 = gtk.HBox()
        self.button_scan = gtk.Button("Scan")
        self.button_scan.connect_object("clicked", self.scan, None)
        self.box2.pack_start(self.button_scan, True, True, 10)
        self.button_scan.show()

        self.button = gtk.Button("Quit")
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.box2.pack_start(self.button, True, True, 10)
        self.button.show()
        self.box1.pack_start(self.box2, True, True, 10)
        self.box2.show()

        self.window.add(self.box1)
        self.box1.show()
        self.window.show()

    def main(self):
        gtk.main()
        
if (__name__ == "__main__"):
    main = MainWindow()
    main.main()

