import Game
import random
import General
from General import Runner_WheelC_Rings as Runner

def main(game:Game.Game):
    runner = Runner(game)
    #OLD CODE, to be rewritten
    
    #region actions and places
    def sectionDdoor():
        game.rolltext("{INNER_SEC_D_DOOR}")
    def sectionCdoor():
        game.rolltext("{INNER_SEC_C_DOOR}")

    #importing elevator event
    elevator = General.elevator(game)
    #importing ladder
    ladder = General.LadderAccess(game, goto)

    def sectionBdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionAdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionBdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionAdoor_read():
        game.showtext("PLACEHOLDER")

    #groups that can be saved.
    #126 people can be saved.
    def tubes(num):
        def chamberRoom():
            key = save.getdata("auxcom:stasispasskey", False)
            visited = save.getdata("inner:stasisroom:"+str(num), False)
            peopleSaved = save.getdata("stasis:peopleSaved", 0)
            if key == False:
                game.rolltext("""
A panel of the door indicates the chamber is closed down by emergency lockdown.
You would need an override key to open it.""")
                game.updateCounter(save, "reactorC", 1) #refunded time cost.
                return
            elif visited:
                game.showtext("You have already cleared this chamber.")
                game.updateCounter(save, "reactorC", 1) #refunded time cost.
            else:
                if num == 0:
                    game.rolltext("""
You enter the chamber, checking each of the stasis tubes.
Most of them are empty. But not all.
So many dead people.
Dead..
Empty, empty, dead,
empty, empty..
You were about to give up when one chamber your almost passed as empty had someone inside it.
You activated the emergency defrost, and resuced a small child.
You told the kid to evacuate.
                    """)
                    peopleSaved += 1
                elif num == 1 or num == 7 or num == 11:
                    game.rolltext("""
You enter the chamber, checking each of the stasis tubes.
Only some of them are empty.
So many people are dead.
You found 17 people alive.
As you retrived them, none of them were in any condition to help you out.
You just told them to evacuate as you hurried on with your business.
                    """)
                    peopleSaved += 17
                elif num == 2 or num == 6:
                    game.rolltext("""
You enter the chamber, checking each of the statis tubes.
All of them are empty!
Well, that's good news.
                    """)
                    peopleSaved += 0
                elif num == 3:
                    game.rolltext("""
You enter the chamber, you were about the check the tubes when you stumbed on someone.
A man. He is unconscious, but alive.
You decide to ingore him for now, to check on the stasis tubes.
In this chamber, it seems a number of the people died during the emergency wakeup.
You found 4 people still alive in stasis.
You brought them out. It took a moment, but you them to help the unconscious man to evacuate.
                    """)
                    peopleSaved += 5
                elif num == 4 or num == 9:
                    game.rolltext("""
You enter the chamber, checking each of the chambers.
What you saw almost mad.. scatch that. it did make you puke.
All of them were dead. All of them.
                    """)
                    peopleSaved += 0
                elif num == 5:
                    game.rolltext("""
The room is chamber with smoke! You fight your way though taking longer
than normal to check all the tubes.
It seems the automatic system that was supposed to wake this group shut itself down
due to the smoke. This smoke would likly kill anyone coming out of stasis unasisted.
That might have been a mixed blessing, as you found most of the occupants still alive.

You took care to help everyone out of stasis, and on their way out to evacuate.
                    """)
                status = game.updateCounter(save, "reactorC", -1)
                peopleSaved += 45
                if status == "death": #if reactor counter reach 0, and the game ends.
                    nav.running = False
                    return
                elif num == 8 or num == 10:
                    game.rolltext("""
You enter the chamber checking each tube.
A found a uneasy number of dead people.
But 12 people were still alive to be revived from stasis.
                    """)
                    peopleSaved += 12
                
            save.setdata("inner:stasisroom:"+str(num), True)
            save.setdata("stasis:peopleSaved", peopleSaved)
        return chamberRoom

    

    #endregion actions and places
    #---------------------------
    def goto(room):
        nav.running = False
        save.goto(room)
    def initNav():
        sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
        sectionA.append((tubes(0), "Stasis tubes 000 - 049", "enter"))      #A 1
        sectionA.append((tubes(1), "Stasis tubes 050 - 099", "enter"))      #A 2
        sectionA.append((tubes(2), "Stasis tubes 100 - 149", "enter"))      #A 3
        sectionA.append((elevator, "Elevator C1A", "use"))                  #A 4
        sectionA.append((tubes(3), "Stasis tubes 150 - 199", "enter"))      #A 5
        sectionA.append((tubes(4), "Stasis tubes 200 - 249", "enter"))      #A 6
        sectionA.append((tubes(5), "Stasis tubes 250 - 299", "enter"))      #A 7
        sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 8

        sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
        sectionB.append((tubes(6), "Stasis tubes 300 - 349", "enter"))      #B 1
        sectionB.append((tubes(7), "Stasis tubes 350 - 399", "enter"))      #B 2
        sectionB.append((tubes(8), "Stasis tubes 400 - 449", "enter"))      #B 3
        sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 4 (entry and exit to and from other rings in the wheel)
        sectionB.append((tubes(9), "Stasis tubes 450 - 499", "enter"))      #B 5
        sectionB.append((tubes(10), "Stasis tubes 500 - 549", "enter"))     #B 6
        sectionB.append((tubes(11), "Stasis tubes 650 - 699", "enter"))     #B 7
        sectionB.append((sectionCdoor, "Section C", "examine"))             #B 8

        prevroom = save.getdata("prevroom")
        if prevroom == "laddershaft":
            nav.setSection("B", 4)
            intro = """
You close the emergency ladder's hatch.
You are now at the inner level ring.
            """
        else:
            nav.setSection("A", 0)
            intro = """
You have walked around aimlessly for a bit, you don't know for how long
And oof! You just walked streight into a large closed door.
            """
        game.rolltext(intro, 0.3)
    if not nav.running:
        initNav()
    nav.loop(save)
    
if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")