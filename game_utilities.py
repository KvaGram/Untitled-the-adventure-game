#this script binds together all scripts such as all others can access each other in a global scope
import sys
import tkinter as tk
from tkinter import filedialog
import time
import random
import about

#This is a map of functions that can be called at any time.
def RunGeneral(save, call):
    if call == "onReactorCTime":
        return onReactorCTime(save)
    if call == "about":
        return about.main()
    return "NOT FOUND"

def choose(list, message = "enter choice number"):
    valid = False
    inp = 0 #placeholder value
    while not valid:
        showtext("\t"+message)
        for i in range (len(list)):
            #if an option is set as None, it is a valid choice, but will not be displayed.
            #This allows for disabled choices and hidden coices.
            if(list[i] != None):
                print ("\t [{0}] - {1}".format(i+1, list[i]))
        inp = input()
        while len(inp) < 1:
            #while no input, silently re-request input
            inp = input()
        try:
            inp = int(inp) - 1
        except:
            showtext("Please enter a valid number")
            continue
        if (inp < 0 or inp >= len(list)):
            showtext("Sorry, that is not an option.")
            continue
        valid = True
    #showtext("you chose {0}".format(list[inp-1]))
    return inp

class navdata:
    def __init__(self, **args):
        #boolean - enabled or disabled!
        #by default, all are disabled.
        self.up = args.get("up", False)
        self.left = args.get("left", False)
        self.right = args.get("right", False)
        self.down = args.get("down", False)

        #special flag for when all nav keys are disabled (maybe becouse of some event)
        self.closed = args.get("closed", False)

        #Custom labels for each direction.
        self.text_left  = args.get("text_left",  u"\u2190")
        self.text_up    = args.get("text_up",    u"\u2191")
        self.text_right = args.get("text_right", u"\u2192")
        self.text_down  = args.get("text_down",  u"\u2193")
        
        self.navtext = args.get("navtext", "UNKNOWN\nAREA")


# NOTE rule:
# if no action or textinputs are requested, and nav is missing or closed, then the game will continue the event.
class request:
    def __init__(self, **args):
        #Text to dramatically roll on screen. default(False): No text will be displayed | mutually exclusive with showtext
        self.rolltext:str    = args.get("rolltext", False)
        #how fast above text will roll. default(0.1): fast, 1 line every 0.1 secunds
        self.rollwtime:float = args.get("rollwtime", 0.1)
        #Text to display instantly. default(False): No text will be displayed | mutually exclusive with rolltext
        self.showtext:str    = args.get("showtext", False)
        #an instance of navdata. enables nav-buttons and nav text. default(navdata(closed = True)): nav is disabled, navtext display UNKNOWN AREA.
        self.navdata:navdata = args.get("navdata", navdata(closed = True))
        #a list of options the player can choose from. default(false): No options to choose from | mutually exclusive with textin
        self.actions:list    = args.get("actions", False)
        #a list of textfields the player can enter text to. default(false): No options to choose from | mutually exclusive with actions
        self.textin:list     = args.get("textin", False)
        #flag for when the UI should refresh inventory elements.
        self.invrefresh:bool = args.get("invrefresh", False)
        #sets next place to load (str) or run (callable) once the current function ends.
        self.next            = args.get("next", False)

class response:
    def __init__(self, pressed:str = None, data:object = None):
        self.pressed = pressed
        self.data    = data





#choose2 documentation
#pList is a list of option for the user to selct from.
#   Items of pList may be a string, a None, or a list/tuple of options
#       If item is a string, then this string acts as both idetifier and displaytext.
#       If item is a None, then None acts as an identefier, but is not displayed (semi-hidden choice)
#       If item is a list or tuple, then first sub-item in the item will be the identifier.
#          Last sub-item is either the display-text or the index of the display text.
#          Any middle sub-item that may exist will be an alternative for a display text.
#          Any middle sub-item would be unsuable if last sub-item is not a valid index.
#              In this scenario, last sub-item defaults to a display text. See example.
#          If display-text is None, then the item will not be displayed (semi-hidden choice)
#   message is the text displayed when the player is asked to make a choice.
#   onSelect is an optional text to display when the player has inputed a valid choice.
#       formatted text includes:
#           {0} choice display index
#           {1} choice identifier
#           {2} displayed choice text

