import time
import threading
import random
import json

# Some dead kittens, I MEAN... globals...
current_game = None
DEFAULT_MIN_PASSES = 2
DEFAULT_GAME_TIMEOUT = 30


# need some default parameters for game:
class Game:
    # use default values for ctor parameters
    def __init__(self, min_passes_between=None, game_timeout=None):
        self.increment = 1  # loop timer, check for timeouts every second
        self.next_loop = int(time.time())
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
        self.dropped = False

    def start_game(self):
        self.start_time = int(time.time())  # format is Unix, ex: 162717366
        self.active = True
        if self.current_player == None:
            random_player_indx = random.randint(0, len(current_game.active_players) - 1)
            current_game.current_player = current_game.active_players[
                random_player_indx
            ]

        self._run()

    def end_game(self, et):
        self.active = False
        # self.end_time = int(int(time.time())) # format is Unix, ex: 162717366

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

    # Game needs to _run a loop for game timer so import threading
    def _run(self):
        self.next_loop += self.increment
        # check for player and game timeouts
        curr_time = int(time.time())

        with open("data/stats.json") as s:
            game_stats = json.load(s)

        print(f"length of active_players in game state is {len(s.active_players)}")
        # print(f"current_player= {self.current_player.username}")

        # global timeout?
        # if (curr_time - self.start_time) > self.game_timeout:
        #     print(f"global timeout")
        #     # resolve
        # elif (
        #     curr_time - self.current_player.time_received
        # ) > self.current_player.player_timeout:
        #     print(f"player timeout")
        #     self.dropped = True
        # resolve
        # player timeout?

        # check potato player to see if they've timed out

        # update self.dropped if needed
        # self.active = False
        if not self.done:
            threading.Timer(self.next_loop - int(time.time()), self._run).start()

    def stop(self):
        self.done = True


def is_game_active():
    global current_game
    print(f"HERY!!! the game is {current_game}")
    if current_game == None:
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


def pass_potato():
    # validate toPlayeri: exists in game, etc

    # check toPlayer lastPassed
    if self.num_passes - toPlayer.last_passed < self.min_passes_between:
        print(f"toPlayer already had it too recently")
        return

    # update game and player states, e.g. time received, last passed, num_passes, current player...

    # TODO: decrease passing player timeout
    return 0


def print_players(ctx):
    # periodically print list of players to chat so people know who's playing
    return
