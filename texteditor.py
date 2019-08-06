import tkinter as TK
import tkinter.ttk as TTK
import tkentrycomplete as TKTC
from tkinter import messagebox as TKmsg
from tkinter import scrolledtext as TKS
import re
import xml
from xml.etree import cElementTree as ElementTree
import os
import sys

ENTRY_NAME_PATTERN = r'^[A-Z]+_(?:[0-9]|_|[A-Z])*$'

dummydata = {
    "TEST" : "Once opon a time there was a lot of text",
    "BEST"  : "There is always more text to be found..",
    "REST"  : "There can never be too much dummy data"
}
#Display language : internal language (filename)
langList = {"English" : "english"}


class Editor(TK.Frame):
    def __init__(self, root:TK.Tk):
        super().__init__(root)
        self.root:TK.Tk = root
        self.running = False
        self.langdata = {}
        self.openEntries = []

        self.langlabel = TK.Label(self, text = "Language")
        self.chooseLangBox = TKTC.AutocompleteCombobox(self)

        self.chooseLangBox.set_completion_list(list(langList.keys()))
        self.chooseLangBox.bind("<<ComboboxSelected>>", self.CheckSelected)

        self.chooseEntryLabel = TK.Label(self, text = "Entry")
        self.chooseEntryBox = TKTC.AutocompleteCombobox(self)

        self.openEntryBtn = TK.Button(self, command=self.OpenEntry, text = "Open Entry", state = TK.DISABLED)
        self.openAddEntry = TK.Button(self, command=self.NewEntry, text = "Add new entry", state = TK.DISABLED)

        self.chooseEntryBox.bind("<<ComboboxSelected>>", self.CheckSelected)

        self.seperators = (
            TTK.Separator(self, orient="horizontal"), #below entry/langauge box
        )

        self.editors = TK.Frame(self)
        #deplying

        self.langlabel.grid(row = 0, column = 0)
        self.chooseEntryLabel.grid(row = 0, column = 1)

        self.chooseLangBox.grid(row = 1, column = 0)
        self.chooseEntryBox.grid(row = 1, column = 1)

        self.openEntryBtn.grid(row = 2, column = 0)
        self.openAddEntry.grid(row = 2, column = 1)
        
        self.seperators[0].grid(row = 3)

        self.editors.grid(row = 4, columnspan = 2)

        self.grid_columnconfigure(index = 0, weight = 1)
        self.grid_columnconfigure(index = 1, weight = 1)
        self.grid_rowconfigure(index = 0, weight = 1)
    def OpenEntry(self, *_, **args):
        l = args.get("l",self.chooseLangBox.get())
        e = args.get("e", self.chooseEntryBox.get())
        if(self.CheckSelected()):
            newEditor = EntryEditor(self.editors, self, self.seldata, e, l)
            newEditor.pack(side = TK.RIGHT)
            self.openEntries.append(newEditor)
            self.openEntryBtn.config(state = TK.DISABLED)

        print("PLACEHOLDER: opens a new editor window for the selected entry")
    def NewEntry(self, event):
        print("PLACEHOLDER: Ads a new entry in the selected language, then opens a new editor window for the new entry")
        #adds new entry. asks if you want to add an empty entry for other langauges.
        l = self.chooseLangBox.get()
        e = self.chooseEntryBox.get()
        result = self.askName("NEW ENTRY", "What do you wish name the entry?", l, e)
        if result:
            self.seldata[result] = ""
        self.OpenEntry(l = l, e = e)

    def RenameEntry(self, language, prevtext):
        result = self.askName("RENAME ENTRY", f"What do you wish rename {prevtext} to?", language, prevtext)

    def askName(self, title, message, langauge, startText):
        askWindow = TK.Toplevel(master=self)
        askWindow.title(title)
        askMsg = TK.Label(askWindow, text=message)
        askMsg.pack()
        askAnswer = TK.StringVar(askWindow, value = startText)
        askInput = TK.Entry(askWindow, textvariable = askAnswer)
        askInput.pack()
        askButtons = TK.Frame(askWindow)
        askButtons.pack()
        askErr = TK.Label(askWindow, text="")
        askErr.pack()

        data = self.getdata(langauge)

        class Askdata:
            ret = None
            run = False
        askData = Askdata()
        
        def askOK():
            ans = askAnswer.get()
            if ans in data.keys():
                askErr.config(text="ERR: An entry with this name already exist.", fg = "orange")
            elif re.match(ENTRY_NAME_PATTERN, ans):
                askData.run = False
                askData.ret = ans
            else:
                askErr.config(text="Entry name must start with a capital letter, and must contain only capitals, underscore and numbers! eg: SPACESHIP_TALK_8", fg = "red")
        def askCANCEL():
            askData.run = False
            askData.ret = False
        askOKbtn = TK.Button(askButtons, text = "OK", command = askOK)
        askOKbtn.pack(side=TK.LEFT)
        askCANCELbtn = TK.Button(askButtons, text = "CANCEL", command = askCANCEL)
        askCANCELbtn.pack(side=TK.RIGHT)
        
        askData.run = True
        while askData.run:
            askWindow.update_idletasks()
            askWindow.update()
        askWindow.destroy()
        return askData.ret

    def CheckSelected(self, *_):
        l = self.chooseLangBox.get()
        e = self.chooseEntryBox.get()
        self.chooseEntryBox.set_completion_list(self.seldata.keys())
        if not langList.get(l):
            self.openEntryBtn.config(state = TK.DISABLED)
            self.openAddEntry.config(state = TK.DISABLED)
            return False
        self.openAddEntry.config(state = TK.NORMAL)
        if self.seldata.get(e):
            for o in self.openEntries:
                if o.language == l and o.entryname == e:
                    self.openEntryBtn.config(state = TK.DISABLED)
                    return False
            self.openEntryBtn.config(state = TK.NORMAL)
            return True
        elif(re.match(ENTRY_NAME_PATTERN, l)):
            self.openEntryBtn.config(state = TK.DISABLED)
            return True
        else:
            self.openEntryBtn.config(state = TK.DISABLED)
            return True
        print(f"Language{l} - entry {e}")
        return True

    def run(self):
        self.running = True
        while self.running:
            try:
                self.update()
                self.update_idletasks()
            except TK.TclError as err:
                print(err)
                self.running = False
    def savetodisk(self):
        pass
        #TODO write code to save to disk.
    
    #The current selcted data
    @property
    def seldata(self)->dict:
        l = self.chooseLangBox.get()
        return self.getdata(l)
    def getdata(self, lang):
        data = self.langdata.get(lang)
        if data == None:
            self.langdata[lang] = self.LoadLang(langList[lang])
            data = self.langdata[lang]
        return data
    
    @staticmethod
    def LoadLang(language:str):
        cwd = os.getcwd()
        try: #if True:
            tree = ElementTree.parse(cwd+"/nerrative/" + language + ".xml")
        except Exception as e:
            print ("Error loading language file {0}: {1}".format(language, e), file=sys.stderr)
            return {"ERROR" : "Error loading language file {0}: {1}".format(language, e)}
        story = {}
        for element in tree.iter():
            story[element.tag] = element.text.strip()
        return story

