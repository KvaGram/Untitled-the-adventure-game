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

#Display language : internal language (filename)
langList = {"English" : "english", "Testlang Alpha" : "test1", "Testlang Beta" : "test2"}


class old_Editor(TK.Frame):
    def __init__(self, root:TK.Tk):
        super().__init__(root)
        self.root:TK.Tk = root
        self.running = False
        self.langdata = {}
        self.openEntries = []
        self._langSaved = {}
        for k in langList.keys():
            self._langSaved[k] = True

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
    def OpenEntry(self, **args):
        l = args.get("l",self.chooseLangBox.get())
        e = args.get("e", self.chooseEntryBox.get())
        if(self.CheckSelected(l = l, e = e)):
            newEditor = old_EntryEditor(self.editors, self, self.seldata, e, l)
            newEditor.pack(side = TK.RIGHT)
            self.openEntries.append(newEditor)
            self.openEntryBtn.config(state = TK.DISABLED)
    def NewEntry(self):
        print("PLACEHOLDER: Ads a new entry in the selected language, then opens a new editor window for the new entry")
        #adds new entry. asks if you want to add an empty entry for other langauges.
        l = self.chooseLangBox.get()
        e = self.chooseEntryBox.get()
        result = self.askName("NEW ENTRY", "What do you wish name the entry?", l, e)
        if result:
            self.seldata[result] = ""
        self.OpenEntry(l = l, e = result)

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
                askErr.config(text="Entry name must\n * Start with a capital letter\n * Contain only capitals, underscore and numbers\n - eg: SPACESHIP_TALK_8", fg = "red")
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

    def CheckSelected(self, *_, **args):
        l = args.get("l",self.chooseLangBox.get())
        e = args.get("e", self.chooseEntryBox.get())
        self.chooseEntryBox.set_completion_list(self.seldata.keys())
        if not langList.get(l):
            self.openEntryBtn.config(state = TK.DISABLED)
            self.openAddEntry.config(state = TK.DISABLED)
            return False
        self.openAddEntry.config(state = TK.NORMAL)
        if self.seldata.get(e) != None:
            for o in self.openEntries:
                if o.language == l and o.entryname == e:
                    self.openEntryBtn.config(state = TK.DISABLED)
                    return False
            self.openEntryBtn.config(state = TK.NORMAL)
            return True
        else:
            self.openEntryBtn.config(state = TK.DISABLED)
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
    def setLangSaved(self, langauge, val):
        self._langSaved[langauge] = val
        for e in self.openEntries:
            if not e.language == langauge:
                continue
            if val:
                e.savebtn.config(state = TK.NORMAL)
            else:
                e.savebtn.config(state = TK.DISABLED)
    
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

class old_EntryEditor(TK.Frame):
    def __init__(self, master, main:old_Editor, data, entryname, language):
        super().__init__(master)
        self.master = master
        self.data = data
        self.language = language
        self.entryname = entryname
        self.main:old_Editor = main

        self.buttongroup = TK.Frame(self)

        self.closebtn = TK.Button(self.buttongroup, text = "CLOSE", bg = "red", command = self.closeme)
        self.renamebtn = TK.Button(self.buttongroup, text = "RENAME", bg = "yellow", command = self.RenameEntry)
        self.deletebtn = TK.Button(self.buttongroup, text = "DELETE", bg = "red4", command = self.DelMe)

        self.namelabel = TK.Label(master=self, text = entryname)
        self.textfield = TKS.ScrolledText(self)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
        self.textfield.bind('<KeyRelease>', self.updateentry)
        self.savebtn = TK.Button(self, text = "SAVE", command = self.save, state = TK.DISABLED)

        #self.liveUpdate = TK.BooleanVar()
        #self.doLiveUpdate = TTK.Checkbutton(self, variable = self.liveUpdate, text = "Update text hash-table live")

        self.buttongroup.pack()
        self.closebtn.pack(side = TK.RIGHT)
        self.renamebtn.pack(side = TK.RIGHT)
        self.deletebtn.pack(side = TK.RIGHT)

        self.namelabel.pack()
        self.textfield.pack()
        self.savebtn.pack()
    def save(self):
        self.main.savefile(self.language)
    def closeme(self):
        self.entry = self.textfield.get('1.0', TK.END)
        try:
            self.pack_forget()
            self.main.openEntries.remove(self)
        except:
            pass
        self.main.CheckSelected()
    def RenameEntry(self):

        result = self.main.askName("RENAME ENTRY", f"What do you wish rename {self.entryname} to?", self.language, self.entryname)
        if not result:
            return
        self.data[result] = self.entry
        self.data.pop(self.entryname, None)
        self.entryname = result
        self.namelabel.config(text = result)
        self.main.CheckSelected()
    def DelMe(self):
        if not TKmsg.askquestion("Delete entry?", f"Are you sure you to delete {self.entryname} from the {self.language} language-file?"):
            return
        self.data.pop(self.entryname, None)
        try:
            self.pack_forget()
            self.main.openEntries.remove(self)
        except:
            pass
        self.main.CheckSelected()
    def asksaveiflast(self):
        if self.saved:
            return
        for e in self.main.openEntries:
            if e == self:
                continue
            if e.language == self.language:
                return
        if TKmsg.askyesno("Save file?", f"Save langaugefile {self.language}?"):
            self.save()

    @property
    def saved(self):
        return self.main._langSaved[self.language]
    @saved.setter
    def saved(self, val):
        self.main.setLangSaved(self.language, val)
    @property
    def entry(self):
        return self.data[self.entryname]
    @entry.setter
    def entry(self, val):
        self.data[self.entryname] = val

    def updateentry(self, evt):
        if False:#not self.liveUpdate.get():
            return
        self.saved = False
        self.entry = self.textfield.get('1.0', TK.END)

