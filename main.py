#NOTE: idea for fixing the break to title or brake to main functions without needing to use exception calls.
# Use genertors. Like in a previus version of this project, have a yield statement on every call that invokes game.update.
# Problem 1: What will the generators yield? Just a "everything is ok here"-true boolean?
# problem 2: What about sub-processes that invoke game.update?
# 1: void. It should not matter what the yield it, as long as the chain can be broken in the game loop.
# 2: Their function can be yielded to the game loop, where they will be put on a stack and ran as the current function.
#!!! ding ding! There it is. I just re-invented the call stack. But this might just be what I need.

# The outer game loop would work thusly:
# * Get place (function / generator)
#   * end game with error if not found
# * Check for game over
#   * end game if game over
# * start new call-stack
# * insert place-generator in stack
# * start inner game loop

# The inner game loop would work like this:
# * Check if stack is empty
#   * if so, break out of inner loop (return)
# * try
#   * fetch next element in current function
#   * check if element is a generator.
#   *   if so, add element to top of stack
#   * check if break to main or break to title is triggured
#       * if so, break out of inner game loop (return)
# * catch/except - end of function error
#   * remove current function from stack.
#
   
# But what if I could access the call stack directly? If I could, then maybe I won't even need to make generator functions.
# Must be reseached!

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
from untitled_const import ReturnToMain
from untitled_const import ReturnToTitle

import room_apartment 
import middlering
import Bathrooms
import Ladder
import Core
import Cafeteria
import outer
import inner

#version number. Major, minor, hotfix.
VERSION = [1, 3, 0]
#if dev is on, some debug info may be displayed in the game
DEV = True

def start():
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1600x900")

    game = Game.Game(tkRoot, VERSION, "english")
    while True:
        try:
            titleMenu(game)
        except ReturnToTitle:
            continue
        except SystemExit:
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
        "outer"     : outer.Start,          #TODO: implement mapnav
        "ladder"    : Ladder.Start,         #TODO: implement mapnav
        "bathrooms" : Bathrooms.Start,      #TODO: implement mapnav
        "cargobay"  : Core.Cargobay,        
        "cafeteria" : Cafeteria.Start       #TODO: implement mapnav
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
            continue
        if r == "LOADGAME":
            if game.loadgame(fromTitle = True):
                game_loop(game)
            return
        if r == "NEWGAME":
            game.newgame()
            game_loop(game)
            return

if __name__ == "__main__":
    start()