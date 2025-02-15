# AI-Controlled Pong Game with NEAT
*Evolving intelligence in a classic game of Pong*

## Overview
This project implements a modern twist on the classic Pong game by integrating the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve intelligent game agents. The system uses Python and Pygame to simulate gameplay while employing neat-python for dynamic neural network evolution. It is designed for developers, researchers, and hobbyists interested in AI, game development, and machine learning. Unique selling points include real-time AI training, interactive checkpointing, and adaptive gameplay that evolves over time.

## Technology Stack
- **Python 3.x**
- **Pygame:** For game rendering and event handling.
- **neat-python:** For implementing the NEAT algorithm.
- **pickle:** For saving and loading checkpoints.
- **glob & os:** For file and checkpoint management.

## Installation & Setup
### Prerequisites
- Python 3.x installation
- Ensure pip is installed

### Dependencies
Install the required packages using:
```bash
pip install pygame neat-python
```

### Clone the Repository
Clone the repository from GitHub:
```bash
git clone https://github.com/muhammadhamzagova666/ai-pong-neat.git
cd ai-pong-neat
```

## Usage Guide
### Training the AI
Start training the AI by running:
```bash
python Source/main.py
```
This will start the game, begin the NEAT training process, and automatically resume from the latest checkpoint if available.

### Testing the AI
After training completes, the best performing network is loaded and a live game session is initiated for demonstration purposes.

## Project Structure
```
ai-pong-neat/
├── AI-Controlled Pong Game Project Presentation.pdf
├── AI-Controlled Pong Game Project Proposal.pdf
├── Report/
│   ├── Report.tex
│   ├── FAST.png
│   ├── Game.png
│   ├── NU-logo.jpg
│   └── Training.png
└── Source/
    ├── best.pickle
    ├── config.txt
    ├── main.py
    ├── README.md
    ├── checkpoints/
    │   ├── neat-checkpoint-0
    │   ├── neat-checkpoint-1
    │   └── ... (other checkpoints)
    └── pong/
        ├── __init__.py
        ├── game.py
        ├── paddle.py
        └── ball.py
```
- **Source/**: Contains the Python source code and NEAT configuration.
- **Source/checkpoints/**: Holds checkpoint files to resume AI training.
- **Report/**: Contains project report, diagrams, and presentation files.

## Configuration & Environment Variables
- **config.txt**: Contains NEAT algorithm settings.
- *(Optional)* Create a `.env` file if any additional environment-specific settings are required.

## Deployment Guide
### Local Deployment
- Simply run the training and testing scripts as mentioned above.
  
### Container Deployment (Optional)
- A Dockerfile can be added for containerized deployment:
  ```dockerfile
  FROM python:3.9-slim
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  CMD ["python", "Source/main.py"]
  ```
  
- Build and run using:
  ```bash
  docker build -t ai-pong-neat .
  docker run -it ai-pong-neat
  ```

## Testing & Debugging
- **Testing:** Currently, interactive tests can be triggered by simulating gameplay, with logs printed to the console.
- **Debugging Tips:** 
  - Use Pygame’s built-in display debugging.
  - Inspect checkpoint files and best.pickle for training state.
  - Review console outputs from NEAT reporters.

## Performance Optimization
- Ensure proper frame rate using `pygame.time.Clock()`.
- Monitor and adjust NEAT parameters in config.txt for balance between training speed and network complexity.

## Security Best Practices
- Validate all configurations.
- Keep repository dependencies up-to-date.
- If deploying publicly, consider sandboxing game execution.

## Contributing Guidelines
- **Bug Reports & Feature Requests:** Submit via GitHub issues.
- **Pull Requests:** Fork the repository, create a feature branch, and submit a pull request.
- Please adhere to the Code of Conduct for contributions.

## Documentation
- For API reference and detailed explanation of modules (e.g., `Source/main.py`), please refer to the docs.

## Roadmap
- Enhance multiplayer support.
- Improve AI training visualization.
- Add comprehensive unit tests.
- Integrate CI/CD for automated testing and deployment.

## FAQ
- **Q: How do I resume training?**  
  A: The system automatically resumes from the latest checkpoint in the `/checkpoints` directory.
- **Q: What are the project dependencies?**  
  A: Python 3.x, Pygame, neat-python.

## Acknowledgments & Credits
- This project was inspired and developed from the teachings of the [Tech with Tim](https://www.youtube.com/@TechWithTim) YouTube channel, particularly the video [Python Pong AI Tutorial - Using NEAT](https://youtu.be/2f6TmKm7yx0?si=ThfO7caTc5XwiM6S).
- Special thanks to contributors and libraries like [Pygame](https://www.pygame.org/docs/) and [neat-python](https://neat-python.readthedocs.io/).

## Contact Information
For support or to contribute, please reach out via GitHub:
- GitHub Profile: [muhammadhamzagova666](https://github.com/muhammadhamzagova666)
