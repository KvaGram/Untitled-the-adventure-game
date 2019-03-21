import game_utilities as game

class roomdata:
    ind = 0 #current location, index
    sec = "A" #current location, section
    running = True #run-status on local game-loop
def main(save):
    sectionA = []
    sectionB = []
    nav = roomdata()
    intro = "place holder corridor intro text (should not show up in the game)"
    def sectionDdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted ingraving on the door, it reads
        _____________________
        |    C3 SECTOR D    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door. There is a faint glow coming from the window.
You look though the window.
On the other side you see a corridor much like the one you are in
except, its on fire!
What happend here?
        """, 0.3)
    def elevator():
        game.rolltext("""
The elevators breaks up the corridor, as the corridor splits to around a large round column you learn is the elevator shaft,
the walls around bending outwards giving way for the path around the shaft until they hit flat outer walls.
You find six elevator doors in pairs of two around the large cylinder.
You also locate a set of call-buttons for up and cargo, whatever that cargo one means.
        """, 0.4)
        choices = ["Press UP call button", "Press CARGO call button", "Leave"]
        a = game.choose(choices)
        if a < 3:
            if(save.getdata("WheelC_elevator") == "dead"):
                text = """
You press the button.
...
Nothing happened.
                """
            else:
                text = """
You press the button.
The button flash on.
...
You hear an odd clang
...         """
                if a == 2:
                    text += "\nTwo of the elevator doors open in a very slight crack."
                else:
                    text += "\nOne of the elevator doors open in a very slight crack."
                text += "\nThen you hear a fizzeling sound, and everything stops working"
                save.setdata("WheelC_elevator", "dead")
            game.rolltext(text)
        else:
            game.showtext("You left the elevators alone")
    def sectionBdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.ind = 0
        nav.sec = "B"
    def sectionAdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.ind = 5
        nav.sec = "A"
    def auxcom():
        game.showtext("This auxillary comunication system on this level is broken.")
        #TODO: idea: attempt to connect to this from middle level to activiate this one
    def ladder():
        text = """
The corridor gives way to a large column, splitting the corridor to go around it on both sides.
On two sides of the column you find large hatches with a colored engraving
        |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
        |    EMERGENCY ESCAPE   |
        |      WHEEL C RING 3   |
        |                       |
        |      BREAK GLASS      |
        |          AND          |
        |       PULL LEVER      |
        |        TO OPEN        |
        |_______________________|

You locate the panel as indicated on the engraving.
        """
        if save.getdata("WheelCOuterLadder") == "open":
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
            if save.getdata("WheelCOuterLadder") == None:
                save.setdata("WheelCOuterLadder", "open")
            game.rolltext(enterText,0.5)
            goto("ladder")
    def sectionCdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted ingraving on the door, it reads
        _____________________
        |    C3 SECTOR C    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door, you look though it.
On the other side you see.. nothing. just blackness.
No, that's not quite right. As your eyes get used to the dark,
you see the walls on the other side of the door.
They go on for a bit over a meter, then abruptly ends in uneven bent metal.
After that, aside from what looks to be some solid tick tube, there is nothing but darkness.
darkness and... lights. moving lights.
Stars, you realize. Stars flying upwards. You are staring into space!
    """, 0.3)
    def reactNode():
        game.showtext("Placeholder. Yeah, important path in the game here. Sorry it is incomplete!")
        game.rolltext("""
The door in front of you are full of warning and hazard signs.
Reactor-ring control node, radiation hazard, chemical hazard, tachyon hazard.
        """)
        if not game.yesno("Are you sure you want to go inside?"):
            return
        #Idea:
        # The reactor may have one day been a marvel of tachyon engineering.
        #A machine that could beat entropy to a pulp, now dieing to it.
        gender = game.getGender(save)
        game.rolltext("""
Alarms bleeping, lights flashing, plasma leaking, then unleaking, as small pockets of local spacetime loops.


.
.
.
..
..
...
....
.......
...........
.......
....
...
..
..
.
.
.
        """)

    def goto(room):
        nav.running = False
        save.goto(room)

    sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
    sectionA.append((elevator, "Elevator C2A", "use"))                  #A 1
    sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 2

    sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
    sectionB.append((auxcom, "Auxillary communications", "use"))        #B 1
    sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 2 (entry and exit to and from other rings in the wheel)
    sectionB.append((reactNode, "Reactor-ring access node", "enter"))   #B 3
    sectionB.append((sectionCdoor, "Section C", "examine"))             #B 4

    prevroom = save.getdata("prevroom")
    if prevroom == "laddershaft":
        nav.ind = 2
        nav.sec = "B"
        intro = """
You close the emergency ladder's hatch.
You are now at the outer level ring.
        """
    else:
        nav.ind = 0
        nav.sec = "A"
        intro = """
You have walked around aimlessly for a bit, you don't know for how long
And oof! You just walked streight into a large closed door.
        """
    game.rolltext(intro, 0.3)
    while nav.running:
        place = None
        disp = "ERROR"
        action = " - "
        canRight = False
        canLeft = False
        places = []
        if nav.sec == "A":
            places = sectionA
        elif nav.sec == "B":
            places = sectionB
        try:
            place = places[nav.ind][0]
            disp =  places[nav.ind][1]
            action =  places[nav.ind][2]
            canRight = nav.ind > 0
            canLeft = nav.ind < len(places)-1
        except:
            pass
        
        message = "You are now next to {0}, what will you do?".format(disp)
        choices = [canLeft and "GO LEFT" or "GO LEFT({0})".format(action), action, canRight and "GO RIGHT" or "GO RIGHT({0})".format(action)]
#        a = -1
#        while a == -1:
        a = game.choose(choices, message)
        if a == 0:
            if canLeft:
                nav.ind += 1
            else:
                a = 1
        elif a == 2:
            if canRight:
                nav.ind -= 1
            else:
                a = 1
        if a == 1: #note: uses if instead of elsif, as the value of a can be changed in above conditions.
            #note: ticks the reactorC counter if enabled.
            status = game.updateCounter(save, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                nav.running = False
            else:
                place()

if __name__ == "__main__":
    game.showtext("testcode for outer ring module not written yet.\nPlease run from main.py instead.")