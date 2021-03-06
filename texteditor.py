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
from untitled_const import *

_CWR = os.getcwd() 

#Display language : internal language (filename)
#langList = {"English" : "english", "Testlang Alpha" : "test1", "Testlang Beta" : "test2"}

#static class for common data.
class Data():
    langList = {}
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
    lst = Data.langstory.get(lang, {})
    lst2 = set()
    for e in lst:
        gn, _ = SplitGroupSubentry(e)
        if not gn in lst2:
            lst2.add(gn)
    return lst2
def GetitemsList(lang:str):
    lst = Data.langstory.get(lang, {})
    lst2 = set()
    for e in lst:
        segs = e.split(SEPERATOR)
        if segs[0] != DATATERM_ITEM or len(segs) < 3:
            continue
        segs.pop(0)
        segs.pop()
        group = "_".join(segs)
        if not group in lst2:
            lst2.add(group)
    return lst2

def GetEntriesByGroup(lang:str, groupname:str):
    lst = Data.langstory.get(lang, {})
    lst2 = set()
    for e in lst:
        if e.startswith(groupname):
            lst2.add(e)
    return lst2        

def CloseAll():
    e:BaseEditor
    for e in reversed(Data.editors):
        e.OnClose()

def askOpenEditor():
    askwindow = TK.Toplevel(Data.root)
    askwindow.title("Open entry")
    running = TK.BooleanVar(askwindow, True)
    editType = TK.IntVar(value = EditorType.SINGLE)
    def onOpen(*_):
        if not validate():
            return

        if editType.get() == EditorType.SINGLE:
            OpenSingleEditor(sel.Language, sel.Entry)
        elif editType.get() == EditorType.MULTI:
            OpenMultiEditor(sel.Language, sel.Entry)
        elif editType.get() == EditorType.ITEM:
            OpenItemEditor(sel.Language)
        #askwindow.destroy()
        running.set(False)
    def onClose(*_):
        #askwindow.destroy()
        running.set(False)
    askwindow.protocol("WM_DELETE_WINDOW", onClose)
    openbtn = TK.Button(askwindow, text = "OPEN", command = onOpen)
    closebtn = TK.Button(askwindow, text = "CLOSE", command = onClose)
    def onLang(*_):
        if editType.get() == EditorType.SINGLE:
            sel.EntryBox.config(state = TK.NORMAL)
            sel.EntryList = Data.langstory.get(sel.Language, {}).keys()
        elif editType.get() == EditorType.MULTI:
            sel.EntryBox.config(state = TK.NORMAL)
            sel.EntryList = GetGroupList(sel.Language)
        elif editType.get() == EditorType.ITEM:
            sel.EntryBox.config(state = TK.DISABLED)
            sel.EntryList = ["ITEM"]
            sel.EntryBox.set("ITEM")
        else:
            sel.EntryList = [] #this should never happen
        validate()
    def validate(*_):
        lang = sel.Language
        target = sel.Entry
        if editType.get() == EditorType.SINGLE:
            e = Data.langstory.get(lang, {}).get(target, None)
            if e == None or getEntryOpen(lang, target):
                openbtn.config(state = TK.DISABLED)
                return False
            openbtn.config(state = TK.NORMAL)
            return True
        elif editType.get() == EditorType.MULTI:
            if len(GetEntriesByGroup(lang, target)) < 1 or getGroupOpen(lang, target):
                openbtn.config(state = TK.DISABLED)
                return False
            openbtn.config(state = TK.NORMAL)
            return True
        elif editType.get() == EditorType.ITEM:
            if not lang in Data.langList.keys() or getGroupOpen(lang, "ITEM"):
                openbtn.config(state = TK.DISABLED)
                return False
            openbtn.config(state = TK.NORMAL)
            return True
        openbtn.config(state = TK.DISABLED)
        return False
    def toSingle():
        editType.set(EditorType.SINGLE)
        toSingleBtn.config(state = TK.DISABLED)
        tomultiBtn.config(state = TK.NORMAL)
        toItemBtn.config(state = TK.NORMAL)

        onLang()
    def tomulti():
        editType.set(EditorType.MULTI)
        toSingleBtn.config(state = TK.NORMAL)
        tomultiBtn.config(state = TK.DISABLED)
        toItemBtn.config(state = TK.NORMAL)

        onLang()
    def toItem():
        editType.set(EditorType.ITEM)
        toSingleBtn.config(state = TK.NORMAL)
        tomultiBtn.config(state = TK.NORMAL)
        toItemBtn.config(state = TK.DISABLED)

        onLang()

    toSingleBtn = TK.Button(master = askwindow, text = "Single-Editor", command = toSingle, state = TK.DISABLED)
    tomultiBtn  = TK.Button(master = askwindow, text = "Multi-Editor", command = tomulti, state = TK.NORMAL)
    toItemBtn  = TK.Button(master = askwindow, text = "Item-Editor", command = toItem, state = TK.NORMAL)
    toSingleBtn.grid(row = 0, column = 0)
    tomultiBtn.grid(row = 1, column = 0)
    toItemBtn.grid(row = 2, column = 0)

    sel = EntrySelector(askwindow, onLang, validate)
    sel.grid(row = 0, column = 1, columnspan=2)
    openbtn.grid(row = 1, column = 1)
    closebtn.grid(row = 1, column = 2)
    validate()

    while(running.get()):
        askwindow.update()
        askwindow.update_idletasks()
    askwindow.destroy()
