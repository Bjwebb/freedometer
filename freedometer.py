#    Freedometer
#
#    (c) Copyright 2008 Benjamin Webb <bjwebb67@googlemail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/python

import os
import platform
import sys
import commands

from optparse import OptionParser

cc_artwork = [ "human-icon-theme", "tangerine-icon-theme", "tango-icon-theme" ]
artwork = []
fonts = [ "gsfonts-other", "sun-java5-fonts", "sun-java6-fonts", "t1-xfree86-nonfree", "ttf-kochi-gothic-naga10", "ttf-kochi-mincho-naga10", "ttf-larabie-deco", "ttf-larabie-straight", "ttf-larabie-uncommon", "ttf-mikachan", "ttf-xfree86-nonfree", "ttf-xfree86-nonfree-syriac", "xfonts-naga10",
"msttcorefonts" ]
fonts_multi = [ "mplayer-fonts", "ttf-liberation" ]
package_titles = [ "Package name", "Category", "Section" ]

def caps(stringy):
    return stringy[0:1].upper() + stringy[1:].lower()

"""if (os.name == "nt"):
    print os.environ
    print platform.win32_ver()
elif (os.name == "posix"):
    print os.uname()
    print platform.dist()"""

def system_summary():
    global system
    global distro
    global winversion
    global packaging
    system = platform.system()
    summary = "The Operating System you are running is: "
    if (system == "Linux"):
        summary += "GNU/Linux"+" - "
        dist = platform.dist()
        if (dist[0] == "debian"):
            packaging = "apt"
            name = commands.getoutput("lsb_release -cis").partition('\n')
            distro = name[0]
            summary += name[0]+" "+name[2]+"\n\n"
        else:
            packaging = "dunno"
            distro = dist[0]
            summary += distro+" "+caps(dist[1])+"\n\n"
        summary += "GNU/Linux is made up most of freedomware. However, many systems have several pieces of propreitary software installed (find out why this is bad).\n\n"
        if (distro == "Debian"):
            summary += "Debian has a good commitment to freedomware, but not quite as far as gnewsense.\n\n"
        elif (distro == "Ubuntu"):
            summary += "Ubuntu has a good commitment to freedomware, but not as much as others such as fedora, debian and gnewsense.\n\n"
        elif (distro == "gNewSense"):
            summary += "gNewSense contains only freedomware, but it is possible that propreitary software may have been installed on it.\n\n"
	elif ("SuSE" in distro):
	    summary += "SuSE has an okay commitment to freedomware, but has signed suspicous patent deals.\n\n"
        if (packaging == "dunno"):
            summary += "Unfortunately the scan functionality does not work for this GNU/Linux distriubtion yet. Please contact us so that we can add it."
        else:
            if (graphics): summary += "Click the scan button below to scan for propreitary software that is installed on your system."
    elif (os.name == "posix"):
        summary += "Unix based, but not GNU/Linux.\nUnfortunately we do not support this operating system yet. If you would like to help us, please tell us what system you are using."
    elif (system == "Windows"):
        winversion = sys.getwindowsversion()
        if (winversion[0] < 4): version = winversion[0]
        elif (winversion[0] == 4):
            if (winversion[1] == 0): version = "95"
            elif (winversion[1] == 10): version = "98"
            elif (winversion[1] == 90): version = "ME"
        elif (winversion[0] == 5):
            if (winversion[1] == 0): version = "2000"
            else: version = "XP"
        elif (winversion[0] == 6): version = "Vista"
        else: version = winversion[0]
        summary += system+" "+version+"\n\n"
        summary += "Windows is a proprietary Operating System. However various pieces of freedomware can be installed.\n\n"
        if (graphics): summary += "Click scan to find common pieces of free software, then our wizard will help you start using more.\n\n"
        summary += "We can also help you install a free software Operating System, such as Ubuntu.\n\n"
    return summary

def free_exception(package):
    exception = False
    for i in cc_artwork:
        if (i==package):
            exception = True
            break
    return exception

def parse_list(pkglist):
    pkgs = []
    spacecount = 0
    while (pkglist != ""):
        pkgarr = pkglist.partition('\n')
        pkgname = pkgarr[0].rstrip()
        #print commands.getoutput("aptitude show "+pkgarr[0])
        if (pkgname != "" and free_exception(pkgname) != True):
            if (pkgname in artwork): cat = "Artwork"
            elif (pkgname in fonts): cat = "Font"
            else: cat = ""
            if (spacecount == 0):
                pkgs.append([pkgname, cat, "Non-free"])
            else:
                pkgs.append([pkgname, cat, "Contrib"])
        else:
            spacecount += 1
        pkglist = pkgarr[2]
    return pkgs

def scan_system():
    global system
    if (system == "Linux"):
        global packaging
        if (packaging == "apt"):
            pkgs = parse_list(commands.getoutput("./vrms -s"))
            return pkgs

def no_nonfree():
    return "You appear to have no non-free packages on your system. However, you may have added non-free software yourself, not using the package manager."

class MainWindow:
    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def scan(self, widget):
        self.liststore.clear()
        packages = scan_system()
        for i in packages:
            self.liststore.append(i)
        if (len(packages) == 0):
            dialog = gtk.Dialog("My dialog", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_DELETE_EVENT))
            label = gtk.Label(no_nonfree())
            dialog.vbox.pack_start(label,True,True,10)
            label.show()
            dialog.run()
            dialog.destroy()


    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(10)
        self.window.set_default_size(400,-1)
    
        self.box1 = gtk.VBox()

        self.system = system_summary()

        self.header = gtk.Label(self.system)
        self.header.set_line_wrap(True)
        self.box1.pack_start(self.header, True, True, 0)
        self.header.show()

        self.liststore = gtk.ListStore(str,str,str)
        self.tree = gtk.TreeView(self.liststore)
        self.textrenderer = gtk.CellRendererText()
        self.columns = []
        self.cells = []
        self.titles = package_titles
        for i in range (0,3):
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

graphics = True

parser = OptionParser
parser = OptionParser()
parser.add_option("-c", action="store_false", dest="graphics", help="Command line mode")
parser.add_option("-g", action="store_true", dest="graphics", help="Graphical (GTK) mode")
(options, args) = parser.parse_args()
if (options.graphics != None): graphics = options.graphics

def add_spaces(string,width):
    padding = width-len(string)
    for i in range (0,padding):
        string += " "
    return string

if (graphics):
    import pygtk
    pygtk.require('2.0')
    import gtk
    import pango
    if (__name__ == "__main__"):
        main = MainWindow()
        main.main()
else:
    print system_summary(),
    packages = scan_system()
    if (len(packages) == 0):
        print no_nonfree()
    else:
        print add_spaces(package_titles[0],50)+add_spaces(package_titles[1],15)+add_spaces(package_titles[2],15)
        for i in packages:
            print add_spaces(i[0],50)+add_spaces(i[1],15)+add_spaces(i[2],15)
    print ""

