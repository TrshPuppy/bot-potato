class Player():
    def __init__(self, u, i, lp, tr, ct):
        self.id = i
        self.username = u
        self.last_passed = lp
        self.time_received = tr
        self.current_timeout = ct

       
def create_and_get_player(ctx):
    p_username = ctx.author.name
    p_id = ctx.author.id
    new_player = Player(p_username, p_id, 0, 1, 2)
    
    return new_player