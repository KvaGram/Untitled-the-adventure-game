import random
import General
import Game
from General import Runner_WheelC_Rings as Runner

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

def Start(game:Game.Game):
    T = Game.Gettexter(game)
    
    runner:Runner = Runner(game)
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
        game.showtext("{MIDDLE_ENTER_ROOM_2A68}")
        goto("apartment")
    def Read_door_2A68():
        game.rolltext("{MIDDLE_READ_ROOM_2A68}")
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
    def cafeteria():
        game.showtext("{MIDDLE_CAFE}")
        goto("cafeteria")
    def sectionBdoor():
        pass #TODO: write description of passage
    def sectionAdoor():
        pass #TODO: write description of passage
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
            return auxcom_cargo() #auxcom_cargo: contact the folks in cargo.
        if(systemStatus == "OK"):
            game.rolltext("{AUXCOM_STATUS_1}")
            return auxcom_contact() #auxcom_contact: finding someone to talk to
        # auxcom main: fix the system
        if(systemStatus == "SHUTDOWN"):
            game.rolltext("{AUXCOM_STATUS_2}")
            if tblueinwhite:
                systemStatus = "OK"
                game.rolltext("{AUXCOM_STATUS_3}")
                game.setdata("auxcom:systemstatus", systemStatus)
                return auxcom_contact()
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
                    text += "\n{AUXCOM_WIREACTION_8A}"
                else:
                    yellowtasted = True
                    text += "\n{AUXCOM_WIREACTION_8B}"
                if tblueinwhite:
                    text += "\n{AUXCOM_WIREACTION_8C}"
                    systemStatus = "OK"
                elif systemStatus == "SHUTDOWN":
                    text += "\n{AUXCOM_WIREACTION_8D}"
                    systemStatus = "BROKEN"
                else:
                    text += "\n{AUXCOM_WIREACTION_8E}"
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
            return auxcom_contact()
        elif not game.getGameover(game):
            game.showtext("{AUXCOM_LEAVE_1}")
        #endregion auxcom repair
    def auxcom_contact():
        #region auxcom
        cargoConnected = game.getdata("auxcom:cargo", False)
        if cargoConnected:
            return auxcom_cargo()
        game.rolltext("{AUXCOM2_INTRO}")
        choices = [
            ("BRIDGE", T("AUXCOM2_COMOP_1")),
            ("ENGINEERING", T("AUXCOM2_COMOP_2")),
            ("RADIATION SHELTER 1", T("AUXCOM2_COMOP_3")),
            ("RADIATION SHELTER 2", T("AUXCOM2_COMOP_4")),
            ("RADIATION SHELTER 3", T("AUXCOM2_COMOP_5")),
            ("RADIATION SHELTER 4", T("AUXCOM2_COMOP_6")),
            ("WHEEL A AUXCOM", T("AUXCOM2_COMOP_7")),
            ("WHEEL B AUXCOM", T("AUXCOM2_COMOP_8")),
            ("WHEEL D AUXCOM", T("AUXCOM2_COMOP_9")),
            ("CARGO", T("AUXCOM2_COMOP_CARGO")),
            ("EXIT", T("AUXCOM2_COMOP_EXIT")),
        ]
        
        responsekey = {
            "BRIDGE" : "{AUXCOM2_NO_RESP_1}",
            "ENGINEERING" : "{AUXCOM2_NO_RESP_1}",
            "RADIATION SHELTER 1" : "{AUXCOM2_NO_RESP_1}",
            "RADIATION SHELTER 2" : "{AUXCOM2_NO_RESP_1}",
            "RADIATION SHELTER 3" : "{AUXCOM2_NO_RESP_1}",
            "RADIATION SHELTER 4" : "{AUXCOM2_NO_RESP_1}",
            "WHEEL A AUXCOM" : "{AUXCOM2_NO_RESP_1}",
            "WHEEL B AUXCOM" : "{AUXCOM2_NO_RESP_1}",
            "WHEEL D AUXCOM" : "{AUXCOM2_NO_RESP_1}",
            "CARGO" :   "{AUXCOM2_RESP_CARGO}",
            "EXIT"  :   "{AUXCOM2_RESP_EXIT}"
        }
        duds = (
            "BRIDGE",
            "ENGINEERING",
            "RADIATION SHELTER 1",
            "RADIATION SHELTER 2",
            "RADIATION SHELTER 3",
            "RADIATION SHELTER 4",
            "WHEEL A AUXCOM",
            "WHEEL B AUXCOM",
            "WHEEL D AUXCOM",
        )
        while(True):
            game.choose(choices, "{AUXCOM2_CONTACTQUEST}")
            data:Game.ActDataInput = game.wait()
            tag = data.tag
            if(data.Type != "action"):
                continue
            game.rolltext(responsekey.get(tag, "..."))
            if tag == "EXIT":
                break
            elif tag in duds:
                choices.pop(tag)
            elif tag == "CARGO":
                return auxcom_cargo()
        #endregion auxcom2
    def auxcom_cargo():
        localfrags = {}
        #Note: Whatever the dialoge, it is up to the player what to do afterwards.
        asshole = game.getInventory("ASSHOLE") #if player has a reputation for being an ass.
        reactorFixed = game.getdata("reactorC:fixed", False)
        prevcontact = game.getdata("auxcom:cargo", False)
        thankedForReactor = game.getdata("auxcom:react_thanks", False)
        # Only change is the information they are given.
        # From here, or the ladder if the player skips this, a counter is enabled that gives the player 10 'time units' before game over.
        if not reactorFixed and game.getCounter(game, "reactorC")[0]: #counter not enabled
            game.setCounter(game, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.

        if prevcontact:
            #TODO: alternate contact for returning to auxcom
            if asshole:
                game.rolltext("{AUXCOM3_INTRO_ASS}")
            elif reactorFixed:
                if not thankedForReactor:
                    game.rolltext("{AUXCOM3_INTRO_THANKS}")
                else:
                    game.rolltext("{AUXCOM3_INTRO_RETURN}")
                choices = (
                    ("CODE", T("AUXCOM_DIALOGE_3_OPTION_CODE")),
                    ("TRUTH",T("AUXCOM_DIALOGE_3_OPTION_TRUTH")),
                    ("EXIT", T("AUXCOM_DIALOGE_3_OPTION_EXIT"))
                )
                while True:
                    game.choose(T("AUXCOM_DIALOGE_3_QUEST"))
                    data = game.wait()
                    if not data or data.Type != "action":
                        continue
                    elif data.tag =="CODE":
                        game.rolltext("{AUXCOM_DIALOGE_3_CODE}")
                    elif data.tag =="TRUTH":
                        game.rolltext("{AUXCOM_DIALOGE_3_TRUTH}")
                        if game.yesno(T("AUXCOM_DIALOGE_3_INTERRUPT_QUEST")):
                            game.rolltext("{AUXCOM_DIALOGE_3_SHORT_STORY}")
                        else:
                            game.rolltext("{AUXCOM_DIALOGE_3_FULL_STORY}")
                    elif data.tag =="EXIT":
                        game.showtext("{AUXCOM_DIALOGE_3_EXIT}")
                        break
            else:
                game.rolltext("{AUXCOM3_INTRO_PLZFIX}")
        else:
            game.showtext("{AUXCOM_CONTACT_MADE}")
            choices = [
                ("", T("AUXCOM_DIALOGE_1_OPTION_1")),
                ("", T("AUXCOM_DIALOGE_1_OPTION_2")),
                ("", T("AUXCOM_DIALOGE_1_OPTION_3")),
                ("", T("AUXCOM_DIALOGE_1_OPTION_4")),
            ]
            while True:
                game.choose(choices, T("AUXCOM_DIALOGE_1_QUEST"))
                data = game.wait()
                if data:
                    if data.Type != "action":
                        continue
                    ind = data.index
                    break
            #game.showtext(">> "+choices[ind][1])
            if ind == 0 or ind == 3:
                p = game.PlayerName
            elif game.PlayerGender == "male":
                p = T("GENDERED_1_MALE")
            else:
                p = T("GENDERED_1_FEMALE")
            localfrags['_P'] = p
            if(reactorFixed):
                game.rolltext("{AUXCOM_DIALOGE_1B_REACTOR_QUEST}",frags=localfrags)
                admitfix = game.yesno(T("QWASIT"))
                localfrags['_REACT_1'] = ""
                localfrags['_REACT_2'] = ""
                if(admitfix):
                    localfrags['_REACT_1'] = "{AUXCOM_DIALOGE_1B_PART_1A}"
                    localfrags['_REACT_2'] = "{AUXCOM_DIALOGE_1B_PART_2A}"
                else:
                    localfrags['_REACT_1'] =  "{AUXCOM_DIALOGE_1B_PART_1B}"
                    localfrags['_REACT_2'] = "{AUXCOM_DIALOGE_1B_PART_2B}"
                game.rolltext("{AUXCOM_DIALOGE_1B}")
                choices = (
                    ("WHY_ME", T("AUXCOM_DIALOGE_2B_OPTION_1")),
                    ("WEAK_CODE", T("AUXCOM_DIALOGE_2B_OPTION_2")),
                    ("EXIT", T("AUXCOM_DIALOGE_2B_OPTION_3"))
                    )
                while True:
                    game.choose(choices, "{AUXCOM_DIALOGE_2B_QUEST}")
                    data = game.wait()
                    if not data or data.Type != "action":
                        continue
                    if data.tag == "WHY_ME":
                        game.rolltext("{AUXCOM_DIALOGE_2B_WHY}")
                    elif data.tag == "WEAK_CODE":
                        game.rolltext("{AUXCOM_DIALOGE_2B_CODE}")
                    elif data.tag == "EXIT":
                        game.rolltext("{AUXCOM_DIALOGE_2B_EXIT}")
                        break
                game.setdata("auxcom:cargo", True)
                game.setdata("auxcom:react_thanks", True)
            
        # If the reactor is not yet fixed:
            game.rolltext("{AUXCOM_DIALOGE_1A}")
            choices = [
                ("SCREWIT", T("AUXCOM_DIALOGE_2A_OPTION_1")), #Asshole option! Locks up all future dialoge
                ("NO", T("AUXCOM_DIALOGE_2A_OPTION_2")),
                ("YES", T("AUXCOM_DIALOGE_2A_OPTION_3")),
                ("WUT", T("AUXCOM_DIALOGE_2A_OPTION_4"))
            ]
            while True:
                game.choose(choices, T("AUXCOM_DIALOGE_2A_QUEST"))
                data = game.wait()
                if not data or data.Type != "action":
                    continue
                elif data.tag == "SCREWIT":
                    asshole = True
                    game.setInventory("ASSHOLE", True)
                    game.rolltext("{AUXCOM_DIALOGE_2A_SCREWIT}")
                    break
                elif data.tag == "NO":
                    game.rolltext("{AUXCOM_DIALOGE_2A_NO}")
                    game.setInventory("KEYCODE", True)
                    break
                elif data.tag == "YES":
                    game.rolltext("{AUXCOM_DIALOGE_2A_YES}")
                    game.setInventory("KEYCODE", True)
                    break
                elif data.tag == "WUT":
                    game.rolltext("{AUXCOM_DIALOGE_2A_WUT}")
                    choices.pop(3)
                    continue
        game.setdata("auxcom:cargo", True)
        game.setdata("auxcom:react_thanks", thankedForReactor)

    def sectionBdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionAdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")

    def sectionCdoor():
        game.rolltext("{MIDDLE_SEC_C_DOOR}")
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)


    #local shorthand.
    #Stops loop and sets next place in the game.
    def goto(place):
        runner.stop()
        game.place = place

    #Import Elevator event from General
    elevator = General.elevator(game)
    #importing ladder
    ladder = General.LadderAccess(game, goto)

    #endregion places and actions
    #----------------------------

    def setupRunner():
        from untitled_const import NAV_MIDDLE_RADIUS as r
        from untitled_const import NAV_LIT_MIDDLE_A as ha
        from untitled_const import NAV_LIT_MIDDLE_B as hb
        runner.nodes = [
            Game.PlaceNode(game, "TO_SEC_D", T("AREANAME_TO-SEC-D"), r, 0.0, [
                ("_", T("ACT_READ_SIGN"), sectionDdoor),
            ]),
            Game.PlaceNode(game, "BATHROOMS", T("AREANAME_BATHROOMS-DOOR"), r, 0.0, [
                ("_", T("ACT_ENTER_ROOM"), bathrooms),
            ]),
            Game.PlaceNode(game, "DOOR_2A68", T("AREANAME_APARTMENT-DOOR"), r, 3.8, [
                ("_", T("ACT_ENTER_ROOM"), door_2A68),
                ("_", T("ACT_READ_SIGN"), Read_door_2A68)
            ]),
            Game.PlaceNode(game, "ELE", T("AREANAME_ELEVATOR-2A"), r, 3.95, [
                ("_", T("ACT_USE"), elevator),
            ]),
            Game.PlaceNode(game, "CAFE", T("AREANAME_"), r, 3.15, [
                ("_", T("ACT_ENTER_ROOM"), cafeteria),
            ]),
            Game.PlaceNode(game, "TO_SEC_B", T("AREANAME_"), r, 0.0, [
                ("_", T("ACT_READ_SIGN"), sectionBdoor),
            ]),
            Game.PlaceNode(game, "TO_SEC_A", T("AREANAME_"), r, 0.0, [
                ("_", T("ACT_READ_SIGN"), sectionAdoor), 
            ]),
            Game.PlaceNode(game, "AUXCOM", T("AREANAME_"), r, 0.0, [
                ("_", T("ACT_USE"), auxcom_repair),
            ]),
            Game.PlaceNode(game, "LADDER", T("AREANAME_"), r, 0.0, [
                ("_", T("ACT_USE"), ladder),
            ]),
            Game.PlaceNode(game, "TO_SEC_C", T("AREANAME_"), r, 0.0, [
                ("_", T("ACT_READ_SIGN"), sectionCdoor),
            ])
        ]
        runner.passActs = [
            ("TO_SEC_B","TO_SEC_A", sectionBdoor_pass),
            ("TO_SEC_A","TO_SEC_B", sectionAdoor_pass)
        ]

        runner.index, intro =  (
        {
            "apartment":("DOOR_2A68", "{MIDDLE_INTRO_2}"),
            "ladder":("LADDER", "{MIDDLE_INTRO_3}"),
            "bathrooms":("BATHROOMS", "{MIDDLE_INTRO_4}"),
            "cafeteria":("CAFE", "{MIDDLE_INTRO_5}"),
        }.get(game.prevPlace, (runner.index, "{MIDDLE_INTRO_5}")))

        if game.getdata("apartment:left", False):
            game.setdata("apartment:left", True)
            intro = "{MIDDLE_INTRO_1}"
        game.rolltext(intro)
    setupRunner()
    runner.run()
if __name__ == "__main__":
    import tkinter
    from main import VERSION
    from main import _testloop

    tkRoot = tkinter.Tk(screenName="TEST! middle ring")
    game:Game.Game = Game.Game(tkRoot, VERSION, "english")
    def testdata():
        game.newgame()
        #setting prevplace and place
        game.place = "ladder"
        game.place = "middle"
        #if game.yesno(message="..."):
        #   pass
    _testloop(game, Start, testdata, "MIDDLE RING")