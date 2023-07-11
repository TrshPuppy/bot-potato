# This is for our main bot code
from twitchio.ext import commands
import json

class Bot(commands.Bot):
    
    def __init__(self):
        # Load api/ oauth data from data/api.json:
        with open('data/api.json') as f:
            api = json.load(f)

        bot_username = api['Bot']['BOT_USERNAME']
        prefix = api['Bot']['PREFIX']
        # target_twitch_channel = [api['Bot']['CHANNEL']]

        super().__init__(# 'irc_token' evidentally has to be 'token' instead
                         token=api['OA_TOKEN'], 
                         client_id=api['CLIENT_ID'], 
                         nick=bot_username, 
                         prefix=prefix,
                         # this has to be an array but setting `target_twitch_channel`
                         # on line 14 to = [api['Bot]['CHANNEL]] didn't work.
                         # Channel name hard coded for now :)
                         initial_channels=['trshpuppy'])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send('Hello World!')

    @commands.command(name='bake')
    async def bake_command(self, ctx):
        await ctx.send('bake')

bot = Bot()
bot.run()