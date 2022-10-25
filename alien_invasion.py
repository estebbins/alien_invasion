import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from mega_bullet import MegaBullet
from alien import Alien

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
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.mega_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #watch for keyboard and mouse events
            #to access the events that pygame detects uses the function below
            #which returns a list of events that have taken place since the
            #last time the fucntion was called
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            #move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_m:
            self._fire_mega_bullet()

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets)+len(self.mega_bullets) <self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_mega_bullet(self):
        """create mega bullet and add it to bullets group"""
        if len(self.bullets)+len(self.mega_bullets) <self.settings.bullets_allowed:
            if len(self.mega_bullets) < self.settings.mega_bullets_allowed:
                new_mega_bullet = MegaBullet(self)
                self.mega_bullets.add(new_mega_bullet)

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        self.bullets.update()
        self.mega_bullets.update()
        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for mega_bullet in self.mega_bullets.copy():
            if mega_bullet.rect.bottom <= 0:
                self.mega_bullets.remove(mega_bullet)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #Make an alien
        alien = Alien(self)
        self.aliens.add(alien)

    def _create_fleet(self):
        """create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        #Create a first row of aliens
        for alien_number in range(number_aliens_x):
            #Create an alien and place it in the row
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)

    def _update_screen(self):
        """update images on the screen flip to a new screen"""
        #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for mega_bullet in self.mega_bullets.sprites():
            mega_bullet.draw_mega_bullet()
        self.aliens.draw(self.screen)

        #make the most recently drawn screen visible. 
        pygame.display.flip()


if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()

