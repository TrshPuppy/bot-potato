class Game():
    def __init__(self):
        self.start_time = 0
        self.active = False
        self.num_passes = 0
        self.current_player = None
        self.active_players = []

    def start_game(self, st):
        self.start_time = st
        self.active = True

    def end_game(self, et):
        self.active = False
        # self.end_time = et

    def check_for_player(self, p):
        if p in self.active_players:
            return True
        return False

    def player_join_game(self, player):
        self.active_players.append(player)

    def get_game_state(self):
        return "game stats"


# def start_new_game(player):

