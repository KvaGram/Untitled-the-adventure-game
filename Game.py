# Merging the utility functions, savedata and UI into one nice and convinient class.
from typing import List
import json
import ui
import tkinter as TK
import time
import random
import sys
import re
#from untitled_const import *
from untitled_const import NAV_BACK_UNKNOWN, NAV_BACK_INTACT, NAV_BACK_BROKEN, ReturnToMain, ReturnToTitle

import ItemDB 
import Storyloader
from tkinter import messagebox as TKmsg


class Game:
    def __init__(self, tkroot:TK.Tk, version:(int,int,int), language:str = "english"):
        T = Gettexter(self)
        self.ui:ui.UntitledUI = ui.UntitledUI(tkroot, savecall = self.savegame, loadcall = self.loadgame, newcall = self.restartGame)
        self.tkroot:TK.Tk = tkroot
        self.version = version
        self.langauge = language
        self.newgame()
        self.story = Storyloader.load(language)
        self.runner:PlaceRunner = None

        self.tkroot.protocol("WM_DELETE_WINDOW", self.onExit)
        self.destroyed = False

        self.returnToTitle = False
        self.returnToMain = False

        ItemDB.SETUP(T, "HEADACHE", "TRANSLATOR","ASSHOLE","KEYCODE","KEEPSAKE","BROKE_TRANSLATOR")
        """
        ItemDB.SET("HEADACHE", T("ITEM_HEADACHE_NAME"), T("ITEM_HEADACHE_DESC"), "headache.gif")
        ItemDB.SET("TRANSLATOR", T("ITEM_TRANSLATOR_NAME"), T("ITEM_TRANSLATOR_DESC"), "translator.gif")
        ItemDB.SET("ASSHOLE", T("ITEM_ASSHOLE_NAME"), T("ITEM_ASSHOLE_DESC"), "asshole.gif")
        ItemDB.SET("KEYCODE", T("ITEM_KEYCODE_NAME"), T("ITEM_KEYCODE_DESC"), "note.gif")
        ItemDB.SET("KEEPSAKE", T("ITEM_KEEPSAKE_NAME"), T("ITEM_KEEPSAKE_DESC"), "smallbox.gif")
        ItemDB.SET("BROKE_TRANSLATOR", T("ITEM_BROKE_TRANSLATOR_NAME"), T("ITEM_BROKE_TRANSLATOR_DESC"), "brokentranslator.gif")
        """
        self.GeneralList = {
            "credits"        : Game.runCredits,
            "onReactorCTime" : Game.onReactorCTime
        }
    def quit(self):
        self.destroyed = True
        self.ui.quit()
    def onExit(self):
        if len (self.savedata) <= 1:
            return self.quit()
        s = TKmsg._show("UNTITLED! The adventure game", "Would you like to save before you quit?", TKmsg.WARNING, TKmsg.YESNOCANCEL)
        if(s == None or s == 'cancel'):
            return
        if(s == True or s == 'yes'):
            self.savegame()
        self.quit()
        sys.exit()
    def opengamemenu(self):
        NotAddedYet()
        #TODO: implement open game menu
    def newgame(self):
        self.savedata = {}
        self.setdata("navdata", Navdata())
    def restartGame(self):
        self.newgame()
        self.returnToMain = True
    def loadgame(self, fromTitle = False):
        res = self.ui.askSaveFile(True)
        if not res:
            return False
        path, exists = res
        if not exists:
            return False
        
        ldata = {}
        with open(path, "r") as f:
            ldata = json.load(f)
            f.close()
        if len(ldata) < 1:
            return
        #comparing versions.
        lversion = ldata.get("version")
        if not lversion:
            return
        major  = lversion[0] - self.version[0]
        minor  = lversion[1] - self.version[1]
        #hotfix = lversion[2] - self.version[2]
        if major == 0:
            if minor == 0:
                #not worth comparing a hotfix
                pass
            elif minor > 0:
                TKmsg.showinfo("Load Game", "This save was made with a newer version of the game. This may cause problems.")
            else:
                TKmsg.showinfo("Load Game", "This save was made with a older version of the game. This should be fine, but could cause issues.")
        elif major > 0:
            TKmsg.showwarning("Load Game", "This save is FROM THE FUTURE! You should run a newer version of the game instead.")
        else:
            TKmsg.showwarning("Load Game", "The save is OLD! The game may not run correctly with this savefile.")
        self.savedata = ldata
        self.setdata("navdata", Navdata())
        self.ui.draw_inventory(itemlist = self.getAllInventory())
        if not fromTitle:
            self.returnToMain = True
        return True
    def savegame(self):
        res = self.ui.askSaveFile(False)
        if not res:
            return False
        path, exists = res
        if(exists):
            if not TKmsg.askokcancel("Override save", "Do you wish to override this savefile?"):
                return False
        toSave = {}
        toSave["version"] = self.version
        _filter = ("navdata",)
        for key, val in self.savedata.items():
            if key in _filter:
                continue
            toSave[key] = val
        self.setdata("version", self.version)
        with open(path, "w+") as f:
            json.dump(toSave, f)
            f.close()
        return True

    def update(self):
        if self.destroyed:
            sys.exit()
            return
        n = self.Navdata
        if n.refresh:
            self.ui.navmap.AreaName = self.Navdata.AreaName
            #TODO set up the nav
            knowledge = self.getdata("wheelC:knowledge", 0)
            if knowledge < 1 or n.MapForceUnknown:
                self.ui.navmap.BackImage = NAV_BACK_UNKNOWN
                self.ui.navmap.LitImage = None
                self.ui.navmap.DotState = None
            else:
                if knowledge < 2:
                    self.ui.navmap.BackImage = NAV_BACK_INTACT
                else:
                    self.ui.navmap.BackImage = NAV_BACK_BROKEN
                self.ui.navmap.LitImage = self.Navdata.LitImage

            if n.canmove:
                self.ui.conf_navkeys(left=n.left, up=n.up, right=n.right, down=n.down)
            else:
                self.ui.conf_navkeys() #by default: all directions disabled.
            n.refresh = False
        try:
            self.tkroot.update()
            self.tkroot.update_idletasks()
        except (TK.TclError): 
            return
        if self.returnToMain:
            self.returnToMain = False
            raise ReturnToMain()
        if self.returnToTitle:
            self.returnToTitle = False
            raise ReturnToTitle()
    # retext runs format_map untill the text is formatted (or up to 5 times)
    # Fills inn all the tags that may show up:
    # game tags: example {game.PlayerSomething} - always starts with 'game.'
    # story tags example {EPIC_PART_9} - Always all caps
    # fragment parts {*OPTIONAL_3} - Always starts with star*
    #
    # Game tags gets data from the game state.
    # Story tags gets data from the nerrative text,
    # fragment tags gets data from the module code (usually a story tag that may alternate)
    def retext(self, text:str, frags:dict):
        if type(text) == str:
            i = 0
            reg = r'(?<=(?<!\{)\{)[^{}]*(?=\}(?!\}))'
            while i < 5 and re.search(reg, text):
                try:
                    text = text.format_map(formatdict(game = self, **self.story, **frags))
                except ValueError as err:
                    print("ERR: There was something wrong with this text:")
                    print(text)
                    print(err)
                    break
                i += 1
        elif type(text) == list:
            for i in range(len(text)):
                text[i] = self.retext(text[i], frags)
        return text
    def deqeue(self):
        data = DataInput.Make(self.ui.deqeue())
        if data and data.Type == "game":
            NotAddedYet() #TODO: handle gamemenu events
        return data
    
    def runGeneral(self, call):
        call = self.GeneralList.get(call)
        if call:
            try:
                call()
            except TypeError:
                call(self)
        else:
            NotAddedYet()

    def choose(self, _list, message = "{GAME_MAKECHOICE}", wait = False, frags = {}):
        _list = self.retext(_list, frags)
        message = self.retext(message, frags)
        self.ui.draw_actions(label = message, actions = _list)
        self.update()
        if wait:
            return self.wait()
    def wait(self, cleanup = True):
        data = None
        while not data:
            self.update()
            data = self.deqeue()
        if cleanup:
            self.ui.draw_noactions()
        return data
    def waitfor(self, type, val, cleanup = True):
        while True:
            self.update()
            data = self.deqeue()
            if data and data[0] == type:
                if cleanup:
                    self.ui.draw_noactions()
                return data[1][0] == val
    def yesno(self, message = "{GAME_PLEASESEL}", wait = True):
        choices = [["True", "{YES}"], ["False", "{NO}"]]
        self.choose(choices, message, False)
        if wait:
            return self.waitfor("action", "True")
        return self.choose(choices, message)
    def truefalse(self, message = "{GAME_PLEASESEL}", wait = True):
        choices = [["True", "{TRUE}"], ["False", "{TRUE}"]]
        self.choose(choices, message, False)
        if wait:
            return self.waitfor("action", "True")
        return self.choose(choices, message, wait)
    def textin(self, fields = [["Input", ""],], entertext = "ENTER", wait = False, frags = {}, **kwargs ):
        entertext = self.retext(entertext, frags)
        self.ui.draw_textinputs(fields = fields, entertext = entertext, **kwargs)
        if wait:
            return self.wait()
    def showtext(self, txt:str, frags:dict = {}):
        txt = self.retext(txt, frags)
        self.ui.writeToDisplay(txt)
        self.update()
    def rolltext(self, txt:str, linepause:float = 0.1, frags:dict = {}):
        txt = self.retext(txt, frags)
        lines = txt.splitlines()
        for l in lines:
            self.showtext(l)
            time.sleep(linepause)
        self.showtext("") #a single line-shift in the end, to break things up.

    #runs as rolltext, but yields if an input is pressed.
    #For use in skippable text, and/or some action can be done while it runs.
    #Yields first the input data, then the list and next index.
    def rolltextWait(self, txt:str, linepause:float = 0.1, frags:dict = {}):
        txt = self.retext(txt, frags)
        lines = txt.splitlines()
        for i in len (lines):
            l = lines[i]
            data = self.deqeue()
            if data:
                yield data
                yield ("rolltexthalt", (lines, i))
            self.ui.writeToDisplay(l)
            self.update()
            time.sleep(linepause)
        self.showtext("") #a single line-shift in the end, to break things up.


    #region dictionaries
    #TODO: get terms from some sort of resource file
    def getGenderedRole(self, role:str, gender:str) -> str:
        fallback:str = gender + " " + role
        gendered_role:dict = {
            "spouse"  : {"male":self.story["HUSBAND"], "female":self.story["WIFE"]},
            "sibling" : {"male":self.story["BROTHER"], "female":self.story["SISTER"]}
        }
        ret:dict = gendered_role.get(role, {})
        return ret.get(gender, fallback)
    
    def roleCounterpart(self, role) -> str:
        counterRole = {
            "spouse" : "sibling",
            "sibling" : "spouse"
        }
        return counterRole.get(role, "")
    #endregion dictionaries

    #region setters and getters.
    def getdata(self, key, default = None):
        if type(key) in (tuple, list):
            d = self.savedata
            for k in key:
                d = d.get(k, default)
                if type(d) != dict:
                    break
        return self.savedata.get(key, default)
    def setdata(self, key, value):
        self.savedata[key] = value
    
    def setInventory(self, key:str, value):
        inv = self.getdata("inventory", {})
        inv[key] = value
        self.setdata("inventory", inv)
        
        self.ui.draw_inventory(itemlist = self.getAllInventory())
    def getInventory(self, item:str):
        inv = self.getdata("inventory", {})
        return inv.get(item, None)
    def getAllInventory(self):
        return self.getdata("inventory", {})
        

    def setGameover(self, reason):
        self.setdata("GAME OVER", reason)
    def getGameover(self):
        return self.getdata("GAME OVER")
    
    @property
    def Navdata(self):
        return self.getdata("navdata")
