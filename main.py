from twitchio.ext import commands
import time
import json
import asyncio

# Local modules:
from player import *
from game import *
from chat import chatter_has_authority

# Load api/ oauth data from data/api.json:
with open("data/api.json") as f:
    api = json.load(f)

bot_username = api["Bot"]["BOT_USERNAME"]
prefix = api["Bot"]["PREFIX"]
channel_mods = api["Bot"]["MODLIST"]
MIN_PLAYERS = 1

# Load game stats from data/stats.json:
with open("data/stats.json") as g:
    stats = json.load(g)

# Create bot using 'commands' from twitchio and api data:
bot = commands.Bot(
    token=api["OA_TOKEN"],
    client_id=api["CLIENT_ID"],
    nick=bot_username,
    prefix=prefix,
    initial_channels=["trshpuppy"],
)
bot.current_game = None
bot.lobby = None


# Bot commands:
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello World!")


@bot.command(name="join")
async def join(ctx):
    if bot.current_game is None:
        await ctx.send("Sorry, there is no potato game right now.")
        return

    await bot.current_game.add_player(ctx)


# MOD commands
@bot.command(name="start")
async def start(ctx):
    if bot.current_game != None:
        await ctx.send("There's already a game in progress.")
        return
    if not chatter_has_authority(ctx, channel_mods):
        await ctx.channel.send(
            f"Sorry {ctx.author.name}, you can't start a potato game :("
        )
        return

    game = Game()
    bot.current_game = game
    bot.lobby = True
    try:
        # Announce the start of the game and wait for players to join
        await ctx.send("Potato game starting soon! Join by typing '!join'")
        await asyncio.sleep(10)
        await ctx.send("30 sec left to join")
        await ctx.send(f"Currently {len(game.active_players)} players have joined")
        await asyncio.sleep(10)

        # Check if there are enough players
        if (
            len(game.active_players) < 1
        ):  # Replace with your desired minimum number of players
            await ctx.send("Not enough players joined the game. Try again later.")
            bot.lobby = False
            return

        # Start the game
        bot.lobby = False
        game.start_game(ctx)
        await ctx.send(
            f"Potato game has started with {len(game.active_players)} players!"
        )

        # # Wait for game to finish
        while game.active:
            await asyncio.sleep(1)
    finally:
        # Once the game has finished or an exception has occurred, set bot's current_game to None
        print("Ending game")
        if game.win:
            await ctx.send(f"Congrats! Chat won hot potato!")
        else:
            await ctx.send(
                f"@{bot.current_game.current_player.username} didn't pass the potato in time :("
            )
        bot.current_game = None
        bot.lobby = None


@bot.command(name="end")
async def end(ctx):
    if not chatter_has_authority(ctx, channel_mods):
        await ctx.send(f"Sorry {ctx.author.name}, you can't end the potato game :(")
        return

    # End the current game
    if hasattr(bot, "current_game"):
        bot.current_game.end_game(win=False)  # or win=True, depending on the context
        await ctx.send("Potato game has ended!")
    else:
        await ctx.send("No game is currently running.")


# nice to have: add an announce command to get players to join

# nice to have: add a prepare command to wrap the announce command in a timed loop so that announce
# can be made and then start game can be made with a single command

# nice to have: end game command for mods

# Player commands


@bot.command(name="pass")
async def pass_potato(ctx):
    if bot.lobby:
        return
    # flags to check here:
    # set a flag to handle failures in  main
    # "trying to send to self" flag
    #  and "trying to send to inactive player" flag to check

    if bot.current_game is None:
        await ctx.channel.send("Sorry, there is no potato to pass.")
        return

    # Get the command content (everything after "!pass ")
    command_content = ctx.message.content.split(" ", 1)[-1].strip()
    print(f"command_content = {command_content}")

    # Check if the command content starts with "@"
    if command_content.startswith("@"):
        # Remove the "@" from the beginning
        username = command_content[1:].lower()
        print(f"username is {username}")

        # Search for the player with this username in the active players of the game
        for player in bot.current_game.active_players:
            if player.username == username:
                print(f"player.username = {player.username}")
                # Found the player, pass the potato to them
                try:
                    bot.current_game._pass_potato(player)
                    await ctx.send(
                        f"{ctx.author.name} passed the potato to @{player.username}!"
                    )
                except Exception as e:
                    # Send the errors greated in game._pass_potato to the chat:
                    await ctx.send(f"{e}")
                finally:
                    return

    # If we didn't find the player or the command was not properly formatted, send an error message
    await ctx.send(
        "Could not find the specified player. Make sure you are using the correct format: !pass @username"
    )


# Bot event listeners:
@bot.event()
async def event_ready():
    print(f"Ready @{bot_username}")


@bot.event()
async def event_message(ctx):
    if ctx.echo:
        return


# Connect and run bot, it's listening to chat, this method is 'stopping':
bot.run()
