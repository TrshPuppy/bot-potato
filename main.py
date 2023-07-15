from twitchio.ext import commands
import time
import json

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
MIN_PLAYERS = 4

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


# Bot commands:
@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello World!")


@bot.command(name="join")
async def join(ctx):
    await bot.current_game.add_player(ctx)


# MOD commands
@bot.command(name="start")
async def start(ctx):
    if not chatter_has_authority(ctx, channel_mods):
        await ctx.channel.send(f"Sorry {ctx.author.name}, you can't start a potato game :(")
        return

    game = Game()
    bot.current_game = game

    # Announce the start of the game and wait for players to join
    await ctx.send("Potato game starting soon! Join by typing '!join'")
    await asyncio.sleep(30)
    await ctx.send('30 sec left to join')
    await ctx.send(f'currently {len(game.active_players)} players have joined')
    await asyncio.sleep(30)

    # Check if there are enough players
    if len(current_game.active_players) < MIN_PLAYERS:  # replace with your desired minimum number of players
        await ctx.send("Not enough players joined the game. Try again later.")
        return

    # Start the game
    game.start_game()
    await ctx.send(f"Potato game has started with {len(game.active_players)} players!")


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

# @bot.command(name="join")
# async def join(ctx):
#     joined_player = create_and_get_player(ctx)

#     player_added = await try_to_add_player(joined_player, ctx)
#     if player_added:
#         print(f"New Player joined, player time received = {joined_player.time_received}")
#         await ctx.send(f"New player joined!, welcome {joined_player.username}")

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


