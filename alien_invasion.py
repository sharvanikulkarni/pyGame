import sys
import pygame
from settings import Settings

class AlienInvasion:
    '''overall class to manage game assets and behaviour'''

    def __init__(self):
        '''initalize the game and create game resources'''
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #set the background color
        self.bg_color = (self.settings.bg_color)

    def run_game(self):
        '''start the main loop for the game'''
        while True:
            #Watch for keyboard and mouse movemnt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)

            #make the most recently drawn screen visible.
            pygame.display.flip()

    
if __name__=='__main__':
    #make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()



