import os
import time
import random
import json
import types

#from tkinter import *
import tkinter as TK
from tkinter import messagebox as TKmsg

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

def onExit():
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

    UI:ui.UntitledUI = ui.UntitledUI(tkRoot)
    #UI.conf_navkeys(left = False)
    #UI.draw_actions(actions = testoptions, label = "These are the test options")
    tkRoot.update_idletasks()
    tkRoot.update()

    save = savadata(VERSION)

    #TODO: remove the handle action and handle nav. re-write: save data to class instead. The UI loop can fetch it!
    event = titleMenu()
    waiting = False
    running = True
    resp:G.response = None
    req:G.request = None
    nextEvent:callable = None

    while running:
        
        tkRoot.update_idletasks()
        tkRoot.update()
        newRes = UI.deqeue()
        if newRes:
            if newRes.pressed == "game":
                pass #TODO: handle game menu
            else:
                resp.copyfrom(newRes)
                waiting = False
        if waiting:
            continue
        
        # run 'event' function to next yield statement.
        # expect a tuple of 2 elements, req and resp to be yielded.
        # if function ends (no new yield statement), set req to "END", and keep resp as it was.
        # req may be a G.request or a str (special case). resp may be a G.response or a Nonetype (special case)
        req, resp = next(event, ("END", resp))
        if req == "QUIT":
            tkRoot.destroy()
            running = False
            break
            

        if req == "END":
            if(type(nextEvent) == callable):
                event = nextEvent.__call__(save)
                nextEvent = None
                req, resp = next(event, ("END", resp))
            else:
                print("DEBUG: UNEXPECTED END OF EVENT FUNCTION!! - returning to title")
                save = savadata(VERSION)
                event = titleMenu()
                req, resp = next(event, ("END", resp))
        if req.rolltext:
            UI.write_linebyline_display(req.rolltext, req.rollwtime)
        elif req.showtext:
            UI.write_all_display(req.showtext)
        if req.actions:
            waiting = True
            UI.draw_actions(actions = req.actions)
            pass #TODO: handle actions request
        elif req.textin:
            pass #TODO: handle text in request
            waiting = True
        else:
            pass #TODO: handle no action request
        if req.navdata:
            pass #TODO: handle navdata
            if req.navdata.canmove():
                waiting = True
        else:
            pass #TODO: handle missing navdata (should never happen, but just in case)
        if req.invrefresh:
            pass #TODO: handle refresh inventory UI
        if req.next:
            n = req.next
            if type(n) == str:
                n = world.get(n, None)
                if n == None:
                    print("DEBUG: Err - could not find " + req.next)
            nextEvent = n
    





def titleMenu():
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

#TODO finish testing this stuff

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