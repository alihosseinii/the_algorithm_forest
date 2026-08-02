class GameState:
    def __init__(self, player_pos, wolf_pos, goal="V"):
        self.player_pos = player_pos
        self.wolf_pos = wolf_pos
        self.goal = goal
        self.score = 0
        self.turn_number = 1
        self.game_over = False
        self.won = False

    def snapshot(self):
        return {
            "player_pos": self.player_pos,
            "wolf_pos": self.wolf_pos,
            "score": self.score,
            "turn_number": self.turn_number,
        }

    def restore(self, snap):
        self.player_pos = snap["player_pos"]
        self.wolf_pos = snap["wolf_pos"]
        self.score = snap["score"]
        self.turn_number = snap["turn_number"]

    def __repr__(self):
        return (f"GameState(player={self.player_pos}, wolf={self.wolf_pos}, "
                f"score={self.score}, turn={self.turn_number})")