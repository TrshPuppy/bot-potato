from twitchio.ext import commands
import time
import json

# Local modules:
from player import *
from game import *
from chat import chatter_has_authority

# Load api/ oauth data from data/api.json:
with open('data/api.json') as f:
    api = json.load(f)

bot_username = api['Bot']['BOT_USERNAME']
prefix = api['Bot']['PREFIX']
channel_mods = api['Bot']['MODLIST']

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

# MOD commands

@bot.command(name="start") # This is the only pplace we  should start a game:
async def start(ctx):
    if chatter_has_authority(ctx, channel_mods):
        print("Starting potato game")
        start_new_game()
    else:
       await ctx.channel.send(f"Sorry {ctx.author.name}, you can't start a potato game :(")

# nice to have: add an announce command to get players to join

# nice to have: add a prepare command to wrap the announce command in a timed loop so that announce
# can be made and then start game can be made with a single command

# nice to have: end game command for mods

# Player commands

@bot.command(name="join")
async def join(ctx):
    joined_player = create_and_get_player(ctx)
    
    player_added = try_to_add_player(joined_player)
    if player_added:
        print(f"New Player joined, player time received = {joined_player.time_received}")
        await ctx.send(f"new player joined!, welcome {joined_player.id}")

# need: pass command

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