#NOTE: remove hasGender and hasName?
    @property
    def hasGender(self)->bool:
        return self.getdata("gender") != None
    @property
    def hasName(self)->bool:
        return self.getdata("name") != None

    @property
    def FemaleFam(self):
        f = self.getdata("femalefam")
        if not f:
            self.defaultFam()
            return self.FemaleFam
        return f
    @property
    def MaleFam(self):
        f = self.getdata("malefam")
        if not f:
            self.defaultFam()
            return self.MaleFam
        return f
    @property
    def Spouse(self):
        return self.getFamByRole("spouse")
    def Sibling(self):
        return self.getFamByRole("sibling")
    def getFamByRole(self, role):
        if self.FemaleFam.role == role:
            return self.FemaleFam
        else:
            return self.MaleFam

    def defaultFam(self):
        m:FamPerson = self.getdata("malefam")
        f:FamPerson = self.getdata("femalefam")
        randRole1 = random.choice(("spouse", "sibling"))
        randRole2 = self.roleCounterpart(randRole1)

        if (m or f) == None:
            m = FamPerson(self, "male", "Jeff", randRole1)
            f = FamPerson(self, "female", "Klara", randRole2)
        elif m:
            f = FamPerson(self, "female", "Klara", m.RoleCounterpart)
        elif f:
            m = FamPerson(self, "male", "Jeff", f.RoleCounterpart)
        self.setdata("malefam", m)
        self.setdata("femalefam", f)

    def setFemaleFam(self, role:str, name:str = "Klara"):
        f = self.getdata("femalefam", FamPerson(self, "female", None, None))
        f.name = name
        f.role = role
        self.setdata("femalefam", f)

    def setMaleFam(self, role:str, name:str = "Jeff"):
        m = self.getdata("malefam", FamPerson(self, "male", None, None))
        m.name = name
        m.role = role
        self.setdata("malefam", m)
    
    @property
    def PlayerName(self)->str:
        return self.getdata("name", "Inkon Nito")
    @property
    def PlayerGender(self)->str:
        g = self.getdata("gender")
        if not g:
            g = random.choices(("male", "female"))
            self.setdata("gender", g)
        return g

    @property
    def place(self):
        return self.getdata("place")
    @property
    def prevPlace(self):
        return self.getdata("prevplace")
    @place.setter
    def place(self, val:str):
        self.setdata("prevplace", self.place)
        self.setdata("place", val)
    #endregion setters and getters
    #region counters

    #get counter fetches a counterdata or creates a new empty one.
    def getCounter(self, counterName):
        return self.getdata(counterName, Counterdata(self, enabled = False, call = None, value = 0))
    # set counter sets or resets data for a counter
    def setCounter(self, counterName, counterCall, counterInit = 0):
        counter = self.getCounter(counterName)
        counter.enabled = True
        counter.call = counterCall
        counter.value = counterInit

    #updates the value of a counter
    def updateCounter(self, counterName, val:int):
        counter = self.getCounter(counterName)
        
        if counter.enabled:
            counter.value += val
            return self.runGeneral(counter.call)
        return "inactive"
    #sets counter enabled to false, runs its call one last time.
    def endCounter(self, counterName):
        counter = self.getCounter(counterName)
        p_enabled = counter.enabled
        counter.enabled = False
        if p_enabled:
            return self.runGeneral(counter.call)
        return "inactive"
    #endregion counters
    

    #region general_functions
    def onReactorCTime(self):
        c = self.getCounter("reactorC")
        if not c.enabled:
            return "safe"
        if c.value <= 0:
            self.showtext("Placeholder - something something you just died due to a reactor meltdown!")
            self.setGameover("You wasted too much time! You're kinda dead now")
            return "death"
        return "safe"
    def runCredits(self):
        self.rollArt("title", 0.05)
        self.rollArt("credits", 0.1)
    #endregion general_functions
    def rollArt(self, artname, linepause:float = 0.1):
        f = open(f"{artname}.txt", 'r', encoding="utf-8")
        artText = f.read()
        self.rolltext(artText, linepause)
        f.close()