def getEntryOpen(lang:str, entry:str):
    gn, _ = SplitGroupSubentry(entry)
    for e in Data.editors:
        if(e.lang != lang):
            continue
        if e.editortype == EditorType.SINGLE:
            if e.entryName == entry:
                return e
        elif e.editortype == EditorType.MULTI or e.editortype == EditorType.ITEM:
            if e.GroupName == gn:
                return e
    return None
def getGroupOpen(lang:str, group:str):
    for e in Data.editors:
        if(e.lang != lang):
            continue
        if e.editortype == EditorType.MULTI:
            if e.GroupName == group:
                return e
        elif e.editortype == EditorType.SINGLE or e.editortype == EditorType.ITEM:
            if SplitGroupSubentry(e.entryName)[0] == group:
                return e
    return None
                
def OpenItemEditor(lang):
    e = getEntryOpen(lang, "ITEM")
    if e:
        e.lift()
        return
    Data.editors.append(ItemEditor(lang))
def OpenSingleEditor(lang:str, entry:str):
    e = getEntryOpen(lang, entry)
    if e:
        e.lift()
        return
    #for e in Data.editors:
    #    if e.entryName == entry and e.lang == lang:
    #        e.lift()
    #        return
    Data.editors.append(SingleEditor(lang, entry))
def OpenMultiEditor(lang:str, group:str):
    e = getEntryOpen(lang, group)
    if e:
        e.lift()
        return
    Data.editors.append(MultiEditor(lang, group))

def NewEntry(lang:str, openNew:bool, entry):
    Data.langstory.get(lang, {})[entry] = " "
    Data.langEdited[lang] = True
    if openNew:
        OpenSingleEditor(lang, entry)
def AskNewEntry(lang:str, openNew:bool = True, entry = ""):
    entry = askName("NEW ENTRY", "What do you wish name the entry?", lang, entry)
    if entry:
        return NewEntry(lang, openNew, entry)
    return entry

def askName(title, message, lang, startText, isGroup = False):
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
        if isGroup:
            for e in story.keys():
                if e.startswith(ans):
                    askErr.config(text="ERR: An entry with this name already exist.", fg = "orange")
                    return
            if re.match(ENTRY_NAME_PATTERN, ans):
                askData.run = False
                askData.ret = ans
            else:
                askErr.config(text="Group name must\n * Start with a capital letter\n * Contain only capitals, underscore, dash and numbers\n - eg: SPACESHIP_TALK", fg = "red")   
        else:
            if ans in story.keys():
                askErr.config(text="ERR: An entry with this name already exist.", fg = "orange")
            elif re.match(ENTRY_NAME_PATTERN, ans):
                askData.run = False
                askData.ret = ans
            else:
                askErr.config(text="Entry name must\n * Start with a capital letter\n * Contain only capitals, underscore, dash and numbers\n - eg: SPACESHIP_TALK-8", fg = "red")
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

