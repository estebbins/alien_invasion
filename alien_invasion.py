import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        #create an istance to store game statistics
        #and create scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.mega_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #watch for keyboard and mouse events
            #to access the events that pygame detects uses the function below
            #which returns a list of events that have taken place since the
            #last time the fucntion was called
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

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
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        #reset game statistics
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()

        #get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()
        self.mega_bullets.empty()

        #create a new sleet and center the shiop
        self._create_fleet()
        self.ship.center_ship()

        #hide mouse cursor
        pygame.mouse.set_visible(False)

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

    def _create_fleet(self):
        """create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row
        #Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2* alien_width)

        # Determine the number rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
            (3* alien_height) - ship_height)
        number_rows = available_space_y // (2* alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            """Create an alien and place it in the row"""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """respond to bullet-alien collisions"""
        #check for bullets that have hit aliens
        #if so, get rid of the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        collisions_mega = pygame.sprite.groupcollide(
            self.mega_bullets, self.aliens, False, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if collisions_mega:
            for aliens in collisions_mega.values():
                self.stats.score += (self.settings.alien_points * 1.5) * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self.mega_bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _ship_hit(self):
        """Respond to the shit being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships_left
            self.stats.ships_left -= 1

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            self.mega_bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            #treat this the same as if the ship got hit
                self._ship_hit()
                break

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

        #draw the score info
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        #make the most recently drawn screen visible. 
        pygame.display.flip()

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

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """
        check if fleet is at an edge, 
        then update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()

