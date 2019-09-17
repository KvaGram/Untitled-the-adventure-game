import os
import tkinter as TK
from tkinter import font as TKF
from tkinter import scrolledtext as TKS
from tkinter import messagebox as TKmsg
import tkentrycomplete as TKTC
import time
from typing import List
import ItemDB
from untitled_const import IMAGE_DIR, FALLBACK_ICON, SAVE_DIR, SAVE_FILETYPE

_INV_BG = "gray80"
class inventoryItem(TK.Frame):
    def __init__(self, root:TK.Tk, itemtype:ItemDB._ItemDB, retext:callable, **args):
        args["bg"] = _INV_BG
        self.retext = retext
        super(inventoryItem, self).__init__(master = root, **args)
        if itemtype:
            displayName = retext(itemtype.dName, {})
            displayImag = IMAGE_DIR + itemtype.image
            displayDesc = retext(itemtype.desc, {})
        else:
            displayName = "((ERROR))"
            displayImag = IMAGE_DIR + FALLBACK_ICON
            displayDesc = " - "
        try:
            self.imageData = TK.PhotoImage(file = displayImag)
        except Exception as err:
            print(err)
            self.imageData = TK.PhotoImage(file = IMAGE_DIR + FALLBACK_ICON)
        self.toplabel = TK.Label(master=self, text = displayName, bg = _INV_BG)
        self.midlabel = TK.Label(master=self, image = self.imageData, bg = _INV_BG)
        self.buttomlabel = TK.Label(master=self, text= displayDesc, bg = _INV_BG)
        
        self.toplabel.pack()
        self.midlabel.pack()
        self.buttomlabel.pack()

    def setItem(self, displayName:str, displayImag:str, displayDesc:str):
        self.toplabel = TK.Label(text = self.retext(displayName, {}))
        self.imageData.config(file = displayImag)
        self.buttomlabel = TK.Label(text= self.retext(displayDesc, {}))
