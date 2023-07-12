import time

# Some dead kittens, I MEAN... globals...
current_game = None
a_game_is_active = False

class Game():
    def __init__(self):
        self.start_time = 0
        self.active = False
        self.num_passes = 0
        self.current_player = None
        self.active_players = []
        #self.potato = None

    def start_game(self, st):
        self.start_time = st
        self.active = True

    def end_game(self, et):
        self.active = False
        # self.end_time = et

    def check_for_player(self, p):
        if p.id in self.active_players:
            return True
        return False

    def player_join_game(self, player):
        self.active_players.append(player.id)

    def get_game_state(self):
        return "game stats"


def start_new_game():
    # This should only define and activate the 'current_game' variable
    global current_game, a_game_is_active
    if a_game_is_active:
        return
        
    game_start_time = int(time.time()) # format is Unix, ex: 1627173662
    current_game = Game()
    current_game.start_game(game_start_time)
    current_game.active = True
    a_game_is_active = current_game.active

    return

def try_to_add_player(p):
    # If there is no current game, start one:
    global current_game
    
    if a_game_is_active == True:
        if current_game.check_for_player(p):
            print("This player is already playing")
            return False
    
        current_game.player_join_game(p)
        return True

    # We should be able to have a game and activate or deactivate it.
    print("Sorry, the game is over")
    return False
    
    