def AskPatchLang(sourcelang = "", targetLang = ""):
    askwindow = TK.Toplevel(Data.root)
    askwindow.title("Patch language")
    
    clonevar = TK.BooleanVar(value = False)
    runningvar = TK.BooleanVar(value = True)

    langframe = TK.Frame(askwindow)
    langframe.pack()
    btnframe = TK.Frame(askwindow)
    btnframe.pack()

    langbox_1 = TKTC.AutocompleteCombobox(langframe)
    langbox_2 = TKTC.AutocompleteCombobox(langframe)
    
    TK.Label(langframe, text = "source langauge").pack(side=TK.LEFT)
    langbox_1.pack(side = TK.LEFT)
    TTK.Separator(master = langframe, orient = TK.HORIZONTAL).pack(side = TK.LEFT)
    langbox_2.pack(side = TK.RIGHT)
    TK.Label(langframe, text = "target langauge").pack(side=TK.RIGHT)

    def doPatch():
        if not validate():
            return

        lang1 = langbox_1.get()
        lang2 = langbox_2.get()
        lang1Story = Data.langstory.get(lang1)
        lang2Story = Data.langstory.get(lang2)
        lang1Keys = lang1Story.keys()
        lang2Keys = lang2Story.keys()

        topatch = lang1Keys - lang2Keys
        if clonevar.get():
            clonetext = "entry-keys and entry-text"
        else:
            clonetext = "entry-keys (but not any text)"
        if not TKmsg.askokcancel("Please confirm action", f"This will copy {len(topatch)} {clonetext} from {lang1} to {lang2}. Is this ok?"):
            return
        
        for e in topatch:
            if(clonevar.get()):
                lang2Story[e] = lang1Story[e]
            else:
                lang2Story[e] = " "
        if TKmsg.askyesno("save progress?", f"You have made changes to {lang2}. Would you like to save?"):
            Savelang(lang2)
        runningvar.set(False)
    def doCancel():
        runningvar.set(False)
    
    checkClone=TK.Checkbutton(btnframe, text="clone text", variable = clonevar)
    btnPatch = TK.Button(btnframe, text="Patch", command = doPatch, state = TK.DISABLED)
    btnCancel= TK.Button(btnframe, text="Cancel",command = doCancel)
    
    checkClone.pack(side = TK.LEFT)
    btnCancel.pack(side = TK.LEFT)
    btnPatch.pack(side = TK.LEFT)
    def setFalse():
        btnPatch.configure(state = TK.DISABLED)
        return False
    def setTrue():
        btnPatch.configure(state = TK.NORMAL)
        return True
    def validate(*_):
        lang1 = langbox_1.get()
        lang2 = langbox_2.get()
        if lang1 == lang2:
            return setFalse()
        if (lang1 in Data.langList.keys()) and (lang2 in Data.langList.keys()):
            return setTrue()
        else:
            return setFalse()

    langbox_1.set_completion_list(list(Data.langList.keys()))
    langbox_1.set(sourcelang)
    langbox_1.bind("<<ComboboxSelected>>", validate)

    langbox_2.set_completion_list(list(Data.langList.keys()))
    langbox_2.set(targetLang)
    langbox_2.bind("<<ComboboxSelected>>", validate)

    while(runningvar.get()):
        askwindow.update()
        askwindow.update_idletasks()
    askwindow.destroy()


class EntryText(TK.Frame):
    def __init__(self, master, TargetEntry:str, lang:str, tosingle:callable, toDel:callable, torename:callable):
        super().__init__(master=master)
        self.label = TK.Label(master=self, text = TargetEntry)
        self.textfield = TKS.ScrolledText(self, width = 70, height = 3, insertbackground = "white")
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.bind('<KeyRelease>', self.updateentry)
        self.lang = lang
        self.TargetEntry = TargetEntry

        self.label.pack()
        self.textfield.pack(fill = TK.BOTH, expand = True)
        TK.Button(master = self, text="Open in\nsingle-edit", command = tosingle, bg="blue").pack(side=TK.RIGHT)
        TK.Button(master = self, text="Delete\nentry", command = toDel, bg="red").pack(side=TK.RIGHT)
        TK.Button(master = self, text="Rename\nentry", command = torename, bg="yellow").pack(side = TK.RIGHT)

    def updateentry(self, evt=None):
        Data.langEdited[self.lang] = True
        self.entry = self.textfield.get('1.0', TK.END)
    def reset(self):
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
    @property
    def entry(self)->str:
        return self.Story.get(self.TargetEntry, "")
    @entry.setter
    def entry(self, val):
        self.Story[self.TargetEntry] = val
    @property
    def Story(self)->dict:
        return Data.langstory.get(self.lang, {})
    
    @property
    def edited(self)->bool:
        return Data.langEdited[self.lang]
    @edited.setter
    def edited(self, val):
        Data.langEdited[self.lang] = val
class EntrySelector(TK.Frame):
    def __init__(self, master, onLangSelect, onEntrySelect):
        super().__init__(master)

        self.langlabel = TK.Label(self, text = "Language")
        self.LangBox = TKTC.AutocompleteCombobox(self)
        self.LangBox.set_completion_list(list(Data.langList.keys()))
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
    ITEM = 3

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
        fileMenu = TK.Menu(tearoff = 0)#(menu)
        editMenu = TK.Menu(tearoff = 0)#(menu)
        menu.add_cascade(label = "file", menu=fileMenu)
        menu.add_cascade(label = "edit", menu=editMenu)

        fileMenu.add_command(label = "open", command=askOpenEditor)
        fileMenu.add_command(label = "Save language file", command=self.save)
        fileMenu.add_command(label = "Save all", command=saveAll)
        fileMenu.add_command(label = "New Entry", command=self.OnNewEntry)
        fileMenu.add_command(label = "Close", command=self.OnClose)
        fileMenu.add_command(label = "Close All", command=CloseAll)

        editMenu.add_command(label = "Patch langauge", command = AskPatchLang)
        editMenu.add_command(label = "Add new lanaguge", command = AskAddLanguage)


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
    @edited.setter
    def edited(self, val):
        Data.langEdited[self._lang] = val
