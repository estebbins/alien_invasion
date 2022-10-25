import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initiaize the game and create game resources"""

        #function initializes background settings pygame needs to work 
        pygame.init()
        self.settings = Settings()

        #call pygame.display.set_mode(()) to create display window
        #1200,800 are the dimensions of the screen defined in a tuple in settings
        #file
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #watch for keyboard and mouse events
            #to access the events that pygame detects uses the function below
            #which returns a list of events that have taken place since the
            #last time the fucntion was called
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            #make the most recently drawn screen visible. 
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()

