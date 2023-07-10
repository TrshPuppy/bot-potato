# This is for our main bot code
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token='oauth:YOUR_TOKEN', 
                         client_id='YOUR_CLIENT_ID', 
                         nick='YOUR_BOT_USERNAME', 
                         prefix='!', 
                         initial_channels=['CHANNEL_NAME'])

    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='hello')
    async def my_command(self, ctx):
        await ctx.send('Hello World!')


bot = Bot()
bot.run()