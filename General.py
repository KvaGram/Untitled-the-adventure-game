#General
#for events that can trigger from more than one module/place in the story.
#TODO: consider moving base runners from Game to this module.
#       That would also moving general functions from Game.
#       Doing so would spread out the code a bit, hopefully making things more readable.

import Game

def elevator(game:Game.Game):
    def content():
        T = Game.Gettexter(game)
        frags = {}
        place = game.place
        #region elevator
        if place == "outer":
            frags["_BUTTONSET"] = "{ELEVATOR_BUTTONSET_BOTTOM}"
            frags["_DESC"] = "{ELEVATOR_DESC_CORRIDOR}"
            choices = (("UP", "{ELEVATOR_OPTION_UP}"), ("CARGO","{ELEVATOR_OPTION_CARGO}"), ("EXIT","{ELEVATOR_OPTION_EXIT}"))
        elif place == "core":
            frags["_BUTTONSET"] = "{ELEVATOR_BUTTONSET_CORE}"
            frags["_DESC"] = "{ELEVATOR_DESC_CORRIDOR}"
            choices = (("DOWN", "{ELEVATOR_OPTION_DOWN}"), ("CARGO","{ELEVATOR_OPTION_CARGO}"), ("EXIT","{ELEVATOR_OPTION_EXIT}"))
        else:
            frags["_BUTTONSET"] = "{ELEVATOR_BUTTONSET_MID}"
            frags["_DESC"] = "{ELEVATOR_DESC_CORRIDOR}"
            choices = (("UP", "{ELEVATOR_OPTION_UP}"), ("DOWN", "{ELEVATOR_OPTION_DOWN}"), ("CARGO","{ELEVATOR_OPTION_CARGO}"), ("EXIT","{ELEVATOR_OPTION_EXIT}"))
        game.rolltext("{ELEVATOR_DESC}", frags=frags)
        
        while True:
            game.choose(choices, "{ELEVATOR_QUEST}")
            data = game.wait()
            if not data or data.Type != "action":
                continue
            if data.tag == "EXIT":
                game.showtext("{ELEVATOR_EXIT}")
                break
            elif game.getdata("WheelC_elevator") == "dead":
                game.rolltext("{ELEVATOR_PRESS_DEAD}")
                
            game.setdata("WheelC_elevator", "dead")
            if   data.tag == "UP":
                game.rolltext("{ELEVATOR_OPTION_UP}")
            elif data.tag == "DOWN":
                game.rolltext("{ELEVATOR_OPTION_DOWN}")
            elif data.tag == "CARGO":
                game.rolltext("{ELEVATOR_OPTION_CARGO}")
    return content
#endregion elevator

def LadderAccess(game:Game.Game, goto:callable):
    frags = {}
    frags["_PLACENAME"] = {
        "middle" : "{MIDDLE_NAME_LADDER}",
        "inner"  : "{INNER_NAME_LADDER}",
        "outer"  : "{OUTER_NAME_LADDER}",
        "core"   : "{CORE_NAME_LADDER}"
    }[game.place]
    varname = {
        "middle" : "WheelCMiddleLadder",
        "inner"  : "WheelCInnerLadder",
        "outer"  : "WheelCOuterLadder",
        "core"   : "WheelCCoreLadder"
    }
    def content():
        if not game.getdata("reactorC:fixed", False) and not game.getCounter(game, "reactorC")[0]: #if counter reactorC is not enabled
            game.setCounter(game, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.
        text = "{LADDER_ACCESS_INTRO}"
        knowledge = game.getdata("wheelC:knowledge", 0)
        if knowledge < 1:
            knowledge = 1
        game.setdata("wheelC:knowledge", knowledge)
        if game.getdata(varname) == "open":
            frags["_INTROPART"] = "{LADDER_ACCESS_INTRO_2}"
            enterText = "{LADDER_ACCESS_ENTERQUEST_1}"
            openText = "{LADDER_ACCESS_ENTER_1}"
        else:
            frags["_INTROPART"] = "{LADDER_ACCESS_INTRO_3}"
            enterText = "{LADDER_ACCESS_ENTER_2}"
            openText = "{LADDER_ACCESS_ENTERQUEST_1}"
        game.rolltext(text, frags=frags)
        if(game.yesno(openText)):
            if game.getdata(varname) == None:
                game.setdata(varname, "open")
            game.rolltext(enterText)
            goto("ladder")
    return content

class Runner_WheelC_Rings(Game.PlaceRunner1D):
    def __init__(self, game:Game.Game, passActs:list=[]):
        super().__init__(game, 'x', 'left', 'right')
        self.passActs = passActs
    def onTravel(self, previndex:int):
        if previndex == self.index:
            print("Null travel error ? ignoring")
        pNodeID = self.nodes[previndex].id
        nNodeID = self.nodes[self.index].id
        for p in self.passActs:
            if (p[0], p[1]) == (pNodeID, nNodeID):
                try:
                    p[2]()
                except:
                    pass
    def runaction(self, action):
        status = self.game.updateCounter("reactorC", -1)
        if status == "death":
            self.running = False
            return
        super().runaction(action)
