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
        r0 = 0
        from untitled_const import NAV_INNER_RADIUS as r1
        from untitled_const import NAV_MIDDLE_RADIUS as r2
        from untitled_const import NAV_OUTER_RADIUS as r3
        from untitled_const import TAU
        rot = 6/16 * TAU
        runner.nodes = [
            Game.PlaceNode(game, "TO_CORE",T("AREANAME_TO-CORE"), r0, rot ,[
                ("_", T("LADDER_CORE_QUEST"), core),
            ]),
            Game.PlaceNode(game, "TO_INNER",T("AREANAME_TO-INNER"), r1, rot ,[
                ("_", T("LADDER_INNER_QUEST"), inner),
            ]),
            Game.PlaceNode(game, "TO_MID",T("AREANAME_TO-MIDDLE"), r2, rot ,[
                ("_", T("LADDER_MID_QUEST"), middle),
            ]),
            Game.PlaceNode(game, "TO_OUT",T("AREANAME_TO-OUTER"), r3, rot ,[
                ("_", T("LADDER_OUT_QUEST"), outer),
            ]),
        ]
    game.rollArt("ladderart", 0.05)
    setupRunner()
    runner.index =  (
        {
            "core":"TO_CORE",
            "inner":"TO_INNER",
            "middle":"TO_MID",
            "outer":"TO_OUT",
        }.get(game.prevPlace, 0))
        
    runner.run()


