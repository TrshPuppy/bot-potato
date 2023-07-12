# This is for our main bot code
from twitchio.ext import commands
import json
from player import Player


# Load api/ oauth data from data/api.json:
with open('data/api.json') as f:
    api = json.load(f)

bot_username = api['Bot']['BOT_USERNAME']
prefix = api['Bot']['PREFIX']

# Load game stats from data/stats.json:
with open('data/stats.json') as g:
    stats = json.load(g)

test_stat = stats["test-stat"]
print(f"Test stat: {test_stat}")

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
    p_username = ctx.author.name
    p_id = ctx.author.id
    new_player = Player(p_username, p_id, 0, 1, 2)
    print(f"New Player joined, player time received = {new_player.time_received}")
    await ctx.send(f"new player joined!, welcome {new_player.id}")

# Bot event listeners: 
@bot.event()
async def event_ready():
    print(f"Ready @{bot_username}")

@bot.event()
async def event_message(ctx):
    if ctx.echo:
        print(f"event_message: ")
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