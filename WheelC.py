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
            game.rolltext("You climb down, feeling a slight stronger pull downwards")
            self.ind += 1
        def minus(self):
            game.rolltext("You climb upwards, feeling yourself getting a bit lighter")
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
        game.showtext("You open the hatch for the inner ring")
        goto("inner")
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

    prevroom = save.getdata("prevroom")
    if prevroom == "core":
        nav.ind = 0
    elif prevroom == "inner":
        nav.ind = 1
    elif prevroom == "middle":
        nav.ind = 2
    elif prevroom == "outer":
        nav.ind = 3

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
    game.rolltext(intro)
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
                save.setdata("core:window", True)
            game.rolltext(text)
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
The inner-most door are closed, but has some large windows where you can see the area past it, clearly.
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
As you turned around, you noticed some people float into view on the, with confused looks.
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
    peopleSaved = save.getdata("stasis:peopleSaved", 0)
    prevcontact = save.getdata("auxcom:cargo", False)
    name = game.getName(save)
    gender = game.getGender(save)
    pronoun = "him" if gender == "male" else "her"
    gendernoun = "sir" if gender == "male" else "miss"
    jeff = game.getJeff(save, True)
    klara = game.getKlara(save, True)


    intro = "As you appreach the innermost door, you hear a muffled barely audiable voice from the other side."
    introA = "Hey, you must be {0}!".format(name)
    introB = "What the? A survivor! Quick, let's open the door and get {0} inside!".format(pronoun)

    p = name if prevcontact else gendernoun
    instruct = """Are you alright there {0}? The door is a bit broken, so I need you to hold down that lever there while we open the door""".format(p)

    reaction = ""
    reactionA = """Well, you saved a few people, {0} by last count, that would otherwise die.
I suppose that's something we can be thankfull for. Sad there are still so many more stuck down there.""".format(peopleSaved)
    reactionB = """Thank you {1}. We never expected you to evacuate so many people on your lonesome. Sorry we could not help.
By our last count, we're at {0}, excluding you.""".format(peopleSaved, name)
    reactionC = """What happened? You fixed the reactor. Was there something wrong with the stasis chambers? Why haven't you evacuated anyone, {0}?""".format(name)
    reactionD = "Well, at least we got you out of there in time."

    followup = ""
    followupA = "Well, proper congratulations will have to wait. You should join the others in the infirmary. And we need to detatch the module now! Hurry on now!"
    followupB = """Wish we could get more people out of there, but it's too late now. Without that improvised dead-man switch on the other side there, this door is locked for good.
You best head to the infirmary. We need to detach the module before it's too late."""

    ending = ""
    endingA = """You push and drag your way following the signs to the infirmary in wheel A section A1
You try not to think about how maybe you could have saved some of the people stuck in stasis.
You excuse it in your mind by saying to yourself that there was nothing you could have done for them.
Though in a way, you know that's a lie."""
    endingB = """You push and drag your way following the signs to the infirmary in wheel A section A1
You try not to think about all the people you left behind, focusing instead on the few you did save"""
    endingC = """You join the last group of surviors you saved on the way to the infirmary.
Pushing and dragging your ways to wheel A, you meet a crew-member.
You get told that the wheel A infirmary is full, so you change course to Wheel D.
As if from nowhere, Jeff, your {0} pokes you on your shoulder.
Apperently, he was in the last group, and you had not even noticed.
Neither had he. Stasis sickness being what it is.
Passing the computer core on the way, you got reaquiented with your {1} Klara too, who pushed out of the room below you and hugged you.
putting both of you in a real awkward spin in the microgravity, untill she got a hold on the railing, stopping you both.
    """.format(jeff, klara)
    endingD = """Hearing that comment, you got an odd feeling. How could you have known there were more people missing?
And that you could have helped them? As you push and drag your way to the infirmary in wheel A,
you conclude there was no way you could have known.
...
It is of little comfort."""


    if prevcontact:
        intro += introA
        if(peopleSaved > 120):
            reaction = reactionB
            followup = followupA
            ending = endingC
        elif(peopleSaved > 0):
            reaction = reactionA
            followup = followupA
            ending = endingB
        elif(reactorFixed):
            followup = followupB
            reaction = reactionC
            ending = endingA
        else:
            followup = followupB
            reaction = reactionD
            ending = endingA
    else:
        intro += introB
        reaction = reactionD
        followup = followupB
        ending = endingD

    game.rolltext("""{0}
{1}
{2}
{3}
{4}
    
    END OF CHAPTER 1""".format(intro, instruct, reaction, followup, ending))
    save.setdata("GAME OVER", "End of the story, so far!")

    game.showtext("PLACEHOLDER! Welcome to end of chapter 1")
    save.setdata("GAME OVER", "End of the story, so far!")

if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")