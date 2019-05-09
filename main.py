import os
import time
import random
import json

#from tkinter import *
import tkinter as TK
from tkinter import font as TKF

import game_utilities as G

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
    #def onBbtn():
    #    print ("The black button")

    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1280x720")
    tkRoot.grid_columnconfigure(0, weight=1)
    tkRoot.grid_rowconfigure(0, weight=1)


    #mainscreen = TK.Frame(tkRoot)
    #sidebar = TK.Frame(tkRoot)

    #mainscreen.grid(columnspan=3)
    #sidebar.grid()

    main_display = TK.Frame(master=tkRoot, background ="#00c4ff")
    main_actions = TK.Frame(master=tkRoot, background ="#2200ff")
    side_inventory = TK.Frame(master=tkRoot, background ="#209d00")
    side_navtext = TK.Frame(master=tkRoot, background ="#ff8f00")
    side_navkeys = TK.Frame(master=tkRoot, background ="#ff0000")

    main_display.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")
    main_actions.grid(row=2, column=0, columnspan=2, rowspan=1, sticky="nsew")
    side_inventory.grid(row=0, column=3, columnspan=1, rowspan=1, sticky="nsew")
    side_navtext.grid(row=1, column=3, columnspan=1, rowspan=1, sticky="nsew")
    side_navkeys.grid(row=2, column=3, columnspan=1, rowspan=1, sticky="nsew")

    main_display_text = TK.Label(master = main_display, text = "main_display", background ="#00c4ff")
    #main_actions_text = TK.Label(master = main_actions, text = "main_actions", background ="#2200ff")
    side_inventory_text = TK.Label(master = side_inventory, text = "side_inventory", background ="#209d00")
    side_navtext_text = TK.Label(master = side_navtext, text = "side_navtext", background ="#ff8f00")
    #side_navkeys_text = TK.Label(master = side_navkeys, text = "side_navkeys", background ="#ff0000")

    testactions = (("TEST", "-test-"),)*16
    ui_build_actions(main_actions, "actions")#, actions = testactions, page = 1)
    #ui_build_actions(main_actions, "text")
    ui_build_navkeys(side_navkeys)

    main_display_text.pack()
    #main_actions_text.pack()
    side_inventory_text.pack()
    side_navtext_text.pack()
    #side_navkeys_text.pack()

    tkRoot.mainloop()
def ui_build_navkeys(master, **args):
    text_left  = args.get("left",  u"\u2190")
    text_up    = args.get("up",    u"\u2191")
    text_right = args.get("right", u"\u2192")
    text_down  = args.get("down",  u"\u2193")
    font       = args.get("font", TKF.Font(family = "Consolas", size=30))
    
    btn_left  = TK.Button(master = master, font=font, text = text_left,  command= lambda: onDirPress("left"))
    btn_up    = TK.Button(master = master, font=font, text = text_up,    command= lambda: onDirPress("up"))
    btn_right = TK.Button(master = master, font=font, text = text_right, command= lambda: onDirPress("right"))
    btn_down  = TK.Button(master = master, font=font, text = text_down,  command= lambda: onDirPress("down"))

    btn_left.grid(row=1, column=0, sticky="nsew")
    btn_up.grid(row=0, column=1, sticky="nsew")
    btn_right.grid(row=1, column=2, sticky="nsew")
    btn_down.grid(row=2, column=1, sticky="nsew")
def onDirPress(dir):
    print("TEST direction, going: " + dir)
def ui_build_actions(master, mode:str, **args):
    master.grid_rowconfigure(0, weight = 1)
    if mode == "text":
        reqFields = args.get("fields", (("Input", ""),))
        fieldfont = args.get("fieldfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        labelfont = args.get("labelfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        entertext = args.get("entertext", "ENTER")
        enterfont = args.get("enterfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        labels = []
        inpFields = []
        length = len(reqFields)
        for i in range(length):
            labels.append(TK.Label(master=master, text=reqFields[i][0], font=labelfont))
            inpFields.append(TK.Entry(master=master, font=fieldfont))
            inpFields[i].insert(0, reqFields[i][1])
            labels[i].grid(row = i, column = 0, sticky="new")
            inpFields[i].grid(row = i, column = 1, columnspan=1, sticky="new")
        master.grid_columnconfigure(0, weight = 1)
        master.grid_columnconfigure(1, weight = 5)
        def packnsend():
            ret = []
            for i in range(length):
                ret.append((labels[i]["text"], inpFields[i].get()))
            onActionPress(ret)
        btnEnter = TK.Button(master=master, text=entertext, font=enterfont, command=packnsend)
        btnEnter.grid(row=length, column=0, columnspan=3, sticky="nsew")
    elif mode == "actions":
        master.grid_columnconfigure(0, weight = 0)
        master.grid_columnconfigure(1, weight = 1)
        master.grid_columnconfigure(2, weight = 0)
        reqActions:tuple = args.get("actions", (("YES", u"\u2713"), ("NO", u"\u2573")))
        reqLabel:str = args.get("label", "Choose")
        page:int = args.get("page", 0)

        buttonfont:TKF.Font = args.get("buttonfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        labelfont:TKF.Font = args.get("labelfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12

        length:int = len(reqActions)
        actionsFrame:TK.Frame = TK.Frame(master=master)
        actionsFrame.grid(row = 0, column = 1, sticky="nsew")

        #actionsFrame.grid_rowconfigure(0, weight = 1)

        btnLeft:TK.Button  = TK.Button(master=master, text = u"\u2190")
        btnRight:TK.Button = TK.Button(master=master, text = u"\u2192")
        if page > 0:
            btnLeft.grid(row = 0, column = 0, sticky="nsw")
        if ( (1+page) * 6 ) < length:
            btnRight.grid(row = 0, column = 2, sticky="nse")
        
        #this slices the requested actions tuple in respect to the current page.
        #This off course have no practical effect in small (size 6 and under) request groups.
        activeActions:list = reqActions[page*6:(page+1)*6]
        actLength:int = len(activeActions)
        
        actionBtns:list = []
        label:TK.Label = TK.Label(master = actionsFrame, text = reqLabel)
        for i in range(actLength):
            actionBtns.append(TK.Button(master=actionsFrame, font=buttonfont, text = activeActions[i][1], command = lambda _i=i: onActionPress((activeActions[_i][0], _i + page*6))))
        if actLength < 4:
            actionsFrame.grid_columnconfigure(0, weight = 1) #<-- TESTME
            label.grid(row = 0, sticky="nsew")
            for i in range(actLength):
                actionBtns[i].grid(row = i + 1, sticky="nsew") 
                actionsFrame.grid_rowconfigure(i, weight = 5)#<--TESTME
        else:
            label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
            for i in range(actLength):
                row = int(i / 2) + 1
                column = i % 2
                actionBtns[i].grid(row=row, column=column, sticky="nsew")
                actionsFrame.grid_rowconfigure(row, weight = 1)#<--TESTME
                actionsFrame.grid_columnconfigure(column, weight=1) #<-- TESTME
        #TODO: add testcase and support for changing action page
def onActionPress(result):
    print("TEST: The input was: " + str(result))





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