#pList is a list of choices. Choice may be None(hidden), string, list of two strings (intentifier, display),
# or a list of strings then an integer (indentifier/display0, display1, ... , displayN, displayIndex)
# algorithm rule: if last element in list is not a valid integer index of the list, it is treated as the display to use.
""" mixed example:
    fruits = [
        ["APPLE", "I choose the apple", "I'll take the apple", 2],
        ["ORANGE", "I shall take the Orange", "I must have an Orange, "Snatch the orange, I shall", 3],
        "BANANA",
        ["PAPAYA", "I choose the papaya", "Papaya it is!", 999]
        ["MELON"],
        ["GRAPE", "I choose the grape", "Grape it is", 0],
        None,
        [PINEAPPLE, "I want a pineapple", "I'll take the pineapple"]

    ]
    fruitIndex, fruitID = choose2(fruits, "choose fruit", "<< you chose '{2}', wich was number {0} on the list)
    ------
    output:
    
    choose fruit
    
    [1] - I'll take the apple
    [2] - Snatch the orange, I shall
    [3] - BANANA
    [4] - 999
    [5] - MELON
    [6] - GRAPE
    [8] - I'll take the pineapple

    > 2
    << you chose 'Snatch the orange, I shall', wich was number 2 on the list

    Please note the count from 1, this is UI only, internal remains from 0.
    Also note absense of option 7, as this choice was a None.
    Finally note the fallback result from the invalid input in option 4. Best to avoid this.

"""
def choose2(pList, message = "enter choice number", onSelect = None):
    valid = False
    inp = 0 #placeholder value
    length = len(pList)
    dispList = [None,] * length #initiate list with empty elements
    for i in range (length):
        choice = pList[i]
        if choice == None:
            continue #if choice is None, hide the option (but keep it valid)
            #This allows for disabled choices and hidden coices.
        if type(choice) == str:
            dispList[i] = choice
        if type(choice) == list or type(choice) == tuple:
            di = choice[-1] #last item in list.
            if type(i) == int and di in range(len(choice)-1): #if di is a valid index in the list, sans its own index then
                dispList[i] = choice[di] # di determines the item to use as display text. (yes, item 0 is a valid option as display text)
            else:
                dispList[i] = di #else di is the display text.
    while not valid:
        showtext("\t"+message)
        for i in range (length):
            if(dispList[i] != None):
                print ("\t [{0}] - {1}".format(i+1, dispList[i]))
        inp = input()
        while len(inp) < 1:
            #while no input, silently re-request input
            inp = input()
        try:
            inp = int(inp) - 1
        except:
            showtext("Please enter a valid number")
            continue
        if (inp < 0 or inp >= len(pList)):
            showtext("Sorry, that is not an option.")
            continue
        valid = True
    #showtext("you chose {0}".format(list[inp-1]))
    choice = pList[inp]
    v = None
    if type(choice) == list or type(choice) == tuple:
        v = choice[0]
    else:
        v = choice #for pure string, None and other odd inputs
    if type(onSelect) == str:
        showtext(onSelect.format(inp+1, v, dispList[inp]))
    return (inp, v)
def yesno(message = "Please select"):
    while True:
        showtext("\t" + message)
        showtext("\t[Y] yes")
        showtext("\t[N] no")
        showtext()
        inp = input()
        while len(inp) < 1:
            #while no input, silently re-request input
            inp = input()
        if(inp[0] == "y" or inp[0] == "Y"):
            return True
        elif(inp[0] == "n" or inp[0] == "N"):
            return False
def truefalse(message = "Please select"):
    while True:
        showtext("\t" + message)
        showtext("\t[T] True")
        showtext("\t[F] False")
        showtext()
        inp = input()
        while len(inp) < 1:
            #while no input, silently re-request input
            inp = input()
        if(inp[0] == "t" or inp[0] == "T"):
            return True
        elif(inp[0] == "f" or inp[0] == "F"):
            return False        
# Displays a multiline text on screen line by line, with an adjustable break between.
def rolltext(txt, linepause = 0.1):
    lines = txt.splitlines()
    for l in lines:
        showtext(l)
        time.sleep(linepause)
# Displays a text on screen. print is not used directly, so the game can be upgraded to use some alternate GUI (like pygame) if needed.
def showtext(text = ""):
    print(text)

def getGenderedTerm(term, gender):
    if term == "spouse":
        if gender == "male":
            return "husband"
        elif gender == "female":
            return "wife"
        else:
            return gender + " " + term #fallback
    if term == "sibling":
        if gender == "male":
            return "brother"
        elif gender == "female":
            return "sister"
        else:
            return gender + " " + term #fallback
def termCounterpart(term):
    if term == "spouse":
        return "sibling"
    if term == "sibling":
        return "spouse"

def getCounter(save, counterName):
        enabled = save.getdata(counterName + ":enabled", False)
        call = save.getdata(counterName + ":call", None)
        value = save.getdata(counterName + ":value", 0)
        return (enabled, call, value)
def setCounter(save, counterName, counterCall, counterInit = 0):
        save.setdata(counterName + ":enabled", True)
        save.setdata(counterName + ":call", counterCall)
        save.setdata(counterName + ":value", counterInit)

def updateCounter(save, counterName, val):
        enabled, call, value = getCounter(save, counterName)
        if enabled:
            save.setdata(counterName + ":value", value + val)
            return RunGeneral(save, call)
        return "inactive"
def endCounter(save, counterName):
    enabled, call, _ = getCounter(save, counterName)
    save.setdata(counterName + ":enabled", False)
    # run the call function if the counter was previusly disabled.
    if enabled:
        return RunGeneral(save, call)
    