class EntryEditor(TK.Frame):
    def __init__(self, master, main:Editor, data, entryname, language):
        super().__init__(master)
        self.master = master
        self.data = data
        self.language = language
        self.entryname = entryname
        self.main = main

        self.closebtn = TK.Button(self, text = "CLOSE", bg = "red", command = self.closeme)
        self.namelabel = TK.Label(master=self, text = entryname)
        self.textfield = TKS.ScrolledText(self)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
        self.bind('<KeyRelease>', self.updateentry)
        self.savebtn = TK.Button(self, text = "SAVE", command = self.save, state = TK.DISABLED)

        self.liveUpdate = TK.BooleanVar()
        self.doLiveUpdate = TTK.Checkbutton(self, variable = self.liveUpdate, text = "Update text hash-table live")

        self.closebtn.pack()
        self.namelabel.pack()
        self.textfield.pack()
        self.savebtn.pack()
    def save(self):
        pass
        #self.entry = self.textfield.get('1.0', TK.END)
        #self.editor.savetodisk()
    def closeme(self):
        try:
            self.pack_forget()
            self.main.openEntries.remove(self)
        except:
            pass


    @property
    def entry(self):
        return self.data[self.entryname]
    @entry.setter
    def entry(self, val):
        self.data[self.entryname] = val


def start():

    #setup
    tkRoot = TK.Tk(screenName="Text resource editor")
    tkRoot.geometry("1600x900")
    editor = Editor(tkRoot)
    editor.grid()

    #running
    editor.run()

    #Cleanup
    editor.grid_forget()
    tkRoot.destroy()

if __name__ == "__main__":
    start()