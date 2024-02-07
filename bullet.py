# Contains functionality to make game
import pygame

# Imports the Sprite class from pygame
from pygame.sprite import Sprite


# Creates a class for Bullet, that is a child-class of Sprite (Sprite in paraenthesis indicates Buttle is a child class of sprite)
class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    
    
    # This instance needs the current instance of AlienInvasion, ie using ai_game in the init. 
    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position"""
        
        # Calling super(), ensures the __init__ inherits properly from SPRITE
        super().__init__()
        # Connects bullet screen with the Alien Invasion game screen
        self.screen = ai_game.screen
        # Connects bullet settings with the Alien Invasion game settings
        self.settings = ai_game.settings
        # Connects bullet color with the settings.py file
        self.color = self.settings.bullet_color
        
        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # Sets the bullet's midtop attribute to match the ship's midtop attribute
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # Store the bullet's position as a decimal value, allows fine adjustment to bullet speed
        self.y = float(self.rect.y)
        
        
    def update(self):
        """Move the bullet up the screen"""
        
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
        
    
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        
        # Fills the part of the screen defined by the bullet's rect with the color stored in self.color
        pygame.draw.rect(self.screen, self.color, self.rect)