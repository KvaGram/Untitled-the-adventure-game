import game_utilities as game
import random
# world is the dictionary list of rooms, events, special functions etc you can call/visit.
# savedata is the save-file, with all choices and saved data so far, this also includes some temporary data.

def main(save):
    def newgame():
        #region NEW GAME
        save.setdata("room", "apartment")
        save.setdata("prevroom", "apartment")
        game.rolltext("""
Weeeee.. you are flying though the sky!
Below you are a beutiful forest, as green as anything you could ever imagine!
Deep down you know you are dreaming, but you can't quite get yourself to wake up.
suddenly you are in a vintage open cokpit biplane flying over the same lands...
                            **CRASH**

Your eyes shook open! Out the window you see the landscape you pictured in your dream.
It seems so nice, yet something seems off. Everything seems off.
You even struggle to remeber your own name.. What.. was.. what was your name?
    """)

        nameExcuses = ["or maybe it was", "no why would.. that be my name.. no it must be ", "no.. ugh.. why can't I remeber my name. Maybe it was", "no no no no! That can't be right, so it must be", "no, I think thats my best friend's name. wait, I got a best friend?? ugh.. what is my name??"]

        inp = ""
        while True:
            inp = input()
            print ()
            if game.yesno("ugh.. Was it {0}?".format(inp)):
               break
            print (random.choice(nameExcuses))
        save.setdata("name", inp)
        game.rolltext("""
Yes {0} the.. uhh.. something something title titles..
You are sure you'll remeber soon enough. Your head is quite foggy.
You think you might have a headache, but you are not sure.
Looking around you see you are in a small room, an apartment maybe? Maybe a hotell room?
You are sitting on the edge of a large bed. next to the bed is a small table.
On the table there are some small white spheres, a glass of water and two framed pictures face down
At the head end of the bed there is a window.
Towards the end of the room there is a sink with a mirror.
At the end is a door, probobly the exit by the looks of it.

        """.format(save.getdata("name")))
        #endregion NEW GAME
    def sink():
        #region Sink()
        if(save.getdata("apartment:sink")):
            game.showtext("The mirror is still broken.")
        else:
            save.setdata("apartment:sink", True)
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
        if save.getdata("apartment:window"):
            game.rolltext("""
You enjoy the holographic nature outside the window.
...
...
a holographic deer just walked past.
....
Time to go.
        """)
        else:
            save.setdata("apartment:window", True)
            game.rolltext("""
You look though the window into the lush forest landscape.
...
The nature seems oddly calming, yet somehow uncanny
...
...
As you move your head around to look form diffrent angles, you notice a sutle lag.
...
You recognize this now.
It is a hologram.
Probobly a cheap class 3 eye-tracking laser-holo, you suddenly realize.
Not that you remeber what that is, or what it means.
Only that you had a class 5 back..
...
back home...
..had.. back home...
so this isen't home then...?
    """)
        #endregion window() 
    def table():
        #region table()
        def glassText():
            g = save.getdata("apartment:glass")
            if g == None or g == 2:
                return "a full glass of water"
            elif g == 1:
                return "aalf glass of water"
            else:
                return "an empty glass"
            #end of glass description
        def pillsText():
            if(save.getdata("apartment:pills")):
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
        a = game.choose(["Glass", "Cyan framed picture", "Golden framed picture", "back off"])
        if a == 0:
            g = save.getdata("apartment:glass")
            if g == None or g == 2:
                save.setdata("apartment:glass", 2)
                if(game.yesno("Take the pills?")):
                    game.showtext("You take the white pills and drink from the glass.")
                    save.setdata("apartment:pills", True)
                    save.setdata("apartment:glass", 1)
                else:
                    game.showtext("You did not take the pills")
            elif g == 1:
                print ("The glass is half empty. Or is it half full?")
                if(game.yesno("Drink from the glass?")):
                    game.showtext("you drank the rest. The glass is now empty.")
                    save.setdata("apartment:glass", 0)
                else:
                    game.showtext("you left the glass alone")
            else:
                game.showtext("The glass is empty")
        elif a == 1:
            j = save.getdata("jeff")
            if(j == None):
                if(save.getdata("klara") == None):
                    j = "spouse"
                else:
                    j = "sibling"
                save.setdata("jeff", j)
                game.rolltext("""
You stare closly at the man in the cyan framed picture.
He looks familiar. Very familiar.
You seem to remeber he insisted you did not need some expensive frame for his picture.
You study his features closly.
suddenly it clicks in your mind.
You recognize him now. It is Jeff, your {0}.
                """.format(game.getGenderedTerm(j, "male")))
            else:
                game.showtext("It is Jeff, your {0}".format(game.getGenderedTerm(j, "male")))
        elif a == 2:
            k = save.getdata("klara")
            if(k == None):
                if(save.getdata("jeff") == None):
                    k = "spouse"
                else:
                    k = "sibling"
                save.setdata("klara", k)
                game.rolltext("""
You stare closly at the lady in the gold framed picture.
You study her close, trying to rember who she is
As you are looking in her eyes when you realize who she is.
Her name is Klara, you seem to remeber.
Klara.. she is your {0}! 'How could you forget that?', you wonder.
                """.format(game.getGenderedTerm(k, "female")))
            else:
                game.showtext("It is Klara, your {0}".format(game.getGenderedTerm(k, "female")))
        else:
            return
        table() #repeat
        #endregion table()    
    def door():
        #region door()
        if save.getdata("apartment:pills"):
            game.rolltext("""
You walk to the door.
Your head is starting to clear up.
You open the door, and walk out.
            """)
            return True
        else:
            game.rolltext("""
You walk towards the door.
Suddenly there is a sharp spike of pain in your head.
When it is over you are back on the bed, panting.
            """)
        return False
        #endregion door()

    if(save.getdata("name") == None):
        newgame()
    choices = ["look out the window", "examine the table", "examine the sink", "go to the door"]
    end = False
    while not end:
        game.showtext("You are sitting on the side of the bed")
        choice = game.choose(choices)
        if choice == 0:
            window()
        elif choice == 1:
            table()
        elif choice == 2:
            sink()
        elif choice == 3:
            if(door()):
                return save.goto("middle")
            pass
        #if room is revisited after the reactor counter has been enabled,
        #you will be wasting time here.
        status = game.updateCounter(save, "reactorC", -1)
        if status == "death":
            end = True



if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")