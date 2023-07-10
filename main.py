# This is for our main bot code
#from twitchio.ext import commands
import json

#class Bot(commands.Bot):
class Bot():
    
    def __init__(self):
        # Load api/ oauth data from data/api.json:
        with open('data/api.json') as f:
            api = json.load(f)

        self.bot_username = api['Bot']['BOT_USERNAME']
        prefix = api['Bot']['PREFIX']
        target_twitch_channel = api['Bot']['CHANNEL']

        # super().__init__(irc_token=api['OA_TOKEN'], 
        #                  client_id=api['CLIENT_ID'], 
        #                  nick=bot_username, 
        #                  prefix=prefix,
        #                  initial_channels=target_twitch_channel)

        # super().__init__(nick=bot_username, 
        #                  prefix=prefix,
        #                  initial_channels=target_twitch_channel)

    def hello_bot(self):
        print(f'Hello, my name is {self.bot_username}')
    # async def event_ready(self):
    #     print(f'Ready | {self.nick}')

    # async def event_message(self, message):
    #     print(message.content)
    #     await self.handle_commands(message)

    # @commands.command(name='hello')
    # async def my_command(self, ctx):
    #     await ctx.send('Hello World!')


bot = Bot()
#bot.run()

bot.hello_bot()