from twitchio.ext import commands
import time
import json

# Local modules:
from player import *
from game import Game

# Some dead kittens, I MEAN... globals...
current_game = None
a_game_is_active = False

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
    if current_game == None:
        start_new_game()
        # new_game = start_and_get_new_game()
        # player_is_already_playing = new_game.check_for_player(p)
        # new_game.player_join_game(p)
        # return True
    
    if current_game.active == False:
        # We should be able to have a game and activate or deactivate it.
        print("Sorry, the game is over")
        return False
    
    if current_game.check_for_player(p):
        print("This player is already playing")
        return False
    
    current_game.player_join_game(p)
    return True

# Load api/ oauth data from data/api.json:
with open('data/api.json') as f:
    api = json.load(f)

bot_username = api['Bot']['BOT_USERNAME']
prefix = api['Bot']['PREFIX']

# Load game stats from data/stats.json:
with open('data/stats.json') as g:
    stats = json.load(g)

# Create bot using 'commands' from twitchio and api data:
bot = commands.Bot(
    token=api['OA_TOKEN'], 
    client_id=api['CLIENT_ID'], 
    nick=bot_username, 
    prefix=prefix,
    initial_channels=['trshpuppy']
    )

# Bot commands:
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello World!")

@bot.command(name="join")
async def join(ctx):
    joined_player = create_and_get_player(ctx)
    
    player_added = try_to_add_player(joined_player)
    if player_added:
        print(f"New Player joined, player time received = {joined_player.time_received}")
        await ctx.send(f"new player joined!, welcome {joined_player.id}")

# Bot event listeners: 
@bot.event()
async def event_ready():
    print(f"Ready @{bot_username}")

@bot.event()
async def event_message(ctx):
    if ctx.echo:
        print("echo")
    await ctx.channel.send(f"hello {ctx.author.name}")

# Connect and run bot, it's listening to chat, this method is 'stopping':
bot.run()

# class Bot(commands.Bot):
    
    # def __init__(self):
    #     # Load api/ oauth data from data/api.json:
    #     with open('data/api.json') as f:
    #         api = json.load(f)

    #     bot_username = api['Bot']['BOT_USERNAME']
    #     prefix = api['Bot']['PREFIX']
    #     # target_twitch_channel = [api['Bot']['CHANNEL']]

    #     super().__init__(# 'irc_token' evidentally has to be 'token' instead
    #                      token=api['OA_TOKEN'], 
    #                      client_id=api['CLIENT_ID'], 
    #                      nick=bot_username, 
    #                      prefix=prefix,
    #                      # this has to be an array but setting `target_twitch_channel`
    #                      # on line 14 to = [api['Bot]['CHANNEL]] didn't work.
    #                      # Channel name hard coded for now :)
    #                      initial_channels=['trshpuppy'])

    # async def event_ready(self):
    #     print(f'Ready | {self.nick}')

    # async def event_message(self, message):
    #     print(message.content)
    #     await self.handle_commands(message)

    # @commands.command(name='hello')
    # async def hello(self, ctx):
    #     print(commands.hello.message.author)
    #     await ctx.send('Hello World!')

    # @commands.command(name='bake')
    # async def bake(self, ctx):
    #     await ctx.send('bake')