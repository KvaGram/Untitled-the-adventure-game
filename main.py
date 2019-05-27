import os
import time
import random
import json
import types

#from tkinter import *
import tkinter as TK
from tkinter import messagebox as TKmsg

#import game_utilities as G
import ui

import room_apartment 
import middlering
import outer
import inner
import WheelC as wheel

import Game

#version number. Major, minor, hotfix.
VERSION = [1, 0, 0]
#if dev is on, some debug info may be displayed in the game
DEV = True

def test():
    print ("Hello world. This is printed in test()")
    yield "This is however not."
    print ("Even more that is not")
    print ("next line will be yielded")
    yield "Is everything neat and in order, I wonder?"
    print("The end is here!")
    return

def onExit():
    global running
    s = TKmsg._show("UNTITLED! The adventure game", "Would you like to save before you quit?", TKmsg.WARNING, TKmsg.YESNOCANCEL)
    if(s == None):
        return
    if(s == True):
        print("DEBUG: Save not yet implemented in this build")
    tkRoot.destroy()
    running = False

def start():
    global tkRoot, running
    build_world()
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1600x900")
    tkRoot.protocol("WM_DELETE_WINDOW", onExit)

    game = Game.Game(tkRoot, VERSION, "english")
    while running:
        titleMenu(game)
    
def titleMenu(game:Game.Game):
    navdata = game.navdata
    navdata.navtext = """TITLE MENU
    WELCOME TO
    UNTITLED!
    the adventure game"""
    navdata.closed = True
    titleroll = "WELCOME TO\n\n"
    f = open("title.txt", 'r', encoding="utf-8")
    titleroll += f.read()
    f.close()
    rollwtime = 0.05
    
    menu = (
    ("NEWGAME", "Start new game"),
    ("LOADGAME", "Load a save"),
    ("ABOUT", "Run credits"),
    ("EXIT", "Exit Game"),
    )

    game.rolltext(titleroll, rollwtime)
    while True:
        game.choose(menu, "Welcome! What do you wish to do?", False)
        etype, data = game.wait()
        if etype != "action":
            continue
        r = data[1] #button press from user
        if r == "EXIT":
            return
        if r == "ABOUT":
            #TODO: run credits
            return
        if r == "LOADGAME":
            #TODO: load game and resule
            return
        if r == "NEWGAME":
            #TODO: start new game
            return





def _titleMenu():
    req = G.request()
    req.rolltext = "WELCOME TO\n\n"
    f = open("title.txt", 'r', encoding="utf-8")
    req.rolltext += f.read()
    f.close()
    req.rollwtime = 0.05
    navtext = """TITLE MENU
    WELCOME TO
    UNTITLED!
    the adventure game
    """
    nav = G.navdata(navtext = navtext, closed = True)
    menu = (
    ("NEWGAME", "Start new game"),
    ("LOADGAME", "Load a save"),
    ("ABOUT", "Run credits"),
    ("EXIT", "Exit Game"),
    )
    req.navdata = nav
    req.actions = menu
    res = G.response()
    while True:
        yield(req, res)
        print("RESPONSE RECIVED! {0}, {1}".format(res.pressed, str(res.data)))
        if res.pressed == "action":
            r = res.data[0]
            if r == "EXIT":
                yield("QUIT", None)
                return
            if r == "ABOUT":
                yield(G.request(next = "CREDITS", nav = nav))
                return
            if r == "LOADGAME":
                yield("LOADGAME", None)
                return
            if r == "NEWGAME":
                yield(G.request(next = "APARTMENT", nav = nav))
                return

def handleAction(data):
    print("Action was made " + str(data))
def handleNav(data):
    if data == "45":
        print("You tried to walk 45 degrees in a text-based adventure game with node-based navigation.\nYou tripped, fell and landed on your face!! Your bloodied nose giving you a lesson.\nYou learned not to make unreasonaly weird demands to the developer.")
    print("Movement was made " + str(data))

def build_world():
    global world
    world = {}
    world['apartment'] = room_apartment.main
    #world['about'] = about.main #moved to G.RunGeneral("about")
    world["core"] = wheel.core #TODO: add proper module for core 
    world["inner"] = inner.main
    world["middle"] = middlering.main
    world["outer"] = outer.main
    world["ladder"] = wheel.emergencyLadder #TODO: move ladder to seperate module
    world["bathrooms"] = middlering.bathrooms #TODO: move bathrooms to its own module, and update this list.
    world["cargobay"] = wheel.Cargobay #TODO: move to a proper module