class ItemEntry(TK.Frame):
    def __init__(self, master, lang:str, itemname:str, resetCall:callable):
        super().__init__(master = master)

        self._lang = lang
        self._target = itemname
        self.resetCall = resetCall

        self._headerIcon:TK.PhotoImage = None

        self._displayName  = TK.StringVar(value="")
        self._iconfileName = TK.StringVar(value="")

        self.iconErrMsg = TK.Label(master = self, fg = "red", text = "")
        self.iconErrMsg.grid(column = 0, row = 7, columnspan = 4)

        self.label_icon = TK.Label(master = self, image = self.HeaderIcon)
        self.label_key = TK.Label(master = self, text = self.HeaderTitle)

        self.label_icon.grid(column = 0, row = 1, rowspan=5)#.pack(side = TK.LEFT)
        self.label_key.grid(column = 0, row = 0, columnspan=4)#.pack(side = TK.LEFT)

        self.label_dispname = TK.Label(master = self, text = "Display name")
        self.label_iconname = TK.Label(master = self, text = "Icon filename")

        self.label_dispname.grid(column = 2, row = 1)
        self.label_iconname.grid(column = 2, row = 3)

        self.entry_dispname = TK.Entry(master = self, textvariable = self._displayName)
        self.entry_iconname = TK.Entry(master = self, textvariable = self._iconfileName)
        self.entry_dispname.bind('<KeyRelease>', self.updateEntry)
        self.entry_iconname.bind('<KeyRelease>', self.updateEntry)

        self.entry_dispname.grid(column = 2, row = 2)
        self.entry_iconname.grid(column = 2, row = 4)

        self.label_desc = TK.Label(master=self, text = "Description")
        self.text_desc  = TK.Text( master=self, width = 40, height = 3, insertbackground = "white")
        self.text_desc.bind('<KeyRelease>', self.updateEntry)

        self.label_desc.grid(column = 3, row = 1)#.pack(side = TK.TOP)
        self.text_desc.grid(column = 3, row = 2, rowspan = 4)#.pack (side = TK.BOTTOM, fill = TK.BOTH)

        self.btn_rename = TK.Button(master=self, text="Rename", bg = "yellow", command = self.OnRename, state = TK.NORMAL)
        self.btn_delete = TK.Button(master=self, text="Delete", bg = "red",    command = self.OnDelete, state = TK.NORMAL)

        self.btn_rename.grid(column = 2, row = 6)#.pack(side=TK.LEFT)
        self.btn_delete.grid(column = 3, row = 6)#.pack(side=TK.LEFT)



        self.reset()
    def reset(self, *_):
        self.text_desc.delete('1.0',TK.END)
        self.text_desc.insert(TK.END, self.Description)
        self._displayName.set(self.Displayname)
        self._iconfileName.set(self.IconFilename)
        self.label_icon.config(image = self.HeaderIcon)
        self.label_key.config(text = self.HeaderTitle)
    def updateEntry(self, *_):
        self.Description = self.text_desc.get('1.0',TK.END)
        self.Displayname = self._displayName.get()
        self.IconFilename = self._iconfileName.get()
        self.label_icon.config(image = self.HeaderIcon)


    @property
    def HeaderTitle(self):
        return f" - {self._target} - "
    @property
    def HeaderIcon(self):
        try:
            self._headerIcon = TK.PhotoImage(file = IMAGE_DIR + self.IconFilename.strip())
            self.iconErrMsg.config(text = "")
        except Exception as err:
            self.iconErrMsg.config(text = err)
            self._headerIcon = TK.PhotoImage(file = IMAGE_DIR +FALLBACK_ICON)
        return self._headerIcon
    @property
    def Story(self):
        return Data.langstory.get(self._lang)
    @property
    def NameTerm(self):
        return f"{DATATERM_ITEM}_{self.KeyName}{DATATERM_NAME}"
    @property
    def DescTerm(self):
        return f"{DATATERM_ITEM}_{self.KeyName}{DATATERM_DESCRIPTION}"
    @property
    def IconTerm(self):
        return f"{DATATERM_ITEM}_{self.KeyName}{DATATERM_ICON}"

    @property
    def KeyName(self):
        return self._target
    @property
    def Displayname(self):
        return self.Story.get(self.NameTerm)
    @property
    def Description(self):
        return self.Story.get(self.DescTerm)
    @property
    def IconFilename(self):
        return self.Story.get(self.IconTerm)
    
    @Displayname.setter
    def Displayname(self, val):
        self.Story[self.NameTerm] = val
    @Description.setter
    def Description(self, val):
        self.Story[self.DescTerm] = val
    @IconFilename.setter
    def IconFilename(self, val):
        self.Story[self.IconTerm] = val    

    def OnDelete(self, *_):
        full_target = DATATERM_ITEM + "_" + self._target
        if askDeleteEntry(self._lang, full_target, True):
            self.resetCall()
            self.edited = True
        """ #Alternate code
        if TKmsg.askyesno("Delete item entries?", f"Are you sure you wish to delete {self._target}?"):
            name = DATATERM_ITEM + "_" + self._target + DATATERM_NAME
            icon = DATATERM_ITEM + "_" + self._target + DATATERM_ICON
            desc = DATATERM_ITEM + "_" + self._target + DATATERM_DESCRIPTION
            self.Story.pop(name, None)
            self.Story.pop(icon, None)
            self.Story.pop(desc, None)
            self.resetCall()
            self.edited = True
        """
        
    def OnRename(self, *_):
        full_target = DATATERM_ITEM + "_" + self._target
        if askRenameEntry(self._lang, full_target, full_target, True):
            self.resetCall()

