import random
import dialoges
import Game

class MiddleRunner(Game.PlaceRunner1D):
    def __init__(self, game:Game.Game):
        super().__init__(game, 'x', 'left', 'right')
    def onTravel(self, previndex:int):
        if previndex == self.index:
            print("Null travel error ? ignoring")
        pass
        #check for section passage
    def runaction(self, action):
        status = self.game.updateCounter("reactorC", -1)
        if status == "death":
            self.running = False
            return
        super().runaction(action)

    #TODO: Continue writing replacement for middleroomnav

def main(game:Game.Game):
    def T(storytag:str)->str:
        fallback = "(({0}))".format(storytag)
        return game.story.get(storytag, fallback)

    navdata = game.Navdata
    runner:MiddleRunner = MiddleRunner(game)
    #intro = "place holder corridor intro text (should not show up in the game)"
    #----------------------------
    #region places and actions
    def sectionDdoor():
        game.rolltext("{MIDDLE_SEC_D_DOOR}")
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
    def bathrooms():
        goto("bathrooms")
    def door_2A68():
        game.showtext("You open the door to your apartment and go inside.")
        goto("apartment")
    def Read_door_2A68():
        game.rolltext("{MIDDLE_READ_ROOM_2A68}")
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
    def cafeteria():
        game.showtext("The Cafeteria is closed!") #TODO: write cafeteria
    def sectionBdoor():
        pass
    def sectionAdoor():
        pass
    def auxcom_repair():
        #grabbing some data from game
        #redwhiteblue = game.getdata("auxcom:redwhiteinblue")
        cargoConnected =  game.getdata("auxcom:cargo")
        blueinblue = game.getdata("auxcom:blueinblue")
        tblueinwhite = game.getdata("auxcom:thickblueinwhite")
        yellowtasted = game.getdata("auxcom:yellowtasted")
        systemStatus = game.getdata("auxcom:systemstatus", "BROKEN")
        #region auxcom repair
        game.rolltext("{AUXCOM_INTRO}")
        if not game.yesno("{AUXCOM_OPENQUEST_1}"):
            game.showtext("{AUXCOM_LEAVE_1}")
            return
        if(cargoConnected):
            return dialoges.auxcom_cargo(game) #auxcom_cargo: contact the folks in cargo.
        if(systemStatus == "OK"):
            game.rolltext("{AUXCOM_STATUS_1}")
            return dialoges.auxcom_contact(game) #auxcom_contact: finding someone to talk to
        # auxcom main: fix the system
        if(systemStatus == "SHUTDOWN"):
            game.rolltext("{AUXCOM_STATUS_2}")
            if tblueinwhite:
                systemStatus = "OK"
                game.rolltext("{AUXCOM_STATUS_3}")
                game.setdata("auxcom:systemstatus", systemStatus)
                return dialoges.auxcom_contact(game)
        else:
            game.showtext("{AUXCOM_STATUS_4}")
        game.rolltext("{AUXCOM_STATUS_5}")
        if not game.yesno("{AUXCOM_OPENQUEST_2}"):
            game.showtext("{AUXCOM_LEAVE_2}")
            return
        game.rolltext("{AUXCOM_STATUS_6}")
        #NOTE: the general idea I have is to have a larger puzzle where options are added and removed as you try things.
        #       For now, there is only a single set of options, where the bad options are removed as they are attempted.
        #       Uses game.choose to allow for options to be added and removed
        choices = []
        choices.append(("THICK BLACK IN WHITE",T("AUXCOM_WIREOPTION_1"))) #a speaker explodes
        choices.append(("BLUE IN BLUE",("AUXCOM_WIREOPTION_2"))) # nothing happens. if left this way, one speaker will later have a (harmless) feedback
        choices.append(("REDWHITE IN WHITE",T("AUXCOM_WIREOPTION_3")))  # screen comes to life, displaying an audiovawe of your panting.
        choices.append(("REDWHITE IN BLUE",T("AUXCOM_WIREOPTION_4"))) # screen remains static, but what looks like flags seems to faintly fly in the background.
        choices.append(("THICK BLUE IN WHITE",T("AUXCOM_WIREOPTION_5"))) #nothing happens (key to make it work)
        choices.append(("TASTE BLACK",T("AUXCOM_WIREOPTION_6"))) # yeah.. death.
        choices.append(("YELLOW IN BLACK",T("AUXCOM_WIREOPTION_7"))) #com system shuts down
        choices.append(("TASTE YELLOW",T("AUXCOM_WIREOPTION_8"))) #this acually works... after you plug blue into white
        random.shuffle(choices)
        choices.append(("EXIT", T("AUXCOM_WIREOPTION_9")))

        cableLoop = True

        while cableLoop:
            text = ""
            game.choose(choices, T("AUXCOM_WIREOPTION_CHOOSE"))
            data = game.wait()
            if data.Type != "action":
                continue
            i = data.index
            a = data.tag
            
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
                text = T("AUXCOM_WIREACTION_1A")
                if systemStatus == "SHUTDOWN":
                    text += "\n" + T("AUXCOM_WIREACTION_1B")
                text += "\n" + T("AUXCOM_WIREACTION_1C")
                systemStatus = "SHUTDOWN"
                choices.pop(i)
            #endof thick black in yellow
            elif a == "BLUE IN BLUE":
                blueinblue = True
                text = T("AUXCOM_WIREACTION_2")
                choices.pop(i)
            #endof blue in blue
            elif a == "REDWHITE IN WHITE":
                text = T("AUXCOM_WIREACTION_3A")
                if systemStatus == "SHUTDOWN":
                    text += "\n" + T("AUXCOM_WIREACTION_3B")
                else:
                    text += "\n" + T("AUXCOM_WIREACTION_3C")
                text += "\n" + T("AUXCOM_WIREACTION_3D")
                choices.pop(i)
            #end of redwhite in white
            elif a == "REDWHITE IN BLUE":
                text = T("AUXCOM_WIREACTION_4A")
                if systemStatus == "SHUTDOWN":
                    text += "\n"+T("AUXCOM_WIREACTION_4B")
                else:
                    text += "\n"+T("AUXCOM_WIREACTION_4C")
                text += "\n"+T("AUXCOM_WIREACTION_4D")
                choices.pop(i)
            #endof redwhite in blue
            elif a == "THICK BLUE IN WHITE":
                text = ""
                if systemStatus == "SHUTDOWN":
                    if tblueinwhite:
                        text += "\n"+T("AUXCOM_WIREACTION_5A")
                    else:
                        text += "\n"+T("AUXCOM_WIREACTION_5B")
                    text += "\n"+T("AUXCOM_WIREACTION_5C")
                else:
                    if tblueinwhite:
                        text += "\n"+T("AUXCOM_WIREACTION_5D")
                    else:
                        text += "\n"+T("AUXCOM_WIREACTION_5E")
                tblueinwhite = True
            elif a == "TASTE BLACK":
                text = T("AUXCOM_WIREACTION_6")
                game.setGameover(game, T("AUXCOM_WIREACTION_6_GAMEOVER"))
                runner.stop()
                cableLoop = False #escape inner loop
            elif a == "YELLOW IN BLACK":
                pass
                if systemStatus == "SHUTDOWN":
                    text = T("AUXCOM_WIREACTION_7A")
                else:
                    text = T("AUXCOM_WIREACTION_7B")
                    choices.pop(i)
                systemStatus = "SHUTDOWN"
            game.rolltext(text)

        #saving data..
        #game.setdata("auxcom:redwhiteinblue", redwhiteblue)
        game.setdata("auxcom:blueinblue", blueinblue)
        game.setdata("auxcom:thickblueinwhite", tblueinwhite)
        game.setdata("auxcom:yellowtasted", yellowtasted)
        game.setdata("auxcom:systemstatus", systemStatus)
        if(systemStatus == "OK"):
            return dialoges.auxcom_contact(game)
        elif not game.getGameover(game):
            game.showtext("{AUXCOM_LEAVE_1}")
        #endregion auxcom repair
    def ladder():
        if not game.getdata("reactorC:fixed", False) and not game.getCounter(game, "reactorC")[0]: #if counter reactorC is not enabled
            game.setCounter(game, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.
        text = "{MIDDLE_LADDER_INTRO}"
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
        if game.getdata("WheelCMiddleLadder") == "open":
            text += "\n{MIDDLE_LADDER_INTRO_2}"
            enterText = "{MIDDLE_LADDER_ENTERQUEST_1}"
            openText = "{}"
        else:
            text += "\n{MIDDLE_LADDER_INTRO_3}"
            enterText = "{}"
            openText = "{MIDDLE_LADDER_ENTERQUEST_1}"
        game.rolltext(text)
        if(game.yesno(openText)):
            if game.getdata("WheelCMiddleLadder") == None:
                game.setdata("WheelCMiddleLadder", "open")
            game.rolltext(enterText)
            goto("ladder")

    def sectionCdoor():
        game.rolltext("{MIDDLE_SEC_C_DOOR}")
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
    def elevator():
        return dialoges.elevator(game)
    #endregion places and actions
    #----------------------------
    #local shorthand.
    #Stops loop and sets next place in the game.
    def goto(place):
        runner.stop()
        game.place = place
    def setupRunner():
        knowledge = game.getdata("wheelC:knowledge", 0)
        game.setdata("wheelC:knowledge", knowledge)
        if knowledge <= 0:
            base_navtext = T("MIDDLE_NAV_DESC_1")
        elif knowledge == 1:
            base_navtext = T("MIDDLE_NAV_DESC_2")
        else:
            base_navtext = T("MIDDLE_NAV_DESC_3")
        runner.nodes = [
            Game.PlaceNode(game, "TO_SEC_D",    base_navtext.format("A", "{MIDDLE_NAV_TO_SEC_D}"), [
                ("_", "{ACT_READ_SIGN}", sectionDdoor),
            ]),
            Game.PlaceNode(game, "BATHROOMS",        base_navtext.format("A", "{MIDDLE_NAV_TO_BATH}"), [
                ("_", "{ACT_ENTER_ROOM}", bathrooms),
            ]),
            Game.PlaceNode(game, "DOOR_2A68",   base_navtext.format("A", "{MIDDLE_NAV_DOOR_2A68}"), [
                ("_", "{ACT_ENTER_ROOM}", door_2A68),
                ("_", "{ACT_READ_SIGN}", Read_door_2A68)
            ]),
            Game.PlaceNode(game, "ELE",         base_navtext.format("A", "{MIDDLE_NAV_ELE}"), [
                ("_", "{ACT_USE}"), #elevator
            ]),
            Game.PlaceNode(game, "CAFE",        base_navtext.format("A", "{MIDDLE_NAV_CAFE}"), [
                ("_", "{ACT_ENTER_ROOM}"), #cafeteria
            ]),
            Game.PlaceNode(game, "TO_SEC_B",    base_navtext.format("A", "{MIDDLE_NAV_TO_SEC_B}"), [
                ("_", "{ACT_READ_SIGN}"), #sectionBdoor
            ]),
            Game.PlaceNode(game, "TO_SEC_A",    base_navtext.format("B", "{MIDDLE_NAV_TO_SEC_A}"), [
                ("_", "{ACT_READ_SIGN}"), #sectionAdoor
            ]),
            Game.PlaceNode(game, "AUXCOM",      base_navtext.format("B", "{MIDDLE_NAV_AUXCOM}"), [
                ("_", "{ACT_USE}"), #auxcom_repair
            ]),
            Game.PlaceNode(game, "LADDER",      base_navtext.format("B", "{MIDDLE_NAV_LADDER}"), [
                ("_", "{ACT_USE}"), #ladder
            ]),
            Game.PlaceNode(game, "TO_SEC_C",    base_navtext.format("B", "{MIDDLE_NAV_TO_SEC_C}"), [
                ("_", "{ACT_READ_SIGN}"), #sectionCdoor
            ])
        ]
        prevplace = game.prevPlace
        if prevplace == "apartment" and game.getdata("apartment:left", False):
            game.setdata("apartment:left", True)
            runner.index = "DOOR_2A68"
            intro = "{MIDDLE_INTRO_1}"
        elif prevplace == "apartment":
            intro = "{MIDDLE_INTRO_2}"
            runner.index = "DOOR_2A68"
            pass
        elif prevplace == "ladder":
            runner.index = "LADDER"
            intro = "{MIDDLE_INTRO_3}"
        elif prevplace == "bathrooms":
            runner.index = "BATHROOMS"
            intro = "{MIDDLE_INTRO_4}"
        else:
            #using the existing index (nav.x) from save or testcode as default.
            intro = "{MIDDLE_INTRO_5}"
        game.rolltext(intro)
    setupRunner()
    runner.run()
if __name__ == "__main__":
    # No testcode
    print("No testcode, please run main.py")