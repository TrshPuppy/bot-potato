import json


def chatter_has_authority(ctx, mods):
    # Chatter should be in mod list, imported from data/api.json
    chatter_u = ctx.author.name
    if chatter_u.lower() in mods:
        return True
    return False


# def get_recent_chatters():
#     with open("data/chattters.json", "r") as f:
#         recent_chatters = json.load(f)

#     if len(recent_chatters) > 2:
#         print(f"Not enough recent chatters.")
#         return
