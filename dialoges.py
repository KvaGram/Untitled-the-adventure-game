#dialoges
#for long dialoges or nerratives that take up much space in a module, or that could be called from multible places.
import game_utilities as game

def auxcom_contact(save):
    #region auxcom
    cargoConnected = save.getdata("auxcom:cargo", False)
    if cargoConnected:
        return auxcom_cargo(save)
    text = """
A list of communication nodes show up on the screen.
Some of them with an error-message saying they are offline
    """
    choices = [
        ("BRIDGE", "Connect to main bridge com system"),
        ("ENGINEERING", "Connect to main engineering"),
        ("RADIATION SHELTER 1", "Connect to radiation shelter One"),
        ("RADIATION SHELTER 2", "Connect to radiation shelter Two"),
        ("RADIATION SHELTER 3", "Connect to radiation shelter Three"),
        ("RADIATION SHELTER 4", "Connect to radiation shetter Four"),
        ("WHEEL A AUXCOM", "Connect to Auxillary coms, wheel One"),
        ("WHEEL B AUXCOM", "Connect to Auxillary coms, wheel two"),
        ("WHEEL D AUXCOM", "Connect to Auxillary coms, wheel four"),
        ("CARGO", "Connect to main cargo bay"),
        ("EXIT", "Exit the auxillary com system")
    ]
    
    useGenericNoResponse = (
        "BRIDGE",
        "ENGINEERING",
        "RADIATION SHELTER 1",
        "RADIATION SHELTER 2",
        "RADIATION SHELTER 3",
        "RADIATION SHELTER 4",
        "WHEEL A AUXCOM",
        "WHEEL B AUXCOM",
        "WHEEL D AUXCOM"
    ) #some of these are placeholders
    game.rolltext(text)
    makingCall = True
    while(makingCall):
        text = ""
        ind, labl = game.choose2(choices, "Who do you wish to contact?")
        if labl == "EXIT":
            text = "You close the lower panel, shutting down the system"
            makingCall = False
        elif labl in useGenericNoResponse:
            text = """
You attempt to make your connection.
...
....
.....
... ....
... .... .....
ERROR: CONNECTION TIMED OUT, SYSTEM MAY BE OFFLINE!
            """
            choices.pop(ind)
        
        elif labl == "CARGO":
            game.rolltext("""
You attempt to make your connection.
...
....
.. '-oming from inside Wheel C!' 'What?! Hello, who's there!?'
You hear two voices from the com system.
            """)
            makingCall = False #sweet clean redundancy
            return auxcom_cargo(save)
        game.rolltext(text)
    #endregion auxcom2
def auxcom_cargo(save):
    #Note: Whatever the dialoge, it is up to the player what to do afterwards.
    reactorFixed = save.getdata("reactorC:fixed", False)
    prevcontact = save.getdata("auxcom:cargo")
    # Only change is the information they are given.
    # From here, or the ladder if the player skips this, a counter is enabled that gives the player 10 'time units' before game over.
    if not reactorFixed and game.getCounter(save, "reactorC")[0]: #counter not enabled
        game.setCounter(save, "reactorC", "onReactorCTime", 10) #sets up a new timer, running onReactorCTime every time it is updated.

    name = game.getName(save)
    gender = game.getGender(save)
    klara =  game.getKlara(save)
    #TODO

    if prevcontact:
        #TODO: alternate contact for returning to auxcom
        if reactorFixed:
            game.showtext("PLACEHOLDER! you are congratulated with stabilizing the reactor. you got time to waste now, but not too much time.")
        else:
            game.showtext("PLACEHOLDER! You are asked why you are back here talking again, and are reminded the reactor may blow at any moment!")
    else:
        if reactorFixed:
            game.showtext("PLACEHOLDER! You are asked by suprised people if it was you who fixed the reactor. (following dialoge assumes you have not yet done so)")
        game.showtext("The people on the other side of the call is waiting for you to answer.")
        choices = [
            ("I'm {0}. I'm lost, where am I?".format(name)),
            ("Help, I don't know who or where I am!"),
            ("uhh"),
            ("I.. I think my name is {0}. I find it hard to remember.")
        ]
    ind, ans = game.choose2(choices, "What do I say?")
    game.showtext(">>"+ans)
    p = "mister" if gender == "male" else "miss"
    if ind == 0 or ind == 3:
        p = name
    game.rolltext("""
Ok. {0}, I need you to stay calm. I'm gonna get some help
(The woman you were talking leaves)
...
(A man, an engineer by the looks of his attire, takes her place)
Ok, {0}. I am not gonna lie, you are in a bit of touble. We are gonna do what we can to help you.
First of, you are onboard the UNS Armstrong on route from Sol to Alpha Centauri.
Your current dizzyness may be from the emergency awakening from stasis.
The reactor onboard is about to explode, so were about to detach the module when you contacted us.

Look {0}, I need you to find the emergency ladd..
(the man is rudely interrupted by a third person)
Hey! I know you. You're Klara's {1} right?
You're a engineer, right? Maybe you could try to stabilize the reactor temporarily?
There are still lots of people stuck in stasis in the upper ring!

Look, {2}, I woulden't blame you for just making a run for the ladder to save yourself, but you could save those people!
    """.format(p, game.getGenderedTerm(klara, gender), name))
    choices = [
        ("Screw them! I'm out of here! I'm gonna climb down and get out of here!"), #ignorant idiot option
        ("I.. I am not gonna take that chance. I'm just gonna go meet you up the ladder!"), #reluctant selfishness
        ("Alright, how do I get to the reactor?"),
        ("What exacly happend?")
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
    elif ind == 1:
        game.rolltext("""
I see. Well, the reactor will reach a meltdown in just a few minutes, we need to detach the module before then.
You need to hurry! The escape ladder should be nearby. You need to climb up as fast as you can.
We will meet you at the airlock in the module core.
Please beware, you will be weightless up here!
See you soon!

(The call has ended)
        """)
    elif ind == 2:
        game.rolltext("""
Thanks for doing this!
Ok, there won't be much time, but we will hold off detaching the module as long as we can.
You should find the emergency stairs nearby. You need to climb down to the outermost ring.
The nearest reactor-node will not be far from the ladder.
You need to first initalize the emergency cooling system, then the emergency particle decelerator.
In that order! You will find detailed instructions on how to do this in the reactor-node control room.
Doing this will buy us maybe an hour before meltdown.
You need to hurry! Get back and contact us again once you have done it!

(The call has ended)
        """)

def elevator(save):
    #region elevator
    room = save.getdata("room")

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
        choices = (("UP, Press UP call button"), ("DOWN","Press DOWN call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))
    elif room == "core":
        choices = (("DOWN","Press DOWN call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))
    elif room == "outer":
        choices = (("UP, Press UP call button"), ("CARGO","Press CARGO call button"), ("EXIT","Leave"))

    _,choice = game.choose2(choices, "Press a button?")
    if choice != "EXIT":
        if(save.getdata("WheelC_elevator") == "dead"):
            text = """
You press the button.
...
Nothing happened.
            """
        else:
            text = """
You press the button.
The button flash on.
...
You hear an odd clang
...         """
            if choice == "CARGO":
                text += "\nTwo of the elevator doors open in a very slight crack."
            else:
                text += "\nOne of the elevator doors open in a very slight crack."
            text += "\nThen you hear a fizzeling sound, and everything stops working"
            save.setdata("WheelC_elevator", "dead")
        game.rolltext(text)
    else:
        game.showtext("You left the elevators alone")
    #endregion elevator