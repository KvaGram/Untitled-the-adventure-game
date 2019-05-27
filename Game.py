# Merging the utility functions, savedata and UI into one nice and convinient class.

import ui
import tkinter as TK
import time
import random
import sys

class Game:
    def __init__(self, tkroot:TK.Tk, version:(int,int,int), language:str = "english"):
        self.ui:ui.UntitledUI = ui.UntitledUI(tkroot)
        self.tkroot:TK.Tk = tkroot
        self.version = version
        self.savedata = {}
        self.langauge = language
        self.navdata = Navdata()
        
        self.GeneralList = {
            "onReactorCTime" : Game.onReactorCTime
        }
    def update(self):
        n = self.navdata
        if n.refresh:
            self.ui.set_navtext(self.navdata.navtext)
            if n.canmove:
                self.ui.conf_navkeys(left=n.left, up=n.up, right=n.right, down=n.down)
            else:
                self.ui.conf_navkeys() #by default: all directions disabled.
            n.refresh = False
        self.tkroot.update()
        self.tkroot.update_idletasks()
    def deqeue(self):
        data = self.ui.deqeue()
        if data and data[0] == "menu":
            raise NotImplementedError() #TODO: handle menu events
        return data
    
    def runGeneral(self, call):
        call = self.GeneralList.get(call)
        if call:
            call()
        else:
            raise NotImplementedError

    def choose(self, list, message = "Please make a choice", wait = False):
        self.ui.draw_actions(label = message, actions = list)
        self.update()
        if wait:
            return self.wait
    def wait(self, cleanup = True):
        data = None
        while not data:
            self.update()
            data = self.deqeue()
        if cleanup:
            self.ui.draw_noactions()
        return data

    def yesno(self, message = "Please select", wait = False):
        choices = (("True", "Yes"), ("False", "No"))
        return self.choose(choices, message, wait)
    def truefalse(self, message = "Please select", wait = False):
        choices = (("True", "True"), ("False", "False"))
        return self.choose(choices, message, wait)
    def textin(self, fields = (("Input", ""),), entertext = "ENTER", wait = False, **kwargs ):
        self.ui.draw_textinputs(fields = fields, entertext = entertext, **kwargs)
        if wait:
            return self.wait()
    def showtext(self, txt:str):
        self.ui.writeToDisplay(txt)
        self.update()
    def rolltext(self, txt:str, linepause:float = 0.1):
        lines = txt.splitlines()
        for l in lines:
            self.showtext(l)
            time.sleep(linepause)
    #runs as rolltext, but yields if an input is pressed.
    #For use in skippable text, and/or some action can be done while it runs.
    #Yields first the input data, then the list and next index.
    def rolltextWait(self, txt:str, linepause:float = 0.1):
        lines = txt.splitlines()
        for i in len (lines):
            l = lines[i]
            data = self.deqeue()
            if data:
                yield data
                yield ("rolltexthalt", (lines, i))
            self.showtext(l)
            time.sleep(linepause)

    #region dictionaries
    #TODO: get terms from some sort of resource file
    def getGenderedRole(self, role:str, gender:str) -> str:
        fallback:str = gender + " " + role
        gendered_role:dict = {
            "spouse"  : {"male":"husband", "female":"wife"},
            "sibling" : {"male":"brother", "female":"sister"}
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
    
    #region setters and getters
    def getdata(self, key, default = None):
        if type(key) == tuple or type(key) == list:
            d = self.savedata
            for k in key:
                d = d.get(k, default)
                if type(d) != dict:
                    break
            return d
        return self.savedata.get(key, default)
    def setdata(self, key, value):
        self.savedata[key] = value

    def setGameover(self, reason):
        self.setdata("GAME OVER", reason)
    def getGameover(self):
        return self.getdata("GAME OVER")

#NOTE: remove hasGender and hasName?
    @property
    def hasGender(self)->bool:
        return self.getdata("gender") != None
    @property
    def hasName(self)->bool:
        return self.getdata("name") != None

    @property
    def FemaleFam(self)->dict:
        f = self.getdata("femalefam")
        if not f:
            self.defaultFam()
            return self.FemaleFam
        return f
    @property
    def MaleFam(self)->dict:
        f = self.getdata("malefam")
        if not f:
            self.defaultFam()
            return self.MaleFam
        return f
    
    def defaultFam(self):
        m:FamPerson = self.getdata("malefam")
        f:FamPerson = self.getdata("femalefam")
        randRole1 = random.choices(("spouse", "sibling"))
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
    #endregion general_functions

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
        
        self.__navtext = args.get("navtext", "UNKNOWN\nAREA")

        self.refresh = True
    @property
    def canmove(self):
        if self.closed:
            return False
        return self.up or self.left or self.right or self.down
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
    def navtext(self)->str:
        return self.__navtext
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
    @navtext.setter
    def navtext(self, val):
        self.__navtext = val
        self.refresh = True
    #endregion setters