class ItemEditor(BaseEditor):
    def __init__(self, lang:str):
        super().__init__(lang, DATATERM_ITEM, EditorType.ITEM)
        def _VOID():
            pass
        self.selectors = EntrySelector(self, self.SetLang, _VOID)
        self.selectors.pack(side=TK.TOP)  
        self.itemEntries:VerticalScrollFrame = None

        self.newItemName = TK.StringVar()

        self.newItemFrame:TK.Frame = None
        self.btnNewItem:TK.Button = None
        self.newErrMsg:TK.Label = None
        #Add general menu options here

        self.UpdateEntries()
        self.resetSelectors()
    def UpdateEntries(self, *_):
        #Add entry spesiffic menu options here.
        if(self.itemEntries != None):
            self.itemEntries.pack_forget()
        itemlist:set = GetitemsList(self.lang)
        self.itemEntries:VerticalScrollFrame = VerticalScrollFrame(self)
        for entry in itemlist:
            self.addpatchItem(entry)
            itementry = ItemEntry(self.itemEntries.viewPort, self.lang, entry, self.UpdateEntries)
            itementry.pack()

        self.newItemFrame = TK.Frame(self.itemEntries.viewPort)
        self.newItemFrame.pack(fill = TK.X)
        TK.Entry(master=self.newItemFrame, textvariable=self.newItemName).pack(side=TK.LEFT, fill = TK.X)
        self.btnNewItem =  TK.Button(self.newItemFrame, text="Add item", command = self.OnAddItem)
        self.btnNewItem.pack(side=TK.LEFT, fill = TK.X)
        self.newErrMsg = TK.Label(master=self.itemEntries.viewPort, fg = "red", text = "...")
        self.newErrMsg.pack(side=TK.BOTTOM, fill = TK.X)

        self.itemEntries.pack()
    def OnAddItem(self, *_):
        itemkey = self.newItemName.get()
        if not re.match(ITEM_NAME_PATTERN, itemkey):
            self.newErrMsg.config(text="Error: Bad name key format. Only allowed:\nupper case, numbers and underscore")
            return False
        if itemkey in GetitemsList(self.lang):
            self.newErrMsg.config(text="Error: Name key already exist.")
            return False
        self.addpatchItem(itemkey)
        self.UpdateEntries()
        return True
    def addpatchItem(self, itemkey):
        name = DATATERM_ITEM + "_" + itemkey + DATATERM_NAME
        icon = DATATERM_ITEM + "_" + itemkey + DATATERM_ICON
        desc = DATATERM_ITEM + "_" + itemkey + DATATERM_DESCRIPTION
        contents = (name, icon, desc)

        for content in contents:
            if content not in self.Story:
                self.Story[content] = " "
                self.edited = True
    def SetLang(self, lang):
        lang = self.selectors.Language
        if lang == self.lang:
            return
        self.UpdateEntries()
        self.resetSelectors()

    def resetSelectors(self):
        self.selectors.reset(self.lang, DATATERM_ITEM, GetGroupList(self.lang))
        self.selectors.EntryBox.config(state=TK.DISABLED)
    def save(self):
        Savelang(self._lang)
        
