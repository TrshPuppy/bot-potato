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
        await ctx.send('Potato game starting...')
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
    
    player_added = await try_to_add_player(joined_player, ctx)
    if player_added:
        print(f"New Player joined, player time received = {joined_player.time_received}")
        await ctx.send(f"New player joined!, welcome {joined_player.username}")

# @bot.command(name="pass")
# async def pass(ctx):
#     #passed = pass_potato(ctx.author.name, ctx.author.id, /*receiving player needs to be parsed from message */)
#     if passed : # passed == 0 on success
#         print(f"pass failed, interpret error codes")
#         await ctx.send(f"pass failed, write informative error to chat")

# Bot event listeners: 
@bot.event()
async def event_ready():
    print(f"Ready @{bot_username}")

# @bot.event()
# async def event_message(ctx):
#     if ctx.echo:
#         return
#     await ctx.channel.send(f"hello {ctx.author.name}")

# Connect and run bot, it's listening to chat, this method is 'stopping':
bot.run()

