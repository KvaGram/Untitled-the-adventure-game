import tkinter as TK

root = TK.Tk()
def buildNAV(master, numAction = 1, updown = True, leftright = True):
    nav_root = TK.Frame(master)
    nav_top = TK.Frame(nav_root)
    nav_bottom = TK.Frame(nav_root)
    nav_top.pack()
    nav_bottom.pack(side=TK.BOTTOM)
    if(updown):
        btn_up = TK.Button(nav_bottom, text="UP")
        btn_up.pack()
    if(leftright):
        btn_left = TK.Button(nav_bottom, text="LEFT")
        btn_left.pack(side=TK.LEFT)
    nav_actions = BuildActionButtons(nav_bottom, numAction)
    nav_actions.pack()

    location = TK.Label(nav_root, text="DUMMY LOCATION") 
    location.pack(side=TK.MITER)

    return nav_root
def BuildActionButtons(master, numButtons = 1):
    act_root = TK.Frame(master)
    for i in range(numButtons):
        btn = TK.Button(act_root, text="ACTION {0}".format(i+1))
        btn.pack()
    return act_root

if __name__ == "__main__":
    root = TK.Tk()
    UI_NAV = buildNAV(root)
    UI_NAV.pack()
    root.mainloop()