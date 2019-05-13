import os
import time
import random
import json
import types

#from tkinter import *
import tkinter as TK

import game_utilities as G
import ui

import room_apartment 
import middlering
import outer
import inner
import WheelC as wheel

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
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1280x720")

    UI:ui.UntitledUI = ui.UntitledUI(tkRoot, handleNav = handleNav, handleAction = handleAction)

    testoptions = (
        ("op1", "option One"),
        ("op2", "option Two"),
        ("op3", "option Three"),
        ("op4", "option Four"),
        ("op5", "option Five"),
        ("op6", "option Six"),
        ("op7", "option Seven"),
        ("op8", "option Eight"),
        ("op9", "option Nine"),
        ("op10", "option Ten"),
    )
    UI.conf_navkeys(left = False)
    UI.draw_actions(actions = testoptions, label = "These are the test options")


    #TODO: remove the handle action and handle nav. re-write: save data to class instead. The UI loop can fetch it!
    while True:
        tkRoot.update_idletasks()
        tkRoot.update()
    

    tkRoot.mainloop()
def handleAction(data):
    print("Action was made " + str(data))
def handleNav(data):
    if data == "45":
        print("You tried to walk 45 degrees in a text-based adventure game with node-based navigation.\nYou tripped, fell and landed on your face!! Your bloodied nose giving you a lesson.\nYou learned not to make unreasonaly weird demands to the developer.")
    print("Movement was made " + str(data))



"""
    process = test()
    for req in process:
        print ("Yielded: " + str(req))
        inn = input()
        print("user entered " + inn)
"""
def oldGame():
    def build_world():
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

        return world
    def _start():
        world = build_world() # areas the player may visit.
        save = savadata(VERSION)

        def game_loop():
            while True:
                roomReq = save.getdata("room")
                if(roomReq == None): #newgame location
                    roomReq = "apartment"
                #space to check for special conditions
                game_over = G.getGameover(save)
                if(game_over):
                    G.showtext("""
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
                    game_over = G.getGameover(save)
                else:
                    G.showtext("""
    |---------------------- !!! ----------------------|
    |    Sorry, something went wrong.                 |
    |    The game could not find {0}                  |
    |    The game will now end.                       |
    |    Do you wish to save the game first?          |
    |---------------------- !!! ----------------------|
                    """.format(roomReq))
                    if(G.yesno("Save game?")):
                        save.savegame()
                    break
                if not game_over:
                    if(G.yesno("Open game menu?")):
                        G.gameMenu(save)
            #end game loop
        #end game loop function

        G.showtext("Welcome to")
        f = open("title.txt", 'r', encoding="utf-8")
        titlecard = f.read()
        G.rolltext(titlecard, 0.05)
        f.close()
        time.sleep(1)
        G.showtext()
        while(True):
            G.showtext("Untitled! The adventure game")
            G.showtext("MAIN MENU")
            choices = ["New Game", "Load Game", "About", "End game"]
            choice = G.choose(choices)
            if(choice == 0):
                save = savadata(VERSION)
                try:
                    game_loop()
                except SystemExit as _:
                    return
                continue
            if(choice == 1):
                save.loadgame()
                try:
                    game_loop()
                except SystemExit as _:
                    return
                continue
            if(choice == 2):
                G.RunGeneral(save,"about")#starts credits roll
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
                G.showtext("Warning: This save was made with a newer version of the game. This may cause problems.")
            else:
                G.showtext("Warning: This save was made with a older version of the game. This should be fine, but could cause issues.")
        elif major > 0:
            G.showtext("WARNING! This save is FROM THE FUTURE! You should run a newer version of the game instead.")
        else:
            G.showtext("WARNING! The save is OLD! The game may not run correctly with this savefile.")
        
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

#TODO: when removing old code, move this further up in file.

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