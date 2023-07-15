import time
from game import current_game

DEFAULT_TIME_TO_PASS = 30


class Player:
    def __init__(self, u, i):
        self.id = i
        self.username = u
        self.last_passed = (
            0  # global turn number where this player last received the potato.
        )
        self.time_received = 0
        self.current_timeout = 0  # the decreasing ammount of time player has to pass
        # self.hasPotato = False  # This might make it easier for game to check players?

    def receive_potato(self, po, turn):
        # time_received is measured in Unix time
        # last passed is measured in number of turns, not time
        self.time_received = int(time.time())
        self.last_passed = turn
        # set when they receive potato (vs when they pass it?)
        # self.hasPotato = True
        self.current_timeout = DEFAULT_TIME_TO_PASS#.  # fixed time to pass, we can make this decay by not here.
        # the passing player's time decays, not the receiving player

    # the player doesn't need to check countdown. 
    # the game loop is responsible for checking timeouts
    def check_countdown(self):
        time_now = int(time.time())
        time_left_to_pass = self.current_timeout - time_now
        self.current_timeout = time_left_to_pass

        if time_left_to_pass < 0:
            return 0

        return time_left_to_pass

    # def pass_potato(self):


async def create_and_get_player(ctx):
    global current_game

    if current_game == None or current_game.active:
        return 0

    p_username = ctx.author.name
    p_id = ctx.author.id
    for p in current_game.active_players:
        if p.id == p_id:
            await ctx.send(f"{ctx.author.name}, you've already joined.")
            return 0

    new_player = Player(p_username, p_id)

    return new_player


# Player.last_passed is a limit on how frequently,
# in number of passes, a player can receive the potato again.
# Basically we want to prevent the potato from being passed
# among a too-small subset
# of players or immediate passbacks.
# We will want to do the comparison


# (Game.num_passes - last_passed >= Game.min_passes_between)
# to determine if the pass is allowed between two players.
# Game.min_passes_between shoud also scale with the number of players in a game.
# This sort of suggests (a really-nice-to-have) that a player roster to be printed periodically so players know who is in game


# Game has a current_player that should point
# to the Player that has the potato.
# The idea behind Game._run() is that it runs every second
# and checks the game state, i.e. timeouts, and does what it do.
# Within that loop, _run() should be able to check
# self.current_player and determine whether player
# timeout has happened by
# checking (int(time.time()) - self.current_player.time_received > self.current_player.player_timeout).
# If player timeout has not happened, it can send a courtesy chat that says
# "Player A has X seconds left to pass!"
