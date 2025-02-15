# Pong Game AI with NEAT

Welcome to the Pong Game AI project! This repository is dedicated to the development of an artificial intelligence (AI) that learns to play the classic game of Pong to near perfection. Utilizing the NeuroEvolution of Augmenting Topologies (NEAT) algorithm, this project showcases the fascinating capabilities of machine learning and neural networks in gaming.

## Table of Contents

- Introduction
- Features
- Getting Started
  - Prerequisites
  - Installation
- Usage
  - Training the AI
  - Testing the AI
- Project Structure

## Introduction

The Pong Game AI project is an exploration into the intersection of gaming and artificial intelligence. By simulating the environment of the Pong game, we provide a platform for AI agents to learn and adapt through the principles of neuroevolution.

The NEAT (NeuroEvolution of Augmenting Topologies) algorithm is a method for evolving artificial neural networks with a genetic algorithm. It was developed by Kenneth Stanley and Risto Miikkulainen in 2002. Here's an in-depth explanation of how NEAT works:

### Overview of NEAT

NEAT is unique because it evolves not only the weights of the neural network connections but also its structure. This means that NEAT can start with simple networks and complexify them over time as needed, which is a process called "complexification."

### Key Concepts of NEAT

- **Genomes and Genes**: In NEAT, each neural network is represented as a genome, which consists of node genes (neurons) and connection genes (synapses).
- **Initial Simplicity**: NEAT begins with a population of simple networks where each network has only input and output nodes.
- **Complexification**: Over generations, the networks can grow more complex through mutations that add new nodes and connections.
- **Speciation**: To protect innovation, NEAT assigns genomes to species based on genetic similarity. This ensures that novel structures have time to optimize before they have to compete with other, more established structures.
- **Fitness Function**: A user-defined fitness function evaluates each genome based on how well it performs a given task. Higher fitness scores indicate better performance.
- **Crossover**: NEAT uses a historical marking system to align genes from different genomes, allowing for meaningful crossover between them.
- **Mutation**: Networks can mutate in several ways, including changing connection weights, adding new connections, or adding new nodes.

### The NEAT Algorithm in Detail

1. **Start with a Population**: Generate an initial population of minimal neural networks.
2. **Evaluate Fitness**: Use the fitness function to determine how well each network performs the task at hand.
3. **Select Parents**: Choose the most fit networks to reproduce.
4. **Crossover**: Create offspring by crossing over parent genomes. NEAT's historical markings ensure that structural genes are aligned correctly during this process.
5. **Mutate**: Apply mutations to the offspring, potentially adding new structure to the networks.
6. **Speciate**: Group similar genomes into species based on genetic distance.
7. **Adjust Fitness**: Share fitness scores within species to prevent any one species from taking over the population.
8. **Reproduce**: Based on shared fitness, allow genomes to reproduce within their species.
9. **Eliminate**: Remove the least fit members of each species.
10. **Loop**: Repeat the process for a set number of generations or until a satisfactory solution is found.

### Advantages of NEAT

- **Adaptive Complexity**: NEAT starts with the simplest possible networks and only adds complexity as needed.
- **Protection of Innovation**: By using speciation, NEAT gives new structures a chance to optimize before they have to compete with more fit structures.
- **Efficient Crossover**: The historical marking system allows NEAT to perform crossover between different topologies effectively.

### Applications of NEAT

NEAT can be applied to any problem that involves training a neural network, such as game playing, control systems, optimization problems, and more. Its ability to evolve network topologies makes it particularly useful for problems where the ideal network structure is not known in advance.

## Features

- **AI Training**: Implementing NEAT to evolve and train AI agents.
- **AI Testing**: Functionality to test the AI's performance against human input.
- **Fitness Tracking**: Dynamic fitness calculation based on game outcomes to inform the evolutionary process.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

```bash
pip install pygame neat-python
```

### Installation

A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository.
2. Navigate to the project directory.

## Usage

### Training the AI

To start training the AI, run the following command in the terminal:

```bash
python main.py
```

## Project Structure

- `main.py`: The entry point of the program.
- `pong/`: Contains the game logic.
- `config.txt`: NEAT configuration file.
- `checkpoints/`: Directory for CheckPoints of tested data.

---
