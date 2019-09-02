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
from general import ReturnToMain
from general import ReturnToTitle

import room_apartment 
import middlering
import Bathrooms
import Ladder
import Core
import Cafeteria
import outer
import inner

#version number. Major, minor, hotfix.
VERSION = [1, 0, 0]
#if dev is on, some debug info may be displayed in the game
DEV = True

def start():
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1600x900")

    game = Game.Game(tkRoot, VERSION, "english")
    while True:
        try:
            titleMenu(game)
        except (ReturnToTitle):
            continue
        except (SystemExit):
            break

            
def _testloop(game:Game, Testcall:callable, Datacall:callable, name:str):
    frags = {'_NAME':name}
    Datacall()
    game.rolltext("""
    -----------------------------------------------
    THIS IS A MODULE TEST FOR {_NAME}.
    FOR FULL PLAY, PLEASE RUN FROM main.py INSTEAD.
    -----------------------------------------------""",frags=frags)
    while True:
        try:
            Testcall(game)
        except (SystemExit):
            break
        game.rolltext("""
        ------------------------------------
        END OF MODULE TEST FOR {_NAME}.
        ------------------------------------""",frags=frags)
        if game.yesno(message="REPEAT TEST?"):
            if game.yesno(message="CLEAN THE SAVEDATA?"):
                Datacall()
        else:
            break


def game_loop(game:Game):
    world = {
        "apartment" : room_apartment.Start,
        "core"      : Core.Core,
        "inner"     : inner.Start,
        "middle"    : middlering.Start,
        "outer"     : outer.Start,
        "ladder"    : Ladder.Start,
        "bathrooms" : Bathrooms.Start,
        "cargobay"  : Core.Cargobay, 
        "cafeteria" : Cafeteria.Start
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
            try:
                place(game)
            except (ReturnToMain):
                #ReturnToMain is called when new game or load game is called from outside the title menu.
                continue
            
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