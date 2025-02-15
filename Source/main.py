# Language: Python

"""
Module: main.py

This module serves as the entry point for an AI-controlled Pong game using the NEAT algorithm.
It manages game initialization, AI training through genome evaluation, checkpoint restoration,
and testing of the best evolved network. The implementation follows the PEP8 style and includes
detailed documentation to facilitate maintainability and ease onboarding for future developers.

Key Functionalities:
- Game initialization with Pygame for a Pong game.
- AI training using NEAT by evaluating genomes in competitive matches.
- Real-time game simulation with both human controls and AI-controlled paddles.
- Periodic checkpointing to allow training resumes and saving of the best performing genome.

Target Users:
Developers and researchers focused on integrating AI with game development.
"""

from pong import Game
import pygame
import neat
import os
import time
import pickle
import glob

class PongGame:
    """
    Manages the game logic and AI interaction for the Pong game.
    
    This class initializes game elements, processes game loops for both training and testing,
    and adjusts genome fitness based on game events.
    """
    def __init__(self, window, width, height):
        """
        Initializes the Pong game interface and obtains game entities.
        
        Args:
            window (pygame.Surface): The Pygame display surface.
            width (int): The width of the game window.
            height (int): The height of the game window.
        """
        # Create a new game instance with display settings
        self.game = Game(window, width, height)
        # Retrieve key game elements for later updates and controls
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle

    def test_ai(self, net):
        """
        Plays a live session of Pong to test a single AI network.
        
        This method initializes a game loop where the given neural network (net) controls
        the right paddle while the left paddle can be controlled manually via keyboard input.
        
        Args:
            net (neat.nn.FeedForwardNetwork): The neural network to be evaluated.
        """
        clock = pygame.time.Clock()  # Maintain consistent FPS
        run = True  # Game loop control flag
        
        while run:
            # Cap the frame rate for smooth gameplay and reproducible behavior
            clock.tick(144)
            game_info = self.game.loop()
            
            # Process system events and user exit requests
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            
            # Activate the network with current game state details to determine paddle movement.
            # The neural network receives inputs: paddle vertical position, horizontal distance to the ball,
            # and ball vertical position.
            output = net.activate((self.right_paddle.y, abs(self.right_paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))
            
            # Map the neural network decision to paddle motion:
            # decision == 1 -> move up; decision == 2 -> move down; otherwise, do not move.
            if decision == 1:
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:
                self.game.move_paddle(left=False, up=False)
            
            # Allow manual control for the left paddle using keyboard inputs.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)
            
            # Refresh game visuals and display debugging score information if needed.
            self.game.draw(draw_score=True)
            pygame.display.update()

    def train_ai(self, genome1, genome2, config, draw=False):
        """
        Trains two AI agents by pitting their derived networks against each other.
        
        This method simulates a game between two genomes and updates their fitness scores
        based on performance (hits or errors) and game duration. The 'draw' parameter allows
        for visual debugging during training sessions.
        
        Args:
            genome1 (neat.DefaultGenome): Genome representing the first AI agent.
            genome2 (neat.DefaultGenome): Genome representing the second AI agent.
            config (neat.Config): NEAT configuration parameters.
            draw (bool, optional): Flag to visualize game elements and score updates. Defaults to False.
        
        Returns:
            bool: True if user-triggered exit occurred, False otherwise.
        """
        run = True
        start_time = time.time()  # Record the start time to compute game duration
        
        # Convert genomes to feed-forward networks based on the provided configuration.
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        # Store genome references for later fitness adjustments.
        self.genome1 = genome1
        self.genome2 = genome2
        
        max_hits = 50  # Limit the number of paddle hits to prevent endless games
        while run:
            # Handle potential exit events from the user.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True  # Immediate termination on quit
            
            game_info = self.game.loop()  # Process game state update
            
            # Update the paddle positions based on neural network decisions.
            self.move_ai_paddles(net1, net2)
            
            # Optionally, refresh the game visuals for debugging.
            if draw:
                self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()
            
            duration = time.time() - start_time  # Elapsed game time
            
            # End the game if a score occurs or if maximum hits are reached.
            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits >= max_hits:
                self.calculate_fitness(game_info, duration)
                break
        return False

    def move_ai_paddles(self, net1, net2):
        """
        Determines and applies moves for both AI-controlled paddles.
        
        This method feeds game state information into each AI network to decide on movement.
        It penalizes indecisive or invalid moves to evolve better strategies over successive generations.
        
        Args:
            net1 (neat.nn.FeedForwardNetwork): Neural network for the left paddle.
            net2 (neat.nn.FeedForwardNetwork): Neural network for the right paddle.
        """
        # Pair each genome with its associated network and paddle direction.
        players = [
            (self.genome1, net1, self.left_paddle, True),
            (self.genome2, net2, self.right_paddle, False)
        ]
        for (genome, net, paddle, left) in players:
            # Obtain a decision based on the current state: paddle position, ball's horizontal distance, and ball's vertical position.
            output = net.activate((paddle.y, abs(paddle.x - self.ball.x), self.ball.y))
            decision = output.index(max(output))
            
            # Penalize neutral decisions to encourage proactive moves.
            if decision == 0:
                genome.fitness -= 0.01
            # Attempt to move the paddle; if the move is invalid (e.g., paddle at the screen edge), impose a heavier penalty.
            elif decision == 1:
                valid = self.game.move_paddle(left=left, up=True)
            else:
                valid = self.game.move_paddle(left=left, up=False)
            if not valid:
                genome.fitness -= 1

    def calculate_fitness(self, game_info, duration):
        """
        Enhances genome fitness scores based on in-game performance metrics.
        
        Genome fitness is incremented by the number of successful paddle hits and the overall
        duration of the match, rewarding both efficiency and longevity in gameplay.
        
        Args:
            game_info (GameInfo): A structure containing game metrics (e.g., hit counts, scores).
            duration (float): The elapsed time (in seconds) for which the game ran.
        """
        self.genome1.fitness += game_info.left_hits + duration
        self.genome2.fitness += game_info.right_hits + duration

def eval_genomes(genomes, config):
    """
    Evaluates multiple genomes by orchestrating head-to-head Pong matches.
    
    This function iterates over each pair of genomes, resets their fitness to ensure a fair competition,
    and then runs training sessions between the corresponding AI agents. Progress is printed in percentage
    to monitor the evaluation progress.
    
    Args:
        genomes (list): A list of tuples (genome_id, genome), representing the competitors.
        config (neat.Config): NEAT algorithm configuration parameters.
    """
    width, height = 700, 500  # Define dimensions for the game display
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    
    # Evaluate each genome compared with subsequent genomes to cover all possible pairs
    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i / len(genomes) * 100), end=" ")  # Inform progress in percentage
        genome1.fitness = 0  # Reset fitness score for a fresh evaluation
        for _, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            # Ensure genome2 has a valid fitness score before evaluation.
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            pong = PongGame(win, width, height)
            force_quit = pong.train_ai(genome1, genome2, config, draw=True)
            if force_quit:
                quit()  # Allow immediate exit on user request

