import game_utilities as game
import random

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
        |    C2 SECTOR D    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door, you look though it.
On the other side you see a corridor much like the one you are in
except, the lights are all off, and a number of dead bodies litter the floor.
What happend here?
        """, 0.3)
    def bathrooms():
        goto("bathrooms")
    def door_2A68():
        game.showtext("You open the door to your apartment go inside.")
        goto("apartment")
    def elevator():
        game.rolltext("""
The elevators breaks up the corridor, as the corridor splits to around a large round column you learn is the elevator shaft,
the walls around bending outwards giving way for the path around the shaft until they hit flat outer walls.
You find six elevator doors in pairs of two around the large cylinder.
You also locate a set of call-buttons for up, down and cargo, whatever that last one means.
        """, 0.4)
        choices = ["Press UP call button", "Press DOWN call button", "Press CARGO call button", "Leave"]
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


    def cafeteria():
        game.showtext("cafeteria placeholder")
    def sectionBdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.ind = 0
        nav.sec = "B"
    def sectionAdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.ind = 5
        nav.sec = "A"
    def auxcom():
        #grabbing some data from save
        #redwhiteblue = save.getdata("auxcom:redwhiteinblue")
        cargoConnected = save.getdata("auxcom:cargo")
        blueinblue = save.getdata("auxcom:blueinblue")
        tblueinwhite = save.getdata("auxcom:thickblueinwhite")
        yellowtasted = save.getdata("auxcom:yellowtasted")
        systemStatus = save.getdata("auxcom:systemstatus", "BROKEN")
        #region auxcom repair
        game.rolltext("""
You find a large panel with a screen on wall next to you.
It has the following text painted and ingraved under it
        |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
        |   AUXILLARY COMS      |
        |                       |
        | FOR AUTHORIZED USE    |
        |          ONLY         |
        |_______________________|
Undert that you find a smaller panel that seem to invite you to push it.
        """)
        if not game.yesno("Push the lower panel?"):
            game.showtext("You leave the auxillary communications panel alone")
            return
        if(cargoConnected):
            return auxcom3() #auxcom 3: contact the folks in cargo.
        if(systemStatus == "OK"):
            game.rolltext("""
You push the panel. The panel lowers as a latch to reveal a keyboard.
The screen turns on and displays the text
        ' AUXILLARY COMS ONLINE. DO YOU WISH TO PLACE A CALL?'
            """)
            return auxcom2() #auxcom 2: finding someone to talk to
        # auxcom main: fix the system
        if(systemStatus == "SHUTDOWN"):
            game.rolltext("""
You push the panel.  The panel lowers as a latch to reveal a keyboard.
The screen remains off for a while. Then you hear a beep.
            """)
            if tblueinwhite:
                systemStatus = "OK"
                game.rolltext("""
The screen turns on and displays the text
        'CONNECTION RE-ESTABLISHED! DO YOU WISH TO PLACE A CALL?'
                """)
                save.setdata("auxcom:systemstatus", systemStatus)
                return auxcom2()
        else:
            game.showtext("You push the panel. The panel lowers as a latch to reveal a keyboard.")
        game.rolltext("""
The screen turns on, but displays static.
Unseen speakers make some some of repeated beeping pattern that
seems oddly familiar, but you cannot quite place it.

You notice a handle on the side of the panel the screen is on.
            """)
        if not game.yesno("open the panel?"):
            game.showtext("You decide it is not worth bothering with, close the lower panel, and turn to leave.")
            return
        """
Opening the panel you find a mess of vires, some of them lose.
Unfortunetly, none of them are labled, and all have the same port shape.
The only diffrence is the thinkness and color of the cables.

