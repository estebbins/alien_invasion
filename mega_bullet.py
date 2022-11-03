import pygame
from pygame.sprite import Sprite

class MegaBullet(Sprite):
    """a class to manage bullets fired from the ship"""
    def __init__(self, ai_game):
        """create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #import bullet image
        self.image = pygame.image.load('/Users/emilystebbins/Desktop/alien_invasion/images/mega_bullet.bmp')

        #createa  bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0,0, 24, 60)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        """move the bullet up the screen"""
        #update the decimal position of the bullet
        self.y -= self.settings.mega_bullet_speed
        #Update the rect position.
        self.rect.y = self.y

    def draw_mega_bullet(self):
        """draw the bullet at it's current location"""
        self.screen.blit(self.image, self.rect)
