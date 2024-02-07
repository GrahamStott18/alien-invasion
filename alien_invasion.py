# Will use tools from this module to exit game when player quits
import sys

# Imports instance of sleep, to pause game (time is in Python standard library)
from time import sleep 

# Contains functionality to make game
import pygame

# Imports the Settings class from the settings.py file
from settings import Settings

# Imports the Ship class from the ship.py file
from ship import Ship

# Imports the Bullet class from the bullet.py file
from bullet import Bullet

# Imports the Alien class from the alien.py file
from alien import Alien

# Creates instance of GameStats
from game_stats import GameStats

# Imports scoreboard from Scoreboard.py file
from scoreboard import Scoreboard

# Imports button from the Button.py file
from button import Button


# Creates a class to setup the game within
class AlienInvasion:
    """The overall class to manage game assets and behaviors."""
    
    
    # self if a parameter that must always be called, when  declaring a new function or method.
    def __init__(self):
        """Initialize the game, and create game resources."""
        
        # Initializes PYGAME 
        pygame.init()
        # Calls the Settings class
        self.settings = Settings()
        
        # Establishes screen size, from the settings.py file
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Adds text caption to display
        pygame.display.set_caption("Alien Invasion")
        
        # Create instance to store game statistics, and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)   
        
        # Call to Ship(), This ia a parameter that gives Ship access to the game's resources, such as the screen object
        self.ship = Ship(self)
        
        # Calls the Bullets class
        self.bullets = pygame.sprite.Group()
        
        # Call the Aliens class
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        # Make the Play button.
        self.play_button = Button(self, "Play")
        
        # Sets the background color, in RGB.
        self.bg_color = (230, 230, 230)
       
        
    def run_game(self):
        """Start the main loop for the game."""
        
        # Starts a while loop.
        while True: 
            # Calls the _check_events() method on each pass of the loop 
            self._check_events()
            
            if self.stats.game_active:
                # Calls the ships update() method on each pass of the loop
                self.ship.update()
                # Calls the _update_bullets() method on each pass of the loop
                self._update_bullets()
                # Calls the _update_aliens() method on each pass of the loop
                self._update_aliens()
                
            # Calls the _update_screen() method on each pass of the loop
            self._update_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events"""
        
        # Watch for keyboard and mouse events, while game is running.
        for event in pygame.event.get():
            # If event triggers quit
            if event.type == pygame.QUIT:
                # Exits system
                sys.exit()
            # Else if, detects a KEYDOWN event (event where Key is pressed down)
            elif event.type == pygame.KEYDOWN:
               self._check_keydown_events(event)
            # Else if, detects when key released        
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # Detects if player clicks mouse button, anywhere on screen.    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # Deactivates button when game is active. 
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            # Reset the game statistics. 
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Hide the mouse cursor. 
            pygame.mouse.set_visible(False)
                
                    
    def _check_keydown_events(self, event):
        """Respond to keypresses"""     
                
         # Checks the right key for event
        if event.key == pygame.K_RIGHT:
            #  Move the ship to the right, based on setting in ship.py file
            self.ship.moving_right = True
        # Checks the left key for event
        if event.key == pygame.K_LEFT:
            #  Move the ship to the left, based on setting in ship.py file
            self.ship.moving_left = True
        # Check Q key for event
        elif event.key == pygame.K_q:
            # Exits system
            sys.exit()
        # Check for SPACE key event
        elif event.key == pygame.K_SPACE:
            # Fires bullet from ship
            self._fire_bullet()
        
               
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        
        # Checks the right key for event
        if event.key == pygame.K_RIGHT:
            # Stops moving to right
            self.ship.moving_right = False
        # Checks the left key for event
        if event.key == pygame.K_LEFT:
            # Stops moving to left
            self.ship.moving_left = False
            
    
    def _create_fleet(self):
        """ Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        # Create an alien
        alien = Alien(self)
        # Get alien's width & height from its rect attribute
        alien_width, alien_height = alien.rect.size 
        # Calculates the horizontal space available for aliens in a row. 
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # Calculates the number of aliens that can fit into that row space.
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        # Calculates available space for rows on screen.  
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        # Calcualates number of row that can fit on screen.
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens.
        # Creates the numbers of rows on screen. 
        for row_number in range(number_rows):
        # Create the first row of aliens. 
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    
    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge"""
        # Loops through the fleet and calls check_edges() on each  alien        
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # If check_edges() returns TRUE, fleet is at edge and reverses direction. 
                self._change_fleet_direction()
                break
            
    
    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            # Loops through all the aliens and dropeach one using the setting fleet_drop_speed
            alien.rect.y += self.settings.fleet_drop_speed
        # Changes fleet direction by multiplying valuse of fleet_direction current value by -1
        self.settings.fleet_direction *= -1
        
    
    def _create_alien(self, alien_number, row_number):
        """ Creates an alien and places it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size 
        # Calculates the HORIZONTAL space an alien takes up plus the empty space between it and the last, starting at zero.
        alien.x = alien_width + 2 * alien_width * alien_number
        # Sets the position of the alien's rect.
        alien.rect.x = alien.x
        # # Calculates the VERTICLE space an alien takes up plus the empty space between it and the last, starting at zero.
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # Add the newly created alien to the sprite group.
        self.aliens.add(alien)
    
    
    def _update_aliens(self):
        """ Check if the fleet is at the edge, then update the positions of all aliens in the fleet"""
        # Calls the _check_fleet_edges
        self._check_fleet_edges()     
        # Update alien fleet  
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
    
    
    def _ship_hit(self):
        """ Respond to the ship being hit by an alien"""
        # Loop checks the players ship count left, to continue to next ship if TRUE.
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # Pauses game for time specified 
            sleep(0.5)
            
        # If zero ships left, active game changed to FALSE.
        else:
            self.stats.game_active = False
            # Makes mouse visible, when game becomes inactive. 
            pygame.mouse.set_visible(True)
    
    
    def _check_aliens_bottom(self):
        """Check is any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # Alien reaches the bottom when its value is greater than or equal to the screen value. 
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    
            
    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group"""
        
        # When fired, checks that len(self.bullets) is less than the bullets allowed in settings.py, if so creates a new bullet.
        if len(self.bullets) < self.settings.bullets_allowed:
            # Creates new instance of Bullet
            new_bullet = Bullet(self)
            # Adds new bullet to the group
            # add() method is similar to append(), but its a method written specifically for Pygame groups
            self.bullets.add(new_bullet)
    
    
    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets"""
        
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared, by creating a loop for the copy() method by allowing us to modify them while inside the loop
        for bullet in self.bullets.copy():
            # Checks each bullet to see if it has disappeared off the top of the screen
            if bullet.rect.bottom <= 0:
                # Removes bullets that have disappeared from the screen
                self.bullets.remove(bullet)
        # Call to print() how many bullets exist in the game currently and verify deletion once at top of screen
        # print(len(self.bullets)) -- Took this out after testing.
        
        self._check_bullet_alien_collisions()
        
        
    def _check_bullet_alien_collisions(self):
        """ Respond to bullet-alien collisions"""
        
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        # Adds points to score as alien ships shot down. 
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level. 
            self.stats.level += 1
            self.sb.prep_level()
        
    
    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen"""
        
        # Redraw the screen during each pass through the loop, from the settings.py file
        self.screen.fill(self.settings.bg_color)
        # Draws the ship on the screen.
        self.ship.blitme()
        
        # Creates loop through the sprites in bullets
        for bullet in self.bullets.sprites():
            # Calls draw_bullets on each pass of the loop
            bullet.draw_bullet()
        # Draws the alien on the screen
        self.aliens.draw(self.screen)
        
        # Draw the score information.
        self.sb.show_score()
        
        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
                
        # Make the most recently drawn screen visible. 
        pygame.display.flip()
        
            
if __name__ == '__main__':
    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    # Puts run_game in an IF block that only runs if the file is called directly.
    ai.run_game()