class Settings:
    """a class to store all settings for Alien Invasion."""

    def __init__(self):
        """initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (69, 50, 145)

        #Ship settings
        self.ship_speed = 1.5

        #Bullet settings
        self.bullet_speed = 1.0
        #image is 12 by 15 instead of 3 by 15
        self.bullets_allowed = 5

        #MegaBullet settings
        self.mega_bullet_speed = 1.5
        #image is 48 by 60
        self.mega_bullets_allowed = 1

        #alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    


