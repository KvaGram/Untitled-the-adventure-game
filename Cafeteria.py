import Game
import General

_VISITED = "cafeteria:visited"

def Main(game:Game.Game):
    def start():
        visited = game.getdata(_VISITED, False)
        game.setdata(_VISITED, True)
        if not visited:
            darkness()
        else:
            game.rolltext("{CAFE_INTRO_2}")
    def darkness():
        game.rolltext("{CAFE_INTRO_1}")

    start()
    game.place = "middle"
    return
    
