#TODO: split or rename
#dialoges
#for long dialoges or nerratives that take up much space in a module, or that could be called from multible places.
#import game_utilities as game

import Game

def auxcom_contact(game):
    T = Game.Gettexter(game)
    #region auxcom
    cargoConnected = game.getdata("auxcom:cargo", False)
    if cargoConnected:
        return auxcom_cargo(game)
    game.rolltext("{AUXCOM2_INTRO}")
    choices = [
        ("BRIDGE", T("AUXCOM2_COMOP_1")),
        ("ENGINEERING", T("AUXCOM2_COMOP_2")),
        ("RADIATION SHELTER 1", T("AUXCOM2_COMOP_3")),
        ("RADIATION SHELTER 2", T("AUXCOM2_COMOP_4")),
        ("RADIATION SHELTER 3", T("AUXCOM2_COMOP_5")),
        ("RADIATION SHELTER 4", T("AUXCOM2_COMOP_6")),
        ("WHEEL A AUXCOM", T("AUXCOM2_COMOP_7")),
        ("WHEEL B AUXCOM", T("AUXCOM2_COMOP_8")),
        ("WHEEL D AUXCOM", T("AUXCOM2_COMOP_9")),
        ("CARGO", T("AUXCOM2_COMOP_CARGO")),
        ("EXIT", T("AUXCOM2_COMOP_EXIT")),
    ]
    
    responsekey = {
        "BRIDGE" : "{AUXCOM2_NO_RESP_1}",
        "ENGINEERING" : "{AUXCOM2_NO_RESP_1}",
        "RADIATION SHELTER 1" : "{AUXCOM2_NO_RESP_1}",
        "RADIATION SHELTER 2" : "{AUXCOM2_NO_RESP_1}",
        "RADIATION SHELTER 3" : "{AUXCOM2_NO_RESP_1}",
        "RADIATION SHELTER 4" : "{AUXCOM2_NO_RESP_1}",
        "WHEEL A AUXCOM" : "{AUXCOM2_NO_RESP_1}",
        "WHEEL B AUXCOM" : "{AUXCOM2_NO_RESP_1}",
        "WHEEL D AUXCOM" : "{AUXCOM2_NO_RESP_1}",
        "CARGO" :   "{AUXCOM2_RESP_CARGO}",
        "EXIT"  :   "{AUXCOM2_RESP_EXIT}"
    }
    duds = (
        "BRIDGE",
        "ENGINEERING",
        "RADIATION SHELTER 1",
        "RADIATION SHELTER 2",
        "RADIATION SHELTER 3",
        "RADIATION SHELTER 4",
        "WHEEL A AUXCOM",
        "WHEEL B AUXCOM",
        "WHEEL D AUXCOM",
    )
    while(True):
        game.choose(choices, "{AUXCOM2_CONTACTQUEST}")
        data:Game.ActDataInput = game.wait()
        tag = data.tag
        if(data.Type != "action"):
            continue
        game.rolltext(responsekey.get(tag, "..."))
        if tag == "EXIT":
            break
        elif tag in duds:
            choices.pop(tag)
        elif tag == "CARGO":
            return auxcom_cargo(game)
    #endregion auxcom2
