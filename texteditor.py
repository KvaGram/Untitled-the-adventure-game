import tkinter as TK
import tkinter.ttk as TTK
from tkinter import messagebox as TKmsg
from tkinter import scrolledtext as TKS

dummydata = {
    "TEST" : "Once opon a time there was a lot of text",
    "BEST"  : "There is always more text to be found.."
}

class Editor(TK.Frame):
    def __init__(self, root:TK.Tk):
        super().__init__(root)
        self.root:TK.Tk = root
        self.running = False
        self.test = TextDisplay(self, dummydata, "TEST")
        self.langlabel = TK.Label(text = "Language")
        self.langBox = TTK.Combobox(self, values = ["test","best","rest","foo","bar","foobar"])
        self.chooseEntryLabel = TK.Label(text = "Entry")
        self.chooseEntryBox = TTK.Combobox(self, values = ["test","best","rest","foo","bar","foobar"])

        self.langlabel.grid(row = 0, column = 0)
        self.langBox.grid(row = 0, column = 1)
        self.chooseEntryLabel.grid(row = 1, column = 0)
        self.chooseEntryBox.grid(row = 1, column = 1)
        self.test.grid(row = 3, column = 0, columnspan = 2)
        self.grid_columnconfigure(index = 0, weight = 1)
        self.grid_columnconfigure(index = 1, weight = 1)
        self.grid_rowconfigure(index = 0, weight = 1)


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
        
class TextDisplay(TK.Frame):
    def __init__(self, master, data, entryname):
        super().__init__(master)
        self.master = master
        self.data = data
        self.entryname = entryname
        self.namelabel = TK.Label(master=self, text = entryname)
        self.textfield = TKS.ScrolledText(self)
        self.textfield.configure(bg='black', fg='cyan')
        self.textfield.delete('1.0',TK.END)
        self.textfield.insert(TK.END, self.entry)
        self.savebtn = TK.Button(self, text = "SAVE", command = self.save)

        self.namelabel.grid()
        self.textfield.grid()
        self.savebtn.grid()
    def save(self):
        self.entry = self.textfield.get('1.0', TK.END)
        self.master.savetodisk()

    
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