You take a moment to brainstorm ideas on what do with with the cables.
...
..
.
You made a list of things you could try.
        """
        #NOTE: the general idea I have is to have a larger puzzle where options are added and removed as you try things.
        #       For now, there is only a single set of options, where the bad options are removed as they are attempted.
        #       Uses game.choose2 to allow for options to be added and removed
        choices = []
        choices.append(("THICK BLACK IN WHITE","Disconnect thick black cable and plug it into white socket")) #a speaker explodes
        choices.append(("BLUE IN BLUE","Plug blue cable into blue socket")) # nothing happens. if left this way, one speaker will later have a (harmless) feedback
        choices.append(("REDWHITE IN WHITE","disconnect red/white striped cable and plug it in white socket"))  # screen comes to life, displaying an audiovawe of your panting.
        choices.append(("REDWHITE IN BLUE","disconnect red/white striped cable and plug it in blue socket")) # screen remains static, but what looks like flags seems to faintly fly in the background.
        choices.append(("THICK BLUE IN WHITE","Disconnect thick Blue cable and plug it into white socket")) #nothing happens (key to make it work)
        choices.append(("TASTE BLACK","disconnect thick black cable and taste it.")) # yeah.. death.
        choices.append(("YELLOW IN BLACK","plug yellow cable into black socket")) #com system shuts down
        choices.append(("TASTE YELLOW","taste yellow cable")) #this acually works... after you plug blue into white
        random.shuffle(choices)
        choices.append(("EXIT", "close panel"))

        cableLoop = True

        while cableLoop:
            text = ""
            i, a = game.choose2(choices, "What will you try next?")
            if a == "EXIT":
                cableLoop = False
                break #redundant?
            #endof exit
            elif a == "TASTE YELLOW":
                text = ""
                if yellowtasted:
                    text +="""
You decide to try and lick the yellow cable again.
...
Yup, still tingley
                    """
                else:
                    yellowtasted = True
                    text += """
On a whim you decided to lick the end of the yellow cable.
It had kind of a tingely taste to it."""
                if tblueinwhite:
                    text += """
As you lick, you notice the system {0}boot, and a robotic voice comes the the speakers.
"<<CONNECTION RE-ESTABLISHED! DO YOU WISH TO PLACE A CALL?>>"
                    """.format("re" if systemStatus != "SHUTDOWN" else "")
                    systemStatus = "OK"
                elif systemStatus == "SHUTDOWN":
                    text += """
As you lick the cable, the com-system suddenly comes back to life!
Though it is back to just beeps and static
                    """
                    systemStatus = "BROKEN"
                else:
                    text += """
The system blinks and reboots.
Nothing seems to have changed though, still just beeps and static.
                    """
            #endof taste yellow
            elif a == "THICK BLACK IN WHITE":
                text = "You disconnect the think black cable, and plug it into the white socket."
                if systemStatus == "SHUTDOWN":
                    text += "\nAt first, this seems to work, as the system seemed to turn back to life. Alas it were not to last."
                text += """
            
Suddenly there was some sparks in the area aroud the white socket.
You hear a faint hum.
Then hum then turns into a screeching sound that increase in frequency and volume.
Then a speaker explodes, and the system goes black{0}.
You quickly disconnect the black cable, and put it back to where it was.
You decide not to try that again.
                """.format(" again" if systemStatus != "SHUTDOWN" else "")
                systemStatus = "SHUTDOWN"
                choices.pop(i)
            #endof thick black in yellow
            elif a == "BLUE IN BLUE":
                blueinblue = True
                text = """
You inser the blue cable in the blue socket.
...
*blip*
....
..
Nothing...
Other than a faint blip, nothing happened. You scratch this off the list.
                """
                choices.pop(i)
            #endof blue in blue
            elif a == "REDWHITE IN WHITE":
                text = "You plug the red-white striped cable in the white socket."
                if systemStatus == "SHUTDOWN":
                    text += "\nBut nothing happened, and the system is still shut down."
                else:
                    text += """
The beeps stop, and you notice the screen stops playing static.
You check the screen
....
'What th..'
you are about to say when all you saw was a flat blue line.
But then you noticed it made a wave as you talked.
Well, that's very 'useful'
                    """
                text += "\nYou disconnect the red-white striped cable.\nThat was a blind end."
                choices.pop(i)
            #end of redwhite in white
            elif a == "REDWHITE IN BLUE":
                text = "You plug the red-white striped cable in the blue socket."
                if systemStatus == "SHUTDOWN":
                    text += "\nBut nothing happened, and the system is still shut down."
                else:
                    text += """
