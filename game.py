from time import sleep
from player import Player

# import threading
import asyncio
import random

# import deque

# Some dead kittens, I MEAN... globals...
DEFAULT_MIN_PASSES = 2
DEFAULT_TIME_TO_PASS = 30
DEFAULT_GAME_TIME = 60 * 3  # for prod: set to 5 * 60


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
        self.recent_potatoholders = [
            None
        ] * self.min_passes  # initializes the list with empty values
        self.game_timer = 0
        self.pass_timer = 0
        self.win = None

    async def start_game(self, ctx):
        self.active = True
        if self.current_player is None:
            self.current_player = random.choice(list(self.active_players))
            # self.current_player = self.active_players.pop()
            # self.active_players.add(self.current_player)

        await ctx.send(
            f"@{self.current_player.username} you caught the Potato first! Pass it to any of these players:"
        )
        await ctx.send("Players: " + ", ".join(p.username for p in self.active_players))
        self.loop_task = asyncio.create_task(self.game_loop(ctx))

    async def game_loop(self, ctx):
        while self.active:
            # Call check_for_win_state() which sets self.win:
            self.check_for_win_state()
            if self.win == True:
                self.end_game()
                break

            if self.win == False:
                self.end_game()
                break

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
            await ctx.send(f"@{ctx.author.name}, you've already joined.")
        else:
            self.active_players.add(new_player)
            # self.active_players.append(new_player)
            await ctx.send(f"Potatoed Up: @{new_player.username}")

    def _pass_potato(self, to_player, from_player_name):
        # Validate  from player is actually playing:
        from_player_is_active = False
        for pl in self.active_players:
            if from_player_name == pl.username:
                from_player_is_active = True

        if not from_player_is_active:
            return

        # Make sure the from player actually has the potato:
        if from_player_name != self.current_player.username:
            raise Exception(f"@{from_player_name} you don't have the Potato right now.")

        # Validate to_player: exists in game, etc.
        player_is_active = False
        for ap in self.active_players:
            if to_player.username == ap.username:
                player_is_active = True

        if not player_is_active:
            raise Exception(
                f"@{to_player.username} is not playing! Choose someone else..."
            )

        # Make sure a player is not passing to themselves:
        if to_player.username == self.current_player.username:
            raise Exception(
                f"@{to_player.username} already has the potato! Choose someone else..."
            )

        # during pass you want to check if to player is in recent potatoholders
        if to_player in self.recent_potatoholders:
            raise Exception(
                f"@{to_player.username} just had the Potato, their hands are too hot! Choose someone else..."
            )

        if self.is_it_not_a_potato():
            raise Exception(
                f"Oh no! @{from_player_name} meant to pass the potato, but instead you passed a puppy! Try again!"
            )

        # if pass is succesfull before actually passing:
        self.recent_potatoholders.pop(0)  # removes the first element
        self.recent_potatoholders.append(
            self.current_player
        )  # adds the last player to the end

        # do the actual passing:
        self.num_passes += 1
        self.pass_timer = 0
        to_player.receive_potato(self.num_passes)
        self.current_player = to_player

    def is_it_not_a_potato(self):
        random_num = random.randint(0, len(self.active_players) - 1)
        if random_num % 3 == 0:
            return True
        return False

    def check_for_win_state(self):
        if self.pass_timer > self.time_to_pass:
            self.win = False

        if self.game_timer > self.game_time:
            self.win = True

        return

    def end_game(self):
        self.active = False

    # def resolve_game(self):
    #     # might need to pass twitchio ctx when creating game so that we can write to chat here
    #     self.active = False
    #     # do we reset game state or destroy this one and always construct a new one?
    #     return
