import tkinter as TK
import tkinter.ttk as TTK
from tkinter import messagebox as TKmsg



class Editor(TK.Frame):
    def __init__(self, root:TK.Tk):
        super().__init__(root)
        self.root:TK.Tk = root
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                self.update()
                self.update_idletasks()
            except TK.TclError as err:
                print(err)
                self.running = False
        

def start():

    #setup
    tkRoot = TK.Tk(screenName="Text resource editor")
    tkRoot.geometry("1600x900")
    editor = Editor(tkRoot)
    editor.pack()

    #running
    editor.run()

    #Cleanup
    editor.pack_forget()
    tkRoot.destroy()

if __name__ == "__main__":
    start()