class MultiEditor(BaseEditor):
    def __init__(self, lang:str, groupName:str):
        super().__init__(lang, groupName, EditorType.MULTI)
        
        self.selectors = EntrySelector(self, self.SetLang, self.SetGroup)
        self.selectors.pack(side=TK.TOP)

        self.textfields:VerticalScrollFrame = None
        self.addEntry:TK.Button = None
        self.menu['to_single'] = TK.Menu(self.menu['edit'], tearoff = 0)
        self.menu['del_entry'] = TK.Menu(self.menu['edit'], tearoff = 0)
        self.menu['ren_entry'] = TK.Menu(self.menu['edit'], tearoff = 0)
        self.menu['edit'].add_command(label = "Rename entry group", command=self.OnRenameGroup)
        self.menu['edit'].add_command(label = "Delete entry group", command=self.OnDeleteGroup)
        self.menu['edit'].add_cascade(label = "Open in single-edit", menu = self.menu['to_single'])
        self.menu['edit'].add_cascade(label = "Delete entry", menu = self.menu['del_entry'])
        self.menu['edit'].add_cascade(label = "Rename entry", menu = self.menu['ren_entry'])
        self.UpdateEntries()
        self.resetSelectors()
    def UpdateEntries(self):
        TS = self.menu['to_single']
        TS.delete(0, TS.index(TK.END))
        DE = self.menu['del_entry']
        DE.delete(0, DE.index(TK.END))
        RE = self.menu['ren_entry']
        RE.delete(0, DE.index(TK.END))

        if(self.textfields != None):
            self.textfields.pack_forget()
        entrylist = GetEntriesByGroup(self.lang, self.GroupName)
        self.textfields = VerticalScrollFrame(self)
        for ename in entrylist:
            TS_callback = lambda x = ename: self.onsinglemode(x)
            DE_callback = lambda x = ename: self.onDelEntry(x)
            RE_callback = lambda x = ename: self.onRenEntry(x)
            entry = EntryText(self.textfields.viewPort, ename, self.lang, TS_callback, DE_callback, RE_callback)
            entry.pack(fill = TK.X, expand=True)

            TS.add_command(label = ename, command=TS_callback)
            DE.add_command(label = ename, command=DE_callback)
            RE.add_command(label = ename, command=RE_callback)
        self.addEntry = TK.Button(self.textfields.viewPort, text = "Add new entry to group", command=self.OnNewEntryToGroup)
        self.addEntry.pack(fill = TK.X)
        self.textfields.pack(side=TK.TOP, fill=TK.BOTH, expand=True)

        self.resetTextfields()
    def OnNewEntryToGroup(self):
        AskNewEntry(self.lang, False, self.GroupName+"_")
        self.UpdateEntries()
    def onDelEntry(self, entry):
        askDeleteEntry(self.lang, entry)
        self.UpdateEntries()
    def onRenEntry(self, entry):
        askRenameEntry(self.lang, entry, entry)
        self.UpdateEntries()
    def SetLang(self, evt=None):
        lang = self.selectors.Language
        gn = self._targetName
        if lang == self.lang:
            return
        openE = getGroupOpen(lang, gn)
        if(openE):
            self.resetSelectors()
            openE.lift()
            return 
        d = Data.langstory.get(lang, None)
        if d == None:
            TKmsg.showwarning("NOT VALID LAGUAGE", "Langauge selected is not valid.")
            self.resetSelectors()
            return
        entrylist = GetEntriesByGroup(self.lang, self.GroupName)
        if len(entrylist) < 1:
            if TKmsg.askyesno("NO ENTRIES FOUND", f"No entries of group {gn} in {lang}. Would you like to patch {lang} from {self.lang}?"):
                AskPatchLang(sourcelang=self.lang, targetLang=lang)
                return self.SetLang() #restart from the top to confirm if the patch was completed succesfully.
            else:
                self.resetSelectors()
                return
        if self.edited:
            if TKmsg.askyesno("SAVE?", f"You have unsaved changes!\nDo you wish to save the {self._lang} languagefile before switching langauge?"):
                self.save()
        self._lang = lang
        self._targetName = gn
        self.resetTextfields()
        self.resetSelectors()
        self.setTitle()
    def SetGroup(self, evt=None):
        gn = self.selectors.Entry
        lang = self.lang
        if gn == self._targetName:
            return
        openE = getGroupOpen(lang, gn)
        if(openE):
            self.resetSelectors()
            openE.lift()
            return
        entrylist = GetEntriesByGroup(self.lang, self.GroupName)
        if len(entrylist) < 1:
            TKmsg.showinfo("NO ENTRY FOUND", f"The entry {gn} was not found.")
            self.resetSelectors()
            return
        self._targetName = gn
        self.resetSelectors()
        self.resetTextfields()
        self.setTitle()
    @property
    def GroupName(self):
        return self._targetName
    @GroupName.setter
    def GroupName(self, val):
        self._targetName = val
        self.UpdateEntries()
    def resetSelectors(self):
        self.selectors.reset(self.lang, self.GroupName, GetGroupList(self.lang))
    def resetTextfields(self):
        slave:EntryText
        for slave in self.textfields.viewPort.slaves():
            if type(slave) != EntryText:
                continue
            slave.reset()
    def onsinglemode(self, entryname):
        Data.editors.remove(self)
        self.destroy()
        OpenSingleEditor(self.lang, entryname)
    def OnRenameGroup(self):
        res = askRenameEntry(self.lang, self.GroupName, self.GroupName, True)
        if res:
            self._targetName = res
            self.UpdateEntries()
            self.resetSelectors()
            self.edited = True
    def OnDeleteGroup(self):
        res = askDeleteEntry(self.lang, self.GroupName, True)
        if res:
            self.OnClose()
