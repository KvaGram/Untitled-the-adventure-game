import Game
import random

def main(game:Game.Game):
    def newgame():
        #region NEW GAME
        game.place = "apartment"
        game.setInventory("HEADACHE", True)
        game.rolltext("""
Weeeee.. you are flying through the sky!
Below you is a beautiful forest, as green as anything you could ever imagine!
Deep down you know you are dreaming, but you can't quite get yourself to wake up.
suddenly you are in a vintage open cockpit biplane flying over the same lands...
                            **CRASH**

Your eyes shook open! Out the window you see the landscape you pictured in your dream.
It seems so nice, yet something seems off. Everything seems off.
You even struggle to remember your own name... 
    """)

        nameExcuses = ["or maybe it was", "no why would.. that be my name.. no it must be ", "no.. ugh.. why can't I remember my name. Maybe it was", "no no no no! That can't be right, so it must be", "no, I think that's my best friend's name. wait, I got a best friend?? ugh.. what is my name??"]
        inp = game.PlayerName
        while True:
            #ask for text input, name, wait for response, get the data. We assume type is textin.
            indata = game.textin(("Name", inp), "What.. was.. what was your name?", True)[1]
            #from indata get first element, then get the text inputted
            inp = [0][1]
            if len(inp) < 1:
                #if no input, re-request input
                continue
            if game.yesno("ugh.. Was it {0}?".format(inp)):
               break
            game.showtext(random.choice(nameExcuses))
        game.setdata("name", inp)
        game.rolltext("""
Yes {0} the.. uhh.. something something title titles..
You are sure you'll remember soon enough. Your head is quite foggy.
You think you might have a headache, but you are not sure.
Looking around you see you are in a small room, an apartment maybe? Maybe a hotel room?
You are sitting on the edge of a large bed. Next to the bed is a small table.
On the table there are some small white spheres, a glass of water and two framed pictures face down
At the head end of the bed there is a window.
Towards the end of the room there is a sink with a mirror.
At the end is a door, probably the exit by the looks of it.

        """.format(game.PlayerName))
        #endregion NEW GAME
    def sink():
        #region Sink()
        if(game.getdata("apartment:sink")):
            game.showtext("The mirror is still broken.")
        else:
            game.setdata("apartment:sink", True)
            game.rolltext("""
You walk to the sink.
You see glass shards in the sink.
The mirror is broken.
What little of yourself you can see looks like a mess.
You might want to find a proper bathroom and freshen up a bit.
            """)
        #endregion Sink
    def window():
        #region window()
        if game.getdata("apartment:window"):
            game.rolltext("""
You enjoy the holographic nature outside the window.
...
...
a holographic deer just walked past.
....
Time to go.
        """)
        else:
            game.setdata("apartment:window", True)
            game.rolltext("""
You look through the window into the lush forest landscape.
...
The nature seems oddly calming, yet somehow uncanny
...
...
As you move your head around to look form different angles, you notice a subtle lag.
...
You recognize this now.
It is a hologram.
Probably a cheap class 3 eye-tracking laser-holo, you suddenly realize.
Not that you remember what that is, or what it means.
Only that you had a class 5 back..
...
back home...
..had.. back home...
so this isn't home then...?
    """)
        #endregion window() 
    def table():
        #region table()
        def glassText():
            g = game.getdata("apartment:glass")
            if g == None or g == 2:
                return "a full glass of water"
            elif g == 1:
                return "a half full glass of water"
            else:
                return "an empty glass"
            #end of glass description
        def pillsText():
            if(game.getdata("apartment:pills")):
                return ""
            else:
                return ", some small white pills"
        #end of pills description
        game.rolltext("""
You look at the nightstand table.
You see {0}{1}
and two framed pictures.
One with a cyan frame, one with a golden frame.
        """.format(glassText(), pillsText()))
        data = game.choose((("GLASS", "Glass"), ("CYAN","Cyan framed picture"), ("GOLD","Golden framed picture"), ("BACK","back off")), "What do you wish to examine", True)[1]
        a = data[1] #index of the choice
        if a == 0:
            g = game.getdata("apartment:glass")
            if g == None or g == 2:
                game.setdata("apartment:glass", 2)
                if(game.yesno("Take the pills?")):
                    game.showtext("You take the white pills and drink from the glass.")
                    game.setdata("apartment:pills", True)
                    game.setdata("apartment:glass", 1)
                    game.setInventory("HEADACHE", False)
                else:
                    game.showtext("You did not take the pills")
            elif g == 1:
                game.showtext ("The glass is half empty. Or is it half full?")
                if(game.yesno("Drink from the glass?")):
                    game.showtext("you drank the rest. The glass is now empty.")
                    game.setdata("apartment:glass", 0)
                else:
                    game.showtext("you left the glass alone")
            else:
                game.showtext("The glass is empty")
        elif a == 1:
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
                indata = game.textin(("name:", "Jeff"), "What is his name?", True)[1]
                mName = indata[0][1]
                if f:
                    mRole = "sibling"
                else:
                    mRole = "spouse"
                game.setMaleFam(mRole, mName) 
                game.showtext("That's right! It's {game.MaleFam.name} your {game.MaleFam.GenderedRole}!".format(game))
            else:
                game.showtext("It is {game.MaleFam.name} your {game.MaleFam.GenderedRole}.".format(game))
        elif a == 2:
            m = game.getdata("malefam", None)
            f = game.getdata("femalefam", None)
            if f == None:
                game.rolltext("""
You stare closely at the lady in the gold framed picture.
You study her close, trying to remember who she is.
As you are looking in her eyes when you realize who she is.
You suddenly recall her name!""")
                indata = game.textin(("name:", "Klara"), "What is her name?", True)[1]
                fName = indata[0][1]
                if m:
                    fRole = "sibling"
                else:
                    fRole = "spouse"
                game.setFemaleFam(fRole, fName)
                game.showtext("{game.FemaleFam.name} was her name! It's {game.FemaleFam.name} your {game.FemaleFam.GenderedRole}! How could you have forgotten?".format(game))
            else:
                game.showtext("It is {game.FemaleFam.name} your {game.FemaleFam.GenderedRole}.".format(game))
        else:
            return
        table() #repeat
        #endregion table()    
    def door():
        pills = game.getdata("apartment:pills", False)
        left = game.getdata("apartment:left", False)
        #region door()
        if left:
            return True
        elif pills:
            game.rolltext("""
You walk to the door.
Your head is starting to clear up.
You open the door, and walk out.
            """)
            game.setdata("apartment:left", True)
            return True
        else:
            game.rolltext("""
You walk towards the door.
Suddenly there is a sharp spike of pain in your head.
When it is over you are back on the bed, panting.
            """)
        return False
        #endregion door()

    if(game.getdata("name") == None):
        newgame()
    choices = (
        ("WINDOW", "look out the window"),
        ("TABLE" "examine the table"),
        ("SINK", "examine the sink"),
        ("DOOR", "go to the door")
        )
    end = False
    while not end:
        game.showtext("You are sitting on the side of the bed")
        game.choose(choices, "What do you wish to do?")
        data = game.wait()
        if data[0] != "action":
            continue
        choice = data[0][0]

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