class UntitledUI:
    def __init__(self, root:TK.Tk, retext:callable, **args):
        #main container, packed into parent (normally TK root)
        self.root:TK.Tk = root
        self.retext = retext
        self.main = TK.Frame(root)
        self.main.pack(fill = TK.BOTH, expand = True)
        self.queue = [] #:List[G.response]

        self.display = TK.Frame(master=self.main, background ="grey95")
        self.navtext = TK.Frame(master=self.main, background ="grey95")
        self.inventory = TK.Frame(master=self.main, background ="grey95")
        self.actions = TK.Frame(master=self.main, background ="grey95")
        self.navkeys = TK.Frame(master=self.main, background ="grey95")

        self.display.grid  (row = 0, column = 0, columnspan = 8, rowspan = 7, sticky = "news")
        self.navtext.grid  (row = 0, column = 8, columnspan = 2, rowspan = 1, sticky = "new")
        self.inventory.grid(row = 1, column = 8, columnspan = 2, rowspan = 9, sticky = "news")
        self.actions.grid  (row = 7, column = 0, columnspan = 6, rowspan = 3, sticky = "news")
        self.navkeys.grid  (row = 7, column = 6, columnspan = 2, rowspan = 3, sticky = "news")

        self.draw_display()
        #self.draw_actions()
        self.draw_noactions
        #self.draw_textinputs()
        self.draw_inventory()
        self.draw_navtext()
        self.draw_navkeys()
        self.draw_menu(**args)

        for i in range(10):
            self.main.grid_columnconfigure(index = i, weight = 1)
            self.main.grid_rowconfigure(index = i, weight = 1)

    def quit(self):
        self.root.quit()
        self.root.destroy()

    @staticmethod
    def emptyframe(frame:TK.Frame):
        for c in frame.winfo_children():
            c.grid_forget()
            c.pack_forget()
            c.destroy()
    def handleAction(self, data):
        self.queue.append(("action", data))
        print("DEBUG: Enqueued action input: " + str(data))

    def handleNav(self, data):
        self.queue.append(("nav", data))
        print("DEBUG: Enqueued nav input: " + str(data))

    def handleTextin(self, data):
        self.queue.append(("text", data))
        print("DEBUG: Enqueued text input: " + str(data))
    def handleGamemenu(self, data):
        self.queue.append(("game", data))
        print("DEBUG: Enqueued game menu command:" + str(data))
    def deqeue(self):
        if(len(self.queue) < 1):
            return False
        return self.queue.pop(0)

    def draw_display(self, **args):
        self.emptyframe(self.display)
        self.dispText = TKS.ScrolledText(master = self.display, state = TK.NORMAL, height = 60)
        self.dispText.pack(fill=TK.BOTH, expand = True, anchor="center")
        self.dispText.insert(TK.END, "")
        self.dispText.config(state = TK.DISABLED)
        self.dispText.configure(bg='black', fg='cyan')
        

    def writeToDisplay(self, text:str):
        self.dispText.config(state = TK.NORMAL)
        self.dispText.insert(TK.END, "\n" + text)
        self.dispText.yview_moveto("1.0")
        self.dispText.config(state = TK.DISABLED)
    def draw_noactions(self, **args):
        self.emptyframe(self.actions)
        #NOTE: might be an idea to add some filler.

    def draw_actions(self, **args):
        
        self.emptyframe(self.actions)
        self.actions.grid_rowconfigure(0, weight = 1)

        self.action_page:int = args.get("page", 0)
        reqActions:tuple = args.get("actions", (("YES", u"\u2713"), ("NO", u"\u2573")))
        reqLabel:str = args.get("label", "Choose")
        buttonfont:TKF.Font = args.get("buttonfont", TKF.Font())
        labelfont:TKF.Font = args.get("labelfont", TKF.Font())

        actionsFrame:TK.Frame = TK.Frame(master=self.actions)
        actionsFrame.grid(row = 0, column = 1, sticky="news")

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
            GRIDX = 2
            GRIDY = 4
            GRIDTOT = GRIDX * GRIDY

            #empties the the action button container and disables the page-buttons.
            btnLeft.config(state=TK.DISABLED)
            btnRight.config(state=TK.DISABLED)
            self.emptyframe(actionsFrame)

            #re-enables the page-buttons as appropriate
            if self.action_page > 0:
                btnLeft.config(state=TK.NORMAL)
            if ( (1+self.action_page) * GRIDTOT ) < fLength:
                btnRight.config(state=TK.NORMAL)
            
            #list of active actions (buttons to draw)
            #made by slicing the requested actions list, with respect to the current page.
            #only usefull for actions lists larger than GRIDTOT.
            aActions:list = reqActions[self.action_page*GRIDTOT:(self.action_page+1)*GRIDTOT]
            aLength:int = len(aActions)

        
            actionBtns:list = []
            label:TK.Label = TK.Label(master = actionsFrame, text = reqLabel, font = labelfont)
            for i in range(aLength):
                actionBtns.append(TK.Button(master=actionsFrame, font=buttonfont, text = aActions[i][1], command = lambda _i=i: self.handleAction((aActions[_i][0], _i + self.action_page*GRIDTOT))))
            if aLength <= GRIDY:
                actionsFrame.grid_columnconfigure(0, weight = 1)
                label.grid(row = 0, sticky="nsew")
                actionsFrame.grid_rowconfigure(0, weight = 3)
                for i in range(aLength):
                    actionBtns[i].grid(row = i + 1, sticky="nsew") 
                    actionsFrame.grid_rowconfigure(i, weight = 5)
            else:
                label.grid(row = 0, column = 0, columnspan = 2, sticky="nsew")
                for i in range(aLength):
                    row = int(i / GRIDX) + 1
                    column = i % GRIDX
                    actionBtns[i].grid(row=row, column=column, sticky="nsew")
                    actionsFrame.grid_rowconfigure(row+1, weight = 1)
                    actionsFrame.grid_columnconfigure(column, weight=1)
        draw_actionbuttons()

    def draw_textinputs(self, **args):
        self.emptyframe(self.actions)
        self.actions.grid_rowconfigure(0, weight = 1)
        reqFields = args.get("fields", (("Input", ""),))
        fieldfont = args.get("fieldfont", TKF.Font())
        labelfont = args.get("labelfont", TKF.Font())
        entertext = args.get("entertext", "ENTER")
        enterfont = args.get("enterfont", TKF.Font())
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
            self.handleTextin(ret)
        btnEnter = TK.Button(master=self.actions, text=entertext, font=enterfont, command=packnsend)
        btnEnter.grid(row=length, column=0, columnspan=3, sticky="nsew")

    def draw_inventory(self, **args):
        itemlist = args.get("itemlist", {})
        self.emptyframe(self.inventory)
        self.itemObjects = []

        for itemtype, value in itemlist.items():
            i = len(self.itemObjects)
            if not value:
                continue
            row = int(i/2)
            column = i%2
            item = inventoryItem(self.inventory, ItemDB.GET(itemtype), self.retext)
            item.grid(row = row, column = column, padx = 1, pady = 1, sticky="new")
            self.inventory.grid_rowconfigure(index = row, weight=1)
            self.inventory.grid_columnconfigure(index = column, weight=1)
    def draw_navtext(self, **args):
        self.emptyframe(self.navtext)
        self.navTextDisplay = TK.Text(master = self.navtext, width = 20, height = 8)
        self.navTextDisplay.pack(fill= TK.BOTH)
        self.navTextDisplay.insert(TK.END, "dummy area\ndummy place\ndoing dummy things...")
        self.navTextDisplay.config(state = TK.DISABLED)
    def set_navtext(self, text:str):
        self.navTextDisplay.config(state = TK.NORMAL)
        self.navTextDisplay.delete("1.0", TK.END)
        self.navTextDisplay.insert(TK.END, text)
        self.navTextDisplay.config(state = TK.DISABLED)
    def draw_navkeys(self, **args):
        self.emptyframe(self.navkeys)
        

        self.nav_left  = NavButton(master = self.navkeys, command= lambda: self.handleNav("left"))
        self.nav_up    = NavButton(master = self.navkeys, command= lambda: self.handleNav("up"))
        self.nav_45    = NavButton(master = self.navkeys, command= lambda: self.handleNav("45"))
        self.nav_right = NavButton(master = self.navkeys, command= lambda: self.handleNav("right"))
        self.nav_down  = NavButton(master = self.navkeys, command= lambda: self.handleNav("down"))

        #self.nav_45.grid(row=0, column=2, sticky="nsew")
        self.nav_left.grid(row=1, column=0, sticky="nsew")
        self.nav_up.grid(row=0, column=1, sticky="nsew")
        self.nav_right.grid(row=1, column=2, sticky="nsew")
        self.nav_down.grid(row=2, column=1, sticky="nsew")

        self.navkeys.grid_columnconfigure(index = 0, weight = 1)
        self.navkeys.grid_columnconfigure(index = 1, weight = 1)
        self.navkeys.grid_columnconfigure(index = 2, weight = 1)
        self.navkeys.grid_rowconfigure(index = 0, weight = 1)
        self.navkeys.grid_rowconfigure(index = 1, weight = 1)
        self.navkeys.grid_rowconfigure(index = 2, weight = 1)

        self.conf_navkeys(**args)
    def conf_navkeys(self, **args):
        state_left  = TK.NORMAL if args.get("left",  False) else TK.DISABLED
        state_up    = TK.NORMAL if args.get("up",    False) else TK.DISABLED
        state_right = TK.NORMAL if args.get("right", False) else TK.DISABLED
        state_down  = TK.NORMAL if args.get("down",  False) else TK.DISABLED

        text_left  = args.get("text_left",  u"GO LEFT\n\u2190")
        text_up    = args.get("text_up",    u"GO UP\n\u2191")
        text_right = args.get("text_right", u"GO RIGHT\n\u2192")
        text_down  = args.get("text_down",  u"GO DOWN\n\u2193")
        text_upright = u"GO 45\n\u2197"
        font       = args.get("font", TKF.Font(family = "Consolas", size=15))

        self.nav_left  .config(font = font, text = text_left, state = state_left)
        self.nav_up    .config(font = font, text = text_up, state = state_up)
        self.nav_right .config(font = font, text = text_right, state = state_right)
        self.nav_down  .config(font = font, text = text_down, state = state_down)
        self.nav_45    .config(font = font, text = text_upright)
    def draw_menu(self, **args):
        def voidcall():
            TKmsg.showinfo("Sorry", "Sorry!\nSomething went wrong\nor this is just a placeholder.")
        saveCall = args.get("savecall", voidcall)
        loadCall = args.get("loadcall", voidcall)
        newCall = args.get("newcall", voidcall)

        rootmenu = TK.Menu(tearoff = False)
        gamemenu = TK.Menu(tearoff = False)
        rootmenu.add_cascade(label="Game", menu = gamemenu)
        gamemenu.add_command(label="Save", command=saveCall)
        gamemenu.add_command(label="Load", command=loadCall)
        gamemenu.add_command(label="New Game", command=newCall)
        
        

        self.menu_root = rootmenu
        self.menu_game = gamemenu
        self.root.config(menu = rootmenu)
    def askSaveFile(self, loadMode:bool):
        class AskData:
            running:bool = True
            ret:tuple = None
        askData = AskData()
        sel = None

        savefiles = []
        savedir = os.path.join(os.getcwd(), SAVE_DIR)
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        for _, _, f in os.walk(savedir):
            for file in f:
                if SAVE_FILETYPE in file:
                    savefiles.append(file.replace(SAVE_FILETYPE, ""))
        

        def onOK():
            if loadMode and not getExists():
                err.config(text="File not found")
                return
            if not loadMode and len(sel.get()) < 1:
                err.config(text="Filename not valid")
                return
            askData.ret = (getFullPath(), getExists())
            askData.running = False

        def onCancel():
            askData.ret = False
            askData.running = None
        def getFullPath():
            return os.path.join(savedir, sel.get() + SAVE_FILETYPE)
        def getExists():
            return sel.get() in savefiles
        
        askwindow = TK.Toplevel(master=self.root)
        
        if (loadMode):
            sel = TKTC.AutocompleteCombobox(askwindow)
            askwindow.title("Load Game")
        else:
            sel = TKTC.AutocompleteEntry(askwindow)
            askwindow.title("Save Game")
        sel.set_completion_list(savefiles)

        sel.grid(column = 0, row = 0, columnspan = 3)
        TK.Label (master = askwindow, text = SAVE_FILETYPE).grid(column = 3, row = 0)
        err = TK.Label(master = askwindow, text = "", fg = "red")
        err.grid(row = 1, column = 0, columnspan = 4)
        TK.Button(master = askwindow, text = "OK", command = onOK).grid(row = 2, columnspan = 2)
        TK.Button(master = askwindow, text = "CANCEL", command = onCancel).grid(row = 2, column = 2, columnspan = 2)

        while(askData.running):
            askwindow.update_idletasks()
            askwindow.update()
        askwindow.destroy()
        return askData.ret


class NavButton(TK.Button):
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
    def config(self, cnf=None, **kw):
        if kw.get("state") == TK.NORMAL:
            kw["bg"] = "white"
        elif kw.get("state") == TK.DISABLED:
            kw["bg"] = "gray60"
        else:
            kw["bg"] = "gray"
        super().config(cnf, **kw)

def testUI():
    tkRoot = TK.Tk(screenName="UNTITLED! The adventure game")
    tkRoot.geometry("1280x720")
    def dummyretext(text, *_,**__):
        return text
    UI:UntitledUI = UntitledUI(tkRoot, dummyretext)

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

if __name__ == "__main__":
    testUI()