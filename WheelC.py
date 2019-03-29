import game_utilities as game
import dialoges

#The Ladder
def emergencyLadder(save):
    class ladderNAV(game.RoomNav1D):
        def __init__(self):
            super().__init__(termPlus= "GO DOWN", termMinus= "GO UP")
        #Override
        def runAction(self):
            act,_,_ = self.getPlace()
            #note: ticks the reactorC counter if enabled.
            status = game.updateCounter(save, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                self.running = False
            else:
                act()
        def plus(self):
            game.rolltext("You climb upwards, feeling yourself getting a bit lighter")
            self.ind += 1
        def minus(self):
            game.rolltext("You climb down, feeling a slight stronger pull downwards")
            self.ind -= 1
    nav = ladderNAV()
    def core():
        game.showtext("The ladder-shaft ends in a roof-hatch, you open it and stare into the huge spherical room above")
#        game.rolltext("""
#You open the hatch, and beholds the spinning room.
#In the light gravity you push off upwards into the core.
#        """)
        goto("core")
    def inner():
        #goto("inner")
        game.showtext(" - Sorry, this section is not written yet. - ")
    def middle():
        game.showtext("You open the hatch for the middle ring")
        goto("middle")
    def outer():
        game.showtext("You open the hatch for the outer ring")
        goto("outer")

    

    #((sectionDdoor, "Section D door", "examine")) 
    nav.places = (
        (core, "The core", "Exit to the Core"),
        (inner, "inner ring", "Exit into the inner ring" ),
        (middle, "middle ring", "Exit into the middle ring" ),
        (outer, "outer ring", "Exit into the outer ring" )
    )
    def goto(room):
        nav.running = False
        save.goto(room)

    nav.loop()
    




def core(save):
    intro = ""
    proom = save.getdata("prevroom")
    if(proom == "ladder"):
        intro = """
As you push off from the laddershaft, you fly upwards in the low gravity.
You reach the center, finding yourself entierly weightless.
You take hold on a rotating pole. Soon the pole seemed to stop rotating, and the room started rotating around you.
You see the ladder you came out from now no longer as "down", but as part of the wall.
From your perspective, "up" has become a set of reinforced windows at one end of the sphere.
"Down" has become a large open doorway, with a sign lableing it "airlock".
That being said, had you turned yourself the other way, it would be the other way around.

As the room spins around you, you take note of the clearly labled entry points around you.
        """
    else:
        intro = """
You float mindlessly around in the huge sphere untill you get a hold on a spinning pole in center.
Soon the pole seemed to stop rotating, and the room started rotating around you.
As the room spins around you, you take note of the clearly labled entry points around you.
        """

    choices = (
        ("WINDOW", "Core window"),
        ("ELEVATOR_SEC_A", "Section A transport elevator"),
        ("LADDER_SEC_B", "Section B emergency access ladder"),
        ("ELEVATOR_SEC_C", "Section C transport elevator"),
        ("LADDER_SEC_D", "Section D emergency access ladder"),
        ("AIRLOCK", "Module primary airlock and dock")
    )
    running = True
    while running:
        _, choice = game.choose2(choices)
        if choice == "WINDOW":
            if save.getdata("core:window", False):
                text = """
You look back at the window area. The window is closed by the huge metal shutter.
You still hear the occational clang and bang.
You decide not to get closer, just in case.
                """
            else:
                text = """
You climb, or rather push and drag your way to the window at one end of the pole.
The pole connected to a set of handrails, rotating with the wall.
It was a awkward transision, but you are now looking out a solid thick window."""
                if(save.getdata("apartment:window")):
                    text +="""
Unlike the 'window' in the room you woke up in, this window was at least not holographic.
You could tell by the lack of lag when you moved your head, the large solid sliding shutters on both sides of the window
uh and the fact you are looking out into space, and not an idyllic forest."""
                else:
                    text += """
The window gives you a great view into space, it is quite impressive view.
You take note of the large solid sliding shutters on both sides of the window."""
                text += """
You took some time to enjoy the view.
...
.....
... ...
Some debris hit the solid window.
You figure this was your cue to leave and focus on the imminent threat on hand.
...
As you push and drag your way back, you hear a odd bang.
Then an alarm starts howling.
You look back, and see the shutters close.
You hear more bangs, debris hitting the shutters.
Might be a good idea to get out of there.
                """
                game.rolltext(text)
                save.setdata("core:window", True)
        elif choice == "ELEVATOR_SEC_A":
            game.rolltext("""
You look at the elevator access rotating around.
A huge A is painted on it.""")
            if(game.yesno("Float over to it?")):
                dialoges.elevator(save)
        elif choice == "ELEVATOR_SEC_C":
            game.rolltext("""
You look at the elevator access rotating around.
A huge C is painted on it.""")
            if(game.yesno("Float over to it?")):
                game.rolltext("""
You push off and float to the elevator.
When you got there, you noticed a flashing electoric board flashing a read light and the text:
BRECH DETECTED! NO ACCESS!
You took off back to the pole.""")
        elif choice == "LADDER_SEC_B":
            game.rolltext("""
You look over to the ladder access rotating around.
It has a huge B painted on it.
float over to it?""")
            if(game.yesno("Float over to it?")):
                save.goto("ladder")
                running = False
        elif choice == "LADDER_SEC_D":
            game.rolltext("""
You look over to the ladder access rotating around.
It has a huge D painted on it.
float over to it?""")
            if(game.yesno("Float over to it?")):
                game.rolltext("""
You push off and float to the ladder.
When you got there, you noticed a flashing electoric board flashing a read light and the text:
BRECH DETECTED! NO ACCESS!
You took off back to the pole.""")
        elif choice == "AIRLOCK":
            game.rolltext("""
You look "down" towards the huge door "below".
Taking in the details, you see the pole ending a bit before it, splitting into 4 aches around the doorway.
Like the pole itself, the doorway was fixed, and not rotating with the room.
On a closer look, there is a secund doorway past it, and two more again, with only some small gap of room between them.
            """)
            if not game.yesno("Take off towards the doorway?"):
                continue
            game.rolltext("""
You rotate yourself so the doorway was now "above" you.
You take off, pushing and dragging along the pole untill you reach the doorway.
            """)
            if not game.yesno("enter the doorway?"):
                game.rolltext("""
For whatever reason, you decide to drag yourself back to the pole.
As you turned around, you noticed some people float into view, with confused looks.
                """)
                continue
            game.rolltext("""
You enter though the first two doorways.
you note the middle section between the doors were diffrent than the other two.
It was shorter and had a seam down the middle.
As you were floating though, you were greeted by someone who suddenly floated into view.
            """)
            save.goto("cargobay")
            running = False
            return
            
        status = game.updateCounter(save, "reactorC", -1)
        if status == "death": #if reactor counter reach 0, and the game ends.
            running = False
    #end of loop
#TODO: Move to a proper module
def Cargobay(save):
    #TODO: write the ending, mention if reactor was fixed, and if the people in stasis was saved. end with being told to go to the infirmary. END OF CHAPTER!
    reactorFixed = save.getdata("reactorC:fixed", False)
    peopleSaved = save.getdata("wheelC:peopleSaved", 0)
    prevcontact = save.getdata("auxcom:cargo", False)

    if prevcontact:
        pass
    else:
        pass
    if peopleSaved > 0:
        pass
    if reactorFixed:
        pass
    else:
        pass
    

    game.showtext("PLACEHOLDER! Welcome to end of chapter 1")
    save.setdata("GAME OVER", "End of the story, so far!")
#barebones placeholder for chapter 1: Wheel C

#TODO: 
def inner(save):
    
    game.showtext("Welcome to the placeholder for inner ring.\nThere is nothing for you to do here yet.\nLater you will be able to save some people currently frozen in here.")
    if game.yesno("return to the emergency ladder?"):
        return save.goto("ladder")

if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")