#!/usr/bin/python

import os
import platform
import sys
import commands
import types
import xml.etree.ElementTree as ET

class Freedometer:
    def __init__(self):
        self.lang = "en"
        itree = ET.parse("interface.xml") 
    
    def caps(self, stringy):
        return stringy[0:1].upper() + stringy[1:].lower()

    def system_summary(self):
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
                summary += distro+" "+self.caps(dist[1])+"\n\n"
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
                #if (graphics):
                summary += "Click the scan button below to scan for propreitary software that is installed on your system."
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
            #if (graphics):
            summary += "Click scan to find common pieces of free software, then our wizard will help you start using more.\n\n"
            summary += "We can also help you install a free software Operating System, such as Ubuntu.\n\n"
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
                if (j.attrib["distro"] == "debian" and j.text in pkgnames):
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
            global packaging
            if (packaging == "apt"):
                pkgs = self.parse_list(commands.getoutput("dpkg -l |awk '/^[hi]i/{print $2}'"))
                return pkgs

    def no_nonfree(self):
        return "You appear to have no non-free packages on your system. However, you may have added non-free software yourself, not using the package manager."

    def get_package_fieldnames(self):
        return [ "Package name", "Reason", "Alternative", "Notes" ]

if (__name__ == "__main__"):
    free = Freedometer()
    print free.parse_list(commands.getoutput("dpkg -l |awk '/^[hi]i/{print $2}'"))