You hear an extra beep as you plug in the cable, but nothing else.
The screen blinks, but seems to be back to show ing static.
You check the screen, and you notice the screen now shows something behind the static.
....
'What the..'
you say as you notice a number of red white and blue flags burned into the background of the static.
Well, that's.. colorful...
                    """
                text += "\nYou disconnect the red-white striped cable.\nThat was a blind end."
                choices.pop(i)
            #endof redwhite in blue
            elif a == "THICK BLUE IN WHITE":
                text = ""
                if systemStatus == "SHUTDOWN":
                    if tblueinwhite:
                        text += "\nYou unplug the thick blue cable, and plug it back in."
                    else:
                        text += "\nYou plug the thick blue cable in the white slot"
                    text += "\nBut nothing happened. The system is still shut down."
                    text += "\nYou decide to leave the cable connected."
                else:
                    if tblueinwhite:
                        text += "\nYou unplug the thick blue cable, and plug it back in."
                        text += "\nThe screen blinks with brief static, but once again displays black screen with the text 'ERROR - PLEASE REBOOT'."
                    else:
                        text += """
You plug the thick blue cable in the white slot
You notise the screen suddenly stopped displaying static.
You check the screen, and find it now displays a black background with a text in white
        'ERROR - PLEASE REBOOT'
                        """
                tblueinwhite = True
            elif a == "TASTE BLACK":
                text = """
You unplug the big thick blue cable, and stuck out your touge to lick it.
You're not sure why you just did that.
As you somewhy put the cable in your mouth, the world goes black.
                """
                save.setdata("GAME OVER", "You put a live power-cable in your mouth. Yeah, you are dead.")
                nav.running = False #escape outer room loop
                cableLoop = False #escape inner loop
            elif a == "YELLOW IN BLACK":
                pass
                if systemStatus == "SHUTDOWN":
                    text = """
You unplug the cable in the black slot, and plug in the yellow.
Nothing happened, and the system is still shut down.
You decide to undo it, plugging the black cable back in.
                    """
                else:
                    text = """
You unplug the cable in the black slot, and plug in the yellow.
As you plug in the yellow cable, there was a breif spark, then system shuts down.
You decide to undo it, and never try that again, putting the black cable back in.
                    """
                    choices.pop(i)
                systemStatus = "SHUTDOWN"
            game.rolltext(text)

        #saving data..
        #save.setdata("auxcom:redwhiteinblue", redwhiteblue)
        save.setdata("auxcom:blueinblue", blueinblue)
        save.setdata("auxcom:thickblueinwhite", tblueinwhite)
        save.setdata("auxcom:yellowtasted", yellowtasted)
        save.setdata("auxcom:systemstatus", systemStatus)
        if(systemStatus == "OK"):
            return auxcom2()
        else:
            game.showtext("You leave the AUX com alone.")
        #endregion auxcom repair
    def auxcom2():
        #region auxcom2
        cargoConnected = save.getdata("auxcom:cargo")
        text = """
A list of communication nodes show up on the screen.
Some of them with an error-message saying they are offline
        """
        choices = [
            ("BRIDGE", "Connect to main bridge com system"),
            ("ENGINEERING", "Connect to main engineering"),
            ("RADIATION SHELTER 1", "Connect to radiation shelter One"),
            ("RADIATION SHELTER 2", "Connect to radiation shelter Two"),
            ("RADIATION SHELTER 3", "Connect to radiation shelter Three"),
            ("RADIATION SHELTER 4", "Connect to radiation shetter Four"),
            ("WHEEL A AUXCOM", "Connect to Auxillary coms, wheel One"),
            ("WHEEL B AUXCOM", "Connect to Auxillary coms, wheel two"),
            ("WHEEL D AUXCOM", "Connect to Auxillary coms, wheel four"),
            ("CARGO", "Connect to main cargo bay"),
            ("EXIT", "Exit the auxillary com system")
        ]
        
        useGenericNoResponse = (
            "BRIDGE",
            "ENGINEERING",
            "RADIATION SHELTER 1",
            "RADIATION SHELTER 2",
            "RADIATION SHELTER 3",
            "RADIATION SHELTER 4",
            "WHEEL A AUXCOM",
            "WHEEL B AUXCOM",
            "WHEEL D AUXCOM"
        ) #some of these are placeholders
        game.rolltext(text)
        makingCall = True
        while(makingCall):
            text = ""
            ind, labl = game.choose2(choices, "Who do you wish to contact?")
            if labl == "EXIT":
                text = "You close the lower panel, shutting down the system"
                makingCall = False
            elif labl in useGenericNoResponse:
                text = """
You attempt to make your connection.
...
....
.....
... ....
... .... .....
ERROR: CONNECTION TIMED OUT, SYSTEM MAY BE OFFLINE!
                """
                choices.pop(ind)
            
            elif labl == "CARGO":
                text = """
