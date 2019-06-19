import Game
def Start(game:Game.Game):
    def bathrooms1():
        while True:
            game.rolltext("{BATH_INTRO}")
            choices = [["MALE", "{BATH_CHOICEMENS}"], ["FEMALE", "{BATH_CHOICELADIES}"], ["EXIT", "{LEAVE}"]]
            game.choose(choices, "{BATH_WHATDOOR}")
            data:Game.ActDataInput = game.wait()
            if data.tag == "MALE":
                bathrooms2("mens")
            elif data.tag == "FEMALE":
                bathrooms2("ladies")
            else:
                game.place = "middle"
                break
            if(game.getGameover()):
                return
    def bathrooms2(subroom):
        gender = None 
        visited = game.getdata("bathroom:visited", False) # if the Player Character has visited the bathrooms beofore
        showered = game.getdata("bathroom:showered", False)  # whatever the player character has showered
        relived = game.getdata("bathroom:relived", False) # whatever the PC has had the chance to relive themself
        keepsake = game.getInventory("KEEPSAKE") # potential use in later chapters. Only unlockable if you have remembered who your spouse is.

        choices = None
        introtext = "" #text-block to display. Will be cunstructed below


        #This section determines PC's gender if not already set.
        if subroom == "mens":
            #if male family is spouse, this unlocks retrival of keepsake in the locker-room
            spouseLocker = (game.MaleFam.role == "spouse")
            introtext += "{BATH_MENS_ENTERING}"

            #Gets gender. If not set, sets it to male.
            gender = game.getdata("gender", "male")
            game.setdata("gender", gender)

            if gender != "male":
                introtext += "\n{BATH_MENS_WRONGROOM}"
            if not visited:
                introtext += "\n{BATH_MENS_DESCRIPTION}"
            choices = [
                ["SINK", "{BATH_OPTION_SINK}"],
                ["TOILET", "{BATH_OPTION_TOILET}"],
                ["URINAL", "{BATH_OPTION_URINAL}"],
                ["HYGINE_MENS", "{BATH_OPTION_HYGINE}"],
                ["SHOWER", "{BATH_OPTION_SHOWER}"],
                ["LOCKERS", "{BATH_OPTION_LOCKERS}"],
                ["EXIT", "{LEAVE}"]
            ]
        elif subroom == "ladies":
            #if female family is spouse, this unlocks retrival of keepsake in the locker-room
            spouseLocker = (game.FemaleFam.role == "spouse")
            introtext += "{BATH_LADIES_ENTERING}"

            #Gets gender. If not set, sets it to female.
            gender = game.getdata("gender", "female")
            game.setdata("gender", gender)
            if gender != "female":
                introtext += "\n{BATH_LADIES_WRONGROOM}"
            if not visited:
                introtext += "\n{BATH_LADIES_DESCRIPTION}"
            choices = [
                ["SINK", "{BATH_OPTION_SINK}"],
                ["TOILET", "{BATH_OPTION_TOILET}"],
                ["HYGINE_LADIES", "{BATH_OPTION_HYGINE}"],
                ["SHOWER", "{BATH_OPTION_SHOWER}"],
                ["LOCKERS", "{BATH_OPTION_LOCKERS}"],
                ["EXIT", "{LEAVE}"]
            ]
        if not visited:
            if gender == "male":
                introtext += "\n{BATH_MIRROR_MALE}"
            if gender == "female":
                introtext += "\n{BATH_MIRROR_FEMALE}"
            
        game.rolltext(introtext)
        visited = True
        game.setdata("bathroom:visited", True)
        while True:

            game.choose(choices, "{GAME_MAKECHOICE2}")
            data:Game.ActDataInput = game.wait()
            if data.Type != "action":
                continue
            if   data.tag == "EXIT":
                if subroom == "mens":
                    game.rolltext("{BATH_MENS_LEAVING}")
                if subroom == "ladies":
                    game.rolltext("{BATH_LADIES_LEAVING}")
                return 
            elif data.tag == "SINK":
                game.rolltext("{BATH_WASHFACE}")
            elif data.tag == "TOILET":
                if(relived): #relived = game.getdata("bathroom:relived", False)
                    game.rolltext("{BATH_TOILET2}")
                else:
                    game.rolltext("{BATH_TOILET1}")
                    game.setdata("bathroom:relived", True)
                    relived = True
            elif data.tag == "URINAL":
                if relived:
                    game.rolltext("{BATH_URINAL2}")
                elif gender == "female":
                    game.rolltext("{BATH_URINAL_FEM1}")
                    if(game.yesno("{BATH_URINAL_FEMQUEST}")):
                        game.rolltext("{BATH_URINAL_FEM2}")
                        if(game.yesno("{BATH_URINAL_DUMPQUEST}")):
                            game.rolltext("{BATH_URINAL_FEM_DUMP}")
                            game.setdata("bathroom:relived", True)
                            relived = True
                    else:
                        game.rolltext("{BATH_URINAL_LEAVE}")
                else:
                    game.rolltext("{BATH_URINAL1}")
                    if(game.yesno("{BATH_URINAL_DUMPQUEST}")):
                        game.rolltext("{BATH_URINAL_MALE_DUMP}")
                        game.setdata("bathroom:relived", True)
                        relived = True
            elif data.tag == "HYGINE_LADIES":
                game.rolltext("{BATH_HYGINE_LADIES}")
            elif data.tag == "HYGINE_MENS":
                game.rolltext("{BATH_HYGINE_MENS}")
            elif data.tag == "SHOWER":
                if showered:
                    game.rolltext("{BATH_SHOWER2}")
                else:
                    game.rolltext("{BATH_SHOWER1}")
                    showered = True
                    game.setdata("bathroom:showered", True)
            elif data.tag == "LOCKERS":
                if (keepsake or not spouseLocker):
                    game.rolltext("{BATH_LOCKERS1}")
                else:
                    game.rolltext("{BATH_LOCKERS2}")
                    keepsake = True
                    game.setInventory("KEEPSAKE", True)
            status = game.updateCounter("reactorC", -1)
            if status == "death": #if reactor counter reach 0, and the game ends.
                break
        #end of loop
    bathrooms1() #Starts the room.