class SingleEditor(BaseEditor):
    def __init__(self, lang:str, entryName:str):
        super().__init__(lang, entryName, EditorType.SINGLE)
        
        self.menu['edit'].add_command(label = "Open in multiedit", command = self.OnMultiMode)
        self.menu['edit'].add_command(label = "Delete Entry", command = self.onDelEntry)
        self.menu['edit'].add_command(label = "Rename Entry", command = self.onRenEntry)

        #building UI

        self.selectors = EntrySelector(self, self.SetLang, self.SetEntry)
        self.selectors.reset(self.lang, self.entryName, self.Story.keys())
        self.selectors.pack()

        self.textfield = TKS.ScrolledText(self, width = 70, insertbackground = "white")
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.bind('<KeyRelease>', self.updateentry)

        self.textfield.pack(fill="both")

        #last fix..
        self.resetTextfield()
        self.resetSelectors()

    def OnMultiMode(self):
        Data.editors.remove(self)
        self.destroy()
        OpenMultiEditor(self.lang, SplitGroupSubentry(self.entryName)[0] )
    def updateentry(self, evt=None):
        Data.langEdited[self.lang] = True
        self.entry = self.textfield.get('1.0', TK.END)

    def SetLang(self, evt=None):
        lang = self.selectors.Language
        en = self._targetName
        if lang == self.lang:
            return
        openE = getEntryOpen(lang, en)
        if openE:
            #TKmsg.showinfo("Already open", f"Cannot open entry {en} from langauge {self.lang}. It is already open")
            openE.lift()
            self.resetSelectors()
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
        lang = self.lang
        if en == self._targetName:
            return
        openE = getEntryOpen(lang, en)
        if openE:
            #TKmsg.showinfo("Already open", f"Cannot open entry {en} from langauge {self.lang}. It is already open")
            openE.lift()
            self.resetSelectors()
            return 
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
    def onDelEntry(self):
        askDeleteEntry(self.lang, self.entryName)
        if self.entry == "":
            Data.editors.remove(self)
            self.destroy()
    def onRenEntry(self):
        newname = askRenameEntry(self.lang, self.entryName, self.entryName)
        if newname:
            self._targetName = newname
            self.resetSelectors()
            self.resetTextfield()
            self.setTitle()        
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
    
def askDeleteEntry(lang, entryname, isGroup = False):
    title1 = ""
    msg1 = ""
    msg2 = ""
    if isGroup:
        count = len(GetEntriesByGroup(lang, entryname))
        title1 = "Delete entries?"
        msg1 =  f"You are about to delete all {count} entries starting with '{entryname}'' from {lang}"
        msg2 = f"All {count} entries starting with {entryname} has been deleted!\nWould you like to save?"
    else:
        title1 = "Delete entry?"
        msg1 = f"You are about to delete {entryname} from {lang}"
        msg2 = f"The entry {entryname} has been deleted. Would you like to save?"
    
    if TKmsg.askokcancel(title1, msg1, icon = TKmsg.WARNING):
        if isGroup:
            story = Data.langstory.get(lang, {})
            for e in story.keys():
                if e.startswith(entryname):
                    story.pop(e, None)
        else:
            Data.langstory.get(lang, {}).pop(entryname, None)
        Data.langEdited[lang] = True

        if TKmsg.askyesno("Save file?", msg2):
            Savelang(lang)
        return True
    return False
def askRenameEntry(lang, oldname, newname="", isGroup = False):
    newname = askName("RENAME ENTRY", f"What do you wish rename {oldname} to?", lang, newname, isGroup)
    if newname:
        return doRenameEntry(lang, oldname, newname, isGroup)
    return False

def doRenameEntry(lang, oldname, newname, isGroup = False):
    if isGroup:
        entries = GetEntriesByGroup(lang, oldname)
        for entry in entries:
            newname2 = entry.replace(oldname, newname)
            doRenameEntry(lang, entry, newname2, False)
        return newname
    story = Data.langstory.get(lang, {})
    story[newname] = story.pop(oldname)
    return newname
def saveAll():
    for k in Data.langList.keys():
        Savelang(k)
def Savelang(lang:str):
    filename = Data.langList[lang]
    story:dict = Data.langstory.get(lang, {})
    with open(_CWR+"/nerrative/" + filename + ".xml", "w+", encoding="utf-8") as datafile:
        datafile.write("<story>\n")
        for key, entry in story.items():
            datafile.write(f"<{key}>\n{entry}\n</{key}>\n")
        datafile.write("</story>")
        datafile.close()
    Data.langEdited[lang] = False
def saveLangFile():
    rootname = "languages"
    with open(_CWR+"/nerrative/languages.xml", "w+", encoding="utf-8") as datafile:
        datafile.write(f"<{rootname}>\n")
        for key, filename in Data.langList.items():
            datafile.write(f"<{key}>\n{filename}\n</{key}>\n")
        datafile.write(f"</{rootname}>")
        datafile.close()

