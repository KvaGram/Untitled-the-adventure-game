import Game
import General

#The Ladder
class LadderRunner(Game.PlaceRunner1D):
    def __init__(self, game:Game.Game):
        super().__init__(game, 'y', 'up', 'down')
    def onTravel(self, previndex:int):
        if previndex == self.index:
            print("Null travel error ? ignoring")
        if previndex > self.index:
            self.game.showtext("{LADDER_GO_DOWN}")
        if previndex < self.index:
            self.game.showtext("{LADDER_GO_UP}")
        #check for section passage
    def runaction(self, action):
        status = self.game.updateCounter("reactorC", -1)
        if status == "death":
            self.running = False
            return
        super().runaction(action)
def Start(game:Game.Game):
    T = Game.Gettexter(game)
    runner = LadderRunner(game)

    def goto(place):
        runner.stop()
        game.place = place

    def core():
        game.showtext("{LADDER_TO_CORE}")
        goto("core")
    def inner():
        game.showtext("{LADDER_TO_INNER}")
        goto("inner")
    def middle():
        game.showtext("{LADDER_TO_MID}")
        goto("middle")
    def outer():
        game.showtext("{LADDER_TO_OUT}")
        goto("outer")

    def setupRunner():
        base_navtext = T("NAV_DESC_TEMPLATE")
        frags = {"_WHEEL" : "Habitat wheel C", "_SECTORNAME" : "Sector B"}
        runner.nodes = [
            Game.PlaceNode(game, "TO_CORE",    game.retext(base_navtext, {**frags, "_RINGNAME":"Core", "_LOCAL_NAME":"Exit to core"}),[
                ("_", T("LADDER_CORE_QUEST"), core),
            ]),
            Game.PlaceNode(game, "TO_INNER",    game.retext(base_navtext, {**frags, "_RINGNAME":"Inner ring", "_LOCAL_NAME":"Exit to inner ring"}),[
                ("_", T("LADDER_INNER_QUEST"), inner),
            ]),
            Game.PlaceNode(game, "TO_MID",    game.retext(base_navtext, {**frags, "_RINGNAME":"Middle ring", "_LOCAL_NAME":"Exit to middle ring"}),[
                ("_", T("LADDER_MID_QUEST"), middle),
            ]),
            Game.PlaceNode(game, "TO_OUT",    game.retext(base_navtext, {**frags, "_RINGNAME":"Outer ring", "_LOCAL_NAME":"Exit to outer ring"}),[
                ("_", T("LADDER_OUT_QUEST"), outer),
            ]),
        ]
    setupRunner()
    runner.index =  (
        {
            "core":"TO_CORE",
            "inner":"TO_INNER",
            "middle":"TO_MID",
            "outer":"TO_OUT",
        }.get(game.prevPlace, 0))
    runner.run()


