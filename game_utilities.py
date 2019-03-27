#this script binds together all scripts such as all others can access each other in a global scope
import sys
import tkinter as tk
from tkinter import filedialog
import time
import random

#This is a map of functions that can be called at any time.
def RunGeneral(save, call):
    if call == "onReactorCTime":
        return onReactorCTime(save)
    return "NOT FOUND"

def loadGame():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    showtext(file_path)
    #TODO try convert textfile to save-file, and load latest room
    return {}

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
    dispList = (None,) * length #initiate fixed length list with empty elements
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
        if(inp[0] == "t" or inp[0] == "T"):
            return True
        elif(inp[0] == "f" or inp[0] == "F"):
            return False        

def rolltext(txt, linepause = 0.1):
    lines = txt.splitlines()
    for l in lines:
        showtext(l)
        time.sleep(linepause)
def showtext(text = ""):
    print(text) # placeholder, in case game upgraded to use pygame

def getGenderedTerm(term, gender):
    if term == "spouse":
        if gender == "male":
            return "husbond"
        elif gender == "female":
            return "wife"
        else:
            return gender + " " + term #fallback
    if term == "sibling":
        if(gender == "male"):
            return "brother"
        elif term == "female":
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
    

#TODO consider moving general functions to its own module
def onReactorCTime(save):
    enabled, time = save.getCounter("reactorC")
    if not enabled:
        return "safe"
    if time <= 0:
        showtext("Placeholder - something something you just died due to a reactor meltdown!")
        setGameover(save, "You wasted too much time! You're kinda dead now")
        return "death"
    return "safe"
def setGameover(save, reason):
    save.setdata("GAME OVER", reason)
#common data
def hasGender(save):
    return save.getData("gender") != None
def hasName(save):
    return save.getData("name") != None
def hasKlara(save):
    return save.getData("klara") != None
def hasJeff(save):
    return save.getData("jeff") != None

#get common data, randomize if not defined.
def getGender(save):
    if hasName(save):
        return save.getData("gender")
    else:
        return save.getdata("gender", random.choice(("male", "female")))
def getName(save):
    return save.getdata("name", "The nameless one")
def getKlara(save, gendered = False):
    if gendered:
        return getGenderedTerm(getKlara(save, False), "female")
    if hasKlara(save):
        return save.getData("klara")
    elif hasJeff(save):
        return save.getData("klara", termCounterpart(getJeff(save)))
    else:
        return save.getdata("klara", random.choice(("spouse", "sibling")))
    
def getJeff(save, gendered = False):
    if gendered:
        return getGenderedTerm(getJeff(save, False), "male")
    if hasJeff(save):
        return save.getData("jeff")
    elif hasKlara(save):
        return save.getData("jeff", termCounterpart(getKlara(save)))
    else:
        return save.getdata("jeff", random.choice(("spouse", "sibling")))

# 1-dimentional navigation (liniar to and from)
class RoomNav1D:
    ind = 0 #current location, index
    running = True #run-status on local game-loop
    places = []
    termPlus = "GO PLUS"
    termMinus = "GO MINUS"
    onSelect = None
    def getPlace(self):
        try:
            return (places[ind])
        except:
            return (None, None, None)
    def __init__(self, termPlus = "GO PLUS", termMinus = "GO MINUS"):
        self.termPlus = termPlus
        self.termMinus = termMinus
    #runPlace is expected to be overitten by child classes
    def runAction(self):
        self.getPlace()[0]()
    def loop(self):
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
                ("MINUS", self.termMinus, "{0}({1})".format(self.termMinus, action), 1 if canMinus else 2)
                )
            _, choice = choose2(choices, message)
            if choice == "PLUS":
                if canPlus:
                    self.ind += 1
                else:
                    self.runAction()
            elif choice == "MINUS":
                if canMinus:
                    self.ind -= 1
                else:
                    self.runAction()
            else:
                self.runAction()



if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this utilities/common code is not written yet.\nPlease run from main.py instead.")