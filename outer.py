import Game
import random
import General
from General import Runner_WheelC_Rings as Runner
from untitled_const import NAV_LIT_OUTER_A
from untitled_const import NAV_LIT_OUTER_B

def Start(game:Game.Game):
    runner:Runner = Runner(game)
    T = Game.Gettexter(game)

    def goto(place):
        runner.stop()
        game.place = place
    #Import Elevator event from General
    elevator = General.elevator(game)
    #importing ladder
    ladder = General.LadderAccess(game, goto)

    #---------------------------
    #region actions and places
    def sectionDdoor_read():
        game.rolltext("{OUTER_SEC_D_DOOR}")
    def sectionBdoor_pass():
        runner.nav.MapLit = NAV_LIT_OUTER_B
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionAdoor_pass():
        runner.nav.MapLit = NAV_LIT_OUTER_A
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionBdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionAdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionCdoor_read():
        game.rolltext("{OUTER_SEC_C_DOOR}")

    def reactNode():
        frags = {}
        hasTrans = game.getInventory("TRANSLATOR")
        if(hasTrans):
            game.rolltext("{REACTORNODE_1A}")
        else:
            game.rolltext("{REACTORNODE_1B}")
        if game.getdata("reactorC:fixed", False):
            game.rolltext("{REACTORNODE_1C}")
            return
        if not game.yesno("{REACTORNODE_1_QUEST}"):
            return
        #Idea:
        # The reactor may have one day been a marvel of tachyon engineering.
        #A machine that could beat entropy to a pulp, now dieing to it.
        if game.PlayerGender == "male":
            frags["_P2"] = T("GENDERED_1_MALE") #man
            frags["_P3"] = T("GENDERED_3_MALE") #his
            frags["_P4"] = T("GENDERED_4_MALE") #he
        else:
            frags["_P2"] = T("GENDERED_1_FEMALE") #lady
            frags["_P3"] = T("GENDERED_3_FEMALE") #her
            frags["_P4"] = T("GENDERED_4_FEMALE") #she
        
        game.rolltext("{REACTORNODE_2}", frags=frags)
        options3 = Game.OptionList([
            ["MANUAL","{REACTORNODE_3_OPTION_1}"],
            ["RANDOM","{REACTORNODE_3_OPTION_2}"],
            ["ESCAPE","{REACTORNODE_3_OPTION_3}"],
        ])
        while True:
            game.choose(options3, "{REACTORNODE_3_QUEST}")
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            if data.tag == "MANUAL":
                game.rolltext("{REACTORNODE_3A}", frags=frags)
                break
            elif data.tag == "RANDOM":
                game.rolltext("{REACTORNODE_3B}", frags=frags)
                game.setGameover("{REACTORNODE_3B_GAMEOVER}")
                runner.stop()
                return
            elif data.tag == "ESCAPE":
                game.rolltext("{REACTORNODE_ESCAPE}", frags=frags)
                game.setGameover("{REACTORNODE_ESCAPE_GAMEOVER}")
                runner.stop()
                return
        if hasTrans:
            game.rolltext("{REACTORNODE_4A}", frags=frags)
            options5List = T("REACTORNODE_5A_OPTION_LIST").split()
        else:
            game.rolltext("{REACTORNODE_4B}", frags=frags)
            options5List = T("REACTORNODE_5B_OPTION_LIST").split()
        options5 = Game.OptionList([
            ["COOLDOWN" ,options5List[0]],
            ["SLOWDOWN" ,options5List[1]],
            ["HURRY"    ,options5List[2]],
            ["FIRE_1"   ,options5List[3]],
            ["FIRE_2"   ,options5List[4]],
            ["INFO"     ,options5List[5]],
            ["DEATH"    ,options5List[6]],
            ["SHUTDOWN" ,options5List[7]],
            ["ESCAPE"   ,options5List[8]],
        ])
        options5.Randomize()
        options5.MoveItemBack("ESCAPE")
        
        
        #unlocks if you have a translator, and use the INFO option, this enables some alternate or aditional text.
        warnedOfLoops = False
        cooledDown = False # If cooled down has been initialized. must be done before slow-down.
        slowedDown = False # If slow down has been initiated. will cause a fire if done before cooldown
        fixing_reactor_loop = True
        while fixing_reactor_loop:
            game.choose(options5, "{REACTORNODE_5_QUEST}")
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            if data.tag == "ESCAPE":
                game.rolltext("{REACTORNODE_ESCAPE}", frags=frags)
                game.setGameover("{REACTORNODE_ESCAPE_GAMEOVER}")
                runner.stop()
                return
            elif data.tag == "COOLDOWN":
                if cooledDown:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_COOLDOWN_3_A}")
                    else:
                        game.rolltext("{REACTORNODE_COOLDOWN_3_B}")
                elif slowedDown:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_COOLDOWN_2_A}")
                    else:
                        game.rolltext("{REACTORNODE_COOLDOWN_2_B}")
                else:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_COOLDOWN_1_A}")
                    else:
                        game.rolltext("{REACTORNODE_COOLDOWN_1_B}")
                cooledDown = True
            elif data.tag == "SLOWDOWN":
                if slowedDown:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_SLOWDOWN_3_A}")
                    else:
                        game.rolltext("{REACTORNODE_SLOWDOWN_3_B}")
                elif not cooledDown:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_SLOWDOWN_1_A}")
                    else:
                        game.rolltext("{REACTORNODE_SLOWDOWN_1_B}")
                else:
                    if hasTrans:
                        game.rolltext("{REACTORNODE_SLOWDOWN_2_A}")
                    else:
                        game.rolltext("{REACTORNODE_SLOWDOWN_2_B}")
                    fixing_reactor_loop = False
                slowedDown = True
            elif data.tag == "HURRY":
                if hasTrans:
                    game.rolltext("{REACTORNODE_HURRY_A}")
                else:
                    game.rolltext("{REACTORNODE_HURRY_B}")
                game.setGameover("{REACTORNODE_TIMELOOP_GAMEOVER}")
                fixing_reactor_loop = False
                runner.stop()
            elif data.tag == "FIRE_1":
                if hasTrans:
                    if slowedDown:
                        game.rolltext("{REACTORNODE_FIREACC_1_A}")
                    else:
                        game.rolltext("{REACTORNODE_FIREACC_2_A}")
                else:
                    game.rolltext("{REACTORNODE_FIREACC_B}")
                slowedDown = False #This action always reaccelerates the reactor
            elif data.tag == "FIRE_2":
                if hasTrans:
                    game.rolltext("{REACTORNODE_FIREROOM_A}")
                else:
                    game.rolltext("{REACTORNODE_FIREROOM_B}")
                options5.pop(data.index)
            elif data.tag == "INFO":
                if hasTrans:
                    infofrags = {}
                    infofrags["_FIRE_ALERTS"] = ""
                    infofrags["_THATSME"] = ""
                    if cooledDown:
                        infofrags["_TEMP"] = "{REACTORNODE_INFO_TEMP_1}"
                    elif slowedDown:
                        infofrags["_TEMP"] = "{REACTORNODE_INFO_TEMP_3}"
                        for _ in range(random.randint(3, 10)):
                            firefrags = {
                                "_SEC" : random.choice(("A", "B", "C", "D")),
                                "_NUM" : random.randint(1,12)
                                }
                            infofrags["_FIRE_ALERTS"] += "\n\t"+T("REACTORNODE_INFO_FIREALERT").format(**firefrags)
                    else:
                        infofrags["_TEMP"] = "{REACTORNODE_INFO_TEMP_2}"
                    if warnedOfLoops:
                        infofrags["_THATSME"] = "{REACTORNODE_THATSME}"
                    
                    game.rolltext("{REACTORNODE_INFO_A}", frags = infofrags)
                else:
                    game.rolltext("{}")
            elif data.tag == "DEATH":
                if hasTrans:
                    game.rolltext("{REACTORNODE_OVERLOAD_A}")
                else:
                    game.rolltext("{REACTORNODE_OVERLOAD_B}")
                runner.stop()
                fixing_reactor_loop = False
                game.setGameover(game, "{REACTORNODE_OVERLOAD_GAMEOVER}")
            elif data.tag == "SHUTDOWN":
                if hasTrans:
                    shutfrags = {"_GOTINFO":""}
                    if warnedOfLoops:
                        shutfrags["_GOTINFO"] = "{REACTORNODE_SHUTDOWN_INFO}"
                        options5.pop(data.index) #you cross out this if you know why it fails.
                    game.rolltext("{REACTORNODE_SHUTDOWN_A}", frags=shutfrags)
                else:
                    game.rolltext("{REACTORNODE_SHUTDOWN_B}")
        
            if cooledDown and slowedDown:
                game.endCounter("reactorC")
                game.setdata("reactorC:fixed", True)
                fixing_reactor_loop = False
                game.rolltext("{REACTORNODE_6}")
                break
        #end of loop
    #endregion actions and places
    #---------------------------

    def setupRunner():
        from untitled_const import NAV_MIDDLE_RADIUS as r
        from untitled_const import TAU
        runner.nodes = []

        runner.nodes += [
            Game.PlaceNode(game, "TO_SEC_D",    T("AREANAME_TO-SEC-D"), r, 12/16 * TAU + 0.00, [("_", T("ACT_READ_SIGN"), sectionDdoor_read)]),
            Game.PlaceNode(game, "TO_ELEVATOR", T("OUTER_NAV_ELE"),      r, 10/16 * TAU + 0.00, [("_", T("ACT_USE"), elevator)]),
            Game.PlaceNode(game, "TO_SEC_B",    T("OUTER_NAV_TO_SEC_B"), r,  8/16 * TAU + 0.05, [("_", T("ACT_READ_SIGN"), sectionBdoor_read )]),
            Game.PlaceNode(game, "TO_SEC_A",    T("OUTER_NAV_TO_SEC_A"), r,  8/16 * TAU - 0.05, [("_", T("ACT_READ_SIGN"), sectionAdoor_read )]),
            Game.PlaceNode(game, "TO_LADDER",   T("OUTER_NAV_LADDER"),   r,  6/16 * TAU + 0.00, [("_", T("ACT_USE"), ladder)]),
            Game.PlaceNode(game, "TO_REACTOR",  T("OUTER_NAV_TO_NODE"),  r,  3/16 * TAU + 0.00, [("_", T("ACT_ENTER_ROOM"), ladder)]),
            Game.PlaceNode(game, "TO_SEC_C",    T("OUTER_NAV_TO_SEC_C"), r,  4/16 * TAU + 0.00, [("_", T("ACT_READ_SIGN"), sectionCdoor_read )]),
        ]
        runner.passActs = [
            ("TO_SEC_B","TO_SEC_A", sectionBdoor_pass),
            ("TO_SEC_A","TO_SEC_B", sectionAdoor_pass)
        ]

        runner.index, intro = {
            "ladder" : ("TO_LADDER","{OUTER_INTRO_2}"),
        }.get(game.prevPlace, ("TO_SEC_C", "{OUTER_INTRO_1}"))
        
        if runner.index > runner.indexofnode("TO_SEC_B"):
            runner.nav.MapLit = NAV_LIT_OUTER_B
        else:
            runner.nav.MapLit = NAV_LIT_OUTER_A
        game.rolltext(intro)
    setupRunner()
    runner.run()
    
#This is the testcode for the module.
#Testers - feel free to edit this code to fit whatever test you need.
if __name__ == "__main__":
    import tkinter
    from main import VERSION
    from main import _testloop

    tkRoot = tkinter.Tk(screenName="TEST! outer ring")
    game:Game.Game = Game.Game(tkRoot, VERSION, "english")
    def testdata():
        game.newgame()
        #setting prevplace and place
        game.place = "ladder"
        game.place = "outer"
        #if game.yesno(message=".."):
        #    game.setInventory("", True)
    _testloop(game, Start, testdata, "OUTER RING")