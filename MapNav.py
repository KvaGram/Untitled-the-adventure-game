import os
import tkinter as TK
from PIL import Image, ImageTk
import math
import time

from untitled_const import(
IMAGE_DIR,
NAV_LIT_CORE,
NAV_BACK_INTACT,
NAV_DOT,
DEFAULT_MAP_SIZE,
DEFAULT_DOT_SIZE,
TAU,
) #constants imported.

class Mapnav(TK.Frame):
    def __init__(self, master, **kw):
        super().__init__(master = master, **kw)
        self._dotstate = None
        self._dotimage =  NAV_DOT       
        self._backimage =  NAV_BACK_INTACT       
        self._litimage =  NAV_LIT_CORE       

        self.image = None   #Image.new("RGBA", _MAP_SIZE, "white")
        self.tkImage = None #ImageTk.PhotoImage(image=self.image)
        self.areaName = TK.StringVar(value = "example")

        self.mapImage = TK.Label(master = self)
        self.nameLabel  = TK.Label(master = self, textvariable = self.areaName)

        self.refresh()

        self.mapImage.pack()
        self.nameLabel.pack()
    def refresh(self):
        self.image = Image.new("RGBA", DEFAULT_MAP_SIZE, "white")

        back = Image.open(self._backimage).convert("RGBA").resize(DEFAULT_MAP_SIZE)
        self.image.paste(back, (0,0), back)

        if (self._litimage):
            high = Image.open(self._litimage).convert("RGBA").resize(DEFAULT_MAP_SIZE)    
            self.image.paste(high, (0,0), high)
        if (self._dotstate):
            assert(type(self._dotstate) is tuple and len(self._dotstate) == 2)
            dot = Image.open(self._dotimage).convert("RGBA").resize(DEFAULT_DOT_SIZE)
            d0 = self._dotstate[0] - DEFAULT_DOT_SIZE[0]/2 + DEFAULT_MAP_SIZE[0]/2
            d1 = self._dotstate[1] - DEFAULT_DOT_SIZE[1]/2 + DEFAULT_MAP_SIZE[1]/2
            self.image.paste(dot, (math.floor(d0),math.floor(d1)), dot)

        self.tkImage = ImageTk.PhotoImage(image=self.image)
        self.mapImage.config(image = self.tkImage)
    def PlaceDot(self, radian, radius):
        x  = math.floor(math.cos(rot) * rad)
        y  = math.floor(math.sin(rot) * rad)
        self.DotState=(x,y)
    #region setters and getters
    @property
    def AreaName(self):
        return self.areaName.get()
    @AreaName.setter
    def AreaName(self, val):
        self.areaName.set(val)
    @property
    def DotState(self):
        return self._dotstate
    @DotState.setter
    def DotState(self, val):
        self._dotstate = val
        self.refresh()
    @property
    def DotImage(self):
        return self._dotimage
    @DotImage.setter
    def DotImage(self, val):
        _dotimage = val
        self.refresh()
    @property
    def BackImage(self):
        return self._backimage
    @BackImage.setter
    def BackImage(self, val):
        _backimage = val
        self.refresh()
    @property
    def LitImage(self):
        return self._litimage
    @LitImage.setter
    def LitImage(self, val):
        _litimage = val
        self.refresh()
    #endregion setters and getters
    

#imported from C# mathf library
def Repeat(t:float, length:float) -> float:
    return t - math.floor(t/length) * length

def pingpong(t, length) -> float:
    t = Repeat(t, length * 2)
    return length - abs(t - length)


if __name__ == "__main__":
    root = TK.Tk()
    mapnav = Mapnav(master = root)
    mapnav.pack()

    maxRad = 100
    radSpeed = 0.5 * 100

    rotspeed = 0.6 * TAU

    rad = 0
    rot = 0

    startTime = time.time()
    doAnimate = TK.BooleanVar(value = True)
    TK.Checkbutton(text = "Animate", variable = doAnimate).pack()
    
    radVar = TK.StringVar(value = rad)
    rotVar = TK.StringVar(value = rot)
    TK.Label(master=root, text = "Radius").pack()
    TK.Entry(master=root, textvariable = radVar).pack()
    TK.Label(master=root, text = "Rotation").pack()
    TK.Entry(master=root, textvariable = rotVar).pack()

    info = TK.Label(master = root)
    info.pack()
    while(True):
        if(doAnimate.get()):
            t = time.time() - startTime
            rad = pingpong(t * radSpeed, maxRad)
            rot = Repeat(t * rotspeed, TAU)

            radVar.set(f"{rad:.2f}")
            rotVar.set(f"{rot:.2f}")
        else:
            try:
                rad = float(radVar.get())
            except ValueError:
                rad = 0
            try:
                rot = float(rotVar.get())
            except ValueError:
                rot = 0
                
        mapnav.PlaceDot(rot, rad)
        info.config(text = f"X, Y {mapnav.DotState}")
        root.update()
        root.update_idletasks()
