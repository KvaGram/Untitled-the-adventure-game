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
def auxcom_cargo(game):
    localfrags = {}
    T = Game.Gettexter(game)
    #Note: Whatever the dialoge, it is up to the player what to do afterwards.
    asshole = game.getdata("auxcom:asshole", False)
    reactorFixed = game.getdata("reactorC:fixed", False)
    prevcontact = game.getdata("auxcom:cargo", False)
    thankedForReactor = game.getdata("auxcom:react_thanks", False)
    
    key = game.getdata("auxcom:stasispasskey", False)
    # Only change is the information they are given.
    # From here, or the ladder if the player skips this, a counter is enabled that gives the player 10 'time units' before game over.
    if not reactorFixed and game.getCounter(game, "reactorC")[0]: #counter not enabled
        game.setCounter(game, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.

    name = game.getName(game)
    gender = game.getGender(game)
    klara =  game.getKlara(game)

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
                ("CODE", "What was that code again?"),
                ("TRUTH","Exacly what happened?"),
                ("EXIT", "Not right now. Bye.")
            )
            while True:
                _, c = game.choose2(choices, "How do you respond?", "<<{2}")
                if c=="EXIT":
                    game.showtext("Ok then. Hope to see you here soon.")
                    break
                elif c=="CODE":
                    game.rolltext("""
As we said earlier, the code is 0-0-0-0-0.
Again, please don't mock us for not changing the factory settings.
                    """)
                elif c=="TRUTH":
                    game.rolltext("""
Well, that's the thing. We are still investigating.
What we know so far is that there was a glitch in the nav system.
We don't know how that happend, nor why nobody noticed.
Well, this glitch caused us to pass though an asteroidbelt.
We don't know how that happened, nor why nobody noticed.
Well, this glitch caused us to pass through an asteroidbelt.

Our fine pilots got us through the worst. The ship may not be very manuverable,
but there are still kilometers between the rocks, so at least we had a good chance.
But alas we hit one of the smaller rocks that we somehow missed on our LIDAR.
                    """)
                    choices2 = ("Ask for short version", "Continue listening to the entire tale")
                    c2 = game.choose2(choices2, "Interrupt?")
                    if c2 == 0:
                        game.rolltext("""
Um.. sorry? Well, you asked.
Ok. Short version.
We got hit hard by an asteroid. Might be sabotage, unknown.
We started an orderly evacuation, then the reactor got bad, and the hull breached a few places.
Then we woke everyone we could, and ran for the exit.
Sorry to say, but it seems you got left behind and forgotten in the chaos.
                        """)
                    else:
                        game.rolltext("""
The rock bounced off Wheel C, causing massive damage.
Immidiatly we sent repair-bots out to fix the damage to the reactor-ring.
The reactor ring and accellerator survived the impact, but got bent on a few places.
And you're an engineer, you know what happens if we keep sending tacheons though a bent reactor ring.
As expected, the nearby hull-section tore itself apart.
We lost all C-sections to vacuum in the matter of secunds.
So fixing the reactor ring proved quite urgent.

But the bots can't get over the the damage from the outside while the wheel was spinning,
and the AG-thursters got wrecked in the impact, so we coulden't brake the wheel.
So we thought we could send the bots though the section-doors, but lacking internal airlocks in the sections, we would need to vacuum the wheel first.
So we started evacuating, first by waking people by small groups at a time.

Our reports say you were amung the first to be recovered from stasis, unfortunatly, you remained unconscious.
So you were put in your bed untill you woke up.
We thought we had plenty of time to evacuate everyone in an slow and organized way.

Then the reactor started going bad.
The tacheon feedback from the bent accellerator ring hit earlier than eastimated.
So with fixing the reactor no longer being an option, we have to ditch the entire module. The neck, wheel and core. all of it.
And with that, we accellerated the evacuation.
We activated the emergency wake-up system, though some of the pods in the inner ring glitched out.

The People who did wake stumbled out of sleep en masse, heard the alarm, and started to panic.
It was already getting a bit chaotic, but then sectors 1D and 2D suddenly breached!

The already disorderly evacuation turned into an outright stampede.
Just as we got the last group though of paniced folks though, the doors decided to glitch up.
Then you suddenly contacted us. Good thing you did. We were about to edject the module,
using the internal atmosphere as thurst. You would have been sucked out into space had we done that.

Sorry you got left down there.
But the important thing now is to get you and everyone else stuck in the module out before we blow this thing.
                    """)
                game.showtext("Did you have more questions?")
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
            p = name
        elif gender == "male":
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
            while (True:
                game.choose(choices, "{AUXCOM_DIALOGE_2B_QUEST}")
                data = game.wait()
                if not data or data.Type != "action":
                    continue
                if data.tag == "WHY_ME":
                    game.rolltext("""
{AUXCOM_DIALOGE_2B_WHY}
                    """)
                elif data.tag == "WEAK_CODE":
                    game.rolltext("""
Well.. yeah.. we never expected there to ever be some kind of security issue onboard,
and we kinda still don't, so we never bothered to change the factory settings.
Don't worry about it.
                    """)
                elif data.tag == "EXIT":
                    game.rolltext("Good luck.\n(Call disconnected)")
                    break
            game.setdata("auxcom:stasispasskey", True)
            game.setdata("auxcom:cargo", True)
            game.setdata("auxcom:react_thanks", True)
        
    # If the reactor is not yet fixed:
        game.rolltext("""
Ok. {_P}, I need you to stay calm. I'm gonna get some help
(The woman you were talking leaves)
...
(A man, an engineer by the looks of his attire, takes her place)
Ok, {_P}. I am not gonna lie, you are in a bit of touble. We are gonna do what we can to help you.
You are onboard the UNS Armstrong on route from Sol to Alpha Centauri.
If this seems unfamiliar to you, this may be due stasis-amnesia,
a common condition caused by emergency awakening from stasis.
The reactor onboard is about to explode, so were about to detach the module when you contacted us.

Look {_P}, I need you to find the emergency ladd..
(the man is rudely interrupted by a third person)
Hey! I know you. You're {game.FemaleFam.name}'s {game.FemaleFam.GenderedRolePlayer} right?
You're a engineer, right? Maybe you could try to stabilize the reactor temporarily?
There are still lots of people stuck in stasis in the upper ring!

Look, {game.PlayerName}, I woulden't blame you for just making a run for the ladder to save yourself, but you could save those people!
        """.format(p, game.getGenderedTerm(klara, gender), name))
        choices = [
            ("Screw them! I'm out of here! I'm gonna climb down and get out of here!"), #ignorant idiot option
            ("I.. I am not gonna take that chance. I'm just gonna go meet you up the ladder!"), #reluctant selfishness
            ("Alright, how do I get to the reactor?"),
            ("What exacly happened?")
        ]
        ind, ans = game.choose2(choices, "How do you respond?", "<< {2}")
        if ind == 3:
            game.rolltext("""
I figured you would ask that. We hit an asteroid!
We don't have time to go into details right now!
I need you to either stabilize the reactor so we can save everyone, or get you safely out of there!
            """)
            choices.pop(3)
            ind, ans = game.choose2(choices, "How do you respond?", "<< {2}")
        
        if ind == 0:
            game.rolltext("""
Well, ehm.. that's rude. ..
uh well, sure go DOWN the ladder. Uh, and take your good time too.
Got to go, bye!

(The call has ended)
            """)
            asshole = True
        elif ind == 1:
            game.rolltext("""
I see. Well, the reactor will reach a meltdown in just a few minutes, we need to detach the module before then.
You need to hurry! The escape ladder should be nearby. You need to climb up as fast as you can.
In case you need to pass though a locked security door, the code is 0-0-0-0-0. And, please dont ask.
Again, the code is 0-0-0-0-0!
We will meet you at the airlock in the module core.
Please beware, you will be weightless up here!
See you soon!

(The call has ended)
            """)
            key = True
        elif ind == 2:
            game.rolltext("""
Thanks for doing this!
Ok, there won't be much time, but we will hold off detaching the module as long as we can.
You should find the emergency stairs nearby. You need to climb down to the outermost ring.
The nearest reactor-node will not be far from the ladder.
You need to first initalize the emergency cooling system, then the emergency particle decelerator.
In that order! You will find detailed instructions on how to do this in the reactor-node control room.
Doing this will buy us maybe an hour or two before meltdown.
In case you need to pass though a locked security door, the code is 0-0-0-0-0. And, please dont ask.
Again, the code is 0-0-0-0-0!
You need to hurry! Get back and contact us again once you have done it!

(The call has ended)
            """)
            key = True
    game.setdata("auxcom:asshole", asshole)
    game.setdata("auxcom:stasispasskey", key)
    game.setdata("auxcom:cargo", True)
    game.setdata("auxcom:react_thanks", thankedForReactor)
def elevator(game):
    #region elevator
    room = game.getdata("room")

    coredesc = """The evevator appears as large cyllinder that smoothly sticks out of the inner sphere of the core.
    The walls sloping inwards to give way to the elevator doors. You float your way over to have a closer look."""
    corridesc = """The elevators breaks up the corridor, as the corridor splits to around a large round column you learn is the elevator shaft,
the walls around bending outwards giving way for the path around the shaft until they hit flat outer walls."""
    if room == "outer":
        buttonsets = "up"
    elif room == "core":
        buttonsets = "down"
    else:
        buttonsets = "up, down"
    game.rolltext("""
{0}
You find six elevator doors in pairs of two around the large cylinder.
You also locate a set of call-buttons for {1} and cargo, whatever that last one means.
    """.format(coredesc if room == "core" else corridesc, buttonsets))
    

    
    if room == "middle" or room == "inner":
        choices = (("UP", "Press UP call button"), ("DOWN","Press DOWN call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))
    elif room == "core":
        choices = (("DOWN","Press DOWN call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))
    elif room == "outer":
        choices = (("UP", "Press UP call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))

    _,choice = game.choose2(choices, "Press a button?")
    if choice != "EXIT":
        if(game.getdata("WheelC_elevator") == "dead"):
            text = """
You press the button.
...
Nothing happened.
            """
        else:
            text = """
You press the button.
The button flashes.
...
You hear an odd clang
...         """
            if choice == "CARGO":
                text += "\nTwo of the elevator doors open in a very slight crack."
            else:
                text += "\nOne of the elevator doors open in a very slight crack."
            text += "\nThen you hear a fizzeling sound, and everything stops working"
            game.setdata("WheelC_elevator", "dead")
        game.rolltext(text)
    else:
        game.showtext("You left the elevators alone")
    #endregion elevator