You attempt to make your connection.
...
....
.. '-oming from inside Wheel C!' 'What?! Hello, who's there!?'
You hear two voices from the com system.
                """
            game.rolltext(text, 0.4)
            cargoConnected = True
            makingCall = False
        save.savedata("auxcom:cargo", cargoConnected)
        if cargoConnected:
            return auxcom3()
        #endregion auxcom2
    def auxcom3():
        #Note: Whatever the dialoge, it is up to the player what to do afterwards.
        # Only change is the information they are given.
        # From here, or the ladder if the player skips this, a counter is enabled that gives the player 10 'time units' before game over.
        if not game.getCounter(save, "reactorC")[0]: #counter not enabled
            game.setCounter(save, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.

        

        name = game.getName(save)
        gender = game.getGender(save)
        klara =  game.getKlara(save)
        #TODO

        if False:
            pass #space for alternate dialuge
        else:
            game.showtext("The people on the other side of the call is waiting for you to answer.")
            choices = [
                ("I'm {0}. I'm lost, where am I?".format(name)),
                ("Help, I don't know who or where I am!"),
                ("uhh"),
                ("I.. I think my name is {0}. I find it hard to remember.")
            ]
        ind, ans = game.choose2(choices, "What do I say?")
        game.showtext(">>"+ans)
        p = "mister" if gender == "male" else "miss"
        if ind == 0 or ind == 3:
            p = name
        game.rolltext("""
Ok. {0}, I need you to stay calm. I'm gonna get some help
(The woman you were talking leaves)
...
(A man, an engineer by the looks of his attire, takes her place)
Ok, {0}. I am not gonna lie, you are in a bit of touble. We are gonna do what we can to help you.
First of, you are onboard the UNS Armstrong on route from Sol to Alpha Centauri.
Your current dizzyness may be from the emergency awakening from stasis.
The reactor onboard is about to explode, so were about to detach the module when you contacted us.

Look {0}, I need you to find the emergency ladd..
(the man is rudely interrupted by a third person)
Hey! I know you. You're Klara's {1} right?
You're a engineer, right? Maybe you could try to stabilize the reactor temporarily?
There are still lots of people stuck in stasis in the upper ring!

Look, {2}, I woulden't blame you for just making a run for the ladder to save yourself, but you could save those people!
        """.format(p, game.getGenderedTerm(klara, gender), name))
        choices = [
            ("Screw them! I'm out of here! I'm gonna climb down and get out of here!"), #ignorant idiot option
            ("I.. I am not gonna take that chance. I'm just gonna go meet you up the ladder!"), #reluctant selfishness
            ("Alright, how do I get to the reactor?"),
            ("What exacly happend?")
        ]
        ind, ans = game.choose2(choices, "How do you respond?", "<< {2}")
        if ind == 3:
            game.rolltext("""
I figured you would ask that. We hit an asteroid!
We don't have time to go into details right now!
I need you to either stabilize the reactor so we can save everyone, or get you safely out of there!
            """)
            choices.pop(3)
        ind, ans = game.choose2(choices, "How do you respond?", "<< {2}")
        
        if ind == 0:
            game.rolltext("""
Well, ehm.. that's rude. ..
uh well, sure go DOWN the ladder. Uh, and take your good time too.
Got to go, bye!

(The call has ended)
            """)
        elif ind == 1:
            game.rolltext("""
I see. Well, the reactor will reach a meltdown in just a few minutes, we need to detach the module before then.
You need to hurry! The escape ladder should be nearby. You need to climb up as fast as you can.
We will meet you at the airlock in the module core.
Please beware, you will be weightless up here!
See you soon!

(The call has ended)
            """)
        elif ind == 2:
            game.rolltext("""
Thanks for doing this!
Ok, there won't be much time, but we will hold off detaching the module as long as we can.
You should find the emergency stairs nearby. You need to climb down to the outermost ring.
The nearest reactor-node will not be far from the ladder.
You need to first initalize the emergency cooling system, then the emergency particle decelerator.
In that order! You will find detailed instructions on how to do this in the reactor-node control room.
Doing this will buy us maybe an hour before meltdown.
You need to hurry! Get back and contact us again once you have done it!

