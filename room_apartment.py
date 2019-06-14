import Game
import random

def main(game:Game.Game):
    navdata:Game.Navdata = game.Navdata
    T = Game.Gettexter(game)
    def newgame():
        navdata.navtext = T("APT_NAVTEXT_1")
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
        navdata.navtext = T("APT_NAVTEXT_2")
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
                return "{APT_GLASS_1}"
            elif g == 1:
                return "{APT_GLASS_2}"
            else:
                return "{APT_GLASS_3}"
            #end of glass description
        def pillsText():
            if(game.getdata("apartment:pills")):
                return ""
            else:
                return "{APT_PILLS}"
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
                if(game.yesno("{APT_GLASS_QUEST_1}")):
                    game.showtext("{APT_GLASS_1}")
                    game.setdata("apartment:pills", True)
                    game.setdata("apartment:glass", 1)
                    game.setInventory("HEADACHE", False)
                else:
                    game.showtext("{APT_GLASS_2}")
            elif g == 1:
                game.showtext ("{APT_GLASS_3}")
                if(game.yesno("{APT_GLASS_QUEST_2}")):
                    game.showtext("{APT_GLASS_4}")
                    game.setdata("apartment:glass", 0)
                else:
                    game.showtext("{APT_GLASS_5}")
            else:
                game.showtext("{APT_GLASS_6}")
        elif data.tag == "CYAN":
            m = game.getdata("malefam", None)
            f = game.getdata("femalefam", None)
            if m == None:
                game.rolltext("""
You stare closely at the man in the cyan framed picture.
He looks familiar. Very familiar.
You seem to remember he insisted you did not need some expensive frame for his picture.
You study his features closely.
Suddenly it clicks in your mind.
You recognize him now. You think you remeber his name.""")
                indata = game.textin((("name:", "Jeff"),), "What is his name?", True)[1]
                mName = indata[0][1]
                if f:
                    mRole = "sibling"
                else:
                    mRole = "spouse"
                game.setMaleFam(mRole, mName) 
                game.showtext("That's right! It's {game.MaleFam.name} your {game.MaleFam.GenderedRole}!" )
            else:
                game.showtext("It is {game.MaleFam.name} your {game.MaleFam.GenderedRole}." )
        elif data.tag == "GOLD":
            m = game.getdata("malefam", None)
            f = game.getdata("femalefam", None)
            if f == None:
                game.rolltext("""
You stare closely at the lady in the gold framed picture.
You study her close, trying to remember who she is.
As you are looking in her eyes when you realize who she is.
You suddenly recall her name!""")
                indata = game.textin((("name:", "Klara"),), "What is her name?", True)[1]
                fName = indata[0][1]
                if m:
                    fRole = "sibling"
                else:
                    fRole = "spouse"
                game.setFemaleFam(fRole, fName)
                game.showtext("{game.FemaleFam.name} was her name! It's {game.FemaleFam.name} your {game.FemaleFam.GenderedRole}! How could you have forgotten?" )
            else:
                game.showtext("It is {game.FemaleFam.name} your {game.FemaleFam.GenderedRole}." )
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
            game.rolltext("""
You walk towards the door.
Suddenly there is a sharp spike of pain in your head.
When it is over you are back on the bed, panting.""")
            return False
        else:
            game.rolltext("""
You walk to the door.
Your head is starting to clear up.
You open the door, and walk out.
            """)
            return True
        #endregion door()

    if(game.getdata("name") == None):
        newgame()
    navdata.closed = True
    navdata.navtext = T("APT_NAVTEXT_2")
    choices = (
        ("WINDOW", "look out the window"),
        ("TABLE", "examine the table"),
        ("SINK", "examine the sink"),
        ("DOOR", "go to the door")
        )
    end = False
    while not end:
        game.showtext("You are sitting on the side of the bed")
        game.choose(choices, "What do you wish to do?")
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