import Game
import random
import General
from General import Runner_WheelC_Rings as Runner

def Main(game:Game.Game):
    T = Game.Gettexter(game)   
    runner = Runner(game)

    def goto(place):
        runner.stop()
        game.place = place

    #region actions and places


    #importing elevator event
    elevator = General.elevator(game)
    #importing ladder
    ladder = General.LadderAccess(game, goto)

    def sectionBdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionAdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionBdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionAdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionDdoor_read():
        game.rolltext("{INNER_SEC_D_DOOR}")
    def sectionCdoor_read():
        game.rolltext("{INNER_SEC_C_DOOR}")

    #groups that can be saved.
    #126 people can be saved.
    def tubes(num):
        def chamberRoom():
            key = game.getInventory("KEYCODE")
            visited = game.getdata("inner:stasisroom:"+str(num), False)
            peopleSaved = game.getdata("stasis:peopleSaved", 0)
            if not key:
                game.rolltext("{INNER_TUBES_LOCKED}")
                game.updateCounter("reactorC", 1) #refunded time cost.
                return
            elif visited:
                game.showtext("{INNER_TUBES_VISITED}")
                game.updateCounter("reactorC", 1) #refunded time cost.
            else:
                if num == 0:
                    game.rolltext("{INNER_TUBES_1}")
                    peopleSaved += 1
                elif num == 1 or num == 7 or num == 11:
                    game.rolltext("{INNER_TUBES_2}")
                    peopleSaved += 17
                elif num == 2 or num == 6:
                    game.rolltext("{INNER_TUBES_3}")
                    peopleSaved += 0
                elif num == 3:
                    game.rolltext("{INNER_TUBES_4}")
                    peopleSaved += 5
                elif num == 4 or num == 9:
                    game.rolltext("{INNER_TUBES_5}")
                    peopleSaved += 0
                elif num == 5:
                    game.rolltext("{INNER_TUBES_6}")
                    peopleSaved += 45
                elif num == 8 or num == 10:
                    game.rolltext("{INNER_TUBES_7}")
                    peopleSaved += 12
            status = game.updateCounter("reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                runner.running = False
                return
            game.setdata("inner:stasisroom:"+str(num), True)
            game.setdata("stasis:peopleSaved", peopleSaved)
        return chamberRoom

    

    #endregion actions and places
    #---------------------------
    def setupRunner():
        base_navtext = T("NAV_DESC_TEMPLATE")
        base_frags = {"_WHEEL":"{WHEEL_C_NAME_1}", "_RINGNAME":T("INNER_RING_NAME"), "_SECTORNAME" : T("SECTOR_A_TERM_1")}
        runner.nodes = []
        runner.nodes += [
             Game.PlaceNode(game, "TO_SEC_D",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_TO_SEC_D}"), [
                ("_", T("ACT_READ_SIGN"), sectionDdoor_read)]),

             Game.PlaceNode(game, "TO_ROOM_A",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_A}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(0))]),
             Game.PlaceNode(game, "TO_ROOM_B",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_B}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(1))]),
             Game.PlaceNode(game, "TO_ROOM_C",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_C}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(2))]),

             Game.PlaceNode(game, "TO_ELEVATOR",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ELE}"), [
                ("_", T("ACT_USE"), elevator)]),

             Game.PlaceNode(game, "TO_ROOM_D",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_D}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(3))]),
             Game.PlaceNode(game, "TO_ROOM_E",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_E}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(4))]),
             Game.PlaceNode(game, "TO_ROOM_F",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_F}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(5))]),
            
            Game.PlaceNode(game, "TO_SEC_B",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_TO_SEC_B}"), [
                ("_", T("ACT_READ_SIGN"), sectionBdoor_read )]),
        ]
        base_frags["_SECTORNAME"] = T("SECTOR_B_TERM")
        runner.nodes += [
             Game.PlaceNode(game, "TO_SEC_A",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_TO_SEC_A}"), [
                ("_", T("ACT_READ_SIGN"), sectionAdoor_read )]),

             Game.PlaceNode(game, "TO_ROOM_G",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_G}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(6))]),
             Game.PlaceNode(game, "TO_ROOM_H",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_H}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(7))]),
             Game.PlaceNode(game, "TO_ROOM_I",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_I}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(8))]),

             Game.PlaceNode(game, "TO_LADDER",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_LADDER}"), [
                ("_", T("ACT_USE"), ladder)]),

             Game.PlaceNode(game, "TO_ROOM_J",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_J}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(9))]),
             Game.PlaceNode(game, "TO_ROOM_K",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_K}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(10))]),
             Game.PlaceNode(game, "TO_ROOM_L",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_ROOM_L}"), [
                ("_", T("INNER_TO_ROOM_QUEST"), tubes(11))]),
            
            Game.PlaceNode(game, "TO_SEC_C",    base_navtext.format(**base_frags, _LOCAL_NAME = "{INNER_NAV_TO_SEC_C}"), [
                ("_", T("ACT_READ_SIGN"), sectionCdoor_read )]),
        ]
        
        runner.passActs = [
            ("TO_SEC_B","TO_SEC_A", sectionBdoor_pass),
            ("TO_SEC_A","TO_SEC_B", sectionAdoor_pass)
        ]

        runner.index, intro = {
            "ladder" : ("TO_LADDER","{INNER_INTRO_2}"),
        }.get(game.prevPlace, ("TO_SEC_C", "{INNER_INTRO_1}"))

        game.rolltext(intro)
    setupRunner()
    runner.run()
    
if __name__ == "__main__":
    import tkinter
    from main import VERSION
    from main import _testloop

    tkRoot = tkinter.Tk(screenName="TEST! inner ring")
    game:Game.Game = Game.Game(tkRoot, VERSION, "english")
    def testdata():
        game.newgame()
        #setting prevplace and place
        game.place = "ladder"
        game.place = "inner"
        if game.yesno(message="ADD KEYCODE?"):
            game.setInventory("KEYCODE", True)
    _testloop(game, Main, testdata, "INNER RING")