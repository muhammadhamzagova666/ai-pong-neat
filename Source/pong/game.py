# Language: Python
"""
Module: game.py

This module implements the core gameplay logic for the AI-controlled Pong game.
It manages the rendering, collisions, scoring, and data reporting of game events,
providing a robust interface for both human and AI-controlled interactions.

Key Functionalities:
- Game loop management and state updates.
- Dynamic rendering of game elements (paddles, ball, scores, and hit counts).
- Collision detection and response logic.
- Support for real-time score and hit tracking.

Target Users:
Developers and researchers integrating AI in real-time gaming environments.
"""

from .paddle import Paddle
from .ball import Ball
import pygame
import random

pygame.init()

class GameInformation:
    """
    Data structure capturing the current state of the game.

    This structure is used to report scores and hit counts after each game iteration,
    facilitating tracking and adjustments during AI training.

    Attributes:
        left_hits (int): Number of successful paddle-ball hits by the left player.
        right_hits (int): Number of successful paddle-ball hits by the right player.
        left_score (int): Score tally for the left player.
        right_score (int): Score tally for the right player.
    """
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score

class Game:
    """
    Core game engine for the Pong game.

    Responsible for initializing game elements, rendering game frames,
    managing collisions, and updating game state. This class also
    encapsulates the logic to adjust paddle and ball behaviors based on game interactions.

    Attributes:
        SCORE_FONT (pygame.font.Font): Font used for rendering scores.
        WHITE (tuple): RGB color code for white.
        BLACK (tuple): RGB color code for black.
        RED (tuple): RGB color code for red (used for hit counts).
        window_width (int): Width of the game window.
        window_height (int): Height of the game window.
        left_paddle (Paddle): Left player's paddle.
        right_paddle (Paddle): Right player's paddle.
        ball (Ball): Ball instance representing the moving object.
        left_score (int): Score counter for the left player.
        right_score (int): Score counter for the right player.
        left_hits (int): Hit counter for the left paddle.
        right_hits (int): Hit counter for the right paddle.
        window (pygame.Surface): Pygame window surface where the game is rendered.
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        """
        Initializes the game environment with paddles, ball, and score counters.

        Uses window dimensions to centrally position game elements.
        This ensures a balanced gameplay initiation every time the game runs.

        Args:
            window (pygame.Surface): Window in which the game will be rendered.
            window_width (int): Width of the game window.
            window_height (int): Height of the game window.
        """
        self.window_width = window_width
        self.window_height = window_height
        
        # Initialize paddles at contrasting edges with vertical centering.
        self.left_paddle = Paddle(10, self.window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(self.window_width - 10 - Paddle.WIDTH, self.window_height // 2 - Paddle.HEIGHT // 2)
        
        # Center the ball to start the game.
        self.ball = Ball(self.window_width // 2, self.window_height // 2)
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
        self.window = window

    def _draw_score(self):
        """
        Renders the score for each player on the game screen.

        The scores are centrally aligned to provide immediate feedback on the game status.
        """
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", True, self.WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", True, self.WHITE)
        # Position scores relative to window width for balanced display.
        self.window.blit(
            left_score_text,
            (self.window_width // 4 - left_score_text.get_width() // 2, 20)
        )
        self.window.blit(
            right_score_text,
            (int(self.window_width * (3 / 4)) - right_score_text.get_width() // 2, 20)
        )

    def _draw_hits(self):
        """
        Renders the combined hit counter on the game screen.

        Displays the total number of paddle-ball hits using a distinct color (red)
        to visually differentiate it from scores.
        """
        hits_text = self.SCORE_FONT.render(f"{self.left_hits + self.right_hits}", True, self.RED)
        self.window.blit(
            hits_text,
            (self.window_width // 2 - hits_text.get_width() // 2, 10)
        )

    def _draw_divider(self):
        """
        Draws a central dashed line divider on the game window.

        Enhances game aesthetics and assists visual tracking of the ball's movement.
        """
        for i in range(10, self.window_height, self.window_height // 20):
            # Skip odd sections to create a dashed effect.
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window,
                self.WHITE,
                (self.window_width // 2 - 5, i, 10, self.window_height // 20)
            )

    def _handle_collision(self):
        """
        Processes all collision events between the ball, paddles, and screen edges.

        Adjusts the ball's velocity based on collision impact points and increments
        hit counters. The logic ensures realistic deflections and maintains game dynamics.
        """
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        # Check vertical collisions: if the ball touches top or bottom edges.
        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1  # Invert vertical speed to mimic a bounce.
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1
        
        # Process collision with left paddle.
        if ball.x_vel < 0:
            if left_paddle.y <= ball.y <= left_paddle.y + Paddle.HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1  # Reverse horizontal direction.
                    # Adjust vertical velocity based on distance from paddle center.
                    middle_y = left_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    # Reduction factor ensures velocity adjustments are proportional.
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    ball.y_vel = -1 * (difference_in_y / reduction_factor)
                    self.left_hits += 1  # Increment left hit counter.
        # Process collision with right paddle.
        else:
            if right_paddle.y <= ball.y <= right_paddle.y + Paddle.HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1  # Reverse horizontal direction.
                    middle_y = right_paddle.y + Paddle.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Paddle.HEIGHT / 2) / ball.MAX_VEL
                    ball.y_vel = -1 * (difference_in_y / reduction_factor)
                    self.right_hits += 1  # Increment right hit counter.

    def draw(self, draw_score=True, draw_hits=False):
        """
        Renders all game elements on the screen for each frame.

        Combines the rendering of the background, divider, paddles, ball,
        and optionally, the scores and hit counts for real-time game feedback.

        Args:
            draw_score (bool, optional): If True, display player scores. Defaults to True.
            draw_hits (bool, optional): If True, display total hits count. Defaults to False.
        """
        self.window.fill(self.BLACK)  # Clear the screen to prepare for new rendering.
        self._draw_divider()          # Draw the center divider line.
        
        if draw_score:
            self._draw_score()        # Overlay the scores on the screen.
        if draw_hits:
            self._draw_hits()         # Overlay combined hit count if required.
        
        # Render all movable game elements.
        for paddle in (self.left_paddle, self.right_paddle):
            paddle.draw(self.window)
        self.ball.draw(self.window)

    def move_paddle(self, left=True, up=True):
        """
        Moves the specified paddle in the controlled direction.

        Checks window boundaries before movement to avoid out-of-bound errors.
        This pre-validation ensures that paddle movements are realistic and contained.

        Args:
            left (bool, optional): Selects the left paddle if True, else the right paddle. Defaults to True.
            up (bool, optional): Determines the direction of movement; up if True, down if False. Defaults to True.

        Returns:
            bool: True if the paddle has moved; False if movement was blocked by window limits.
        """
        if left:
            # Prevent upward movement if already at the top.
            if up and self.left_paddle.y - Paddle.VEL < 0:
                return False
            # Prevent downward movement if paddle would go off screen.
            if not up and self.left_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.left_paddle.move(up)
        else:
            if up and self.right_paddle.y - Paddle.VEL < 0:
                return False
            if not up and self.right_paddle.y + Paddle.HEIGHT > self.window_height:
                return False
            self.right_paddle.move(up)
        return True

    def loop(self):
        """
        Executes a single iteration of the game loop.

        Updates the ball's position, handles collisions,
        manages score updates when the ball goes out of bounds, and
        constructs a snapshot of the current game state.

        Returns:
            GameInformation: Object encapsulating the current scores and hit counts.
        """
        self.ball.move()         # Progress ball movement based on its velocity.
        self._handle_collision() # Process any collisions to adjust trajectory.
        
        # Check if ball has passed beyond the left boundary.
        if self.ball.x < 0:
            self.ball.reset()    # Reset ball position and velocity.
            self.right_score += 1
        # Check if ball has passed beyond the right boundary.
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1
        
        # Package game metrics for external tracking and debugging.
        return GameInformation(self.left_hits, self.right_hits, self.left_score, self.right_score)

    def reset(self):
        """
        Reinitializes the entire game state, restoring initial positions and resetting scores.

        Useful when starting a new game session after a score or a training run.
        """
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0