#static class for common data.
class Data():
    editors = []
    langstory = {}
    langEdited = {}
    root = None

def OpenEditor(lang:str, entry:str):
    for e in Data.editors:
        if e.entryName == entry and e.lang == lang:
            e.lift()
            return
    Data.editors.append(Editor(lang, entry))

def NewEntry(lang:str, openNew:bool, entry):
    Data.langstory.get(lang, {})[entry] = " "
    if openNew:
        OpenEditor(lang, entry)
def AskNewEntry(lang:str, openNew:bool = True, entry = ""):
    entry = askName("NEW ENTRY", "What do you wish name the entry?", lang, entry)
    if entry:
        return NewEntry(lang, openNew, entry)
    return entry

def askName(title, message, lang, startText):
    askWindow = TK.Toplevel(Data.root)
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

    story = Data.langstory.get(lang, {})

    class Askdata:
        ret = None
        run = False
    askData = Askdata()
    
    def askOK():
        ans = askAnswer.get()
        if ans in story.keys():
            askErr.config(text="ERR: An entry with this name already exist.", fg = "orange")
        elif re.match(ENTRY_NAME_PATTERN, ans):
            askData.run = False
            askData.ret = ans
        else:
            askErr.config(text="Entry name must\n * Start with a capital letter\n * Contain only capitals, underscore and numbers\n - eg: SPACESHIP_TALK_8", fg = "red")
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

class Editor(TK.Toplevel):
    def __init__(self, lang:str, entryName:str):
        super().__init__(Data.root)
        self._lang = lang
        self._entryName = entryName

        self.protocol("WM_DELETE_WINDOW", self.OnClose)

        #Building menu
        menu = TK.Menu(self)
        self.config(menu = menu)
        fileMenu = TK.Menu(menu)
        editMenu = TK.Menu(menu)
        menu.add_cascade(label = "file", menu=fileMenu)
        menu.add_cascade(label = "edit", menu=editMenu)

        fileMenu.add_command(label = "New Entry", command=self.OnNewEntry)
        fileMenu.add_command(label = "VOID", command=None)
        fileMenu.add_command(label = "VOID", command=None)
        fileMenu.add_command(label = "VOID", command=None)

        editMenu.add_command(label = "VOID", command=None)
        editMenu.add_command(label = "VOID", command=None)
        editMenu.add_command(label = "VOID", command=None)
        editMenu.add_command(label = "VOID", command=None)

        #manu refrence
        self.menu = ({
        'root':menu,
        'file':fileMenu,
        'edit':editMenu
        })

        #building UI
        self.selectionZone = TK.Frame(self)
        self.selectionZone.pack()

        self.langlabel = TK.Label(self.selectionZone, text = "Language")
        self.chooseLangBox = TKTC.AutocompleteCombobox(self.selectionZone)
        self.chooseLangBox.set_completion_list(list(langList.keys()))
        self.chooseLangBox.bind("<<ComboboxSelected>>", self.SetLang)

        self.chooseEntryLabel = TK.Label(self.selectionZone, text = "Entry")
        self.chooseEntryBox = TKTC.AutocompleteCombobox(self.selectionZone)
        self.chooseEntryBox.bind("<<ComboboxSelected>>", self.SetEntry)
        self.chooseEntryBox.set_completion_list(list(self.Story.keys()))

        self.langlabel.grid(row = 0, column = 0)
        self.chooseEntryLabel.grid(row = 0, column = 1)

        self.chooseLangBox.grid(row = 1, column = 0)
        self.chooseEntryBox.grid(row = 1, column = 1)

        self.textfield = TKS.ScrolledText(self)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.bind('<KeyRelease>', self.updateentry)

        self.textfield.pack()

        TK.Label(self, text = "Tip: you can copy-paste the text using keyboard shortcuts.\nthis way you can use external programs for spell checks.", fg = "gray").pack()
        #last fix..
        self.resetTextfield()
        self.resetSelectors()
        self.setTitle()

    def OnClose(self):
        if TKmsg.askyesno("Close window?", "Are you sure you want to close this editorwindow?"):
            Data.editors.remove(self)
            self.destroy()

    def OnNewEntry(self):
        AskNewEntry(self._lang)
    def updateentry(self, evt=None):

        Data.langEdited[self.lang] = True
        self.entry = self.textfield.get('1.0', TK.END)

    def SetLang(self, evt=None):
        lang = self.chooseLangBox.get()
        en = self._entryName
        if lang == self.lang:
            return
        d = Data.langstory.get(lang, None)
        if d == None:
            TKmsg.showwarning("NOT VALID LAGUAGE", "Langauge selected is not valid.")
            self.resetSelectors()
            return
        if d.get(en, None) == None:
            if TKmsg.askyesno("NO ENTRY FOUND", f"The entry {en} was not found in {lang}.\nWould you like to add it?"):
                NewEntry(lang, False, en)
            else:
                self.resetSelectors()
                return
        if self.edited:
            if TKmsg.askyesno("SAVE?", f"You have unsaved changes!\nDo you wish to save the {self._lang} languagefile before switching langauge?"):
                self.save()
        self._lang = lang
        self._entryName = en
        self.resetTextfield()
        self.resetSelectors()
        self.setTitle()
    def SetEntry(self, evt=None):
        en = self.chooseEntryBox.get()
        if en == self._entryName:
            return
        entry = self.Story.get(en, None)
        if entry == None:
            if TKmsg.askyesno("NO ENTRY FOUND", f"The entry {en} was not found.\nDo you wish to create it?"):
                NewEntry(self._lang, False, en)
            else:
                pass
            self.resetSelectors()
            return
        self._entryName = en
        self.resetSelectors()
        self.resetTextfield()
        self.setTitle()
    def resetTextfield(self):
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
    def resetSelectors(self):
        self.chooseLangBox.set(self._lang)
        self.chooseEntryBox.set(self._entryName)
        self.chooseEntryBox.set_completion_list(list(self.Story.keys()))
    def setTitle(self):
        self.title(f"Untitled! Storytext editor - {self._lang} - {self._entryName}")
    def save(self):
        NotAddedYet()
    @property
    def lang(self)->str:
        return self._lang
    @property
    def entryName(self)->str:
        return self._entryName
    @property
    def entry(self)->str:
        return self.Story.get(self._entryName, "")
    @entry.setter
    def entry(self, val):
        self.Story[self._entryName] = val
    @property
    def Story(self)->dict:
        return Data.langstory.get(self._lang, {})
    @property
    def edited(self)->bool:
        return Data.langEdited[self._lang]
    



