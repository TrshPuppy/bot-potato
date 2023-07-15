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


# Bot commands:
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello World!")


@bot.command(name="join")
async def join(ctx):
    if bot.current_game is None:
        await ctx.channel.send("Sorry, there is no potato game right now.")
        return

    await bot.current_game.add_player(ctx)


# MOD commands
@bot.command(name="start")
async def start(ctx):
    if not chatter_has_authority(ctx, channel_mods):
        await ctx.channel.send(
            f"Sorry {ctx.author.name}, you can't start a potato game :("
        )
        return

    game = Game()
    bot.current_game = game
    try:
        # Announce the start of the game and wait for players to join
        await ctx.send("Potato game starting soon! Join by typing '!join'")
        await asyncio.sleep(10)
        await ctx.send("30 sec left to join")
        await ctx.send(f"Currently {len(game.active_players)} players have joined")
        await asyncio.sleep(10)

        # Check if there are enough players
        if (
            # len(game.active_players) < MIN_PLAYERS
            len(game.active_players)
            < 1
        ):  # Replace with your desired minimum number of players
            await ctx.send("Not enough players joined the game. Try again later.")
            return

        # Start the game
        game.start_game()
        await ctx.send(
            f"Potato game has started with {len(game.active_players)} players!"
        )

        # Wait for game to finish
        game.game_thread.join()
    finally:
        # Once the game has finished or an exception has occurred, set bot's current_game to None
        print("Ending game")
        bot.current_game = None


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
    print(f"current game is {bot.current_game}")
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
                bot.current_game._pass_potato(player, ctx)
                await ctx.send(f"{ctx.author.name} passed the potato to {username}!")
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

    # # create chatter to put in recetn_chatters arr:
    # new_chatter_obj = {
    #     "name": ctx.author.name,
    #     "id": ctx.author.id,
    #     "last_chat_time": int(time.time()),
    # }

    # with open("data/chattters.json", "r") as f:
    #     recent_chatters = json.load(f)

    # found_chatter = -1

    # for indx, c in enumerate(recent_chatters):
    #     if c["id"] == new_chatter_obj["id"]:
    #         found_chatter = indx

    # if found_chatter == -1:
    #     recent_chatters.append(new_chatter_obj)
    # else:
    #     recent_chatters[found_chatter] = new_chatter_obj

    # with open("data/chattters.json", "w") as j:
    #     json.dump(recent_chatters, j)


# @bot.event()
# async def join_event(ch, user):
#     print(f"welcome to the chat {user.name}")

#     # {
#     # chatter.name
#     # chatter.id
#     # chatter.join_time (time.time())}

#     recent_chatters.append(user)


# Connect and run bot, it's listening to chat, this method is 'stopping':
bot.run()


# newChatter = {
#     name: NameError
#     id: id
#     time: now
# }


# found = chatList.findIndex((x) => x.id == newChatter.id)

# if found === -1{
#     add that guy to end
# }else{
#     chatList[found] = newChatter
# }
