# Pong AI
This is an attempt at creating an Ai using the NEST Python module.

# Documentation Overview

### Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Game Structure](#game-structure)
6. [Game Loop](#game-loop)
7. [Entities](#entities)
    - [Paddle](#paddle)
        - [__init__](#__init__)
        - [move](#move)
        - [draw](#draw)
    - [Ball](#ball)
        - [__init__](#__init__)
        - [move](#move)
        - [handle_collision](#handle_collision)
        - [draw](#draw)
    - [Game](#game)
        - [__init__](#__init__)
        - [draw_text](#draw_text)
        - [draw_board](#draw_board)
        - [create_sprites](#create_sprites)
        - [reset_ball](#reset_ball)
        - [handle_input](#handle_input)
        - [update_speed](#update_speed)
        - [handle_paddle_movement](#handle_paddle_movement)
        - [loop](#loop)
8. [License](#license)

## Introduction

The `game.py` file is the main script for the Pong_AI project. It contains the implementation of the Pong game, where a player-controlled paddle faces off against an AI-controlled paddle in a classic Pong match.

## Prerequisites

Before running the game, make sure you have the following prerequisites installed:

- Python 3.x
- [pygame](https://www.pygame.org/) library

## Installation

To install the required dependencies, run the following command:

```bash
pip install pygame
```

## Usage

Run the game using the following command:

```bash
python game.py
```

## Game Structure

The game is structured in a modular way, with separate classes for entities like the Paddle and Ball. The main game loop manages the flow of the game.

## Game Loop

The game follows a standard game loop structure with the following stages:

1. **Input Handling**: Detects player input to move the paddle.
2. **Update**: Updates the positions of the paddle and ball.
3. **Collision Detection**: Checks for collisions between entities.
4. **AI Logic**: Controls the AI paddle's movement.
5. **Rendering**: Draws the game entities on the screen.

## Entities

### Paddle

#### `__init__`

The `__init__` method initializes a `Paddle` object with the specified parameters.

```python
def __init__(self, x, y, width, height, color, speed):
    """Initialize Paddle object."""
    self.rect = pygame.Rect(x, y, width, height)
    self.color = color
    self.speed = speed
```

#### `move`

The `move` method adjusts the paddle's position based on the given direction.

```python
def move(self, direction):
    """Move the paddle based on the given direction."""
    self.rect.y += direction * self.speed
    # Ensure the paddle stays within the screen boundaries
    self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
```

#### `draw`

The `draw` method draws the paddle on the given surface.

```python
def draw(self, surface):
    """Draw the paddle on the given surface."""
    pygame.draw.rect(surface, self.color, self.rect)
```

### Ball

#### `__init__`

The `__init__` method initializes a `Ball` object with the specified parameters.

```python
def __init__(self, x, y, radius, color, speed):
    """Initialize Ball object."""
    self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
    self.color = color
    self.speed = speed
    self.direction = [1, 1]  # Initial movement direction
```

#### `move`

The `move` method updates the ball's position based on its current direction.

```python
def move(self):
    """Move the ball."""
    self.rect.x += self.speed * self.direction[0]
    self.rect.y += self.speed * self.direction[1]

    # Reflect the ball if it hits the top or bottom of the screen
    if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
        self.direction[1] = -self.direction[1]
```

#### `handle_collision`

The `handle_collision` method checks for collisions with paddles and updates the ball's direction.

```python
def handle_collision(self, paddle):
    """Handle collisions with paddles."""
    if self.rect.colliderect(paddle.rect):
        self.direction[0] = -self.direction[0]
```

#### `draw`

The `draw` method draws the ball on the given surface.

```python
def draw(self, surface):
    """Draw the ball on the given surface."""
    pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)
```

### Game

#### `__init__`

The `__init__` method initializes a `Game` object.

```python
def __init__(self):
    """Initialize Game object."""
    # Initialize pygame
    pygame.init()
    # Other game initialization code...
```

#### `draw_text`

The `draw_text` method draws text on the screen.

```python
def draw_text(self, text, size, x, y, color):
    """Draw text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    self.screen.blit(text_surface, text_rect)
```

#### `draw_board`

The `draw_board` method draws the game board on the screen.

```python
def draw_board(self):
    """Draw the game board."""
    # Other drawing code...
```

#### `create_sprites`

The `create_sprites` method creates game sprites (paddles and ball).

```python
def create_sprites(self):
    """Create game sprites."""
    # Create paddle and ball objects...
```

#### `reset_ball`

The `reset_ball` method resets the ball to its initial position.

```python
def reset_ball(self):
    """Reset the ball to its initial position."""
    # Other reset code...
```

#### `handle_input`

The `handle_input` method processes user input.

```python
def handle_input(self):
    """Handle user input."""
    # Other input handling code...
```

#### `update_speed`

The `update_speed` method adjusts the game speed.

```python
def update_speed(self):
    """Adjust the game speed."""
    # Other speed adjustment code...
```

#### `handle_paddle_movement`

The `handle

_paddle_movement` method controls the movement of the paddles.

```python
def handle_paddle_movement(self):
    """Control the movement of paddles."""
    # Other paddle movement code...
```

#### `loop`

The `loop` method represents the main game loop.

```python
def loop(self):
    """Main game loop."""
    # Other loop code...
```

Feel free to use this documentation as a starting point and customize it based on your specific code or additional information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this documentation based on additional information or details you may have about the code.
