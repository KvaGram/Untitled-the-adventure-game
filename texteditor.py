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
from scrollFrame import VerticalScrollFrame

ENTRY_NAME_PATTERN = r'^[A-Z]+(?:[0-9]|_|[A-Z])*$'
SEPERATOR = "_"

#Display language : internal language (filename)
langList = {"English" : "english", "Testlang Alpha" : "test1", "Testlang Beta" : "test2"}

#static class for common data.
class Data():
    editors = []
    langstory = {}
    langEdited = {}
    root = None

def SplitGroupSubentry(entryname:str):
    
    segs = entryname.split(SEPERATOR)
    subentry = segs.pop(-1)
    groupname = SEPERATOR.join(segs)

    return (groupname, subentry)
    
def GetGroupList(lang:str):
    #TODO GetGroupList
    #placeholder data
    return ["foo", "bar", "foobar"]

def GetEntriesByGroup(lang:str, groupname:str):
    #TODO GetEntriesByGroup
    #placeholder data
    NUM_TEST_SAMPLE = 12
    storykeys = Data.langstory.get(lang, {}).keys()
    k2 = []
    for k in storykeys:
        k2.append(k)
        if len(k2) >= NUM_TEST_SAMPLE:
            break
    return k2
        

def CloseAll():
    e:SingleEditor
    for e in reversed(Data.editors):
        e.OnClose()

def askOpenEditor():
    askwindow = TK.Toplevel(Data.root)
    askwindow.title("Open entry")
    running = TK.BooleanVar(askwindow, True)
    def onOpen(*_):
        if not validate():
            return
        OpenEditor(sel.Language, sel.Entry)
        #askwindow.destroy()
        running.set(False)
    def onClose(*_):
        #askwindow.destroy()
        running.set(False)
    openbtn = TK.Button(askwindow, text = "OPEN", command = onOpen)
    closebtn = TK.Button(askwindow, text = "CLOSE", command = onClose)
    def onLang(*_):
        sel.EntryList = Data.langstory.get(sel.Language, {}).keys()
        validate()
    def validate(*_):
        lang = sel.Language
        entry = sel.Entry
        e = Data.langstory.get(lang, {}).get(entry, None)
        if e == None or checkEntryOpen(lang, entry):
            openbtn.config(state = TK.DISABLED)
            return False
        
        openbtn.config(state = TK.NORMAL)
        return True
    sel = EntrySelector(askwindow, onLang, validate)
    sel.grid(row = 0, column = 0, columnspan=2)
    openbtn.grid(row = 1, column = 0)
    closebtn.grid(row = 1, column = 1)
    validate()

    while(running.get()):
        askwindow.update()
        askwindow.update_idletasks()
    askwindow.destroy()
def checkEntryOpen(lang:str, entry:str):
    return False #TODO: write the check entry open function

    

def OpenEditor(lang:str, entry:str):
    for e in Data.editors:
        if e.entryName == entry and e.lang == lang:
            e.lift()
            return
    Data.editors.append(SingleEditor(lang, entry))
    

def NewEntry(lang:str, openNew:bool, entry):
    Data.langstory.get(lang, {})[entry] = " "
    Data.langEdited[lang] = True
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

class EntryText(TK.Frame):
    def __init__(self, master, TargetEntry:str, lang:str):
        super().__init__(master=master)
        self.label = TK.Label(master=self, text = TargetEntry)
        self.textfield = TKS.ScrolledText(self, width = 60, height = 3)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.bind('<KeyRelease>', self.updateentry)
        self.lang = lang
        self.TargetEntry = TargetEntry

        self.label.pack()
        self.textfield.pack()

    def updateentry(self, evt=None):
        Data.langEdited[self.lang] = True
        self.entry = self.textfield.get('1.0', TK.END)
    @property
    def entry(self)->str:
        return self.Story.get(self.TargetEntry, "")
    @entry.setter
    def entry(self, val):
        self.Story[self.TargetEntry] = val
    @property
    def Story(self)->dict:
        return Data.langstory.get(self.lang, {})
