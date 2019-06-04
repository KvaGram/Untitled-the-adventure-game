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
import Game

import room_apartment 
import middlering
import Bathrooms
#import outer
#import inner
#import WheelC as wheel

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

def start():
    global tkRoot, running
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1600x900")

    game = Game.Game(tkRoot, VERSION, "english")
    running = True
    while running:
        titleMenu(game)

def game_loop(game:Game.Game):
    world = {
        "apartment" : room_apartment.main,
        #"core"      : wheel.core,
        #"inner"     : inner.main,
        "middle"    : middlering.main,
        #"outer"     : outer.main,
        #"ladder"    : wheel.emergencyLadder,
        #"bathrooms" : middlering.bathrooms,
        #"cargobay"  : wheel.Cargobay
    }

    while True:
        placeReq = game.place
        if(placeReq == None): #newgame location
            placeReq = "apartment"
        #space to check for special conditions
        game_over = game.getGameover()
        if(game_over):
            game.showtext("""
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\\_GAME_OVER_/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
{0}
_________________________________________________
            """.format(game_over))
            break
        #general rule
        place = None
        try:
            place = world[placeReq]
        except:
            place = None
        if(place):
            place(game)
            game_over = game.getGameover()
        else:
            game.showtext("""
|---------------------- !!! ----------------------|
|    Sorry, something went wrong.                 |
|    The game could not find {0}                  |
|    The game will now end.                       |
|    Do you wish to save the game first?          |
|---------------------- !!! ----------------------|
            """.format(placeReq))
            if(game.yesno("Save game?")):
                game.savegame()
            break
    #end game loop
#end game loop function
    
def titleMenu(game:Game.Game):
    navdata = game.Navdata
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
        r = data[0] #button press from user
        if r == "EXIT":
            game.quit()
            return
        if r == "ABOUT":
            game.runGeneral("credits")
            return
        if r == "LOADGAME":
            if game.loadgame():
                game_loop(game)
            return
        if r == "NEWGAME":
            game.newgame()
            game_loop(game)
            return


#old code:
"""
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

"""

if __name__ == "__main__":
    start()