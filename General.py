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

class Runner_WheelC_Rings(Game.PlaceRunner1D):
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