import game_utilities as game

#The Ladder
def emergencyLadder(save):
    pass


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

#placeholder finally obsolete!
def middleA(save):
    game.showtext("Welcome to the placeholder for middle ring sector A. Where do you wish to go?")
    choice = game.choose(["Inner B", "my room"])
    if (choice == 0):
        return save.goto("middleB")
    elif (choice == 1):
        return save.goto("apartment")

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