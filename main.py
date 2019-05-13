import os
import time
import random
import json

#from tkinter import *
import tkinter as TK
from tkinter import font as TKF
from tkinter import scrolledtext as TKS

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
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1280x720")

    UI:UntitledUI = UntitledUI(tkRoot, handleNav = handleNav, handleAction = handleAction)

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

    tkRoot.mainloop()
def handleAction(data):
    print("Action was made " + str(data))
def handleNav(data):
    if data == "45":
        print("You tried to walk 45 degrees in a text-based adventure game with node-based navigation.\nYou tripped, fell and landed on your face!! Your bloodied nose giving you a lesson.\nYou learned not to make unreasonaly weird demands to the developer.")
    print("Movement was made " + str(data))

class UntitledUI:
    def __init__(self, root:TK.Tk, **args):
        self.main = TK.Frame(root)
        self.main.pack(fill = TK.BOTH, expand = 1)

        self.handleAction:callable = args.get("handleAction", self.handleAction_dummy)
        self.handleNav:callable = args.get("handleNav", self.handleNav_dummy)

        self.display = TK.Frame(master=self.main, background ="#00c4ff")
        self.actions = TK.Frame(master=self.main, background ="#2200ff")
        self.inventory = TK.Frame(master=self.main, background ="#209d00")
        self.navtext = TK.Frame(master=self.main, background ="#ff8f00")
        self.navkeys = TK.Frame(master=self.main, background ="#ff0000")

        self.display.grid(row=0, column=0, columnspan=1, rowspan=2, sticky="nsew")
        self.actions.grid(row=2, column=0, columnspan=1, rowspan=1, sticky="nsew")
        self.inventory.grid(row=0, column=1, columnspan=1, rowspan=1, sticky="nsew")
        self.navtext.grid(row=1, column=1, columnspan=1, rowspan=1, sticky="nsew")
        self.navkeys.grid(row=2, column=1, columnspan=1, rowspan=1, sticky="nsew")

        self.draw_display()
        self.draw_actions()
        #self.draw_textinputs()
        self.draw_inventory()
        self.draw_navtext()
        self.draw_navkeys()

        self.main.grid_columnconfigure(0, weight=10)
        self.main.grid_columnconfigure(1, weight=1)
        self.main.grid_rowconfigure(0, weight=10)
        self.main.grid_rowconfigure(1, weight=4)
        self.main.grid_rowconfigure(2, weight=5)
    @staticmethod
    def emptyframe(frame:TK.Frame):
        for c in frame.winfo_children():
            c.grid_forget()
            c.pack_forget()
            c.destroy()
    def handleAction_dummy(self, data):
        print("TEST: The action input was: " + str(data))
    def handleNav_dummy(self, data):
        print("TEST: The direction input was: " + str(data))


    def draw_display(self, **args):
        self.emptyframe(self.display)
        #TODO: build display
        self.dispText = TKS.ScrolledText(master = self.display, state = TK.NORMAL)
        self.dispText.pack(fill=TK.BOTH)
        self.dispText.insert(TK.END, "This is a\nloooooooong test\nof this scrollable text\nwidget.\nwell, long by standards of a codeline\nby GUI, this is quite short")
        self.dispText.config(state = TK.DISABLED)

    def write_all_display(self, text:str):
        self.dispText.config(state = TK.NORMAL)
        self.dispText.insert(TK.END, "\n" + text)
        self.dispText.config(state = TK.DISABLED)
    def write_linebyline_display(self, text, wtime:float = 0.1):
        if type(text) == str:
            text = text.splitlines()
        self.dispText.config(state = TK.NORMAL)
        for t in text:
            self.dispText.insert(TK.END, "\n" + t)
            time.sleep(wtime)
        self.dispText.config(state = TK.DISABLED)
    
    def draw_actions(self, **args):
        
        self.emptyframe(self.actions)
        self.actions.grid_rowconfigure(0, weight = 1)

        self.action_page:int = args.get("page", 0)
        reqActions:tuple = args.get("actions", (("YES", u"\u2713"), ("NO", u"\u2573")))
        reqLabel:str = args.get("label", "Choose")
        buttonfont:TKF.Font = args.get("buttonfont", TKF.Font())
        labelfont:TKF.Font = args.get("labelfont", TKF.Font())

        actionsFrame:TK.Frame = TK.Frame(master=self.actions)
        actionsFrame.grid(row = 0, column = 1, sticky="nsew")

        def nextpage():
            self.action_page += 1
            draw_actionbuttons()
        def prevpage():
            self.action_page -= 1
            draw_actionbuttons()
        btnLeft:TK.Button  = TK.Button(master=self.actions, text = u"\u2190", command = prevpage)
        btnRight:TK.Button = TK.Button(master=self.actions, text = u"\u2192", command = nextpage)
        btnLeft.grid(row = 0, column = 0, sticky="nsw")
        btnRight.grid(row = 0, column = 2, sticky="nse")

        self.actions.grid_columnconfigure(0, weight = 0)
        self.actions.grid_columnconfigure(1, weight = 1)
        self.actions.grid_columnconfigure(2, weight = 0)
        fLength:int = len(reqActions) #full length of the requested actions list

        def draw_actionbuttons():
            
            #empties the the action button container and disables the page-buttons.
            btnLeft.config(state=TK.DISABLED)
            btnRight.config(state=TK.DISABLED)
            self.emptyframe(actionsFrame)

            #re-enables the page-buttons as appropriate
            if self.action_page > 0:
                btnLeft.config(state=TK.NORMAL)
            if ( (1+self.action_page) * 6 ) < fLength:
                btnRight.config(state=TK.NORMAL)
            
            #list of active actions (buttons to draw)
            #made by slicing the requested actions list, with respect to the current page.
            #only usefull for actions lists larger than 6.
            aActions:list = reqActions[self.action_page*6:(self.action_page+1)*6]
            aLength:int = len(aActions)

        
            actionBtns:list = []
            label:TK.Label = TK.Label(master = actionsFrame, text = reqLabel)
            for i in range(aLength):
                actionBtns.append(TK.Button(master=actionsFrame, font=buttonfont, text = aActions[i][1], command = lambda _i=i: self.handleAction((aActions[_i][0], _i + self.action_page*6))))
            if aLength < 4:
                actionsFrame.grid_columnconfigure(0, weight = 1)
                label.grid(row = 0, sticky="nsew")
                for i in range(aLength):
                    actionBtns[i].grid(row = i + 1, sticky="nsew") 
                    actionsFrame.grid_rowconfigure(i, weight = 5)
            else:
                label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
                for i in range(aLength):
                    row = int(i / 2) + 1
                    column = i % 2
                    actionBtns[i].grid(row=row, column=column, sticky="nsew")
                    actionsFrame.grid_rowconfigure(row, weight = 1)
                    actionsFrame.grid_columnconfigure(column, weight=1)
        draw_actionbuttons()

    def draw_textinputs(self, **args):
        self.emptyframe(self.actions)
        self.actions.grid_rowconfigure(0, weight = 1)
        reqFields = args.get("fields", (("Input", ""),))
        fieldfont = args.get("fieldfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        labelfont = args.get("labelfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        entertext = args.get("entertext", "ENTER")
        enterfont = args.get("enterfont", TKF.Font()) #NOTE: if required, use family="helvetica", size=12
        labels = []
        inpFields = []
        length = len(reqFields)
        for i in range(length):
            labels.append(TK.Label(master=self.actions, text=reqFields[i][0], font=labelfont))
            inpFields.append(TK.Entry(master=self.actions, font=fieldfont))
            inpFields[i].insert(0, reqFields[i][1])
            labels[i].grid(row = i, column = 0, sticky="new")
            inpFields[i].grid(row = i, column = 1, columnspan=1, sticky="new")
        self.actions.grid_columnconfigure(0, weight = 1)
        self.actions.grid_columnconfigure(1, weight = 5)
        def packnsend():
            ret = []
            for i in range(length):
                ret.append((labels[i]["text"], inpFields[i].get()))
            self.handleAction(ret)
        btnEnter = TK.Button(master=self.actions, text=entertext, font=enterfont, command=packnsend)
        btnEnter.grid(row=length, column=0, columnspan=3, sticky="nsew")

    def draw_inventory(self, **args):
        self.emptyframe(self.inventory)
        #TODO build inventory
        TK.Label(master=self.inventory, text = "PLACEHOLDER Inventory").pack()
    def draw_navtext(self, **args):
        self.emptyframe(self.navtext)
        #TODO build navtext
        self.navTextDisplay = TK.Text(master = self.navtext, width = 20, height = 24)
        self.navTextDisplay.pack(fill= TK.BOTH)
        self.navTextDisplay.insert(TK.END, "dummy area\ndummy place\ndoing dummy things...")
        self.navTextDisplay.config(state = TK.DISABLED)
    def set_navtext(self, text:str):
        self.navTextDisplay.config(state = TK.NORMAL)
        self.navTextDisplay.delete(1, TK.END)
        self.navTextDisplay.insert(TK.END, text)
        self.navTextDisplay.config(state = TK.DISABLED)
    def draw_navkeys(self, **args):
        self.emptyframe(self.navkeys)

        self.nav_left  = TK.Button(master = self.navkeys, command= lambda: self.handleNav("left"))
        self.nav_up    = TK.Button(master = self.navkeys, command= lambda: self.handleNav("up"))
        self.nav_45    = TK.Button(master = self.navkeys, command= lambda: self.handleNav("45"))
        self.nav_right = TK.Button(master = self.navkeys, command= lambda: self.handleNav("right"))
        self.nav_down  = TK.Button(master = self.navkeys, command= lambda: self.handleNav("down"))

        self.nav_45.grid(row=0, column=2, sticky="nsew")
        self.nav_left.grid(row=1, column=0, sticky="nsew")
        self.nav_up.grid(row=0, column=1, sticky="nsew")
        self.nav_right.grid(row=1, column=2, sticky="nsew")
        self.nav_down.grid(row=2, column=1, sticky="nsew")
        
        self.conf_navkeys(**args)
    def conf_navkeys(self, **args):
        state_left  = TK.NORMAL if args.get("left",  True) else TK.DISABLED
        state_up    = TK.NORMAL if args.get("up",    True) else TK.DISABLED
        state_right = TK.NORMAL if args.get("right", True) else TK.DISABLED
        state_down  = TK.NORMAL if args.get("down",  True) else TK.DISABLED

        text_left  = args.get("text_left",  u"\u2190")
        text_up    = args.get("text_up",    u"\u2191")
        text_right = args.get("text_right", u"\u2192")
        text_down  = args.get("text_down",  u"\u2193")
        font       = args.get("font", TKF.Font(family = "Consolas", size=30))

        self.nav_left  .config(font = font, text = text_left, state = state_left)
        self.nav_up    .config(font = font, text = text_up, state = state_up)
        self.nav_right .config(font = font, text = text_right, state = state_right)
        self.nav_down  .config(font = font, text = text_down, state = state_down)
        self.nav_45    .config(font = font, text = "45")

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