(The call has ended)
            """)

        game.showtext("Aux com dialoge placeholder.\nimagine you just learned just how fucked you are.\nAnd yeah, you are. Keywords: emergency ladder, climb up, minutes to live. Run fool! RUN!")
    def ladder():
        if not game.getCounter(save, "reactorC")[0]: #if counter reactorC is not enabled
            game.setCounter(save, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.
        text = """
The corridor gives way to a large column, splitting the corridor to go around it on both sides.
On two sides of the column you find large hatches with a colored engraving
        |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
        |    EMERGENCY ESCAPE   |
        |      WHEEL C RING 2   |
        |                       |
        |      BREAK GLASS      |
        |          AND          |
        |       PULL LEVER      |
        |        TO OPEN        |
        |_______________________|

You locate the panel as indicated on the engraving.
        """
        if save.getdata("WheelCMiddleLadder") == "open":
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
            if save.getdata("WheelCMiddleLadder") == None:
                save.setdata("WheelCMiddleLadder", "open")
            game.rolltext(enterText,0.5)
            goto("ladder")

    def sectionCdoor():
        game.rolltext("""
You stare at the large solid door in front of you.
There is a painted ingraving on the door, it reads
        _____________________
        |    C2 SECTOR C    |
        |   EMERGENCY DOOR  |
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is a small reinforced window on the door, you look though it.
On the other side you see.. nothing. just blackness.
No, that's not quite right. As your eyes get used to the dark,
you see the walls on the other side of the door.
They go on for a bit over a meter, then abruptly ends in uneven bent metal.
And you see some small faint light far back in the darknes, moving.
Stars, you realize. Stars flying upwards. You are staring into space!
    """, 0.3)
    #local shorthand.
    #Stops loop and sets next room in the save.
    def goto(room):
        nav.running = False
        save.goto(room)

    sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
    sectionA.append((bathrooms, "Public bathrooms", "enter"))           #A 1
    sectionA.append((door_2A68, "Door C2A68", "enter"))                 #A 2 (from apartment, newgame location)
    sectionA.append((elevator, "Elevator C2A", "use"))                  #A 3
    sectionA.append((cafeteria, "cafeteria C2A", "enter"))              #A 4
    sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 5

    sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
    sectionB.append((auxcom, "Auxillary communications", "use"))        #B 1
    sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 2 (entry and exit to and from other rings in the wheel)
    sectionB.append((sectionCdoor, "Section C", "examine"))             #B 3

    prevroom = save.getdata("prevroom")
    if prevroom == "apartment":
        
        nav.ind = 2
        nav.sec = "A"
        intro = "You exit out of your room, and behold the large corridor streching as far as you can see in either direction."
        if save.getdata("middlering:visited") == None:
            intro += """
You may still be a bit dizzy, as you could swear the floor bends a bit upwards both ways.
The lights flicker, and you see random trash, maybe forgotten items, strewn around the floor.
As the door closes, you note the number-plate on your door.
    _________________
    |   C2A - 068   |
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
There is an uneasy silence.
        """
    elif prevroom == "laddershaft":
        nav.ind = 2
        nav.sec = "B"
        intro = """
You close the emergency ladder's hatch.
You are now at the middle level ring.
        """
    else:
        nav.ind = 3
        nav.sec = "B"
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

#TODO: move this to its own module
def bathrooms(save):


    while True:
        game.rolltext("""
You stand in front of the bathrooms. There are two doors in front of you.
One door with a depiction of a man, one depicting a woman.
        """)
        choices = [("MALE", "Enter men's room"), ("FEMALE", "Enter lady's room"), ("EXIT", "Leave")]
        ind, val = game.choose2(choices, "What door do you enter")
        if val == "MALE":
            mensroom()
        elif val == "FEMALE":
            ladysroom()
        else:
            save.goto("middle")
            break


    def mensroom():
        #sets gender to male if not set.
        gender = save.getdata("gender", "male") 
        #TODO: Write scene for mensroom
        game.showtext("PLACEHOLDER mensroom")
    def ladysroom():
        #sets gender to female if not set.
        gender = save.getdata("gender", "female")
        #TODO: writescene for ladies room.
        game.showtext("PLACEHOLDER ladysroom")

if __name__ == "__main__":
    game.showtext("--- Welcome to the middle ring test code. For a regular playthugh, please run main.py instead. ---")
    #testing-code
    from main import savadata
    from main import VERSION
    testsave1 = savadata(VERSION)
    testsave1.setdata("name","Tester")

    main(testsave1)