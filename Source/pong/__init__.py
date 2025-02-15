# Language: Python

"""
Module: __init__.py

This module acts as the entry point for the Pong game package. It primarily
exposes the main game logic by importing the Game class from the game module.
This abstraction allows other parts of the application to interact with 
the Pong game without depending on its internal implementation details.
"""

# Import the Game class from the game module. This class encapsulates the core
# mechanics of the Pong game such as the game loop, event handling, and rendering.
from .game import Game