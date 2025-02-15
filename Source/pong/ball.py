# Language: Python
"""
Module: ball.py

This module is responsible for managing the ball object used in the AI-controlled Pong game.
It handles the initialization, movement, drawing, and resetting of the ball state.

Project Type: AI-controlled Pong game
Key Functionalities: Ball movement, collision handling, and game state resetting
Target Users: Developers and researchers in AI game development
"""

import pygame
import math
import random

class Ball:
    """
    Represents the moving ball in the Pong game.

    The Ball class encapsulates all properties and behaviors of the game ball, including its movement,
    drawing on the game window, and resetting its position and velocity for a new play session. 
    It leverages randomization for unpredictable initial conditions, enhancing the game's challenge.

    Attributes:
        MAX_VEL (int): Maximum speed the ball is allowed.
        RADIUS (int): Visual radius of the ball.
        x (float): Current horizontal position.
        y (float): Current vertical position.
        original_x (float): Initial horizontal position, used for resets.
        original_y (float): Initial vertical position, used for resets.
        x_vel (float): Current horizontal movement velocity.
        y_vel (float): Current vertical movement velocity.
    """
    MAX_VEL = 5  # Limit the ball's horizontal speed for consistent gameplay.
    RADIUS = 7   # Define the ball size for rendering and collision checks.

    def __init__(self, x, y):
        """
        Initializes the ball's state at a given position and assigns an initial random velocity.

        The ball's velocity is initialized using a random angle to ensure varied gameplay,
        while the direction (left/right) is also randomized. This design creates a dynamic game
        start scenario by not favoring any fixed trajectory.

        Args:
            x (float): Starting horizontal position.
            y (float): Starting vertical position.
        """
        # Store the provided position as both current and original positions.
        self.x = self.original_x = x
        self.y = self.original_y = y

        # Calculate a random angle within a range that avoids strictly horizontal movement.
        angle = self._get_random_angle(-30, 30, [0])

        # Decide initial horizontal direction randomly for an unpredictable game start.
        pos = 1 if random.random() < 0.5 else -1

        # Set the velocity components using trigonometric computations.
        # The 'abs' function ensures positive magnitude, while 'pos' assigns the direction.
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL

    def _get_random_angle(self, min_angle, max_angle, excluded):
        """
        Generates a random angle (in radians) within a specified range, excluding undesired values.

        This method is essential to ensure that the ball never starts moving straight horizontally,
        which can reduce the game's dynamic behavior. The loop continues until an acceptable angle is found.

        Args:
            min_angle (int): Lower bound for angle generation in degrees.
            max_angle (int): Upper bound for angle generation in degrees.
            excluded (list): List of angles (in degrees) that should not be selected.

        Returns:
            float: Valid random angle in radians.
        """
        angle = 0  # Initialize angle to ensure loop entry.
        # Continue generating until the angle isn't in the excluded list.
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        # Return the computed angle in radians for accurate motion calculations.
        return angle

    def draw(self, win):
        """
        Renders the ball on the given Pygame window.

        Uses Pygame's drawing functions to represent the ball visually on the game surface.
        White color is used to contrast with potential dark game backgrounds.

        Args:
            win (pygame.Surface): The game window or surface to draw the ball on.
        """
        # The position must be converted to integers as Pygame expects pixel positions.
        pygame.draw.circle(win, (255, 255, 255), (int(self.x), int(self.y)), self.RADIUS)

    def move(self):
        """
        Updates the ball's position based on its current velocity.

        This method accumulates the velocity to the current position, simulating a simple linear motion.
        It forms the basis of the ball movement logic and is called on every frame update.
        """
        # Update position coordinates by incorporating the current velocities.
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """
        Resets the ball to its initial position and recalculates its velocity.

        This method is crucial when restarting a game or after a score, ensuring the ball
        starts from a consistent state and with a fresh, unpredictable velocity.
        """
        # Reinstate the ball's original coordinates.
        self.x = self.original_x
        self.y = self.original_y

        # Generate a new random angle ensuring non-horizontal movement.
        angle = self._get_random_angle(-30, 30, [0])
        
        # Recalculate the vertical velocity component with the new angle.
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL
        self.y_vel = y_vel

        # Reverse horizontal direction on reset to alternate gameplay dynamics.
        self.x_vel *= -1