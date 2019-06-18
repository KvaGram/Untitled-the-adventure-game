import os
import time
import random
import json
import types

#from tkinter import *
import tkinter as TK
from tkinter import messagebox as TKmsg

import ui
import Game
import Storyloader

import room_apartment 
import middlering
import Bathrooms
import Ladder
import Core
import Cafeteria
#import outer
#import inner

#version number. Major, minor, hotfix.
VERSION = [1, 0, 0]
#if dev is on, some debug info may be displayed in the game
DEV = True

def start():
    global tkRoot, running
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1600x900")

    game = Game.Game(tkRoot, VERSION, "english")
    running = True
    while running:
        try:
            titleMenu(game)
        except (SystemExit):
            running = False

            

def game_loop(game:Game.Game):
    world = {
        "apartment" : room_apartment.main,
        #"core"      : Core.Core,
        #"inner"     : inner.main,
        "middle"    : middlering.main,
        #"outer"     : outer.main,
        "ladder"    : Ladder.Main,
        "bathrooms" : Bathrooms.main,
        #"cargobay"  : Core.Cargobay
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
    
    menu = [
    ["NEWGAME", "{TITLE_STARTNEW}"],
    ["LOADGAME", "{TITLE_LOADASAVE}"],
    ["ABOUT", "{TITLE_RUNCREDITS}"],
    ["EXIT", "{TITLE_EXITGAME}"],
    ]

    game.rolltext(titleroll, rollwtime)
    while True:
        game.choose(menu, "{TITLE_WELCOME}", False)
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

if __name__ == "__main__":
    start()