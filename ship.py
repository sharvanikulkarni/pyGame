import pygame

class Ship:
    def __init__(self, ai_game):
        '''initialise the ship and set its starting position'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #movement flag
        self.moving_right = False

    def update(self):
        '''update the ship's posistion based on the ovement flag '''
        if self.moving_right:
            self.rect.x +=1

    def blitme(self):
        '''draw the ship at its current location'''
        self.screen.blit(self.image, self.rect)