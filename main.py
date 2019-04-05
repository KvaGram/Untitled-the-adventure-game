import os
import time
import random
import json

#from tkinter import *
import tkinter as TK
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

import game_utilities as game

import room_apartment 
import middlering
import outer
import inner
import about
import WheelC as wheel

#version number. Major, minor, hotfix.
VERSION = [0, 5, 8]


def build_world():
    world = {}
    world['apartment'] = room_apartment.main
    world['about'] = about.main
    world["core"] = wheel.core #TODO: add proper module for core 
    world["inner"] = inner.main
    world["middle"] = middlering.main
    world["outer"] = outer.main
    world["ladder"] = wheel.emergencyLadder #TODO: move ladder to seperate module
    world["bathrooms"] = middlering.bathrooms #TODO: move bathrooms to its own module, and update this list.
    world["cargobay"] = wheel.Cargobay #TODO: move to a proper module

    return world
def start():
    world = build_world() # areas the player may visit.
    save = savadata(VERSION)

    def game_loop():
        while True:
            roomReq = save.getdata("room")
            if(roomReq == None): #newgame location
                roomReq = "apartment"
            #space to check for special conditions
            game_over = save.getdata("GAME OVER")
            if(game_over):
                game.showtext("""
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\\_GAME_OVER_/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
{0}
_________________________________________________
                """.format(game_over))
                break
            #general rule
            room = None
            try:
                room = world[roomReq]
            except:
                room = None
            if(room):
                room(save)
                game_over = save.getdata("GAME OVER")
            else:
                game.showtext("""
|---------------------- !!! ----------------------|
|    Sorry, something went wrong.                 |
|    The game could not find {0}                  |
|    The game will now end.                       |
|    Do you wish to save the game first?          |
|---------------------- !!! ----------------------|
                """.format(roomReq))
                if(game.yesno("Save game?")):
                    save.savegame()
                break
            if not game_over:
                if(game.yesno("Would you like to save the game?")):
                    save.savegame()
        #end game loop
    #end game loop function

    game.showtext("Welcome to")
    f = open("title.txt", 'r', encoding="utf-8")
    titlecard = f.read()
    game.rolltext(titlecard, 0.05)
    f.close()
    time.sleep(1)
    game.showtext()
    while(True):
        game.showtext("Untitled! The adventure game")
        game.showtext("MAIN MENU")
        choices = ["New Game", "Load Game", "About", "End game"]
        choice = game.choose(choices)
        if(choice == 0):
            game_loop()
            continue
        if(choice == 1):
            save.loadgame()
            game_loop()
            continue
        if(choice == 2):
            world['about'](save)#starts credits roll
            continue
        if(choice == 3):
            return
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
        game.showtext("WARNING, save and load is not fully tested yet. ")
        #dialouge = TK.Tk()
        path = TK.filedialog.asksaveasfilename(initialdir = "/", title = "Save game", filetypes = (("Untitled adventuregame savegame", "*.uagsave"),("all files", "*.*")))
        #dialouge.destroy()
        saveOK = True
        if path == "":
            saveOK = False
        elif os.path.isfile(path):
            messagebox.askokcancel("Untitled adventure game","Override existing savefile?")
            saveOK = False
        if ".uagsave" not in path:
            path = path + ".uagsave"

        if saveOK:
            self.setdata("version", self.version)
            f = open (path, "w+")
            json.dump(self.data, f)#, True, True, True, True, None, (', ', ': '), "UTF-8", False)
            f.close()
        elif game.yesno("The game was not saved. Try again?"):
            return self.savegame()
    def loadgame(self):
        game.showtext("WARNING, save and load is not fully tested yet. ")
        path = TK.filedialog.askopenfilename(initialdir = "/", title = "Save game", filetypes = (("Untitled adventuregame savegame", "*.uagsave"),("all files", "*.*")))
        if path == "" or not os.path.isfile(path):
            if game.yesno("The game was not loaded. Try again?"):
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
                game.showtext("Warning: This save was made with a newer version of the game. This may cause problems.")
            else:
                game.showtext("Warning: This save was made with a older version of the game. This should be fine, but could cause issues.")
        elif major > 0:
            game.showtext("WARNING! This save is FROM THE FUTURE! You should run a newer version of the game instead.")
        else:
            game.showtext("WARNING! The save is OLD! The game may not run correctly with this savefile.")
        
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
    #sets the room save data.
    #example use
    # return save.goto("middleA")
    #return statment may be seperate as goto does not return value
    #but it is symbolic as you usually use this to move from a room (module
    def goto(self, room):
        if(room == None):
            return
        self.setdata("prevroom", self.getdata('room'))
        self.setdata("room", room)
        self.setNav(None) #Cleans roomnav
    def versionText(self):
        return "v{0}.{1}.{2}".format(self.version[0], self.version[1], self.version[2])
if __name__ == "__main__":
    start()