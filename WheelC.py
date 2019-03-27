import game_utilities as game

#The Ladder
def emergencyLadder(save):
    class ladderNAV(game.RoomNav1D):
        def __init__(self):
            super().__init__(termPlus= "GO DOWN", termMinus= "GO UP")
        #Override
        def runAction(self):
            act,_,_ = self.getPlace()
            #note: ticks the reactorC counter if enabled.
            status = game.updateCounter(save, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                self.running = False
            else:
                act()
        def plus(self):
            game.rolltext("You climb upwards, feeling yourself getting a bit lighter")
            self.ind += 1
        def minus(self):
            game.rolltext("You climb down, feeling a slight stronger pull downwards")
            self.ind -= 1
    nav = ladderNAV()
    def core():
#        game.rolltext("""
#You open the hatch, and beholds the spinning room.
#In the light gravity you push off upwards into the core.
#        """)
        goto("core")
    def inner():
        #goto("inner")
        game.showtext(" - Sorry, this section is not written yet. - ")
    def middle():
        goto("middle")
    def outer():
        goto("outer")

    

    #((sectionDdoor, "Section D door", "examine")) 
    nav.places = (
        (core, "The core", "Exit to the Core"),
        (inner, "inner ring", "Exit into the inner ring" ),
        (middle, "middle ring", "Exit into the middle ring" ),
        (outer, "outer ring", "Exit into the outer ring" )
    )
    def goto(room):
        nav.running = False
        save.goto(room)

    nav.loop()
    


#barebones placeholder for chapter 1: Wheel C

def ladder(save):
    game.showtext("Welcome to placeholder for the ladder. Choose where to go from here:")
    choice = game.choose(["Climb to CORE", "Climb to inner ring", "climb to middle ring", "climb to outer ring"])
    if(choice == 0):
        return save.goto("core")
    if(choice == 1):
        return save.goto("innerB")
    if(choice == 2):
        return save.goto("middle")
    if(choice == 3):
        return save.goto("outer")

def core(save):
    game.showtext("welcome to the placeholder for the core. Where do you wish to go from here?")
    choice = game.choose(["Airlock", "Ladder"])
    if(choice == 0):
        return save.goto("Airlock")
    if(choice == 1):
        return save.goto("ladder")

def innerA(save):
    game.showtext("Welcome to the placeholder for inner ring sector A. Where do you wish to go?")
    choice = game.choose(["Inner B"])
    if (choice == 0):
        return save.goto("innerB")

def innerB(save):
    game.showtext("Welcome to the placeholder for inner ring sector B. Where do you wish to go?")
    choice = game.choose(["Ladder", "Inner A"])
    if(choice == 0):
        return save.goto("ladder")
    if (choice == 1):
        return save.goto("innerA")

def outerB(save):
    game.showtext("Welcome to the placeholder for middle ring sector B. Where do you wish to go?")
    choice = game.choose(["Ladder", "Inner A"])
    if(choice == 0):
        return save.goto("ladder")
    if (choice == 1):
        return save.goto("outerA")

def wheelCAirlock(save):
    game.showtext("Welcome to end of chapter 1")
    save.setdata("GAME OVER", "End of the story, so far!")

if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    game.showtext("Testcode for this room is not written yet.\nPlease run from main.py instead.")