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
        nav.setSection("A", 2)
    #endregion actions and places
    #---------------------------
    def goto(room):
        nav.running = False
        save.goto(room)

    sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
    sectionA.append((elevator, "Elevator C1A", "use"))                  #A 1
    sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 2

    sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
    sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 2 (entry and exit to and from other rings in the wheel)
    sectionB.append((sectionCdoor, "Section C", "examine"))             #B 3

    prevroom = save.getdata("prevroom")
    if prevroom == "laddershaft":
        nav.setSection("B", 1)
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