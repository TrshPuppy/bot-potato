import time
import threading

# Some dead kittens, I MEAN... globals...
current_game = None
DEFAULT_MIN_PASSES = 2
DEFAULT_GAME_TIMEOUT = 30

# need some default parameters for game

class Game():
    #use default values for ctor parameters
    def __init__(self, min_passes_between = None, game_timeout = None):
        self.increment = 1 # loop timer, check for timeouts every second
        self.next_loop = time.time()
        self.done = False

        self.start_time = 0
        self.active = False
        self.num_passes = 0
        self.current_player = None
        self.active_players = []
        if min_passes_between == None:
            self.min_passes_between = DEFAULT_MIN_PASSES
        else:
            self.minPasses_between = min_passes_between
        if game_timeout == None:
            self.game_timeout = DEFAULT_GAME_TIMEOUT
        else:
            self.game_timeout = game_timeout
        # note that player_timeout is not here because we now add players before starting the game
        #self.potato = None
        self.dropped = False

    def start_game(self):
        self.start_time = int(time.time()) # format is Unix, ex: 162717366
        self.active = True

    def end_game(self, et):
        self.active = False
        # self.end_time = int(time.time()) # format is Unix, ex: 162717366

    def check_for_player(self, p):
        if p.id in self.active_players:
            return True
        return False

    def player_join_game(self, player):
        self.active_players.append(player.id)

    def get_game_state(self):
        return "game stats"

    def resolve_game(self):
        #might need to pass twitchio ctx when creating game so that we can write to chat here

        #do we reset game state or destroy this one and always construct a new one?
        return

    #Game needs to _run a loop for game timer so import threading
    def _run(self):
        self.next_loop += self.increment
        #check for player and game timeouts
        #update self.dropped if needed
        #self.active = False
        if not self.done:
            threading.Timer(self.next_loop - time.time(), self._run).start()

    def stop(self):
        self.done = True



def is_game_active():
    return current_game.active

def start_new_game():
    # This should only define and activate the 'current_game' variable
    global current_game
    if is_game_active():
        return
        
    current_game = Game()
    current_game.start_game()

    return

def try_to_add_player(p):
    # If there is no current game, start one:
    global current_game

    #is this the correct condition? the game is not active while we are joining players
    #game becomes active when start_new_game is called
    if is_game_active() == True:
        if current_game.check_for_player(p):
            print("This player is already playing")
            return False
    
        current_game.player_join_game(p)
        return True

    # We should be able to have a game and activate or deactivate it.
    print("Sorry, the game is over")
    return False
    
def pass_potato():
    #validate toPlayer
    #check toPlayer lastPassed
    #update game and player states, e.g. time received, last passed, num_passes, current player...
    #TODO: decrease passing player timeout
   return 0

