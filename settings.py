class Settings:
    '''a class to store all settings for alien invasion'''

    def __init__(self):
        '''initialize the game's static settings'''
        #screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (230,230,230)

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 1.5

        #bullets settings
        self.bullet_speed = 1.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        #how quickly the game speeds up
        self.speedup_scale = 1.1

        #how quickly the alien point value increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        #fleet direction of 1 represents right, -1 represents left
        #self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        '''initialize settings that change throughout the game'''
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1.0

        #fleet direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50

    def increase_speed(self):
        '''increase speed settings and alien point values'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        #print(self.alien_points)

