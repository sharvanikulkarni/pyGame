import sys
from time import sleep
from matplotlib.style import available
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    '''overall class to manage game assets and behaviour'''

    def __init__(self):
        '''initalize the game and create game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #set the background color
        self.bg_color = (230,230,230)

    def run_game(self):
        '''start the main loop for the game'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_bullets(self):
        '''update position of bullets and get rid of old bullets'''
        #update bullet position
        self.bullets.update()
            

        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collisions()        
    
    def _check_bullet_alien_collisions(self):
        '''respond to bullet alien collision'''
        #remove any bullets and aliens that have collided
        #check for any bullets that have hit the aliens
        #if so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _check_events(self):
        '''respond to keypresses and mouse events'''
        #Watch for keyboard and mouse movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        '''respondes to keypresses'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''create a new bullet and add it to the bullet group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        #redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #make the most recently drawn screen visible.
        pygame.display.flip()

    def _create_fleet(self):
        '''create a fleet of aliens'''
        #create an alien and find the number of aliens in a row
        #spaceing between each alien is equal to one alien width
        #make an alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3* alien_height) - ship_height)
        
        number_rows = available_space_y // (2*alien_height)

        #create the full fleet of aliens
        for row_number in range(number_rows):
            #create the first row of aliens
            for alien_number in range(number_aliens_x):
            #create an alien and place it in a row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''create an aien and place it in the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        #alien_width = alien.rect.width
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
        self.aliens.add(alien)


    def _update_aliens(self):
        '''update the position of all the aliens in the fleet'''
        '''check if the fleet is at an edge then update the position of all aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()

        #look for aliens hitting bottom of the screen.
        self._check_aliens_bottom()


    
    def _check_fleet_edges(self):
        '''respond appropriately if any alien have reached an edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
            '''drop the entire fleet and change the fleet's direction'''
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

    def _ship_hit(self):
        '''respond to the ship being hit by the alien'''
        if self.stats.ships_left > 0:
            #decrement ship_left
            self.stats.ships_left -= 1

            #get rid of any alien or bullets
            self.aliens.empty()
            self.bullets.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        '''check if any aliens have reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #trat this the same as if the ship is hit
                self._ship_hit()
                break


if __name__=='__main__':
    #make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()



