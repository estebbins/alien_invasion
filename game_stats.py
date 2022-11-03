import json

class GameStats:    
    """Track statistics for alien invasion"""  
    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        #start alien invasion in an active state
        self.game_active = False

        #High score should never be reset.
        self.high_score = self.get_saved_high_score()
        self.high_level = self.get_saved_high_level()

    def get_saved_high_score(self):
        """gets high score from file if it exists"""
        try:
            with open('high_score.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def get_saved_high_level(self):
        """gets high level from file if it exists"""
        try:
            with open('high_level.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return 1

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1