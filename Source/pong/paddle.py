# Language: Python
"""
Module: paddle.py

This module defines the Paddle class for the AI-controlled Pong game.
It is responsible for rendering, movement, and position resetting of each paddle.
Target Users: Developers and researchers in AI game development.
Code Style: PEP8
"""

import pygame

class Paddle:
    """
    Represents a paddle used in the Pong game.
    
    This class manages the paddle's appearance and movement logic. The paddle can move
    vertically within the game window and be reset to its starting position.
    
    Attributes:
        VEL (int): The speed (velocity) at which the paddle moves.
        WIDTH (int): The fixed width of the paddle.
        HEIGHT (int): The fixed height of the paddle.
        x (int): The current horizontal position of the paddle.
        y (int): The current vertical position of the paddle.
        original_x (int): The initial horizontal coordinate, used for resetting.
        original_y (int): The initial vertical coordinate, used for resetting.
    """
    VEL = 4
    WIDTH = 20
    HEIGHT = 100

    def __init__(self, x, y):
        """
        Initializes a Paddle instance at the specified coordinates.
        
        The starting position is recorded so that the paddle can be reset to this position later.
        
        Args:
            x (int): The x-coordinate for the paddle's initial position.
            y (int): The y-coordinate for the paddle's initial position.
        """
        # Store both the current and the original positions to allow future resets.
        self.x = self.original_x = x
        self.y = self.original_y = y

    def draw(self, win):
        """
        Draws the paddle on the specified game window.
        
        This method uses Pygame's drawing functions to render the paddle as a white rectangle.
        The choice of white ensures good visibility against the game background.
        
        Args:
            win (pygame.Surface): The surface representing the game window.
        """
        # Render the paddle as a rectangle using its current position and fixed dimensions.
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def move(self, up=True):
        """
        Adjusts the paddle's vertical position based on the specified direction.
        
        The movement is constrained by a fixed velocity to ensure consistent paddle speed.
        This function avoids any additional logic so that boundary handling can be managed elsewhere.
        
        Args:
            up (bool, optional): If True, move the paddle upward; otherwise, move it downward.
                Defaults to True.
        """
        # Subtracting VEL decreases the y-coordinate, which moves the paddle upward.
        if up:
            self.y -= self.VEL
        # Adding VEL increases the y-coordinate, which moves the paddle downward.
        else:
            self.y += self.VEL

    def reset(self):
        """
        Resets the paddle's position to its original starting coordinates.
        
        This method is crucial when restarting the game or after a score, ensuring
        that the paddle returns to its default position for consistent gameplay.
        """
        # Restore initial x and y coordinates to recover starting position.
        self.x = self.original_x
        self.y = self.original_y