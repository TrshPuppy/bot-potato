import time

DEFAULT_TIME_TO_PASS = 30

class Player():
    def __init__(self, u, i):
        self.id = i
        self.username = u
        self.last_passed = 0 # the last time the potato was received
        self.time_received = 0
        self.current_timeout = 0 # the decreasing ammount of time player has to pass
        self.hasPotato = False # This might make it easier for game to check players?
        
    def receive_potato(self, po):
        self.time_received = time.time()
        self.last_passed = time.time() # set when they receive potato (vs when they pass it?)
        self.hasPotato = True
        self.current_timeout = DEFAULT_TIME_TO_PASS

    def check_countdown(self):
        time_now = time.time()
        time_left_to_pass = self.current_timeout - time_now
        self.current_timeout = time_left_to_pass

        if time_left_to_pass < 0:
            return 0
        
        return time_left_to_pass        
    
def create_and_get_player(ctx):
    p_username = ctx.author.name
    p_id = ctx.author.id
    new_player = Player(p_username, p_id, 0, 1, 2)
    
    return new_player