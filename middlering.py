import game_utilities as game
import random
import dialoges


def main(save):
    sectionA = []
    sectionB = []
    class middleRoomNAV(game.RoomNav1D):
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
        

    nav = middleRoomNAV()
    intro = "place holder corridor intro text (should not show up in the game)"
    #----------------------------
    #region places and actions
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
        """)
    def bathrooms():
        goto("bathrooms")
    def door_2A68():
        game.showtext("You open the door to your apartment go inside.")
        goto("apartment")
    def cafeteria():
        game.showtext("The Cafeteria is closed!")
    def sectionBdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.setSection("B", 0)
    def sectionAdoor():
        game.showtext("You pass though the open door seperating the two sectors")
        nav.setSection("A", 5)
    def auxcom_repair():
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
            return dialoges.auxcom_cargo(save) #auxcom_cargo: contact the folks in cargo.
        if(systemStatus == "OK"):
            game.rolltext("""
You push the panel. The panel lowers as a latch to reveal a keyboard.
The screen turns on and displays the text
        ' AUXILLARY COMS ONLINE. DO YOU WISH TO PLACE A CALL?'
            """)
            return dialoges.auxcom_contact(save) #auxcom_contact: finding someone to talk to
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
                return dialoges.auxcom_contact(save)
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
            return dialoges.auxcom_contact(save)
        else:
            game.showtext("You leave the AUX com alone.")
        #endregion auxcom repair
    def ladder():
        if not save.getdata("reactorC:fixed", False) and not game.getCounter(save, "reactorC")[0]: #if counter reactorC is not enabled
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
        game.rolltext(text)
        if(game.yesno(openText)):
            if save.getdata("WheelCMiddleLadder") == None:
                save.setdata("WheelCMiddleLadder", "open")
            game.rolltext(enterText)
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
    """)
    def elevator():
        return dialoges.elevator(save)
    #endregion places and actions
    #----------------------------
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
    sectionB.append((auxcom_repair, "Auxillary communications", "use"))        #B 1
    sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 2 (entry and exit to and from other rings in the wheel)
    sectionB.append((sectionCdoor, "Section C", "examine"))             #B 3

    prevroom = save.getdata("prevroom")
    if prevroom == "apartment":
        nav.setSection("A", 2)
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
        nav.setSection("B", 2)
        nav.ind = 2
        nav.sec = "B"
        intro = """
You close the emergency ladder's hatch.
You are now at the middle level ring.
        """
    else:
        nav.setSection("B", 3)
        intro = """
You have walked around aimlessly for a bit, you don't know for how long
And oof! You just walked streight into a large closed door.
        """
    game.rolltext(intro)
    nav.loop()

