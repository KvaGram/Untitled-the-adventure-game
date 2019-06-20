import Game
import random
import General
from General import Runner_WheelC_Rings as Runner

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

    
    #OLD CODE, to be rewritten

    nav = outerRoomNAV.GET_NAV(save)
    #---------------------------
    #region actions and places
    def sectionDdoor():
        game.rolltext("""{OUTER_SEC_D_DOOR}""")
    def sectionBdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionAdoor_pass():
        game.showtext("{PASS_SECTOR_DOORWAY}")
    def sectionBdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionAdoor_read():
        game.showtext("PLACEHOLDER")
    def sectionCdoor():
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
                game.rolltext("{REACTORNODE_3A}")
                break
            elif data.tag == "RANDOM":
                game.rolltext("{REACTORNODE_3B}")
                game.setGameover("{REACTORNODE_3B_GAMEOVER}")
                runner.stop()
                return
            elif data.tag == "ESCAPE":
                game.rolltext("{REACTORNODE_ESCAPE}")
                game.setGameover("{REACTORNODE_ESCAPE_GAMEOVER}")
                runner.stop()
                return
        if hasTrans:
            game.rolltext("{REACTORNODE_4A}")
            options5List = T("REACTORNODE_5A_OPTION_LIST").split()
        else:
            game.rolltext("{REACTORNODE_4B}")
            options5List = T("REACTORNODE_5B_OPTION_LIST").split()
        options5 = Game.OptionList([
            ["COOLDOWN" ,options5List[0]],
            ["SLOWDOWN" ,options5List[1]],
            ["HURRY"    ,options5List[2]],
            ["FIRE_1"   ,options5List[3]],
            ["FIRE_2"   ,options5List[4]],
            ["INFO"     ,options5List[5]],
            ["DEATH"    ,options5List[6]],
            ["REVERSE"  ,options5List[7]],
            ["SHUTDOWN" ,options5List[8]],
            ["ESCAPE"   ,options5List[9]],
        ])
        options5.Randomize()
        options5.MoveItemBack("ESCAPE")
        while True:
            game.choose(options5, "{REACTORNODE_5_QUEST}")
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            if data.tag == "ESCAPE":
                game.rolltext("{REACTORNODE_ESCAPE}")
                game.setGameover("{REACTORNODE_ESCAPE_GAMEOVER}")
                runner.stop()
                return
            


        #You need to first initalize the emergency cooling system, then the emergency particle decelerator.
        choices = [
            ("COOL DOWN", "Initiate Emergency cooling system"),
            ("SLOW DOWN", "Engage emergency particle decelerator"),
            ("HURRY UP", "Engage emergency particle accelerator"),
            ("FIRE SUP 1", "Engage accellerator fire suppression system"),
            ("FIRE SUP 2", "Engage control room fire suppression system"),
            ("INFO", "Run automatic diagnostics"),
            ("INSTADEATH", "Engage emergency overload"),
            ("REVERSE", "Depolorize the tacheon emitter"),
            ("SHUTDOWN", "Shutdown tacheon emitter array")
            ]
        random.shuffle(choices)
        cooledDown = False # must be done first
        slowedDown = False # will cause a fire if done before cooldown
        #fireSuppressed_1 = False # will have no effect if there are no fire ### unused ###
        warnedOfLoops = False #unlocks with the INFO option, enables some alternate text.
        #depolorized = False #unlocks with the reversed option, it adds more time loops. ### unused ###

        fixing_reactor_loop = True

        while fixing_reactor_loop:
            ind, val = game.choose2(choices, "What procedure will you attept?" )
            if val == "SHUTDOWN":
                game.rolltext("""
You followed the instructions to shut down the the tacheon emitter array.
...
The system register succesful, then not successful shutdown, then both at the same time.
                """)
                if warnedOfLoops:
                    game.rolltext("""
It took you a moment to see it, but you now realized why this is.
Looking over the diagnatic data you retrived earlier,
you see most of the emitters are stuck in time-loops.
They are running perpetually.
Trying to just shutting them down just won't work.
                    """)
                else:
                    game.rolltext("""
You are completly baffled at what this. You ended the shutdown process.
You decide to try something else.
                    """)
                choices.pop(ind)
            elif val == "REVERSE":
                game.rolltext("""
You followed the instructions to depolarize the tacheon emitters, whatever that means.
Shortly after doing so, you noticed something quite off.
A hole just appeared in the side of the wall, then seemed to reassamle into a wall again before suddenly turning back into a hole, and repeated.
Whatever you just did, you are pretty sure you just made it all worse.
You decided not to try that again.
                """)
                #depolorized = True
                choices.pop(ind)
            elif val == "INSTADEATH":
                nav.running = False
                fixing_reactor_loop = False
                game.setGameover(game, "You found a way to blow youself up. You are very VERY dead!")
                game.rolltext("""
You followed the instructions for initiating an emergency overload.
Right after pressing the confirm key on the screen, you got an odd feeling.
The reactor started humming. Did you just make a huge mis..
...
You never got to finish that thought. You just ceased to exist.
To say you were atomized is not entierly accurate,
but that may be the closest terminology to describe what happened to you.
At least, there were no pain.
                """)
                return
            elif val == "FIRE SUP 2":
                game.rolltext("""
You followed the quite simple instruction, and...
the entire room just got sprayed by a dense foam, convering every surface.
yuck.
If there acually was a fire, you are convinved the fire would be gone by now.
But there was no fire. 'Why did I do this?' you think to yourself while trying to get foam out of your hair.
                """)
                choices.pop(ind)
            elif val == "FIRE SUP 1":
                if slowedDown:
                    game.rolltext("""
You followed the quite simple instruction,
The fire in the accellerator ring went out.
Unfortunatly this also made the accellerater accellerate back up.
                """)
                else:
                    slowedDown = False
                    game.rolltext("""
You followed the quite simple instruction,
Nothing seems to have happened.
                """)
            elif val == "HURRY UP":
                nav.running = False
                fixing_reactor_loop = False
                game.setGameover(save, "You got yourself trapped in a timeloop")
                game.rolltext("""
The instructions for accellerating the accellerator were quite easy to follow.
you just adjusted that sqiggly thing, increased that varible,
pressed that confirm button, changed that dial, adjusted that sqiggly thing,
increased that varia.. wait.. wha
you adjusted that sqiggly thing, incr..
you just had a sudden feeling of déjà vu, as you again adjusted that sqiggly thing.

uh no, you realize, as you got your thinking stright again.
you try to undo what you did when.. you followed instructions to adjust that sqiggly thi..

'shit' you managed to think as you suddenly find yourself adjusting that squigg..
and again.. at shorter and shorter intervals.

The after looping for what seemed like forever, with the intervals going shorter and shorter, they suddenly stopped getting shorter.
From what you could tell, with the little self awareness you could muster, the intervals were at about 1 secund.
And you soon realied why.

Aside from your little looping bobble, everything was gone.
You aren't dead. Not really. But by now, you wish you were.
                """)
                return
            elif val == "SLOW DOWN":
                if slowedDown:
                    game.rolltext("""
As you were about to start following the instructions,
you realized you have already done this. There is no need to do it again.
                    """)
                elif not cooledDown:
                    game.rolltext("""
You followed the instructions to decelerate the accellerator.
...
It seems to work, for a while. Then suddenly a new alarm starts bleeping.
Fire. There is a fire in the accellerator now.
                    """)
                    
                else:
                    game.rolltext("""
You typed in the final instructions for decellerating the system.
...
You check the readouts, and several alarms stops beeping.
The reactor is no longer critical, but that might change.
                    """)
                    fixing_reactor_loop = False #Fixed the reactor
                slowedDown = True
            elif val == "COOL DOWN":
                if cooledDown:
                    game.rolltext("""
As you were about to start following the instructions,
you realized you have already done this. There is no need to do it again.
                    """)
                elif slowedDown:
                    game.rolltext("""
{REACTORNODE_COOLDOWN_2_A}
                    """)
                else:
                    game.rolltext("""
{REACTORNODE_COOLDOWN_1_A}
                    """)
                    cooledDown = True
            elif val == "INFO":
                textFlow =""
                textTemp="SAFE" if cooledDown else "VERY HIGH!" if slowedDown else "HIGH!"
                textFireAlert=""
                if slowedDown:
                    for _ in range(random.randint(3, 10)):
                        textFireAlert += "\n\tALERT: FIRE DETECTED IN REACTOR SUBSEGMENT {0}{1}".format(random.choice(("A", "B", "C", "D")), random.randint(1,12))
                textFirsttime="" if warnedOfLoops else """
It did not take long for you to realize that the 'human operator' is you.
This might explain the anomolies.
You should be extra careful of what you do here.
                """
                game.rolltext("""
You followed the instructions to initiate a diognastic of the reactor.
...
    STATUS: CRITICAL
    TACHEON EMITTERS: ONLINE
    TACHEON FLOW: {0} ((IRREGULAR))
    TEMPERATURE: {1} ((HIGH!))
    STRUCTURE INTEGRETY: COMPROMISED!
    TEMPERAL INTEGRETY: COMPROMISED!

    {2}
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT A06 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT A12 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B04 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B08 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT B12 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C01 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C02 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C06 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C09 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT C11 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D01 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D02 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D03 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D04 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D07 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D08 - POTENTIAL TACHEON LEAK
    ALERT: UNCONTROLLED TIME LOOP EVENT(S) DETECTED AT SUBSEGMENT D09 - POTENTIAL TACHEON LEAK

    WARNING: REACTOR BREACH(ES) DETECTED!
    WARNING: MELTDOWN IMMINENT!
    WARNING: HUMAN OPERATOR DETECTED IN COMPROMIZED SUBSECTION B04! EVACUATION IS ADVICED!

{3}
                """.format(textFlow, textTemp, textFireAlert, textFirsttime)) #Lots TODO here...
                warnedOfLoops = True
        #end of loop
        if cooledDown and slowedDown:
            game.endCounter(save, "reactorC")
            save.setdata("reactorC:fixed", True)
        game.rolltext("""
Leaving the room, you fuss over your hand. You are slowly regaining feeling in it.
Suddenly you notice something.. someone in front of you.
You look up at the stranger.
It took you a bit by surprise, but then you remembered what happened when you first came in.
And as before, the other person suddenly disappeared.
You leave the room content you have done what you could to fix it up.""")


    #endregion actions and places
    #---------------------------
    def goto(room):
        nav.running = False
        save.goto(room)

    def initNav():
        sectionA.append((sectionDdoor, "Section D door", "examine"))        #A 0
        sectionA.append((elevator, "Elevator C3A", "use"))                  #A 1
        sectionA.append((sectionBdoor, "Section B door", "enter"))          #A 2

        sectionB.append((sectionAdoor, "Section A door", "enter"))          #B 0
        #sectionB.append((auxcom, "Auxillary communications", "use"))       #(removed)
        sectionB.append((ladder, "Emergency escape ladder hatch", "open"))  #B 1 (entry and exit to and from other rings in the wheel)
        sectionB.append((reactNode, "Reactor-ring access node", "enter"))   #B 2
        sectionB.append((sectionCdoor, "Section C", "examine"))             #B 3

        prevroom = save.getdata("prevroom")
        if prevroom == "ladder":
            nav.setSection("B", 1)
            intro = """
You close the emergency ladder's hatch.
You are now at the outer level ring.
            """
        else:
            nav.setSection("A", 0)
            intro = """
You have walked around aimlessly for a bit, you don't know for how long
And oof! You just walked streight into a large closed door.
            """
        game.rolltext(intro, 0.3)
    if not nav.running:
        initNav()
    nav.loop(save)
    
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
        if game.yesno(message="ADD KEYCODE?"):
            game.setInventory("KEYCODE", True)
    _testloop(game, Start, testdata, "OUTER RING")