def find_latest_checkpoint():
    """
    Returns the most recent NEAT checkpoint file from the 'checkpoints' directory.
    
    This function uses file creation times to select the latest saved checkpoint,
    allowing training sessions to resume from the best-known state.
    
    Returns:
        str or None: The filename of the latest checkpoint, or None if no checkpoint exists.
    """
    list_of_files = glob.glob('checkpoints/neat-checkpoint-*')
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def run_neat(config, total_generations):
    """
    Initiates and resumes (if applicable) the NEAT training process.
    
    The function attempts to locate an existing checkpoint. If found and training is
    not complete, it resumes the training session. Otherwise, it starts a new training session.
    
    Args:
        config (neat.Config): NEAT algorithm configuration parameters.
        total_generations (int): Total number of generations to train.
    """
    latest_checkpoint = find_latest_checkpoint()
    if latest_checkpoint:
        # Extract the generation number from the filename and resume training.
        generation_number = int(latest_checkpoint.split('-')[-1]) + 1
        if generation_number >= total_generations:
            print(f"{total_generations} generations completed. Skipping training.")
            return
        print(f"Resuming from checkpoint: {latest_checkpoint}")
        p = neat.Checkpointer.restore_checkpoint(latest_checkpoint)
    else:
        print("No checkpoints found. Starting new training session.")
        p = neat.Population(config)
    
    # Attach reporters for real-time progress, statistics, and automatic checkpointing.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1, filename_prefix='checkpoints/neat-checkpoint-'))
    
    # Execute the NEAT algorithm and save the best performing genome.
    winner = p.run(eval_genomes, total_generations - (generation_number if latest_checkpoint else 0))
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_best_network(config):
    """
    Plays a live game using the best evolved neural network.
    
    This function loads the best genome from disk, reconstructs its neural network, and
    launches a playable game session to demonstrate its performance.
    
    Args:
        config (neat.Config): NEAT configuration detailing genome and network structures.
    """
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    
    width, height = 700, 500  # Define game window dimensions.
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    
    pong = PongGame(win, width, height)
    pong.test_ai(winner_net)

if __name__ == '__main__':
    """
    Main entry point of the application.
    
    The script loads the NEAT configuration, begins the training process, and finally
    demonstrates the best network obtained after evolution in a live game.
    """
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    run_neat(config, 50)
    test_best_network(config)