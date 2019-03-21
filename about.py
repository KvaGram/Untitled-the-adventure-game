#import time
import game_utilities as game

def main(savedata):
    f = open("title.txt", 'r', encoding="utf-8")
    titlecard = f.read()
    game.rolltext(titlecard, 0.05)
    f.close()
    f = open("credits.txt", 'r', encoding="utf-8")
    creditsText = f.read()
    game.rolltext(creditsText, 0.1)
    f.close()
    #time.sleep(1)

if __name__ == "__main__":
    game.showtext("PLEASE RUN GAME FROM main.py INSTEAD!")
    pass #testing-code