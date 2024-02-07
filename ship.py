# Imports the pygame module before defining the class.
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""
    
    def __init__(self, ai_game): 
        """Initializes the ship and set its starting position."""
        super().__init__()
        
        # Assigns the screen to an attribute of Ship, so its easily accessible in all the methods in this class. 
        self.screen = ai_game.screen
        # Creates a settings attribute for Ship
        self.settings = ai_game.settings
        # Accesses the screens rect attribute and assigns it to self.screen_rect (rect = rectangle)
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load the ship image and get its rect.
        self.image = pygame.image.load('python_projects/alieninvasion/images/ship.bmp')
        self.rect = self.image.get_rect()
        
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        
        # Store a decimal value for the ship's horizontal position, float() converts value of self.rect to a decimal and assigns the value to self.x
        self.x = float(self.rect.x)
        
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        
        
    def update(self):
        """Update the ship's position based on the movement flags."""
        
        ## Update the ship's x value, not the rect. 
        # Moves the ship right if true, but limits to right edge of screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # Moves the ship left if true, but limits to left edge of screen (0 = left edge of screen in pygame)
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Update rect object from self.x
        self.rect.x = self.x
        
        
    def blitme(self):
        """Draw the ship at its current location."""
        
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)