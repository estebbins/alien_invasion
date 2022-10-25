class Settings:
    """a class to store all settings for Alien Invasion."""

    def __init__(self):
        """initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (69, 50, 145)

        #Ship settings
        self.ship_limit = 3

        #Bullet settings
        #image is 12 by 15 instead of 3 by 15
        self.bullets_allowed = 5

        #MegaBullet settings
        #image is 48 by 60
        self.mega_bullets_allowed = 1

        #alien settings
        self.fleet_drop_speed = 10

        #how quickly the game speeds up 
        self.speedup_scale = 1.1
        #how quickly alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed = 1
        self.bullet_speed = 2.0
        self.mega_bullet_speed = 1.5
        self.alien_speed = 1.0

        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.mega_bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)




    