def auxcom_cargo(game:Game.Game):
    localfrags = {}
    T = Game.Gettexter(game)
    #Note: Whatever the dialoge, it is up to the player what to do afterwards.
    asshole = game.getInventory("ASSHOLE") #if player has a reputation for being an ass.
    reactorFixed = game.getdata("reactorC:fixed", False)
    prevcontact = game.getdata("auxcom:cargo", False)
    thankedForReactor = game.getdata("auxcom:react_thanks", False)
    # Only change is the information they are given.
    # From here, or the ladder if the player skips this, a counter is enabled that gives the player 10 'time units' before game over.
    if not reactorFixed and game.getCounter(game, "reactorC")[0]: #counter not enabled
        game.setCounter(game, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.

    if prevcontact:
        #TODO: alternate contact for returning to auxcom
        if asshole:
            game.rolltext("{AUXCOM3_INTRO_ASS}")
        elif reactorFixed:
            if not thankedForReactor:
                game.rolltext("{AUXCOM3_INTRO_THANKS}")
            else:
                game.rolltext("{AUXCOM3_INTRO_RETURN}")
            choices = (
                ("CODE", T("AUXCOM_DIALOGE_3_OPTION_CODE")),
                ("TRUTH",T("AUXCOM_DIALOGE_3_OPTION_TRUTH")),
                ("EXIT", T("AUXCOM_DIALOGE_3_OPTION_EXIT"))
            )
            while True:
                game.choose(T("AUXCOM_DIALOGE_3_QUEST"))
                data = game.wait()
                if not data or data.Type != "action":
                    continue
                elif data.tag =="CODE":
                    game.rolltext("{AUXCOM_DIALOGE_3_CODE}")
                elif data.tag =="TRUTH":
                    game.rolltext("{AUXCOM_DIALOGE_3_TRUTH}")
                    if game.yesno(T("AUXCOM_DIALOGE_3_INTERRUPT_QUEST")):
                        game.rolltext("{AUXCOM_DIALOGE_3_SHORT_STORY}")
                    else:
                        game.rolltext("{AUXCOM_DIALOGE_3_FULL_STORY}")
                elif data.tag =="EXIT":
                    game.showtext("{AUXCOM_DIALOGE_3_EXIT}")
                    break
        else:
            game.rolltext("{AUXCOM3_INTRO_PLZFIX}")
    else:
        game.showtext("{AUXCOM_CONTACT_MADE}")
        choices = [
            ("", T("AUXCOM_DIALOGE_1_OPTION_1")),
            ("", T("AUXCOM_DIALOGE_1_OPTION_2")),
            ("", T("AUXCOM_DIALOGE_1_OPTION_3")),
            ("", T("AUXCOM_DIALOGE_1_OPTION_4")),
        ]
        while True:
            game.choose(choices, T("AUXCOM_DIALOGE_1_QUEST"))
            data = game.wait()
            if data:
                if data.Type != "action":
                    continue
                ind = data.index
                break
        #game.showtext(">> "+choices[ind][1])
        if ind == 0 or ind == 3:
            p = game.PlayerName
        elif game.PlayerGender == "male":
            p = T("GENDERED_1_MALE")
        else:
            p = T("GENDERED_1_FEMALE")
        localfrags['_P'] = p
        if(reactorFixed):
            game.rolltext("{AUXCOM_DIALOGE_1B_REACTOR_QUEST}",frags=localfrags)
            admitfix = game.yesno(T("QWASIT"))
            localfrags['_REACT_1'] = ""
            localfrags['_REACT_2'] = ""
            if(admitfix):
                localfrags['_REACT_1'] = "{AUXCOM_DIALOGE_1B_PART_1A}"
                localfrags['_REACT_2'] = "{AUXCOM_DIALOGE_1B_PART_2A}"
            else:
                localfrags['_REACT_1'] =  "{AUXCOM_DIALOGE_1B_PART_1B}"
                localfrags['_REACT_2'] = "{AUXCOM_DIALOGE_1B_PART_2B}"
            game.rolltext("{AUXCOM_DIALOGE_1B}")
            choices = (
                ("WHY_ME", T("AUXCOM_DIALOGE_2B_OPTION_1")),
                ("WEAK_CODE", T("AUXCOM_DIALOGE_2B_OPTION_2")),
                ("EXIT", T("AUXCOM_DIALOGE_2B_OPTION_3"))
                )
            while True:
                game.choose(choices, "{AUXCOM_DIALOGE_2B_QUEST}")
                data = game.wait()
                if not data or data.Type != "action":
                    continue
                if data.tag == "WHY_ME":
                    game.rolltext("{AUXCOM_DIALOGE_2B_WHY}")
                elif data.tag == "WEAK_CODE":
                    game.rolltext("{AUXCOM_DIALOGE_2B_CODE}")
                elif data.tag == "EXIT":
                    game.rolltext("{AUXCOM_DIALOGE_2B_EXIT}")
                    break
            game.setdata("auxcom:stasispasskey", True)
            game.setdata("auxcom:cargo", True)
            game.setdata("auxcom:react_thanks", True)
        
    # If the reactor is not yet fixed:
        game.rolltext("{AUXCOM_DIALOGE_1A}")
        choices = [
            ("SCREWIT", T("AUXCOM_DIALOGE_2A_OPTION_1")), #Asshole option! Locks up all future dialoge
            ("NO", T("AUXCOM_DIALOGE_2A_OPTION_2")),
            ("YES", T("AUXCOM_DIALOGE_2A_OPTION_3")),
            ("WUT", T("AUXCOM_DIALOGE_2A_OPTION_4"))
        ]
        while True:
            game.choose(choices, T("AUXCOM_DIALOGE_2A_QUEST"))
            data = game.wait()
            if not data or data.Type != "action":
                continue
            elif data.tag == "SCREWIT":
                asshole = True
                game.setInventory("ASSHOLE", True)
                game.rolltext("{AUXCOM_DIALOGE_2A_SCREWIT}")
                break
            elif data.tag == "NO":
                game.rolltext("{AUXCOM_DIALOGE_2A_NO}")
                game.setInventory("KEYCODE", True)
                break
            elif data.tag == "YES":
                game.rolltext("{AUXCOM_DIALOGE_2A_YES}")
                game.setInventory("KEYCODE", True)
                break
            elif data.tag == "WUT":
                game.rolltext("{AUXCOM_DIALOGE_2A_WUT}")
                choices.pop(3)
                continue
    game.setdata("auxcom:cargo", True)
    game.setdata("auxcom:react_thanks", thankedForReactor)
def elevator(game:Game.Game):
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
    #endregion elevator