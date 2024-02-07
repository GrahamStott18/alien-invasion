# Imports the pygame module before defining the class.
import pygame

# Imports the Sprite class from pygame
from pygame.sprite import Sprite

# Creates a class for Alien, that is a child-class of Sprite (Sprite in paraenthesis indicates Alien is a child class of sprite)
class Alien(Sprite):
    """ A class to represent a single alien in the fleet"""

    # This instance needs the current instance of AlienInvasion, ie using ai_game in the init. 
    def __init__(self, ai_game):
        """ Initialize the alien and set its starting position"""

        # Calling super(), ensures the __init__ inherits properly from SPRITE
        super().__init__()
        # Assigns the screen to an attribute of Alien, so its easily accessible in all the methods in this class. 
        self.screen = ai_game.screen
        
        # Loads the settings of the Alien ship(s)
        self.settings = ai_game.settings
        
        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('python_projects/alieninvasion/images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)
        
        
    def check_edges(self):
        """ Return True if alien is at edge of screen"""
        
        screen_rect = self.screen.get_rect()
        # The alien is at the right edge if the right attribute of its rect is greater than or equal to the right attribute of the screens rect. 
        # The alien is at the left edge if its left value is less than or equal to 0.
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True      
        
        
    def update(self):
        """ Move the alien to the right or left"""
        
        # Tracks the aliens position, using the self.x attribute and moves the aliens by multiplying the aliens speed by the value of fleet_direction
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        # Updates the position of the aliens rect
        self.rect.x = self.x