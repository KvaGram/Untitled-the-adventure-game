import tkinter as TK
import tkinter.ttk as TTK
class VerticalScrollFrame(TK.Frame):
    #Credit goes to this github post:
    #https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    def __init__(self, parent, **kw):
        super().__init__(parent, kw) # create a frame (self)

        self.canvas = TK.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = TK.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = TK.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.viewPort.pack(side=TK.TOP, fill=TK.BOTH, expand=True)

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas.create_window((4,4), window=self.viewPort, anchor="n",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.
        #self.canvas.config(self.winfo_width())

#code based on
#https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
class ResizingCanvas(TK.Canvas):
    def __init__(self,parent,**kwargs):
        TK.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width-4
        self.height = event.height-4
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)


# ********************************
# Example usage of the above class
# ********************************

class Example(TK.Frame):
    def __init__(self, root):

        TK.Frame.__init__(self, root)
        self.scrollFrame = VerticalScrollFrame(self) # add a new scrollable frame.
        
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        for row in range(100):
            a = row
            TK.Label(self.scrollFrame.viewPort, text="%s" % row, width=3, borderwidth="1", 
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            TK.Button(self.scrollFrame.viewPort, text=t, command=lambda x=a: self.printMsg("Hello " + str(x))).grid(row=row, column=1)

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
    
    def printMsg(self, msg):
        print(msg)

if __name__ == "__main__":
    root=TK.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()