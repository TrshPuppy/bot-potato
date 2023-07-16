# Bot Potato!
This is a team project submitted for the [Time Enjoyed Code Jam '23](https://codejam.timeenjoyed.dev)!

## Team Mates:
- TrshPuppy
- Rulerlefi
- Turing_Moon_Yatch

# The Dream, the Vision, the Reality:
To satisfy the codejam requirements of coding a Twitch-related project which includes the theme of 'time', we decided to make a chat bot which can play Hot Potato with chatters!

## Setup:
### Make sure your bot is cloned into an environment which can run python code and install these required libraries:
- `twitchio.ext` (or `pip install twitchio`)
- `time`
- `json`
- `asynchio`
- `requests`

### Twitch Auth:
All of the values needed to authenticate with Twitch can be set in `data/api.json`. The JSON file looks like this with the valuse that need to be changed marked:
```json
{
  "OA_TOKEN": "oa_token",                                  # change this (OA_TOKEN)
  "CLIENT_ID": "client_id",                                # change this (CLIENT_ID)
  "CLIENT_SECRET": "client_secret",                        # change this (CLIENT_SECRET)
  "REDIRECT_URI": "http://localhost:3000",
  "CODE_FROM_LAST_REQUEST": "code",
  "SCOPE": "chat%3Aread+chat%3Aedit+channel%3Amoderate",
  "REFRESH_TOKEN": "refresh_token",                        # change this (REFRESH_TOKEN)
  "OA_EXPIRE": 13203,
  "LAST_REFRESH": 1689523922,
  "Bot": {
    "PREFIX": "!",
    "CHANNEL": "trshpuppy",                                # change this (CHANNEL)
    "STREAMER_NICK": "",                                   # optional (STREAMER_NICK)
    "BOT_USERNAME": "trsh_bot",                            # change this (BOT_USERNAME)
    "KEYWORD_PLURAL": "keywords",
    "KEYWORD_SINGULAR": "keyword",
    "MODLIST": [                                           # change this (MODLIST) 
      "<mod username>",                                    # Add chatters here who are authorized to start and stop the game
      "",
      ""
    ]
  }
}
```
#### Once the values are set:
The bot will check and refresh auth tokens on startup and every hour while running!

## Potato Game:
Once setup is complete, start the bot by running `python main.py` in your terminal. The bot will connect to the Twitch channel set in `data/api.json` under `Bot.CHANNEL`.
When you're ready to start a game, a moderator (listed in `api.json` under `Bot.MODLIST`) can use `!start` in chat to start the game.

### Joining the game:
After the `!start` command is called in chat, there is a 60 second lobby period. Chatters can join during this time by typing `!join`.

### Potato drops!
Once the 60 second lobby period has ended, and if there are enough joined players  (at least 3), the potato will drop into the hannds of a random player.

### Pass the potato:
The player who has the potato has 30 seconds to pass it. They can use `!pass @<player username>` to pass the potato. If they try to pass to themselves, or someone who isn't
playing (didn't join during the lobby) the bot will remind them of these rules. Depending on the number of players, a certain amount of passes have to happen before the same
chatter can have the potato again.

### Winning and Losing:
#### Lose state:
- If the player who has the potato doesn't pass it w/i 30 seconds of receiving it, chat loses the game.
#### Win state:
- If chat is able to keep the potato up before the game ends (5 minutes after starting) chat wins the game!

## Dreams for the future:
### Rewards for Winning:
In the future, we want to integrate a point system so if chat wins the game, they can receive points which can be used to buy perks/ redeems/ etc..
Due to how the Twitch API works, this would have to be a fake point currency.
