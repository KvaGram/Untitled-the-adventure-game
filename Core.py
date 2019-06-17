import Game
import General

def Core(game:Game.Game):
    T = Game.Gettexter(game)
    #importing elevator from General
    elevator = General.elevator(game)

    frags = {}
    intro = ""
    prevplave = game.prevPlace
    if(prevplave == "ladder"):
        intro = "{CORE_INTRO_1}"
    else:
        intro = "{CORE_INTRO_2}"
    game.rolltext(intro)
    choices = (
        ("WINDOW", T("CORE_OPTION_WINDOW")),
        ("ELEVATOR_SEC_A", T("CORE_OPTION_SEC_A")),
        ("LADDER_SEC_B", T("CORE_OPTION_SEC_B")),
        ("ELEVATOR_SEC_C", T("CORE_OPTION_SEC_C")),
        ("LADDER_SEC_D", T("CORE_OPTION_SEC_D")),
        ("AIRLOCK", T("CORE_OPTION_AIRLOCK")),
    )
    running = True
    while running:
        game.choose(choices, T("CORE_QUEST"))
        data:Game.ActDataInput = game.wait()
        if not data or data.Type != "action":
            continue
        elif data.tag == "WINDOW":
            if game.getdata("core:window", False):
                game.rolltext("{CORE_WINDOW_2}", frags = frags)
            else: #CORE_WINDOW_1
                if(game.getdata("apartment:window")):
                    frags["_WINDOW_PART"] = "{CORE_WINDOW_1_PART_A}"
                else:
                    frags["_WINDOW_PART"] = "{CORE_WINDOW_1_PART_B}"
                game.rolltext("{CORE_WINDOW_1}", frags = frags)
                game.setdata("core:window", True)
        elif data.tag == "ELEVATOR_SEC_A":
            game.rolltext("{CORE_TO_ELE_A}")
            if(game.yesno("{FLOAT_TO_QUEST}")):
                elevator()
        elif data.tag == "ELEVATOR_SEC_C":
            game.rolltext("{CORE_TO_ELE_C}")
            if(game.yesno("{FLOAT_TO_QUEST}")):
                game.rolltext("{CORE_ELE_C}")
        elif data.tag == "LADDER_SEC_B":
            game.rolltext("{CORE_TO_LADDER_B}")
            if(game.yesno("{FLOAT_TO_QUEST}")):
                game.goto("ladder")
                running = False
        elif data.tag == "LADDER_SEC_D":
            game.rolltext("{CORE_TO_LADDER_D}")
            if(game.yesno("{FLOAT_TO_QUEST}")):
                game.rolltext("{CORE_LADDER_D}")
        elif data.tag == "AIRLOCK":
            game.rolltext("{CORE_AIRLOCK_1}")
            if not game.yesno("{CORE_AIRLOCK_1_QUEST}"):
                continue
            game.rolltext("{CORE_AIRLOCK_2}")
            if not game.yesno("{CORE_AIRLOCK_2_QUEST}"):
                game.rolltext("{CORE_AIRLOCK_3B}")
                continue
            game.rolltext("{CORE_AIRLOCK_3A}")
            game.goto("cargobay")
            running = False
            return
            
        status = game.updateCounter("reactorC", -1)
        if status == "death": #if reactor counter reach 0, and the game ends.
            running = False
    #end of loop


def Cargobay(game:Game.Game):
    #TODO: Rewrite needed!
    T = Game.Gettexter(game)
    frags = {}
    reactorFixed = game.getdata("reactorC:fixed", False)
    peopleSaved = game.getdata("stasis:peopleSaved", 0)
    prevcontact = game.getdata("auxcom:cargo", False)

    frags["_NUM_PEOPLE_SAVED"] = str(peopleSaved)

    if prevcontact:
        frags["_P"] = game.PlayerName
    else:
        if game.PlayerGender == "male":
            frags["_P"] = T("GENDERED_1_MALE")
        else:
            frags["_P"] = T("GENDERED_1_FEMALE")

    if prevcontact:
        frags["_INTRO_PART"] = "{CARGOBAY_INTRO_PART_A}"
        if(peopleSaved > 120):
            frags["_REACTION"] = "{CARGOBAY_REACTION_B}"
            frags["_FOLLOWUP"] = "{CARGOBAY_FOLLOWUP_A}"
            frags["_END"]      = "{CARGOBAY_ENDING_C}"
        elif(peopleSaved > 0):
            frags["_REACTION"] = "{CARGOBAY_REACTION_A}"
            frags["_FOLLOWUP"] = "{CARGOBAY_FOLLOWUP_A}"
            frags["_END"]      = "{CARGOBAY_ENDING_B}"
        elif(reactorFixed):
            frags["_REACTION"] = "{CARGOBAY_REACTION_C}"
            frags["_FOLLOWUP"] = "{CARGOBAY_FOLLOWUP_B}"
            frags["_END"]      = "{CARGOBAY_ENDING_A}"
        else:
            frags["_REACTION"] = "{CARGOBAY_REACTION_D}"
            frags["_FOLLOWUP"] = "{CARGOBAY_FOLLOWUP_B}"
            frags["_END"]      = "{CARGOBAY_ENDING_A}"
    else:
        frags["_INTRO_PART"] = "{CARGOBAY_INTRO_PART_B}"
        frags["_REACTION"] = "{CARGOBAY_REACTION_D}"
        frags["_FOLLOWUP"] = "{CARGOBAY_FOLLOWUP_B}"
        frags["_END"]      = "{CARGOBAY_ENDING_D}"
    game.rolltext("{CARGOBAY_ENDING}", frags = frags)
    game.setGameover("End of the story, so far!")

if __name__ == "__main__":
    #testers, feel free to enter your testcode here.
    #if your only change is in this code-block, feel free to commit.
    print("Testcode for this room is not written yet.\nPlease run from main.py instead.")