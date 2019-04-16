import game_utilities as game
import random
import dialoges
def main(save):
    sectionA = []
    sectionB = []
    class outerRoomNAV(game.RoomNav1D):
        termPlus = "GO LEFT"   #
        termMinus = "GO RIGHT" #
        roomname = "outer" #

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
    nav = outerRoomNAV.GET_NAV(save)
    intro = "place holder corridor intro text (should not show up in the game)"
    #---------------------------
    #region actions and places
    def sectionDdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted engraving on the door, it reads
        _____________________
        |    C3 SECTOR D    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door. There is a faint glow coming from the window.
You look through the window.
On the other side you see a corridor much like the one you are in
except, its on fire!
What happened here?
        """)
    def elevator():
        dialoges.elevator(save)
    def sectionBdoor():
        game.showtext("You pass through the open door separating the two sectors")
        nav.setSection("B", 0)
    def sectionAdoor():
        game.showtext("You pass through the open door separating the two sectors")
        nav.setSection("A", 2)
    #def auxcom():
    #    game.showtext("This auxillary comunication system on this level is broken.")
    #    #TODO: idea: attempt to connect to this from middle level to activiate this one
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
        game.rolltext(text)
        if(game.yesno(openText)):
            if save.getdata("WheelCOuterLadder") == None:
                save.setdata("WheelCOuterLadder", "open")
            game.rolltext(enterText)
            goto("ladder")
    def sectionCdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted engraving on the door, it reads
        _____________________
        |    C3 SECTOR C    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door, you look through it.
On the other side you see.. nothing. just blackness.
No, that's not quite right. As your eyes get used to the dark,
you see the walls on the other side of the door.
They go on for a bit over a meter, then abruptly ends in uneven bent metal.
After that, aside from what looks to be some solid tick tube, there is nothing but darkness.
darkness and... lights. moving lights.
Stars, you realize. Stars flying upwards. You are staring into space!
    """)

    def reactNode():
        game.rolltext("""
The door in front of you are full of warning and hazard signs.
Reactor-ring control node, radiation hazard, chemical hazard, tachyon hazard.
        """)
        if save.getdata("reactorC:fixed", False):
            game.rolltext("""You peek inside.
You catch a brief glimse of yourself operating the control system.
The reactor may not be entierly stable, but you have done what you could.
You closed the door so not to disturb yourself.""")
            return
        if not game.yesno("Are you sure you want to go inside?"):
            return
        #Idea:
        # The reactor may have one day been a marvel of tachyon engineering.
        #A machine that could beat entropy to a pulp, now dieing to it.
        g = game.getGender(save)
        p1 = "man" if g == "male" else "woman"
        p2 = "he" if g == "male" else "she"
        p3 = "his" if g == "male" else "her"
        #reason why this shutdwn could not be done remotly: temperal bleeding corrupted all data packages, repeating the signals randomly.
        game.rolltext("""
Alarms bleeping, lights flashing, plasma leaking, then unleaking, as small pockets of local spacetime loops.
As you enter the room you instinctivly step aside to let a oddly familiar {0} out of the room.
Suprisingly, {1} looked oddly familiar. Looking up from {2} hands and at you, the {0} looks as shocked as you.
But as suddenly as {1} appeared, the {0} suddenly dissappeard.

What was {1}? A ghost?

You sit down on the chair in front of the controls.
You look around at all the virtual knobs and dials on the control-screen.

Looking to your left, you find a manua.. wait.
..
it's gone.
no, now it's there again.
..and it's gone!
        """.format(p1, p2, p3))
        ind, val = game.choose2(("try to snatch the manual next time it appears", "randomly enter data into the control-screen"), "What will you do?")
        #stupid choice resulting in a game over:
        if(ind == 1):
            game.setGameover(save, "You got yourself trapped in a timeloop")
            game.rolltext("""
Not knowing what to do, you start hammering on the controls.
You tried adjesting that sqiggly thing, you tried to increase that number, you tried to stop that ticking..
you tried any little thing you could think of..
then you, without knowing what to do, start hammering on the controls.
you tried adjusting that sq..

you realized you were now doing what you did a minute ago. are you stu..
tried adjusting that little sqiggly..

uh no, you realize, as you got your thinking stright again.
you try to undo what you did when.. you try adjusting that sqiggly thi..

'shit' you managed to think as you suddenly find yourself trying to adjust that squigg..
and again.. at shorter and shorter intervals.

The after looping for what seemed like forever, with the intervals going shorter and shorter, they suddenly stopped getting shorter.
From what you could tell, with the little self awareness you could muster, the intervals were at about 1 secund.
And you soon realied why.

Aside from your little looping bobble, everything was gone.
You aren't dead. Not really. But by now, you wish you were.
            """)
            nav.running = False
            return
        #end of game over stupity
        game.rolltext("""
You hover your hand over where the manual were a secund ago.
...
There it is! you snatch it!
..!
Ouch!
You got the manual book in your hand, but your fingers are now covered in a layor of some oily substance.
And they feel cold, really cold and numb.
Looking at the where you picked up the manual, it suddenly flashed in again, despite also being in your hand.
Moreover, there was now something else.. your fingers!
your disenbodied fingers appearing out of nowhere to grab the manual,
only to dissappear, and reappear.
You decide to ignore this odd phenomenon, as you focus on your task.

Browsing the manual you find instructions for a number of emergency procedures.
        """)
        #You need to first initalize the emergency cooling system, then the emergency particle decelerator.
        choices = [
            ("COOL DOWN", "Initiate Emergency cooling system"),
            ("SLOW DOWN", "Engage emergency particle decelerator"),
            ("HURRY UP", "Engage emergency particle accelerator"),
            ("FIRE SUP 1", "Engage accellerator fire suppression system"),
            ("FIRE SUP 2", "Engage control room fire suppression system"),
            ("INFO", "Run automatic diagnostics"),
            ("INSTADEATH", "Engage emergency overload"),
            ("REVERSE", "Depolorize the tacheon emitter"),
            ("SHUTDOWN", "Shutdown tacheon emitter array")
            ]
        random.shuffle(choices)
        cooledDown = False # must be done first
        slowedDown = False # will cause a fire if done before cooldown
        #fireSuppressed_1 = False # will have no effect if there are no fire ### unused ###
        warnedOfLoops = False #unlocks with the INFO option, enables some alternate text.
        #depolorized = False #unlocks with the reversed option, it adds more time loops. ### unused ###

        fixing_reactor_loop = True

        while fixing_reactor_loop:
            ind, val = game.choose2(choices, "What procedure will you attept?" )
            if val == "SHUTDOWN":
                game.rolltext("""
You followed the instructions to shut down the the tacheon emitter array.
...
The system register succesful, then not successful shutdown, then both at the same time.
                """)
                if warnedOfLoops:
                    game.rolltext("""
It took you a moment to see it, but you now realized why this is.
Looking over the diagnatic data you retrived earlier,
you see most of the emitters are stuck in time-loops.
They are running perpetually.
Trying to just shutting them down just won't work.
                    """)
                else:
                    game.rolltext("""
You are completly baffled at what this. You ended the shutdown process.
You decide to try something else.
                    """)
                choices.pop(ind)
            elif val == "REVERSE":
                game.rolltext("""
You followed the instructions to depolarize the tacheon emitters, whatever that means.
Shortly after doing so, you noticed something quite off.
A hole just appeared in the side of the wall, then seemed to reassamle into a wall again before suddenly turning back into a hole, and repeated.
Whatever you just did, you are pretty sure you just made it all worse.
You decided not to try that again.
                """)
                #depolorized = True
                choices.pop(ind)
            elif val == "INSTADEATH":
                nav.running = False
                fixing_reactor_loop = False
                game.setGameover(game, "You found a way to blow youself up. You are very VERY dead!")
                game.rolltext("""
You followed the instructions for initiating an emergency overload.
Right after pressing the confirm key on the screen, you got an odd feeling.
The reactor started humming. Did you just make a huge mis..
...
You never got to finish that thought. You just ceased to exist.
To say you were atomized is not entierly accurate,
but that may be the closest terminology to describe what happened to you.
At least, there were no pain.
                """)
                return
            elif val == "FIRE SUP 2":
                game.rolltext("""
You followed the quite simple instruction, and...
the entire room just got sprayed by a dense foam, convering every surface.
yuck.
If there acually was a fire, you are convinved the fire would be gone by now.
But there was no fire. 'Why did I do this?' you think to yourself while trying to get foam out of your hair.
                """)
                choices.pop(ind)
            elif val == "FIRE SUP 1":
                if slowedDown:
                    game.rolltext("""
You followed the quite simple instruction,
The fire in the accellerator ring went out.
Unfortunatly this also made the accellerater accellerate back up.
                """)
                else:
                    slowedDown = False
                    game.rolltext("""
You followed the quite simple instruction,
Nothing seems to have happened.
                """)
            elif val == "HURRY UP":
                nav.running = False
                fixing_reactor_loop = False
                game.setGameover(save, "You got yourself trapped in a timeloop")
                game.rolltext("""
The instructions for accellerating the accellerator were quite easy to follow.
you just adjusted that sqiggly thing, increased that varible,
pressed that confirm button, changed that dial, adjusted that sqiggly thing,
increased that varia.. wait.. wha
you adjusted that sqiggly thing, incr..
you just had a sudden feeling of déjà vu, as you again adjusted that sqiggly thing.

uh no, you realize, as you got your thinking stright again.
you try to undo what you did when.. you followed instructions to adjust that sqiggly thi..

'shit' you managed to think as you suddenly find yourself adjusting that squigg..
and again.. at shorter and shorter intervals.

The after looping for what seemed like forever, with the intervals going shorter and shorter, they suddenly stopped getting shorter.
From what you could tell, with the little self awareness you could muster, the intervals were at about 1 secund.
And you soon realied why.

Aside from your little looping bobble, everything was gone.
You aren't dead. Not really. But by now, you wish you were.
                """)
                return
            elif val == "SLOW DOWN":
                if slowedDown:
                    game.rolltext("""
As you were about to start following the instructions,
you realized you have already done this. There is no need to do it again.
                    """)
                elif not cooledDown:
                    game.rolltext("""
You followed the instructions to decelerate the accellerator.
...
It seems to work, for a while. Then suddenly a new alarm starts bleeping.
Fire. There is a fire in the accellerator now.
                    """)
                    
                else:
                    game.rolltext("""
You typed in the final instructions for decellerating the system.
...
You check the readouts, and several alarms stops beeping.
The reactor is no longer critical, but that might change.
                    """)
                    fixing_reactor_loop = False #Fixed the reactor
                slowedDown = True
            elif val == "COOL DOWN":
                if cooledDown:
                    game.rolltext("""
As you were about to start following the instructions,
you realized you have already done this. There is no need to do it again.
                    """)
                elif slowedDown:
                    game.rolltext("""
You attempt to follow the instructions for initiating emergency cooling,
unfortunalty, it seems the fire is making it more or less impossible to initiate the cooling system.
                    """)
                else:
                    game.rolltext("""
You follow the instructions, and soon the emergency cooling brought the temperature down.
some of the alarms stops bleeping, and you notice the previusly looping instruction manual disappeard.
Well, your fingers somewhy still remained there, looping as creepy as before, but now they were reaching for nothing.
                    """)
                    cooledDown = True
            elif val == "INFO":
                textFlow =""
                textTemp="SAFE" if cooledDown else "VERY HIGH!" if slowedDown else "HIGH!"
                textFireAlert=""
                if slowedDown:
                    for _ in range(random.randint(3, 10)):
                        textFireAlert += "\n\tALERT: FIRE DETECTED IN REACTOR SUBSEGMENT {0}{1}".format(random.choice(("A", "B", "C", "D")), random.randint(1,12))
                textFirsttime="" if warnedOfLoops else """
It did not take long for you to realize that the 'human operator' is you.
This might explain the anomolies.
You should be extra careful of what you do here.
                """
                game.rolltext("""
You followed the instructions to initiate a diognastic of the reactor.
...
    STATUS: CRITICAL
    TACHEON EMITTERS: ONLINE
    TACHEON FLOW: {0} ((IRREGULAR))
    TEMPERATURE: {1} ((HIGH!))
    STRUCTURE INTEGRETY: COMPROMISED!
    TEMPERAL INTEGRETY: COMPROMISED!

    {2}
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT A06 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT A12 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B04 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B08 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B12 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C01 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C02 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C06 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C09 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C11 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D01 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D02 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D03 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D04 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D07 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D08 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D09 - POTENTIAL TACHEON LEAK

    WARNING: REACTOR BREACH(ES) DETECTED!
    WARNING: MELTDOWN IMMINENT!
    WARNING: HUMAN OPERATOR DETECTED IN COMPROMIZED SUBSECTION B04! EVACUATION IS ADVICED!

{3}
                """.format(textFlow, textTemp, textFireAlert, textFirsttime)) #Lots TODO here...
                warnedOfLoops = True
        #end of loop
        if cooledDown and slowedDown:
            game.endCounter(save, "reactorC")
            save.setdata("reactorC:fixed", True)
        game.rolltext("""
Leaving the room, you fuss over your hand. You are slowly regaining feeling in it.
Suddenly you notice something.. someone in front of you.
You look up at the stranger.
It took you a bit by surprise, but then you remembered what happened when you first came in.
And as before, the other person suddenly disappeared.
You leave the room content you have done what you could to fix it up.""")


    #endregion actions and places
    #---------------------------
    def goto(room):
        nav.running = False
        save.goto(room)

    def initNav():
        sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
        sectionA.append((elevator, "Elevator C3A", "use"))                  #A 1
        sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 2

        sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
        #sectionB.append((auxcom, "Auxillary communications", "use"))       #(removed)
        sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 1 (entry and exit to and from other rings in the wheel)
        sectionB.append((reactNode, "Reactor-ring access node", "enter"))   #B 2
        sectionB.append((sectionCdoor, "Section C", "examine"))             #B 3

        prevroom = save.getdata("prevroom")
        if prevroom == "ladder":
            nav.setSection("B", 1)
            intro = """
You close the emergency ladder's hatch.
You are now at the outer level ring.
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