class EntrySelector(TK.Frame):
    def __init__(self, master, onLangSelect, onEntrySelect):
        super().__init__(master)

        self.langlabel = TK.Label(self, text = "Language")
        self.LangBox = TKTC.AutocompleteCombobox(self)
        self.LangBox.set_completion_list(list(langList.keys()))
        self.LangBox.bind("<<ComboboxSelected>>", onLangSelect)

        self.EntryLabel = TK.Label(self, text = "Entry")
        self.EntryBox = TKTC.AutocompleteCombobox(self, width = 80)
        self.EntryBox.bind("<<ComboboxSelected>>", onEntrySelect)
        self.selectionSep = TTK.Separator(self, orient="vertical")
        
        self.langlabel.grid(row = 0, column = 0)
        self.EntryLabel.grid(row = 0, column = 3, columnspan = 2)
        self.selectionSep.grid(row = 0, column = 1, rowspan=2, sticky = "news")
        self.LangBox.grid(row = 1, column = 0)
        self.EntryBox.grid(row = 1, column = 3, columnspan = 2)

    def reset(self, lang, entry, entrylist):
        self.Language = lang
        self.Entry = entry
        self.EntryBox.set_completion_list(entrylist)
    
    @property
    def Entry(self):
        return self.EntryBox.get()
    @property
    def Language(self):
        return self.LangBox.get()
    @property #becouse python @property NEEDS a get function to have a set function... :/
    def EntryList(self):
        return self.EntryBox._completion_list
    @Entry.setter
    def Entry(self, val):
        self.EntryBox.set(val)
    @Language.setter
    def Language(self, val):
        self.LangBox.set(val)
    @EntryList.setter
    def EntryList(self, val):
        self.EntryBox.set_completion_list(val)

class EditorType:
    NONE = 0 #not set
    SINGLE = 1
    MULTI = 2

class BaseEditor(TK.Toplevel):
    def __init__(self, lang, targetname:str, editortype):
        super().__init__(Data.root)
        self._lang = lang
        self._targetName = targetname
        self.editortype = editortype
        self.protocol("WM_DELETE_WINDOW", self.OnClose)

        self.buildMenu()
        self.tooltip = TK.Label(self, text = "Tip: you can copy-paste the text using keyboard shortcuts.\nthis way you can use external programs for spell checks.", fg = "gray")
        self.tooltip.pack(side=TK.BOTTOM)
        
        self.setTitle()
        self.lift()
    def buildMenu(self):
        menu = TK.Menu(self)
        self.config(menu = menu)
        fileMenu = TK.Menu(menu)
        editMenu = TK.Menu(menu)
        menu.add_cascade(label = "file", menu=fileMenu)
        menu.add_cascade(label = "edit", menu=editMenu)

        fileMenu.add_command(label = "open", command=askOpenEditor)
        fileMenu.add_command(label = "Save language file", command=self.save)
        fileMenu.add_command(label = "Save all", command=saveAll)
        fileMenu.add_command(label = "New Entry", command=self.OnNewEntry)
        fileMenu.add_command(label = "Close", command=self.OnClose)
        fileMenu.add_command(label = "Close All", command=CloseAll)


        #menu refrence
        self.menu = ({
        'root':menu,
        'file':fileMenu,
        'edit':editMenu
        })
    def OnClose(self):
        #if there are unsaved changes.
        asksave = self.edited
        if asksave:
            #if no other entries uses thing langauge file
            for e in Data.editors:
                if e == self:
                    continue
                if e.lang == self.lang:
                    asksave = False
                    break
        #then ask the user if they wish to save first.
        if asksave:
            ans = TKmsg.askyesnocancel(f"Do you wish to close {self._targetName}?", f"You may have unsaved changes, and this is the last open editor in {self.lang}")
            if ans == None:
                return #this is the cancel option. Here the entry is not closed after all.
            if ans == True:
                self.save()
            #if ans is False, "NO", then proceed with closing without saving.
        
        #removes refrence
        Data.editors.remove(self)
        #destroys entry / window
        self.destroy()
    def setTitle(self):
        self.title(f"Untitled! Storytext editor - {self._lang} - {self._targetName}")
    def OnNewEntry(self):
        AskNewEntry(self._lang)
    def save(self):
        print("Please don't use this abstrct base class.")
    @property
    def lang(self)->str:
        return self._lang

    @property
    def Story(self)->dict:
        return Data.langstory.get(self._lang, {})
    @property
    def edited(self)->bool:
        return Data.langEdited[self._lang]
