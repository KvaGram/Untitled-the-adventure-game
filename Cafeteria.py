import Game
import General
import random

_LIT = "cafeteria:lit"

def Start(game:Game.Game):
    from untitled_const import NAV_MIDDLE_RADIUS as rad
    from untitled_const import NAV_LIT_MIDDLE_A
    rot = 3.16
    T = Game.Gettexter(game)
    navdata:Game.Navdata = game.Navdata
    navdata.MapLit = NAV_LIT_MIDDLE_A
    navdata.MapRadians = rot
    navdata.MapRadius = rad
    navdata.AreaName = T("AREANAME_CAFETERIA")

    def start():
        if not game.getdata(_LIT, False):
            darkness()
        else:
            game.rolltext("{CAFE_INTRO_LIT}")
            lit()
    def lit():
        options = [
            ["BODY",      T("CAFE_LIT_OPTION_1"), lit_body],
            ["LAMP",      T("CAFE_LIT_OPTION_2"), lit_lamp],
            ["TABLE",     T("CAFE_LIT_OPTION_3"), lit_table],
            ["COUNTER",   T("CAFE_LIT_OPTION_4"), lit_counter],
            ["RACK",      T("CAFE_LIT_OPTION_5"), trans_rack],
        ]
        random.shuffle(options)
        options = Game.OptionList(options)
        options.append(["EXIT", T("CAFE_LIT_OPTION_EXIT"), lit_exit])
        while(True):
            game.choose(options)
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            #runs action from options.
            #if true, break out from loop
            if options.RunAct(data):
                break
        #end of lit part

    def darkness():
        game.rolltext("{CAFE_DARK_1}")
        options = [
            ["BODY",      T("CAFE_DARK_OPTION_1"), dark_body],
            ["LAMP",      T("CAFE_DARK_OPTION_2"), dark_lamp],
            ["TABLE",     T("CAFE_DARK_OPTION_3"), dark_table],
            ["COUNTER",   T("CAFE_DARK_OPTION_4"), dark_counter],
        ]
        random.shuffle(options)
        options = Game.OptionList(options)
        options.append(["EXIT", T("CAFE_DARK_OPTION_EXIT"), dark_exit])
        while(True):
            game.choose(options)
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            #runs action from options.
            #if true, break out from loop
            if options.RunAct(data):
                break
    #end of darkness part
    def dark_body():
        game.setInventory("BROKE_TRANSLATOR", True)
        game.rolltext("{CAFE_DARK_BODY}")
        game.setInventory("BROKE_TRANSLATOR", False)
        return False
    def dark_lamp():
        game.rolltext("{CAFE_DARK_LAMP}")
        game.setdata(_LIT, True)
        lit() # Runs the Lit storypart, then signals to exit darkness()
        return True
    def dark_table():
        game.rolltext("{CAFE_DARK_TABLE}")
        return False
    def dark_counter():
        game.rolltext("{CAFE_DARK_COUNTER}")
        return False
    def dark_exit():
        game.rolltext("{CAFE_DARK_EXIT}")
        game.place = "middle"
        return True
        
    def lit_body():
        game.setInventory("BROKE_TRANSLATOR", True)
        game.rolltext("{CAFE_LIT_BODY}")
        return False
    def lit_lamp():
        game.rolltext("{CAFE_LIT_LAMP}")
        return False
    def lit_table():
        game.rolltext("{CAFE_LIT_TABLE}")
        return False
    def lit_counter():
        game.rolltext("{CAFE_LIT_COUNTER}")
        return False
    def lit_exit():
        game.rolltext("{CAFE_LIT_EXIT}")
        game.place = "middle"
        return True
    def trans_rack():
        game.setInventory("TRANSLATOR", True)
        game.rolltext("{CAFE_TRANS_RACK}")
        return False
    start()
#end of CAFE Main
    
#TESTCODE
if __name__ == "__main__":
    import tkinter
    from main import VERSION
    from main import _testloop

    tkRoot = tkinter.Tk(screenName="TEST! Cafeteria scene")
    game = Game.Game(tkRoot, VERSION, "english")
    def testdata():
        game.newgame()
    _testloop(game, Start, testdata, "CAFETERIA")
