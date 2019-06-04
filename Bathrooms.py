def main(game):
    def bathrooms1():
        while True:
            game.rolltext("""
You stand in front of the bathrooms. There are two doors in front of you.
One door with a depiction of a man, one depicting a woman.
            """)
            choices = [("MALE", "Enter men's room"), ("FEMALE", "Enter ladies' room"), ("EXIT", "Leave")]
            _, val = game.choose2(choices, "What door do you enter")
            if val == "MALE":
                bathrooms2("mens")
            elif val == "FEMALE":
                bathrooms2("ladies")
            else:
                game.goto("middle")
                break
            if(game.getGameover(game)):
                return

    def bathrooms2(subroom):
        gender = None 
        visited = game.getdata("bathroom:visited", False) # if the Player Character has visited the bathrooms beofore
        showered = game.getdata("bathroom:showered", False) # whatever the PC has showered
        relived = game.getdata("bathroom:relived", False) # whatever the PC has had the chance to relive themself
        keepsake = game.getdata("spouse:keepsake", False) # potential use in later chapters. Only unlockable if you have remembered who your spouse is.

        relationKlara = game.getdata("klara", None) #if spouse, unlocks retrival of keepsake in ladies locker-room
        relationJeff = game.getdata("jeff", None) #if spouse, unlocks retrival of keepsake in mens locker-room

        choices = None

        wrongroom = "" #if the PC enters the wrong bathroom, this extra nerrative is added.
        facedesc = "" #describes what the PC sees in the mirror (male or female)
        areadesc = "" #describes the facilities in the room (mens or ladies)

        #This section determines PC's gender if not already set.
        if subroom == "mens":
            gender = game.getdata("gender", "male")
            if gender != "male":
                wrongroom = """
You're not exacly sure why you went into the men's room, and not the ladies' room.
Though you suppose it doesn't really matter. There is nobody here anyways."""
            areadesc = """ a line of toilet stalls, a large urinal, a few changing rooms, a locker room,
showers, couple of them private, and a dispenser of hygine products."""
            choices = (
                ("SINK", "Spash water in your face"),
                ("TOILET", "Visit a toilet booth"),
                ("URINAL", "Visit the urinal"),
                ("HYGINE_MENS", "open the hygine dispenser"),
                ("SHOWER", "Go the the showers"),
                ("LOCKERS", "Go to the locker room"),
                ("EXIT", "leave")
            )
        elif subroom == "ladies":
            gender = game.getdata("gender", "female")
            if gender != "female":
                wrongroom = """
A man going inside the ladies room would normally be seen as quite perverted.
But as it is, the ladies is as vacant of people as the rest of this place."""
            areadesc = """ a line of toilet stalls, a few changing rooms, a looker room, showers, couple of them private
and a hygine despenser with varius.. products..."""
            choices = (
                ("SINK", "Spash water in your face"),
                ("TOILET", "Visit a toilet booth"),
                ("HYGINE_LADIES", "open the hygine dispenser"),
                ("SHOWER", "Go the the showers"),
                ("LOCKERS", "Go to the locker room"),
                ("EXIT", "leave")
            )
        if gender == "male":
            facedesc = "a rugged man with a stubby beard."
        if gender == "female":
            facedesc = "a tired looking woman with clear bags under they eyes."
        if not visited:
            game.rolltext("""
You enter the {0} room.{1}
Finding yourself in front of the large array of sinks and mirrors.
Some of the mirrors are broken, but you found one that was relativly intact.
You have a look at yourself.
What you see is {2}
You look about as shitty as you feel, yet it does look familiar.
That's a good thing, right?
Looking around, you see {3}
            """.format(subroom, wrongroom, facedesc, areadesc))
        else:
            game.showtext("PLACEHOLDER text for return visit to bathrooms.")
        visited = True
        game.setdata("bathroom:visited", True)
        while True:
            _,choice = game.choose2(choices, "What do you want to do?")
            if   choice == "EXIT":
                game.showtext("You leave the {0} room".format(subroom))
                return
            elif choice == "SINK":
                game.showtext("You splash some water on your face. It feels refreshing.")
            elif choice == "TOILET":
                act = ""
                if(relived): #relived = game.getdata("bathroom:relived", False)
                    act = "You sit for a bit, resting. You don't feel the need to 'do' anything."
                else:
                    act = "You relieve yourself right there and then. You must have held it in for a while without thinking about it."
                    game.setdata("bathroom:relived", True)
                    relived = True
                game.rolltext("""You locate a nice toilet booth, and sit down on a porcelain throne.
                Well, ok, not porcelain, these toilets are made of metal.
                {0}
                After a while you decide it is time to get back up""".format(act))
            elif choice == "URINAL":
                if relived:
                    game.showtext("you stand over by the urinal for a bit, but you don't feel any need to use it.")
                elif gender == "female":
                    game.showtext("As you approach the urinal, you wondered how it was like for men to use contraptions like this.")
                    if(game.yesno("Try to piss in it?")):
                        game.rolltext("""You awkwardly posision yourself,
and partially relive youself down the urinal.
It was kinda fun.
And you mostly hit the target.
mostly..

Still, having done that, you realize you have 'other' needs to relive youself of.""")
                        if(game.yesno("Take a dump in the uninal?")):
                            game.showtext("You did the deed in the urinal. you slowly back off, giggling a bit as your inner girl got her wicked wish.")
                            game.setdata("bathroom:relived", True)
                            relived = True
                    else:
                        game.showtext("You left the uninal alone.")
                else:
                    game.rolltext("""You instinctively unzip and relive youself down the uninal.
 it was quickly done.
 But soon you realize you have 'other' needs to relive youself of.""")
                    if(game.yesno("Take a dump in the uninal?")):
                        game.showtext("You did the deed in the urinal. you slowly back off, giggling a bit as your inner child got his very childish wish.")
                        game.setdata("bathroom:relived", True)
                        relived = True
            elif choice == "HYGINE_LADIES":
                game.showtext("You examine the dispenser. You find some soaps, tampons, manual razor blades, a few female condoms. Nothing you really need right now")
            elif choice == "HYGINE_MENS":
                game.showtext("You examine the dispenser. You find some soaps, condoms, razor blades. Nothing you really need right now.")
            elif choice == "SHOWER":
                if showered:
                    game.showtext("You go over to the showers. But you already feel clean, so you go back.")
                else:
                    game.rolltext("""You enter one of the private show stalls.
You undress, and turn on the shower
You note as all the grime washes off you.
you feel a lot better now.
...
...
you dry up, dress yourself and again, and leave the shower.""")
                    showered = True
                    showered = game.setdata("bathroom:showered", True)
            elif choice == "LOCKERS":
                text = "You take a walk along the lockers."
                if keepsake:
                    text += "\nThere was not much more to see."
                elif subroom == "mens" and relationJeff == "spouse":
                    text+= """
You stumble upon a familiar locker. Jeff's locker.
Your hands move on their own, it seems his locker combination is deep in your subconsius.
Inside you find a small box.
It feels important.
You take it with you."""
                    keepsake = True
                elif subroom == "ladies" and relationKlara == "spouse":
                    text+= """
You stumble upon a familiar locker. Klara's locker.
Your hands move on their own, it seems her locker combination is deep in your subconsius.
Inside you find a small box.
It feels important.
You take it with you.""" 
                    keepsake = True
                else:
                    text += "\nThere was not much to see."
                game.setdata("spouse:keepsake", keepsake)
                game.rolltext(text)
            status = game.updateCounter(game, "reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                break
        #end of loop
    bathrooms1() #Starts the room.
