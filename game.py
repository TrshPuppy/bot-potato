from time import sleep
from player import Player
import threading
import asyncio

# Some dead kittens, I MEAN... globals...
DEFAULT_MIN_PASSES = 2
DEFAULT_TIME_TO_PASS = 30
DEFAULT_GAME_TIME = 35


# need some default parameters for game:
class Game:
    # use default values for ctor parameters
    def __init__(
        self,
        min_passes=DEFAULT_MIN_PASSES,
        time_to_pass=DEFAULT_TIME_TO_PASS,
        game_time=DEFAULT_GAME_TIME,
    ):
        self.min_passes = min_passes
        self.time_to_pass = time_to_pass
        self.game_time = game_time
        self.active = False
        self.num_passes = 0
        self.current_player = None
        self.active_players = set()
        self.game_timer = 0
        self.pass_timer = 0

    def start_game(self, ctx):
        self.active = True
        if self.current_player is None:
            self.current_player = self.active_players.pop()
            self.active_players.add(self.current_player)

        self.loop_task = asyncio.create_task(self.game_loop(ctx))

    async def game_loop(self, ctx):
        while self.active:
            if self.pass_timer > self.time_to_pass:
                await ctx.send(
                    f"{self.current_player.username} failed to pass the potato in time!"
                )
                self.end_game(win=False)
            if self.game_timer > self.game_time:
                self.end_game(win=True)
            await asyncio.sleep(1)  # non-blocking sleep
            self.game_timer += 1
            self.pass_timer += 1

    async def add_player(self, ctx):
        if self.active:
            await ctx.send(
                "The game is already active. Wait for the next game to join."
            )
            return

        new_player = Player(ctx.author.name, ctx.author.id)

        if new_player in self.active_players:
            await ctx.send(f"{ctx.author.name}, you've already joined.")
        else:
            self.active_players.add(new_player)
            await ctx.send(f"New player joined!, welcome {new_player.username}")

    def _pass_potato(self, to_player):
        # Validate to_player: exists in game, etc.
        # if to_player not in self.active_players:
        #     raise Exception(f"@{to_player.username} is not in the game.")

        # Make sure a player is not passing to themselves:
        if to_player.username == self.current_player.username:
            raise Exception(f"You cannnot pass to yourself {to_player.username}!")

        # Check passes
        if self.num_passes - to_player.last_passed < self.min_passes:
            raise Exception(f"{to_player.username} had the potato too recently.")

        # update game and player states, e.g. time received, last passed, num_passes, current player...
        self.num_passes += 1
        self.pass_timer = 0
        to_player.receive_potato(self.num_passes)
        self.current_player = to_player

    def end_game(self, win):
        self.active = False
        if win:
            print("Players won the game!")
        else:
            print("Players lost the game!")

    # def check_for_player(self, p):
    #     print(f"new player id is {p.id}")
    #     if p in self.active_players:
    #         return True
    #     return False
    #
    #
    # def get_game_state(self):
    #     return "game stats"
    #
    # def resolve_game(self):
    #     # might need to pass twitchio ctx when creating game so that we can write to chat here
    #     self.active = False
    #     # do we reset game state or destroy this one and always construct a new one?
    #     return
