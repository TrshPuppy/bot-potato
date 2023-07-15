class Player:
    def __init__(self, u, i):
        self.id = i
        self.username = u
        self.last_passed = (
            0  # global turn number where this player last received the potato
        )
        # self.hasPotato = False  # This might make it easier for game to check players?

    def receive_potato(self, turn):
        print(f"Player {self.username} has been passed the potato")
        self.last_passed = turn

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):  # So python can make sure  two players aren't the same
        if isinstance(other, Player):
            return self.id == other.id
        return False