#Gettexter generates a function T as a shortcut for getting text from game.story.
#This intended for use by other modules.
def Gettexter(game:Game):
    def T(storytag:str)->str:
        fallback = "(({0}))".format(storytag)
        return game.story.get(storytag, fallback)
    return T
class OptionList(list):
    def GetAct(self, indTag):
        if type(indTag) == ActDataInput:
            indTag = indTag.index
        elif type(indTag) != int:
            indTag = self.GetInd(indTag)
        if indTag not in range(self.Len):
            return None
        try:
            return self[indTag][2]
        except:
            return None
    def RunAct(self, indTag, **kwargs):
        try:
            return self.GetAct(indTag)(**kwargs)
        except:
            return None
    def GetInd(self, tag):
        for i in range(self.Len):
            if self[i][0] == tag:
                return i
        return -1
    def MoveItemFront(self, tag):
        i = self.GetInd(tag)
        if i == -1:
            return False
        opt = self.pop(i)
        self.insert(0, opt)
    def MoveItemBack(self, tag):
        i = self.GetInd(tag)
        if i == -1:
            return False
        opt = self.pop(i)
        self.append(0, opt)
        #wraps random.shuffle
    def Randomize(self, r:float = None):
        random.shuffle(self, r)
    @property
    def Len(self):
        return len(self)


    