#TODO: move this to its own module
def bathrooms(save):
    def bathrooms1():
        while True:
            game.rolltext("""
You stand in front of the bathrooms. There are two doors in front of you.
One door with a depiction of a man, one depicting a woman.
            """)
            choices = [("MALE", "Enter mens room"), ("FEMALE", "Enter ladies room"), ("EXIT", "Leave")]
            _, val = game.choose2(choices, "What door do you enter")
            if val == "MALE":
                bathrooms2("mens")
            elif val == "FEMALE":
                bathrooms2("ladies")
            else:
                save.goto("middle")
                break
            if(save.getdata("GAME OVER")):
                return

    def bathrooms2(subroom):
        gender = None 
        visited = save.getdata("bathroom:visited", False) # if the Player Character has visited the bathrooms beofore
        showered = save.getdata("bathroom:showered", False) # whatever the PC has showered
        relived = save.getdata("bathroom:relived", False) # whatever the PC has had the chance to relive themself
        keepsake = save.getdata("spouse:keepsake", False) # potential use in later chapters. Only unlockable if you have remembered who your spouse is.

        relationKlara = save.getdata("klara", None) #if spouse, unlocks retrival of keepsake in ladies locker-room
        relationJeff = save.getdata("jeff", None) #if spouse, unlocks retrival of keepsake in mens locker-room

        choices = None

        wrongroom = "" #if the PC enters the wrong bathroom, this extra nerrative is added.
        facedesc = "" #describes what the PC sees in the mirror (male or female)
        areadesc = "" #describes the facilities in the room (mens or ladies)

        #This section determines PC's gender if not already set.
        if subroom == "mens":
            gender = save.getdata("gender", "male")
            if gender != "male":
                wrongroom = """
You're not exacly sure why you went into the mens room, and not the ladies room.
Though you suppose it dosen't really matter. There is nobody here anyways."""
            areadesc = """ a line of toiler stalls, a large urinal, a few changing rooms, a locker room,
showers, couple of them private, and a dispenser of hygine products."""
            choices = (
                ("SINK", "Spash water in your face"),
                ("TOILET", "Visit a toilet booth"),
                ("URINAL", "Visit the urinal"),
                ("HYGINE_MENS", "open the hygine dispenser"),
                ("SHOWER", "Go the the showers"),
                ("LOCKERS", "Go to the locker room"),
                ("EXIT", "leave")
            )
        elif subroom == "ladies":
            gender = save.getdata("gender", "female")
            if gender != "female":
                wrongroom = """
A man going inside the ladies room would normally be seen as quite perverted.
But as it is, the ladies is as vacant of people as the rest of this place."""
            areadesc = """ a line of toilet stalls, a few changing rooms, a looker room, showers, couple of them private
and a hygine despenser with varius.. products..."""
            choices = (
                ("SINK", "Spash water in your face"),
                ("TOILET", "Visit a toilet booth"),
                ("HYGINE_LADIES", "open the hygine dispenser"),
                ("SHOWER", "Go the the showers"),
                ("LOCKERS", "Go to the locker room"),
                ("EXIT", "leave")
            )
        if gender == "male":
            facedesc = "a rugged man with a stubby beard."
        if gender == "female":
            facedesc = "a tired looking woman with clear bags under they eyes."
        if not visited:
            game.rolltext("""
You enter the {0} room.{1}
Finding yourself in front of the large array of sinks and mirror.
Some of the mirrors are broken, but you found one that was relativly intact.
you have a look at yourself.
What you see is {2}
You look about as shitty as you feel, yet it does look familiar.
That's a good thing, right?
Looking around, you see {3}
            """.format(subroom, wrongroom, facedesc, areadesc))
        else:
            game.showtext("PLACEHOLDER text for return visit to bathrooms.")
        visited = True
        save.setdata("bathroom:visited", True)
        while True:
            _,choice = game.choose2(choices, "What do you want to do?")
            if   choice == "EXIT":
                game.showtext("You leave the {0} room".format(subroom))
                return
            elif choice == "SINK":
                game.showtext("You splash some water on your face. It feels refreshing.")
            elif choice == "TOILET":
                act = ""
                if(relived): #relived = save.getdata("bathroom:relived", False)
                    act = "You sit for a bit, resting. You don't feel the need to 'do' anything."
                else:
                    act = "You relive yourself right there and then. You must have held it in for a while without thinking about it."
                    save.setdata("bathroom:relived", True)
                    relived = True
                game.rolltext("""You locate a nice toilet booth, and sit down on a porcelain throne.
                Well, ok, not porcelain, these toilets are made of metal.
                {0}
                After a while you decide it is time to get back up""".format(act))
            elif choice == "URINAL":
                if relived:
                    game.showtext("you stand over by the urinal for a bit, but you don't feel any need to use it.")
                elif gender == "female":
                    game.showtext("As you approach the urinal, you wondered how it was like for men to use contraptions like this.")
                    if(game.yesno("Try to piss in it?")):
                        game.rolltext("""You awkwardly posision yourself,
and partially relive youself down the urinal.
It was kinda fun.
And you mostly hit the target.
mostly..

Still, having done that, you realize you have 'other' needs to relive youself of.""")
                        if(game.yesno("Take a dump in the uninal?")):
                            game.showtext("You did the deed in the urinal. you slowly back off, giggling a bit as your inner girl got her wicked wish.")
                            save.setdata("bathroom:relived", True)
                            relived = True
                    else:
                        game.showtext("You left the uninal alone.")
                else:
                    game.rolltext("""You instinctively unzip and relive youself down the uninal.
 it was quickly done.
 But soon you realize you have 'other' needs to relive youself of.""")
                    if(game.yesno("Take a dump in the uninal?")):
                        game.showtext("You did the deed in the urinal. you slowly back off, giggling a bit as your inner child got his very childish wish.")
                        save.setdata("bathroom:relived", True)
                        relived = True
            elif choice == "HYGINE_LADIES":
                game.showtext("you examine the dispenser. You find some soaps, tampons, manual razor blades, a few female condoms. Nothing you really need right now")
            elif choice == "HYGINE_MENS":
                game.showtext("You examine the dispenser. You find some soaps, condoms, razer blades. Nothing you really need right now.")
            elif choice == "SHOWER":
                if showered:
                    game.showtext("You go over to the showers. But you aleady feel clean, so you go back.")
                else:
                    game.rolltext("""You enter one of the private show stalls.
You undress, and turn on the shower
You note as all the grime washes off you.
you feel a lot better now.
...
...
you dry up, dress yourself and again, and leave the shower.""")
                    showered = True
                    showered = save.setdata("bathroom:showered", True)
            elif choice == "LOCKERS":
                text = "You take a walk along the lockers."
                if keepsake:
                    text += "\nThere was not much more to see."
                elif subroom == "mens" and relationJeff == "spouse":
                    text+= """
You stumble upon a familiar locker. Jeff's locker.
Your hands move on their own, it seems his locker combination is deep in your subconsius.
Inside you find a small box.
It feels important.
You take it with you."""
                    keepsake = True
                elif subroom == "ladies" and relationKlara == "spouse":
                    text+= """
You stumble upon a familiar locker. Klara's locker.
Your hands move on their own, it seems her locker combination is deep in your subconsius.
Inside you find a small box.
It feels important.
You take it with you.""" 
                    keepsake = True
                else:
                    text += "\nThere was not much to see."
                save.setdata("spouse:keepsake", keepsake)
                game.rolltext(text)
            status = game.updateCounter(save, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                break
        #end of loop
    bathrooms1() #Starts the room.

if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("--- Welcome to the middle ring test code. For a regular playthugh, please run main.py instead. ---")
    #testing-code
    from main import savadata
    from main import VERSION
    testsave1 = savadata(VERSION)
    testsave1.setdata("name","Tester")
    testsave1.goto("middle")

    main(testsave1)