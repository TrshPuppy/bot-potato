def chatter_has_authority(ctx, mods):
    # Chatter should be in mod list, imported from data/api.json
    chatter_u = ctx.author.name
    if chatter_u.lower() in mods:
        return True
    return False
