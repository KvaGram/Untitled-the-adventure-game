import game_utilities as game
import random
import dialoges
def main(save):
    sectionA = []
    sectionB = []
    class outerRoomNAV(game.RoomNav1D):
        def __init__(self):
            super().__init__(termPlus= "GO LEFT", termMinus= "GO RIGHT")

        sec = "A" #current location, section
        #Override
        def runAction(self):
            act,_,_ = self.getPlace()
            #note: ticks the reactorC counter if enabled.
            status = game.updateCounter(save, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                self.running = False
            else:
                act()
        def setSection(self, newSec, newInd):
            if newSec == "A":
                self.places = sectionA
            elif newSec == "B":
                self.places = sectionB
            else:
                raise("INVALID ROOM SECTION LABEL")
            self.sec = newSec
            self.ind = newInd
    nav = outerRoomNAV()
    intro = "place holder corridor intro text (should not show up in the game)"
    #region actions and places
    def sectionDdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted ingraving on the door, it reads
        _____________________
        |    C1 SECTOR D    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door. There is a faint glow coming from the window.
You look though the window.
On the other side you see a corridor much like the one you are in
except, it is littered by dead people, and remains from broken stasis chambers.
What happend here?
        """)
    def sectionCdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted ingraving on the door, it reads
        _____________________
        |    C1 SECTOR C    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door, you look though it.
You see the roof and most of the frame of the corridor ahead go on,
with the occational blink from the roof light.
Most of the corridor is blown open to darkness.
And you see some small faint light far back in the darknes, moving.
Stars, you realize. Stars flying upwards. You are staring into space!
    """)

    def elevator():
        dialoges.elevator(save)
    
    def ladder():
        text = """
The corridor gives way to a large column, splitting the corridor to go around it on both sides.
On two sides of the column you find large hatches with a colored engraving
        |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
        |    EMERGENCY ESCAPE   |
        |      WHEEL C RING 1   |
        |                       |
        |      BREAK GLASS      |
        |          AND          |
        |       PULL LEVER      |
        |        TO OPEN        |
        |_______________________|

You locate the panel as indicated on the engraving.
        """
        if save.getdata("WheelCInnerLadder") == "open":
            text += "\nThe glass is already broken."
            enterText = "You reach in the panel, and pull the lever.\nThe hatch opens and you go inside."
            openText = "Pull the lever?"
        else:
            text += "\nThe glass look thin and you feel an odd temtation to smash it.\nWritten on the glass is a warning."
            text += "\nFOR EMERGENCIES ONLY.\nSECURITY WILL BE ALERTED TO MISUSE!"
            enterText = "You smash the glass, and pull the lever.\nThe hatch opens and you go inside."
            openText = "Smash the glass?"
        game.rolltext(text, 0.3)
        if(game.yesno(openText)):
            if save.getdata("WheelCInnerLadder") == None:
                save.setdata("WheelCInnerLadder", "open")
            game.rolltext(enterText,0.5)
            goto("ladder")


    def sectionBdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.setSection("B", 0)
    def sectionAdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.setSection("A", 8)

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
    nav.loop()
    
if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")