def LoadStory(lang:str):
    rootname = "story"
    filename = Data.langList[lang]
    try:
        tree = ElementTree.parse(_CWR+"/nerrative/" + filename + ".xml")
    except Exception as e:
        err = f"Error loading language file {lang}: {e}"
        TKmsg.showerror("LOADING-ERROR", err)
        print (err, file=sys.stderr)
        return False
    story = {}
    for element in tree.iter():
        if element.tag == rootname:
            continue #do not store the top-level element
        story[element.tag] = element.text.strip()
    Data.langstory[lang] = story
    Data.langEdited[lang] = False

def LoadLangfile():
    rootname = "languages"
    try:
        tree = ElementTree.parse(_CWR+"/nerrative/languages.xml")
    except:# Exception as e:
        if TKmsg.askokcancel("Woops..","List of languages failed to load.\nDo you wish to generate new file by adding a language?"):
            Data.langList = {}
            AskAddLanguage()
        if len(Data.langList) < 1:
            return False
        return True
    Data.langList = {}
    for element in tree.iter():
        if element.tag == rootname:
            continue
        Data.langList[element.tag] = element.text.strip()
    return True
def AskAddLanguage():
    LANG_NAME_PATTERN = r'^[A-Za-z]+(?:[0-9]|_|[A-Za-z])*$'

    askwindow = TK.Toplevel(Data.root)
    runningvar = TK.BooleanVar(value=True)
    returnvar = TK.BooleanVar(value=False)
    keynamevar = TK.StringVar(value="")
    filenamevar = TK.StringVar(value="")
    
    frames = [TK.Frame(askwindow),TK.Frame(askwindow),TK.Frame(askwindow),TK.Frame(askwindow)]
    for f in frames:
        f.pack()

    TK.Label(frames[0], text="Display/key name").pack(side=TK.LEFT)
    TK.Entry(frames[0], textvariable = keynamevar).pack(side=TK.RIGHT)
    TK.Label(frames[1], text="Filename").pack(side=TK.LEFT)
    TK.Entry(frames[1], textvariable = filenamevar).pack(side=TK.LEFT)
    TK.Label(frames[1], text=".xml").pack(side=TK.RIGHT)
    def onOK():
        kname = keynamevar.get()
        fname = filenamevar.get()

        if len(kname) < 1 or len(fname) < 1:
            errMessage.config(text = "Please fill in both fields.")
            return
        for l in Data.langList.keys():
            if l == kname:
                errMessage.config(text = "Sorry, this langauge key already exist.")
                return
        for l in Data.langList.values():
            if l == fname:
                errMessage.config(text = "Sorry, this langauge key already exist.")
                return
        if not re.match(string=kname, pattern=LANG_NAME_PATTERN) or not re.match(string=fname, pattern=LANG_NAME_PATTERN):
            errMessage.config(text = "Sorry, you got a poorly formatted name or displayname/key. Please rename.\nPlease avoid space, special and extended alphabet characters")
            return
        Data.langList[kname] = fname
        saveLangFile()
        Savelang(kname) #this will generate the langauge file
        runningvar.set(False)
        returnvar.set(True)
    def onCancel():
        runningvar.set(False)
        returnvar.set(False)
    TK.Button(frames[2], text="OK", command = onOK).pack(side=TK.LEFT)
    TK.Button(frames[2], text="CANCEL", command = onCancel).pack(side=TK.LEFT)
    errMessage = TK.Label(frames[3], text = "", fg="red")
    errMessage.pack(side=TK.LEFT)
    while(runningvar.get()):
        askwindow.update()
        askwindow.update_idletasks()
    askwindow.destroy()
    return returnvar.get()



def start():
    root = TK.Tk()
    root.withdraw()

    LoadLangfile()

    for k in Data.langList.keys():
        LoadStory(k)

    if len(Data.langstory) < 1:
        if TKmsg.askokcancel(icon = TKmsg.ERROR, title="NO DATA ERROR!", message="""
        No story datafile were found!
        If there was an error during loading,
        you may want to exit this program, and manually fix the issue.
        Alternativly: do you wish to create an empty langauge file?
        """.strip()):
            Savelang(list(Data.langList.keys())[0])
            LoadStory(list(Data.langList.keys())[0])
        else:
            root.quit() #to be moved to the else-branch above when adding new language files are supported.
            return
    startlang = list(Data.langList)[0]
    if len(Data.langstory[startlang]) < 1:
        if TKmsg.askokcancel(icon = TKmsg.ERROR, title="NO DATA ERROR!", message=f"""
        No story-entries were found!
        If there was an error during loading,
        you may want to exit this program, and manually fix the issue.
        Alternativly: do you wish to create a new entry in {startlang}?
        """.strip()):
            AskNewEntry(startlang)
        else:
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