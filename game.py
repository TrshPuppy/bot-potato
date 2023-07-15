from time import sleep
import threading
import random
import json

# Some dead kittens, I MEAN... globals...
current_game = None
DEFAULT_MIN_PASSES = 2
DEFAULT_TIME_TO_PASS = 30
DEFAULT_GAME_TIME = 5 * 60


# need some default parameters for game:
class Game:
    # use default values for ctor parameters
    def __init__(self,
                 min_passes=DEFAULT_MIN_PASSES,
                 time_to_pass=DEFAULT_TIME_TO_PASS,
                 game_time=DEFAULT_GAME_TIME):

        self.min_passes = min_passes
        self.time_to_pass = time_to_pass
        self.game_time = game_time
        self.active = False
        self.num_passes = 0
        self.current_player = None
        self.active_players = []
        self.game_timer = 0
        self.pass_timer = 0

    def start_game(self):
        self.active = True
        if self.current_player is None:
            random_player_indx = random.randint(0, len(self.active_players) - 1)
            self.current_player = self.active_players[
                random_player_indx
            ]

        self.game_thread = threading.Thread(target=self.game_loop)
        self.game_thread.start()

    def game_loop(self):
        while self.active:
            if self.pass_timer > self.time_to_pass:
                print(f"{self.current_player.username} failed to pass the potato in time!")
                self.end_game(win=False)
            if self.game_timer > self.game_time:
                self.end_game(win=True)
            sleep(1)
            self.game_timer += 1
            self.pass_timer += 1

    def pass_potato(self, to_player):
        # Validate to_player: exists in game, etc.
        if to_player not in self.active_players:
            print(f"{to_player.username} is not in the game.")
            return
            
        # Check passes
        if self.num_passes - to_player.last_passed < self.min_passes_between:
            print(f"{to_player.username} already had it too recently.")
            return

        # update game and player states, e.g. time received, last passed, num_passes, current player...
        self.num_passes += 1
        self.pass_timer = 0
        to_player.receive_potato(
            self.num_passes)
        self.current_player = to_player
        

    def end_game(self, win):
        self.active = False
        if win:
            print('Players won the game')
        else:
            print('Players lost the game')

    def check_for_player(self, p):
        print(f"new player id is {p.id}")
        if p in self.active_players:
            return True
        return False

    def player_join_game(self, player):
        self.active_players.append(player)

    def get_game_state(self):
        return "game stats"

    def resolve_game(self):
        # might need to pass twitchio ctx when creating game so that we can write to chat here
        self.active = False
        # do we reset game state or destroy this one and always construct a new one?
        return


def is_game_active():
    print(f"HEY!!! the game is {current_game}")
    if current_game is None:
        return False
    return current_game.active


def announce_new_game():
    global current_game
    print(f"announce new game current game is {current_game}")
    if is_game_active():
        print(f" announce is game active is {is_game_active()}")
        return

    current_game = Game()
    print(f"after game made is game active call = {is_game_active()}")
    print(f"announce after game made current game is {current_game}")
    current_game.active = False
    return


def start_new_game():
    # This should only define and activate the 'current_game' variable
    global current_game
    if is_game_active() or current_game == None:
        return

    current_game.start_game()
    return


async def try_to_add_player(p, ctx):
    # with open("data/stats.json", "r") as f:
    #     game_stats = json.load(f)

    # if game_stats['active'] == 1:

    # active_players = game_stats['active_players']

    global current_game
    if current_game == None or is_game_active():
        return

    current_game.player_join_game(p)
    return True


def print_players(ctx):
    # periodically print list of players to chat so people know who's playing
    return
