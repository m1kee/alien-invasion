class GameStats:
    """All the main stats of the game"""

    def __init__(self, game):
        """Initialize all the stats"""
        self.ship_lives = game.settings.ship_lives
        self.settings = game.settings
        self.game_active = False
        self.game_paused = False
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """Initialize all stats that could change during the game"""
        self.ship_lives = self.settings.ship_lives
        self.score = 0
        self.level = 1
