#!/usr/bin/python

import os
import platform
import sys
import commands
import types
import xml.etree.ElementTree as ET

class Freedometer:
    def __init__(self, gui=False):
        self.gui = gui
        self.lang = "en"
        self.itree = ET.parse("interface.xml") 
    
    def list_packages(self):
        if (self.pacman == "dpkg"):
            return commands.getoutput("dpkg -l |awk '/^[hi]i/{print $2}'")
    
    def caps(self, stringy):
        return stringy[0:1].upper() + stringy[1:].lower()

    def system_summary(self):
        global system
        global distro
        global winversion
        system = platform.system()
        sumtree = self.itree.find("summary")
        errtree = self.itree.find("errors")
        summary = self.getlang(sumtree.findall("osnametext"))
        if (system == "Linux"):
            for i in sumtree.findall("os"):
                if i.attrib["name"] == "gnulinux":
                    ostree = i
                    break
            summary += "GNU/Linux"+" - "
            dist = platform.dist()
            if (dist[0] == "debian"):
                name = commands.getoutput("lsb_release -cis").partition('\n')
                distro = name[0]
                summary += name[0]+" "+name[2]+"\n\n"
                self.pacman = "dpkg"
            else:
                if ("SuSE" in dist[0]):
                    distro = "suse"
                summary += dist[0]+" "+self.caps(dist[1])+"\n\n"
                self.pacman = "none"
            summary += self.getlang(ostree.findall("summary"))+"\n\n"
            for i in ostree.findall("distro"):
                if (i.attrib["name"] == distro.lower()):
                    summary += self.getlang(i.findall("summary"))+"\n\n"
                    break
            if (self.pacman == "none"):
                summary += self.getlang(errtree.findall("noscan"))
            else:
                if (self.gui):
                    summary += self.getlang(ostree.findall("scantext"))
        elif (os.name == "posix"):
            summary += getlang(errtree.findall("othunix"))
        elif (system == "Windows"):
            for i in sumtree.findall("os"):
                if i.attrib["name"] == "windows":
                    ostree = i
                    break
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
            summary += self.getlang(ostree.findall("summary"))+"\n\n"
            if (self.gui):
                summary += self.getlang(ostree.findall("scantext"))
        return summary

    def item_to_array(self, k):
        if (k.tagName == "name" and k.attributes.getNamedItem("lang").value == "en"):
            self.info[0] = k.childNodes[0].data
        if (k.tagName == "reason"):
            self.info[1] = k.childNodes[0].data
        if (k.tagName == "notes" and k.attributes.getNamedItem("lang").value == "en"):
            self.info[3] = k.childNodes[0].data

    def getlang(self, arr):
        for i in arr:
            if i.attrib["lang"] == self.lang:
                return i.text

    def parse_list(self, pkglist):
        pkginfo = []
        pkgnames = pkglist.split()
        pltree = ET.parse("packagelist.xml") 
        plroot = pltree.getroot()
        for i in plroot:
            for j in i.findall("packagename"):
                if (j.attrib["pacman"] == self.pacman and j.text in pkgnames):
                    alt = ""; reason = ""
                    if i.find("alternative").__class__ != types.NoneType:
                        alt = self.getlang(i.find("alternative").findall("name"))
                    if i.find("reason").__class__ != types.NoneType:
                        reason = i.find("reason").text
                    pkginfo.append([self.getlang(i.findall("name")), reason, alt, self.getlang(i.findall("notes"))])
                    break
        return pkginfo

    def scan_system(self):
        global system
        if (system == "Linux"):
            pkgs = self.parse_list(self.list_packages())
            return pkgs

    def no_nonfree(self):
        return "You appear to have no non-free packages on your system. However, you may have added non-free software yourself, not using the package manager."

    def get_package_fieldnames(self):
        return [ "Package name", "Reason", "Alternative", "Notes" ]

if (__name__ == "__main__"):
    free = Freedometer()
    print free.system_summary()
    print free.scan_system()