def start():
    root = TK.Tk()
    root.withdraw()

    cwd = os.getcwd()
    for k, l in langList.items():
        try: #if True:
            tree = ElementTree.parse(cwd+"/nerrative/" + l + ".xml")
        except Exception as e:
            err = f"Error loading language file {l}: {e}"
            TKmsg.showerror("LOADING-ERROR", err)
            print (err, file=sys.stderr)
            continue #if it fails, tell the user, and skip this one.        
        story = {}
        for element in tree.iter():
            if element.tag == 'story':
                continue #do not store the top-level element
            story[element.tag] = element.text.strip()
        Data.langstory[k] = story
        Data.langEdited[k] = False
    
    if len(Data.langstory) < 1:
        if TKmsg.askokcancel(icon = TKmsg.ERROR, title="NO DATA ERROR!", message="""
        No story datafile were found!
        If there was an error during loading,
        you may want to exit this program, and manually fix the issue.
        Alternativly: do you wish to create an empty langauge file?
        """.strip()):
            NotAddedYet()
        else:
            pass
        root.quit() #to be moved to the else-branch above when adding new language files are supported.
        return
    startlang = list(langList)[0]
    if len(Data.langstory[startlang]) < 1:
        if TKmsg.askokcancel(icon = TKmsg.ERROR, title="NO DATA ERROR!", message=f"""
        No story-entries were found!
        If there was an error during loading,
        you may want to exit this program, and manually fix the issue.
        Alternativly: do you wish to create a new entry in {startlang}?
        """.strip()):
            NotAddedYet()
        else:
            pass
        root.quit() #To be moved to else branch once above action is supported.
        return
    startEntry = list(Data.langstory[startlang].keys())[0]

    OpenEditor(startlang, startEntry)

    while True:
        root.update()
        root.update_idletasks()
        if len(Data.editors) < 1:
            root.quit()
            return

    


def NotAddedYet():
    TKmsg.showwarning("WOOPS..","Sorry, that feature is not added yet.\nPlease be impatient.\nI am very lazy, and need the pressure.")





    #old stuff, kept for refrence till everything is redone
    return

    #setup
    tkRoot = TK.Tk(screenName="Text resource editor")
    tkRoot.geometry("400x300")
    editor = Editor(tkRoot)
    editor.grid()

    #running
    editor.run()

    #Cleanup
    editor.grid_forget()
    tkRoot.destroy()

if __name__ == "__main__":
    start()