class savadata:
    # data contains all save data, including choices and the player's location
    data = {}
    # version is saved as an array of 3 numbers to easly warn of potential version conflicts
    version = []
    def __init__(self, version):
        self.data = {}
        self.version = version
    def getdata(self, name, default = None):
        try:
            return self.data[name]
        except:
            self.setdata(name, default)
            return default
    def setdata(self, name, value):
        self.data[name] = value
    def savegame(self):
        G.showtext("WARNING, save and load is not fully tested yet. ")
        #dialouge = TK.Tk()
        path = TK.filedialog.asksaveasfilename(initialdir = "/", title = "Save game", filetypes = (("Untitled adventuregame savegame", "*.uagsave"),("all files", "*.*")))
        #dialouge.destroy()
        saveOK = True
        if path == "":
            saveOK = False
        elif os.path.isfile(path):
            TK.messagebox.askokcancel("Untitled adventure game","Override existing savefile?")
            saveOK = False
        if ".uagsave" not in path:
            path = path + ".uagsave"

        if saveOK:
            self.setdata("version", self.version)
            f = open (path, "w+")
            json.dump(self.data, f)#, True, True, True, True, None, (', ', ': '), "UTF-8", False)
            f.close()
        elif G.yesno("The game was not saved. Try again?"):
            return self.savegame()
    def loadgame(self):
        G.showtext("WARNING, save and load is not fully tested yet. ")
        path = TK.filedialog.askopenfilename(initialdir = "/", title = "Save game", filetypes = (("Untitled adventuregame savegame", "*.uagsave"),("all files", "*.*")))
        if path == "" or not os.path.isfile(path):
            if G.yesno("The game was not loaded. Try again?"):
                return self.loadgame()
            else:
                return False
        f = open(path, "r")
        ldata = json.load(f)
        lversion = ldata["version"]
        #comparing version
        major  = lversion[0] - self.version[0]
        minor  = lversion[1] - self.version[1]
        #hotfix = lversion[2] - self.version[2]
        if major == 0:
            if minor == 0:
                #not worth comparing a hotfix
                pass
            elif minor > 0:
                TKmsg.showinfo("UNTITLED! The adventure game","This save was made with a newer version of the game. This may cause problems.")
            else:
                TKmsg.showinfo("UNTITLED! The adventure game","This save was made with a older version of the game. This should be fine, but could cause issues.")
        elif major > 0:
            TKmsg.showwarning("UNTITLED! The adventure game","This save is FROM THE FUTURE! You should run a newer version of the game instead.")
        else:
            TKmsg.showwarning("UNTITLED! The adventure game","The save is OLD! The game may not run correctly with this savefile.")
        
        self.data = ldata
        return True

    def setNav(self, nav):
        self.setdata("roomnav", nav)
    def getNav(self, request = None):
        nav = self.getdata("roomnav", None)
        if nav == None or request == None:
            return nav
        if nav.roomname == request:
            return nav
        return None

    def setInventory(self, key:str, value, display:str):
        inv = self.getdata("inventory", {})
        inv[key] = (value, display)
        self.setdata("inventory", inv)
    def getInventory(self, item:str):
        inv = self.getdata("inventory", {})
        return inv.get(item, (None, "NO ITEM"))
    def getAllInventory(self):
        return self.getdata("inventory", {})
    

    def getplace(self) -> (str, str):
        return (self.getdata('place'), self.getdata('prevplace'))
    #sets place data. Used for context in events.
    def setplace(self, place):
        if(place == None):
            return
        self.setdata("prevplace", self.getdata('place'))
        self.setdata("place", place)
    

def versionText(self):
    return "v{0}.{1}.{2}".format(self.version[0], self.version[1], self.version[2])

#TODO: finish testing this

import xml.etree.ElementTree as ET
datafiles = {}

def get(reqFile, reqPart, reqlang, reqSubPart):
    _fallbacklang = "eng"
    if not (reqFile in datafiles):
        try:
            datafiles[reqFile] = ET.parse("/nerrative/" + reqFile + ".xml")
        except:
            print("ERROR LOADING DATA!")
            #todo: add dummy data containing 'ERROR'
            if(DEV):
                return ("ERROR LOADING DATA! Please check requested data exist in the datafile\n\treqFile={0}, reqPart={1}, reqlang={2}, reqSubPart={3}".format(reqFile, reqPart, reqlang, reqSubPart),[])
            else:
                return ("ERROR!", [])
        pass
    reqstring = "./content[@name={0}]/part[@name={1}".format(reqPart, reqSubPart)
    _tree = datafiles[reqFile]
    _part = _tree.find(reqstring)
    text = _part.find("text").text
    variables = []
    for var in _part.findall("var"):
        variables.append(var.text)
    return (text, variables)

if __name__ == "__main__":
    start()