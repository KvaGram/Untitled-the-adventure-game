from untitled_const import IMAGE_DIR
import os
import tkinter as TK
from PIL import Image, ImageTk

_TEST_BACK_IMG = os.path.join(IMAGE_DIR, "mapB.png")
_TEST_MID_IMG  = os.path.join(IMAGE_DIR, "InnerB.png")
_TEST_FRONT_IMG = os.path.join(IMAGE_DIR, "dot.png")
_MAP_SIZE = (200, 200)

class Mapnav(TK.Frame):
    def __init__(self, master, **kw):
        super().__init__(master = master, **kw)

        backlayerData  = Image.open(_TEST_BACK_IMG ).convert("RGBA").resize(_MAP_SIZE)
        midlayerData   = Image.open(_TEST_MID_IMG  ).convert("RGBA").resize(_MAP_SIZE)
        frontlayerData = Image.open(_TEST_FRONT_IMG).convert("RGBA")

        combo = Image.new("RGBA", _MAP_SIZE, "white")
        combo.paste(backlayerData, (0,0), backlayerData)
        combo.paste(midlayerData, (0,0), midlayerData)
        combo.paste(frontlayerData, (40,120), frontlayerData)

        self.imagedata = ImageTk.PhotoImage(image=combo)
        self.mapImage = TK.Label(master= self, image = self.imagedata)
        self.nameLabel  = TK.Label(master = self, text = "Example")

        self.mapImage.pack()
        self.nameLabel.pack()

if __name__ == "__main__":
    root = TK.Tk()
    mapnav = Mapnav(master = root)
    
    mapnav.pack()
    root.mainloop()
