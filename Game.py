# Merging the utility functions, savedata and UI into one nice and convinient class.

import ui
import tkinter as TK
import time
import random
import sys

class Game:
    def __init__(self, tkroot:TK.Tk, version:(int,int,int), language:str = "english"):
        self.ui = ui.UntitledUI(tkroot)
        self.tkroot:TK.Tk = tkroot
        self.version = version
        self.savedata = {}
        self.langauge = language




    def update(self):
        self.tkroot.update()
        self.tkroot.update_idletasks()
    
    
        
        
    def runGeneral(self, call):
        pass
    def choose(self, list, message = "Please make a choice", onSelect = None) -> (int, str):
        pass
    def yesno(self, message = "Please select") -> bool:
        choices = (("True", "Yes"), ("False", "No"))
        res:(int,bool) = self.choose(choices, message)
        return res[1] == "True"
    def truefalse(self, message = "Please select") -> bool:
        choices = (("True", "True"), ("False", "False"))
        res:(int,bool) = self.choose(choices, message)
        return res[1] == "True"
    def showtext(self, txt:str):
        self.ui.writeToDisplay(txt)
        self.update()
    def rolltext(self, txt:str, linepause:float = 0.1):
        lines = txt.splitlines()
        for l in lines:
            self.showtext(l)
            time.sleep(linepause)
    
    #region dictionaries
    def getGenderedTerm(self, term, gender) -> str:
        #TODO: move to some sort of resource file
        fallback:str = gender + " " + term
        gendered_term:dict = {
            "spouse"  : {"male":"husband", "female":"wife"},
            "sibling" : {"male":"brother", "female":"sister"}
        }
        ret:dict = gendered_term.get(term, {})
        return ret.get(gender, fallback)
    
    def termCounterpart(self, term) -> str:
        counterTerms = {
            "spouse" : "sibling",
            "sibling" : "spouse"
        }
        return counterTerms.get(term, "")
    #endregion dictionaries
    
    #region setters and getters
    def getdata(self, key, default = None):
        if type(key) == tuple or type(key) == list:
            d = self.savedata
            for k in key:
                d = d.get(k)
                if d == None:
                    d = default
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

    @property
    def hasGender(self)->bool:
        return self.getdata("gender") != None
    @property
    def hasName(self)->bool:
        return self.getdata("name") != None
    @property
    def hasFemaleFam(self)->bool:
        return self.getdata("femalefam") != None
    @property
    def hasMaleFam(self)->bool:
        return self.getdata("malefam") != None
    
    def defaultFam(self):
        m = self.getdata("malefam")
        f = self.getdata("femalefam")
        randRole1 = random.choices(("spouse", "sibling"))
        randRole2 = self.termCounterpart(randRole1)

        if (m or f) == None:
            m = {name : "Jeff", role : randRole1}
            f = {name : "Klara", role : randRole2}
    #TODO: CONTINUE WORK HERE!

    @property
    def femaleFamName(self):
        self.getdata(("femalefam", "name"), "Klara")
    @property
    def maleFamName(self):
        self.getdata(("malefam", "name"), "Jeff")
    
    @property
    def femaleFamRole(self):
        if not self.hasFemaleFam:
            if self.hasMaleFam:
                self.setFemaleFam(self.termCounterpart(self.getdata(("malefam", role))), "Klara")
            else:
                self.setFemaleFam(random.choices(("spouse", "sibling")), "Klara")
        return self.getdata

        
    @property
    def maleFamRole(self):


    def setFemaleFam(self, role:str, name:str = "Klara")->str:
        self.setdata("femalefam", {"role" : role, "name" : name} )

    def setMaleFam(self, role:str, name:str = "Jeff")->str:
        self.setdata("femalefam", {"role" : role, "name" : name} )
    
    def getName(self)->str:
        return self.getdata("name", "Inkon Nito")

    #endregion setters and getters
    #region counters
    def getCounter(self, counterName):
            counter = self.getdata(counterName, {"enabled" : False, "call" : None, "value" : 0})

            enabled = self.getdata(counterName + ":enabled", False)
            call = self.getdata(counterName + ":call", None)
            value = self.getdata(counterName + ":value", 0)
            return (enabled, call, value)
    def setCounter(self, counterName, counterCall, counterInit = 0):
            self.setdata(counterName + ":enabled", True)
            self.setdata(counterName + ":call", counterCall)
            self.setdata(counterName + ":value", counterInit)

    def updateCounter(self, counterName, val):
            enabled, call, value = self.getCounter(counterName)
            if enabled:
                self.setdata(counterName + ":value", value + val)
                return self.runGeneral(call)
            return "inactive"
    def endCounter(self, counterName):
        enabled, call, _ = self.getCounter(counterName)
        self.setdata(counterName + ":enabled", False)
        # run the call function if the counter was previusly disabled.
        if enabled:
            return self.runGeneral(call)
    #endregion counters
    

    #region general_functions
    def onReactorCTime(self):
        enabled, _ , time = self.getCounter("reactorC")
        if not enabled:
            return "safe"
        if time <= 0:
            self.showtext("Placeholder - something something you just died due to a reactor meltdown!")
            self.setGameover("You wasted too much time! You're kinda dead now")
            return "death"
        return "safe"
    #endregion general_functions
