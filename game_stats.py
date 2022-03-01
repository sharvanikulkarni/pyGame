class GameStats:
    '''track statistics for Alien Invasion'''

    def __init__(self,ai_game):
        '''initialize statistics'''
        self.settings = ai_game.settings
        self.reset_stats()
        #start game in the inactive state
        self.game_active = False

    def reset_stats(self):
        #initialize stats that can change during the game
        self.ships_left = self.settings.ship_limit
        self.score = 0