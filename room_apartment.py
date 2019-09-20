import Game
import random
from untitled_const import NAV_LIT_MIDDLE_A
from untitled_const import NAV_MIDDLE_RADIUS

def Start(game:Game.Game):
    #Resetting the NAV data module.
    navdata:Game.Navdata = game.Navdata
    #Getting quick-translate 
    T = Game.Gettexter(game)
    
    #Arrow inputs are not used here
    navdata.closed = True
    #Setting name, dot-radius and dot-radianrotation
    navdata.AreaName = T("AREANAME_APARTMENT")
    navdata.MapRadius = NAV_MIDDLE_RADIUS
    navdata.MapRadians = 3.8 #where Tau (6.28) is a full rotation.
    def newgame():
        navdata.AreaName = T("AREANAME_UNKNOWN")

        #region NEW GAME
        game.place = "apartment"
        game.setInventory("HEADACHE", True)
        game.rolltext("{APT_DREAM}")

        nameExcuses = T("APT_NAME_EXCUSES").split("\n")
        inp = game.PlayerName
        while True:
            #ask for text input, name, wait for response, get the data. We assume type is textin.
            indata = game.textin((("Name", inp),), T("APT_NAME_SUBMIT"), True)[1]
            #from indata get first element, then get the text inputted
            inp = indata[0][1]
            if len(inp) < 1:
                #if no input, re-request input
                continue
            game.setdata("name", inp)
            if game.yesno("{APT_NAME_CONFIRM}"):
               break
            game.showtext(random.choice(nameExcuses))
        navdata.AreaName = T("AREANAME_APARTMENT")
        game.rolltext("{APT_NAME_CONFIRMED}")
        #endregion NEW GAME
    def sink():
        #region Sink()
        if(game.getdata("apartment:sink")):
            game.showtext("{APT_SINK_2}")
        else:
            game.setdata("apartment:sink", True)
            game.rolltext("{APT_SINK_1}")
        #endregion Sink
    def window():
        #region window()
        if game.getdata("apartment:window"):
            game.rolltext("{APT_WINDOW_2}")
        else:
            game.setdata("apartment:window", True)
            game.rolltext("{APT_WINDOW_1}")
        #endregion window() 
    def table():
        frags = {}
        #region table()
        def glassText():
            g = game.getdata("apartment:glass")
            if g == None or g == 2:
                return "{APT_GLASS_FRAG_1}"
            elif g == 1:
                return "{APT_GLASS_FRAG_2}"
            else:
                return "{APT_GLASS_FRAG_3}"
            #end of glass description
        def pillsText():
            if(game.getdata("apartment:pills")):
                return ""
            else:
                return "{APT_PILLS_FRAG}"
        #end of pills description
        frags["_GLASS"] = glassText()
        frags["_PILLS"] = pillsText()
        game.rolltext("{APT_TABLE}", frags = frags)
        choices = (("GLASS", T("APT_TABLE_OPTION_GLASS")),("CYAN", T("APT_TABLE_OPTION_CYAN")),("GOLD", T("APT_TABLE_OPTION_GOLD")),("BACK", T("APT_TABLE_OPTION_BACK")),)
        data:Game.ActDataInput = game.choose(choices, T("APT_TABLE_QUEST"), True)
        
        if data.tag == "GLASS":
            g = game.getdata("apartment:glass")
            if g == None or g == 2:
                game.setdata("apartment:glass", 2)
                game.showtext ("{APT_GLASS_EX_1}")
                if(game.yesno("{APT_GLASS_QUEST_1}")):
                    game.showtext("{APT_GLASS_TAKE_1}")
                    game.setdata("apartment:pills", True)
                    game.setdata("apartment:glass", 1)
                    game.setInventory("HEADACHE", False)
                else:
                    game.showtext("{APT_GLASS_NOTAKE_1}")
            elif g == 1:
                game.showtext ("{APT_GLASS_EX_2}")
                if(game.yesno("{APT_GLASS_QUEST_2}")):
                    game.showtext("{APT_GLASS_TAKE_2}")
                    game.setdata("apartment:glass", 0)
                else:
                    game.showtext("{APT_GLASS_NOTAKE_2}")
            else:
                game.showtext("{APT_GLASS_EX_3}")
        elif data.tag == "CYAN":
            m = game.getdata("malefam", None)
            f = game.getdata("femalefam", None)
            if m == None:
                game.rolltext("{APT_CYAN_1}")
                indata = game.textin((("name:", "Jeff"),), "{APT_CYAN_SUBMIT}", True)[1]
                mName = indata[0][1]
                if f:
                    mRole = "sibling"
                else:
                    mRole = "spouse"
                game.setMaleFam(mRole, mName) 
                game.showtext("{APT_CYAN_2}")
            else:
                game.showtext("{APT_CYAN_3}")
        elif data.tag == "GOLD":
            m = game.getdata("malefam", None)
            f = game.getdata("femalefam", None)
            if f == None:
                game.rolltext("{APT_GOLD_1}")
                indata = game.textin((("name:", "Klara"),), "{APT_GOLD_SUBMIT}", True)[1]
                fName = indata[0][1]
                if m:
                    fRole = "sibling"
                else:
                    fRole = "spouse"
                game.setFemaleFam(fRole, fName)
                game.showtext("{APT_GOLD_2}")
            else:
                game.showtext("{APT_GOLD_3}")
        else:
            return
        table() #repeat
        #endregion table()    
    def door():
        ache = game.getInventory("HEADACHE")
        left = game.getdata("apartment:left", False)
        #region door()
        if left:
            return True
        elif ache:
            game.rolltext("{APT_DOOR_1}")
            return False
        else:
            game.rolltext("{APT_DOOR_2}")
            return True
        #endregion door()

    if(game.getdata("name") == None):
        newgame()
    choices = (
        ("WINDOW", T("APT_OPTION_WINDOW")),
        ("TABLE", T("APT_OPTION_TABLE")),
        ("SINK", T("APT_OPTION_SINK")),
        ("DOOR", T("APT_OPTION_DOOR")),
        )
    end = False
    while not end:
        game.showtext("{APT_BED}")
        game.choose(choices, "{APT_BED_QUEST}")
        data = game.wait()
        if data.Type != "action":
            continue
        choice = data.tag

        if choice == "WINDOW":
            window()
        elif choice == "TABLE":
            table()
        elif choice == "SINK":
            sink()
        elif choice == "DOOR":
            if(door()):
                game.place = "middle"
                return 

        #if room is revisited after the reactor counter has been enabled,
        #you will be wasting time here.
        status = game.updateCounter("reactorC", -1)
        if status == "death":
            end = True



if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    print("Testcode is not written yet.\nPlease run from main.py instead.")