class MultiEditor(BaseEditor):
    def __init__(self, lang:str, groupName:str):
        super().__init__(lang, groupName)

        entrylist = GetEntriesByGroup(lang, groupName)

        #TODO: continue work from here!

class SingleEditor(BaseEditor):
    def __init__(self, lang:str, entryName:str):
        super().__init__(lang, entryName, EditorType.SINGLE)

        self.menu['edit'].add_command(label = "Switch to multiedit", command = self.OnMultiMode)

        #building UI

        self.selectors = EntrySelector(self, self.SetLang, self.SetEntry)
        self.selectors.reset(self.lang, self.entryName, self.Story.keys())
        self.selectors.pack()

        self.textfield = TKS.ScrolledText(self, width = 60)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.bind('<KeyRelease>', self.updateentry)

        self.textfield.pack(fill="both")

        #last fix..
        self.resetTextfield()
        self.resetSelectors()

    def OnMultiMode(self):
        #TODO open new entry in multimode
        pass
    def updateentry(self, evt=None):
        Data.langEdited[self.lang] = True
        self.entry = self.textfield.get('1.0', TK.END)

    def SetLang(self, evt=None):
        lang = self.selectors.Language
        en = self._targetName
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
        self._targetName = en
        self.resetTextfield()
        self.resetSelectors()
        self.setTitle()
    def SetEntry(self, evt=None):
        en = self.selectors.Entry
        if en == self._targetName:
            return
        if checkEntryOpen(self.lang, en):
            TKmsg.showinfo("Already open", f"Cannot open entry {en} from langauge {self.lang}. It is already open")
            self.resetSelectors()
        entry = self.Story.get(en, None)
        if entry == None:
            if TKmsg.askyesno("NO ENTRY FOUND", f"The entry {en} was not found.\nDo you wish to create it?"):
                NewEntry(self._lang, False, en)
            else:
                pass
            self.resetSelectors()
            return
        self._targetName = en
        self.resetSelectors()
        self.resetTextfield()
        self.setTitle()
    def resetTextfield(self):
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
    def resetSelectors(self):
        self.selectors.reset(self.lang, self.entryName, self.Story.keys())
    def save(self):
        Savelang(self._lang)
    @property
    def lang(self)->str:
        return self._lang
    @property
    def entryName(self)->str:
        return self._targetName
    @property
    def entry(self)->str:
        return self.Story.get(self._targetName, "")
    @entry.setter
    def entry(self, val):
        self.Story[self._targetName] = val
    

def saveAll():
    for k in langList.keys():
        Savelang(k)
def Savelang(lang:str):
    cwd = os.getcwd()
    filename = langList[lang]
    story:dict = Data.langstory[lang]
    with open(cwd+"/nerrative/" + filename + ".xml", "w+", encoding="utf-8") as datafile:
        datafile.write("<story>\n")
        for key, entry in story.items():
            datafile.write(f"<{key}>\n{entry}\n</{key}>\n")
        datafile.write("</story>")
        datafile.close()
    Data.langEdited[lang] = False

def Loadlang(lang:str):
    cwd = os.getcwd()
    filename = langList[lang]
    try:
        tree = ElementTree.parse(cwd+"/nerrative/" + filename + ".xml")
    except Exception as e:
        err = f"Error loading language file {lang}: {e}"
        TKmsg.showerror("LOADING-ERROR", err)
        print (err, file=sys.stderr)
        return False
    story = {}
    for element in tree.iter():
        if element.tag == 'story':
            continue #do not store the top-level element
        story[element.tag] = element.text.strip()
    Data.langstory[lang] = story
    Data.langEdited[lang] = False

def start():
    root = TK.Tk()
    root.withdraw()

    for k in langList.keys():
        Loadlang(k)

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
            AskNewEntry(startlang)
        else:
            pass
        root.quit() #To be moved to else branch once above action is supported.
        return
    if len(Data.editors) < 1:
        askOpenEditor()

    while True:
        root.update()
        root.update_idletasks()
        if len(Data.editors) < 1:
            root.quit()
            return

    


def NotAddedYet():
    TKmsg.showwarning("WOOPS..","Sorry, that feature is not added yet.\nPlease be impatient.\nI am very lazy, and need the pressure.")

if __name__ == "__main__":
    start()