class Counterdata:
    def __init__(self, game:Game, **args):
        self.enabled = args.get("enabled", False)
        self.call = args.get("call", None)
        self.value = args.get("value", 0)
        self.game = game
class FamPerson:
    def __init__(self, game:Game, gender:str, name:str, role:str):
        self.gender = gender
        self.name = name
        self.role = role
        self.game = game
    @property
    def GenderedRole(self):
        return self.game.getGenderedRole(self.role, self.gender)
    @property
    def GenderedRolePlayer(self):
        return self.game.getGenderedRole(self.role, self.game.PlayerGender)
    @property
    def RoleCounterpart(self):
        return self.game.roleCounterpart(self.role)
class Navdata:
    def __init__(self, **args):
        #boolean - enabled or disabled!
        #by default, all are disabled.
        self.__up = args.get("up", False)
        self.__left = args.get("left", False)
        self.__right = args.get("right", False)
        self.__down = args.get("down", False)

        #special flag for when all nav keys are disabled (maybe becouse of some event)
        self.__closed = args.get("closed", False)

        #Custom labels for each direction.
        self.text_left  = args.get("text_left",  u"\u2190")
        self.text_up    = args.get("text_up",    u"\u2191")
        self.text_right = args.get("text_right", u"\u2192")
        self.text_down  = args.get("text_down",  u"\u2193")
        
        self.__areaName = args.get("areaname", "UNKNOWN AREA")
        self.__mapRadians = args.get("mapradians", 0.0)
        self.__mapRadius = args.get("mapradius", 50)
        self.__mapLit    = args.get("maplit", None)
        self.__mapForceUnknown = args.get("mapforceunknown", False)
        self.cleanxyz()
        self.refresh = True
    
    @property
    def canmove(self):
        if self.closed:
            return False
        return self.up or self.left or self.right or self.down
    #X, Y and Z are varables for use by the active code/place to keep its place.
    def cleanxyz(self):
        self.x = 0
        self.y = 0
        self.z = 0
    def cleantextdirs(self):
        self.text_left  = u"\u2190"
        self.text_up    = u"\u2191"
        self.text_right = u"\u2192"
        self.text_down  = u"\u2193"
    #region getters
    @property
    def up(self)->bool:
        return self.__up
    @property
    def left(self)->bool:
        return self.__left
    @property
    def right(self)->bool:
        return self.__right
    @property
    def down(self)->bool:
        return self.__down
    @property
    def closed(self)->bool:
        return self.__closed
    @property
    def AreaName(self):
        return self.__areaName
    @property
    def MapRadians(self):
        return self.__mapRadians
    @property
    def MapRadius(self):
        return self.__mapRadius
    @property
    def MapLit(self):
        return self.__mapLit
    @property
    def MapForceUnknown(self):
        return self.__mapForceUnknown
    
    #endregion getters
    #region setters
    @up.setter
    def up(self, val):
        self.__up = val
        self.refresh = True
    @left.setter
    def left(self, val):
        self.__left = val
        self.refresh = True
    @right.setter
    def right(self, val):
        self.__right = val
        self.refresh = True
    @down.setter
    def down(self, val):
        self.__down = val
        self.refresh = True
    @closed.setter
    def closed(self, val):
        self.__closed = val
        self.refresh = True
    @AreaName.setter
    def AreaName(self, val):
        self.__areaName = val
        self.refresh = True
    @MapRadians.setter
    def MapRadians(self, val):
        self.__mapRadians = val
        self.refresh = True
    @MapRadius.setter
    def MapRadius(self, val):
        self.__mapRadius = val
        self.refresh = True
    @MapLit.setter
    def MapLit(self, val):
        self.__mapLit = val
        self.refresh = True
    @MapForceUnknown.setter
    def MapForceUnknown(self, val):
        self.__mapForceUnknown = val
        self.refresh = True

    def setdir(self, dir:str, val:bool):
        if dir == "up":
            self.up = val
        elif dir == "left":
            self.left = val
        elif dir == "right":
            self.right = val
        elif dir == "down":
            self.down = val
    def resetDirs(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
    #endregion setters

class PlaceRunner:
    def __init__(self, game:Game):
        self.game:Game = game
        self.running = False
        self.nav:Navdata = game.Navdata
    def stop(self):
        self.running = False

class PlaceRunner1D(PlaceRunner):
    def __init__(self, game:Game, axis:str = 'x', minusDir = "left", plusDir = "right"):
        super().__init__(game)
        self.nodes:List[PlaceNode] = []
        self.axis = axis
        self.minusDir = minusDir
        self.plusDir = plusDir
        self.frags = []
    def run(self):
        if len(self.nodes) == 0:
            print("ERR: place has no nodes!")
            return
        #ensure the nav is open
        self.nav.closed = False
        self.nav.resetDirs()
        # ensure the index is valid.
        self.index = self.index
        self.running = True
        while self.running:
            i:int = self.index
            n:PlaceNode = self.nodes[i]
            self.nav.setdir(self.minusDir, i > 0)
            self.nav.setdir(self.plusDir, i < len(self.nodes)-1)
            self.nav.AreaName = n.areaName
            self.nav.MapRadians = n.navRadian
            self.nav.MapRadius = n.navRadius
            if len (n.actions) > 0:
                self.game.choose(n.actions, "")
            data:ActDataInput = self.game.wait()
            if data.Type == "action":
                actIndex = data.index
                self.runaction(n.actions[actIndex])
            elif data[0] == "nav":
                previndex = self.index
                if data[1] == self.minusDir:
                    self.index -= 1
                elif data[1] == self.plusDir:
                    self.index += 1
                self.onTravel(previndex)
    def indexofnode(self, nodeid:str):
        for i in range(len(self.nodes)):
            if self.nodes[i].id == nodeid:
                return i
        return None
    #should be overritten
    def runaction(self, action):
        if len(action) > 2:
            action[2]()
        else:
            print("Unhandled call to run " + action[0])
    def onTravel(self, previndex:int):
        pass
    @property
    def index(self):
        if self.axis == 'x':
            return self.nav.x
        elif self.axis == 'y':
            return self.nav.y
        elif self.axis == 'z':
            return self.nav.z
        else:
            return None
    @index.setter
    def index(self, val):
        if type(val) == str:
            val = self.indexofnode(val)
        if val == None:
            return
        i = val % len(self.nodes)
        if self.axis == 'x':
            self.nav.x = i
        elif self.axis == 'y':
            self.nav.y = i
        elif self.axis == 'z':
            self.nav.z = i


class DataInput(list):
    @staticmethod
    def Make(dataInput):
        if not dataInput:
            return None
        elif dataInput[0] == "action":
            return ActDataInput(dataInput)
        elif dataInput[0] == "text":
            return TextinDataInput(dataInput)
        elif dataInput[0] == "nav":
            return NavDataInput(dataInput)
        elif dataInput[0] == "game":
            return GameMenuInput(dataInput)
        else:
            return DataInput(dataInput)

    def __init__(self, dataInput):
        super().__init__(dataInput)
    @property
    def Data(self):
        return self[1]
    @property
    def Type(self):
        return self[0]
class ActDataInput(DataInput):
    def __init__(self, data):
        super().__init__(data)
    @property
    def index(self)->int:
        return self.Data[1]
    @property
    def tag(self)->str:
        return self.Data[0]
class TextinDataInput(DataInput):
    def __init__(self, data):
        super().__init__(data)
class NavDataInput(DataInput):
    def __init__(self, data):
        super().__init__(data)
class GameMenuInput(DataInput):
    def __init__(self, data):
        super().__init__(data)

class PlaceNode:
    def __init__(self, game:Game, _id:str, areaName:str, navRadius:int, navRadian:float, actions:list):
        self.game = game
        self.id = _id
        self.areaName = areaName
        self.navRadius = navRadius
        self.navRadian = navRadian
        self.actions = actions
class formatdict(dict):
    def __missing__(self, key):
        return "{"+key+"}"

def NotAddedYet():
    TKmsg.showwarning("WOOPS..","Sorry, that feature is not added yet.\nPlease be impatient.\nI am very lazy, and need the pressure.")