#NOTE consider moving general functions to its own module
def onReactorCTime(save):
    enabled, _ , time = getCounter(save, "reactorC")
    if not enabled:
        return "safe"
    if time <= 0:
        showtext("Placeholder - something something you just died due to a reactor meltdown!")
        setGameover(save, "You wasted too much time! You're kinda dead now")
        return "death"
    return "safe"
def setGameover(save, reason):
    save.setdata("GAME OVER", reason)
def getGameover(save):
    return save.getdata("GAME OVER")
#common data
def hasGender(save):
    return save.getdata("gender") != None
def hasName(save):
    return save.getdata("name") != None
def hasKlara(save):
    return save.getdata("klara") != None
def hasJeff(save):
    return save.getdata("jeff") != None

#get common data, randomize if not defined.
def getGender(save):
    if hasGender(save):
        return save.getdata("gender")
    else:
        return save.getdata("gender", random.choice(("male", "female")))
def getName(save):
    return save.getdata("name", "The nameless one")
def getKlara(save, gendered = False):
    if gendered:
        return getGenderedTerm(getKlara(save, False), "female")
    if hasKlara(save):
        return save.getdata("klara")
    elif hasJeff(save):
        return save.getdata("klara", termCounterpart(getJeff(save)))
    else:
        return save.getdata("klara", random.choice(("spouse", "sibling")))
    
def getJeff(save, gendered = False):
    if gendered:
        return getGenderedTerm(getJeff(save, False), "male")
    if hasJeff(save):
        return save.getdata("jeff")
    elif hasKlara(save):
        return save.getdata("jeff", termCounterpart(getKlara(save)))
    else:
        return save.getdata("jeff", random.choice(("spouse", "sibling")))
#opes game menu.
#requires save.
#Returns True if game needs to return to main.
def gameMenu(save):
    choices = (
        ("CONTINUE", "Continue game"),
        ("SAVE", "Save game"),
        ("LOAD", "Load game"),
        ("ABOUT", "Credits"),
        ("EXIT", "Close game")
    )
    while True:
        _, choice = choose2(choices, "Welcome to the game menu. What would you like to do?")
        if choice == "CONTINUE":
            return False
        elif choice == "SAVE":
            save.savegame()
        elif choice == "LOAD":
            if yesno("Are you sure you wish to load a game?"):
                if save.loadgame():
                    return True           
        elif choice == "EXIT":
            if yesno("Are you sure you wish to quit?"):
                #sys.exit("Goodbye")
                quit(0)
                return True
        elif choice == "ABOUT":
            RunGeneral(save,"about")
    return False

# 1-dimentional navigation (liniar to and from)
class RoomNav1D:
    ind = 0 #current location, index
    running = False #run-status on local game-loop. Also indicates if the nav has already been initiated.
    places = []
    termPlus = "GO PLUS"   #Should be changed in sub-class / implementation
    termMinus = "GO MINUS" #Should be changed in sub-class / implementation
    roomname = "BASE" #Must be changed in sub-class / implementation
    save = None
    @classmethod
    def GET_NAV(cls, save = None):
        if save == None:
            return cls()
        nav = save.getNav(cls.roomname)
        if not isinstance(nav, cls):
            nav = cls()
        save.setNav(nav)
        return nav


    def __init__(self):
        pass
        
    def getPlace(self):
        try:
            return self.places[self.ind]
        except:
            return (None, None, None)
    #runPlace, plus and minus can be overritten for flavor text and aditional function calls.
    def plus(self):
        self.ind += 1
    def minus(self):
        self.ind -= 1
    def runAction(self): #should be overwritten by sub-classes
        self.getPlace()[0]()
    #calls utility gameMenu. can be overritten.
    #returns value from gameMenu
    def openGameMenu(self, save): 
        return gameMenu(save)
    def loop(self, save):
        self.running = True
        while self.running:
            disp = "ERROR"
            action = " - "
            canPlus = False
            canMinus = False
            try:
                _, disp, action = self.getPlace()
                canMinus = self.ind > 0
                canPlus = self.ind < len(self.places)-1
            except:
                pass
            message = "You are now next to {0}, what will you do?".format(disp)
            choices = (
                ("PLUS", self.termPlus, "{0}({1})".format(self.termPlus, action), 1 if canPlus else 2),
                ("ACT", action, 1),
                ("MINUS", self.termMinus, "{0}({1})".format(self.termMinus, action), 1 if canMinus else 2),
                ("MENU", "(open game menu)")
                )
            _, choice = choose2(choices, message)
            if(choice == "MENU"):
                if self.openGameMenu(save):
                    return
                else:
                    continue
            elif choice == "PLUS":
                if canPlus:
                    self.plus()
                else:
                    self.runAction()
            elif choice == "MINUS":
                if canMinus:
                    self.minus()
                else:
                    self.runAction()
            else:
                self.runAction()



if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    showtext("Testcode for this utilities/common code is not written yet.\nPlease run from main.py instead.")