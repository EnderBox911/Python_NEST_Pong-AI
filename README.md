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
   - [PongGame](#ponggame)
        - [__init__](#__init__)
        - [test_ai](#test_ai)
        - [train_ai](#train_ai)
        - [calculate_fitness](#calculate_fitness)
        - [eval_genomes](#eval_genomes)
        - [run_neat](#run_neat)
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
9. [License](#license)

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

The `run_game` function takes in a difficulty level and essentially starts the game with the player and the AI with the chosen difficulty.
```python
def run_game(config, difficulty):
    screen_width, screen_height = 600, 500
    screen = pyg.display.set_mode((screen_width, screen_height))

    with open(f"ai_checkpoints/{difficulty}/best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGame(screen, screen_width, screen_height)
    game.test_ai(winner, config)
```

The following section of code is to set up the configurations and call the `run_game` function to start the game.
```
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    configs = neat.Config(neat.DefaultGenome,
                          neat.DefaultReproduction,
                          neat.DefaultSpeciesSet,
                          neat.DefaultStagnation,
                          config_path)

    # Line below is to train the AI model
    # run_neat(configs)
    run_game(configs, "hard")
```

## Entities

### PongGame

#### `__init__`

The `__init__` method initializes a `PongGame` object with the specified parameters. When the object is instantiated, it takes in the screen window and its width and height. It also sets the different entities into it's owm variables.

```python
def __init__(self, screen, width, height):
    self.game = Game(width, height, screen)
    self.left_paddle = self.game.ai_paddle
    self.right_paddle = self.game.player_paddle
    self.ball = self.game.pong   
```

#### `test_ai`

The `test_ai` method is essentially the actual running of the game and setting it up with an AI opponenent. While the game is running, it checks for player movement input, the AI's next move and move it's paddle accordingly, and prings/updates the game board.

```python
def test_ai(self, genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    self.game.run = True

    while self.game.run:
        self.game.clock.tick(self.game.FPS)
        for event in pyg.event.get():
            self.game.handle_input(event)

        # Setup AI against player
        output = net.activate((self.left_paddle.rect.y,
                               self.ball.rect.y,
                               abs(self.left_paddle.rect.x - self.ball.rect.x)))

        # Gets index, 0 = stay still, 1 = move up, 2 = move down
        decision = output.index(max(output))

        if decision == 0:
            pass
        elif decision == 1 and self.left_paddle.rect.top > self.game.margin:
            self.left_paddle.move(True)
        elif decision == 2 and self.left_paddle.rect.bottom < self.game.screen_height:
            self.left_paddle.move(False)

        self.game.loop()
        # print(self.game.player_score, self.game.ai_score)
        self.game.draw_board()
        pyg.display.update()

    pyg.quit()
```

#### `train_ai`

The `train_ai` method is the method used to further train the AI. It takes in the first and second genomes and the configuration settings. The method starts a game automatically without stop between genome1 and genome2, and depending on the genome's decision, it will move the paddle accordingly. If either paddle miss, to avoid a loop of nothing moving, we end the game straight away.

```python
def train_ai(self, genome1, genome2, config):
    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    # Keeps it running
    self.game.run = True
    self.game.live_ball = True

    while self.game.run:
        # For quitting when closed
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                quit()

        output1 = net1.activate((self.left_paddle.rect.y,
                                 self.ball.rect.y,
                                 abs(self.left_paddle.rect.x - self.ball.rect.x)))

        # Gets index, 0 = stay still, 1 = move up, 2 = move down
        decision1 = output1.index(max(output1))

        if decision1 == 0:
            pass
        elif decision1 == 1 and self.left_paddle.rect.top > self.game.margin:
            self.left_paddle.move(True)
        elif decision1 == 2 and self.left_paddle.rect.bottom < self.game.screen_height:
            self.left_paddle.move(False)

        output2 = net2.activate((self.right_paddle.rect.y,
                                 self.ball.rect.y,
                                 abs(self.right_paddle.rect.x - self.ball.rect.x)))

        decision2 = output2.index(max(output2))

        if decision2 == 0:
            pass
        elif decision2 == 1 and self.right_paddle.rect.top > self.game.margin:
            self.right_paddle.move(True)
        elif decision2 == 2 and self.right_paddle.rect.bottom < self.game.screen_height:
            self.right_paddle.move(False)

        # print(output1, output2)

        self.game.loop()
        self.game.draw_board()
        pyg.display.update()

        # If either paddle misses, end the game
        if self.game.ai_score >= 1 or self.game.player_score >= 1 or self.game.ai_score > 50:
            self.calculate_fitness(genome1, genome2)
            break 
```

#### `calculate_fitness`

The `calculate_fitness` method is used to calculate the fitness, or "how well" genome1 and genome2 are doing, based on the according paddle's scores.

```python
def calculate_fitness(self, genome1, genome2):
    genome1.fitness += self.game.ai_score
    genome2.fitness += self.game.player_score
```

#### `eval_genomes`

The `eval_genomes` method is used to make the genomes play against each other and calculate the fitness from all the games played in total.

```python
def eval_genomes(genomes, config):
    screen_width, screen_height = 600, 500
    screen = pyg.display.set_mode((screen_width, screen_height))

    # To make genomes play against each other
    # The fitness is the sum of the fitness from every game
    for i, (genome_id1, genome1) in enumerate(genomes):

        # To stop index out of range
        if i == len(genomes) - 1:
            break

        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            # Sets genome2's fitness 0 if not already given a fitness
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness

            game = PongGame(screen, screen_width, screen_height)
            game.train_ai(genome1, genome2, config)
```

#### `run_neat`

The `run_neat` method is used to run the neat package. This is to load up the AI checkpoint to continue training from that on point, or if wanted, restart the trainging.

```python
def run_neat(config):
    # Setting up the population

    p = neat.Checkpointer.restore_checkpoint("ai_checkpoints/hard/neat-checkpoint-50")
    # For restoring checkpoints, comment out the next line
    # p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Saves a checkpoint after X generations
    p.add_reporter(neat.Checkpointer(1, filename_prefix='ai_checkpoints/hard/neat-checkpoint-'))

    # Takes all genomes in the population and give a fitness.
    # The winner is the best fitness
    winner = p.run(eval_genomes, 50)

    with open("ai_checkpoints/hard/best.pickle", "wb") as f:
        print("Saved winner")
        pickle.dump(winner, f)
```

### Paddle

#### `__init__`

The `__init__` method initializes a `Paddle` object with the specified parameters. When the object is instantiated, it takes in an X and Y coordinate as its start point. 

```python
def __init__(self, x, y):
        self.x = x  
        self.y = y 
        self.width = 20
        self.height = 100
        self.rect = pyg.Rect((self.x, self.y, self.width, self.height))
        self.speed = 5
```

#### `move`

The `move` method adjusts the paddle's position based on the given direction. This is used inside the Game class `handle_paddle_movement`, moving the paddle's direction using Pygame's built-in function `move_ip()`, which takes an X and Y coordinate as it's parameters.

```python
def move(self, up):
    if up:
        self.rect.move_ip(0, -1 * self.speed)  # x,y
    if not up:
        self.rect.move_ip(0, self.speed)  # x,y
```

#### `draw`

The `draw` method draws the paddle on the given window.

```python
def draw(self, screen):
        pyg.draw.rect(screen, (255, 255, 255), self.rect)
```

### Ball

#### `__init__`

The `__init__` method initializes a `Ball` object with the specified parameters. As these variables are needed to be reset, it simply calls a method that initialises the same varibles it would have needed for an `__init__`. It passes the X and Y parameters into the `reset` method. It also randomises the direction of the bll when it spawns.

```python
def __init__(self, x, y):
        self.reset(x, y)
        # Setting random movements
        self.speedY *= -1 if randint(0,2) == 1 else self.speedY
```

### `reset`

The `reset` method resets the class's variables. This is used for when needing to restart the ball's position and speed. It takes in X and Y coordinates for it's starting point. SpeedX is the X-velocity and SpeedY is the Y-velocity of the ball. `self.winner` is automatically set as 0; When it turns 1, the player won the round; when it turns -1, the AI won the round.

```python
def reset(self, x, y):
        self.x = x  # Start position
        self.y = y  # Start position
        self.radius = 8
        self.rect = pyg.Rect((self.x, self.y, self.radius * 2, self.radius * 2))
        self.speedX = random.choice([-5, 5])
        self.speedY = randint(2,5)  # Initial Y velocity of the ball
        self.max_Y_vel = self.speedY
        self.winner = 0  # 1 = player, -1 = ai
```

#### `move`

The `move` method updates the ball's position based on its current direction. It takes in the window dimentions and the paddles. If the built-in Pygame `colliderect()` detects a collision, it calls the `handle_paddle_collision` method. If it passes the left side of the screen, the player gets a point; If it passes the right, the AI gets a point.

```python
def move(self, margin, screen_width, screen_height, player_paddle, ai_paddle):
        # Top and bottom border check
        if self.rect.top < margin or self.rect.bottom > screen_height:
            self.speedY *= -1

        # Check for paddle collision
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(ai_paddle):
            self.handle_paddle_collision(player_paddle, ai_paddle)

        # Passes left side, user wins round
        if self.rect.left < 0:
            self.winner = 1

        # Passes right side, AI wins round
        if self.rect.right > screen_width:
            self.winner = -1

        # Adds speeds to ball
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.winner
```

#### `handle_paddle_collision`

The `handle_paddle_collision` method checks for collisions with paddles and updates the ball's direction. This calculates the Y-velocity depending on where it touches on the paddle. The closer it is to the middle, the Y-veloctity gets closer to 0. The farther it is, the Y-velocity gets closer to its max velocity.

```python
    def handle_paddle_collision(self, player_paddle, ai_paddle):
        self.speedX *= -1

        # Getting which paddle collided
        paddle = player_paddle if self.rect.colliderect(player_paddle) else ai_paddle

        # Finding middle of paddle
        middle_y = paddle.rect.y + paddle.height / 2

        # Difference in Y axis of ball to middle of paddle
        diff_in_y = middle_y - self.rect.y

        # Farther from center of paddle = the Y velocity is greater. When the ball hits the edge of the
        # paddle, it reaches the maximum velocity. Finding the amount of Y velocity for each unit paddle length,
        # meaning that if the ball hits the edge (the full length) of the paddle, it gives the maximum Y velocity
        reducing_factor = (paddle.height / 2) / self.max_Y_vel

        # Squeezes the difference in y to the range of the max velocity
        y_vel = diff_in_y / reducing_factor

        # Makes that the y velocity
        self.speedY = -1 * y_vel
```

#### `draw`

The `draw` method draws the ball on the given surface.

```python
def draw(self, screen):
        pyg.draw.circle(screen, (255, 255, 255), (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)
```

### Game

#### `__init__`

The `__init__` method initializes a `Game` object. Takes in the screen and it's width and height. This also initializes the paddles and the pong.

```python
def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = 50
        self.screen = screen
        pyg.display.set_caption('Pong')
        self.clock = pyg.time.Clock()
        self.live_ball = False
        self.ai_score = 0
        self.player_score = 0
        self.FPS = 60
        self.winner = 0
        self.speed_increase = 0
        self.font = pyg.font.SysFont('Constantia', 30)
        self.run = True
        self.white = (255, 255, 255)
        self.bg = (50, 25, 50)
        self.player_paddle, self.ai_paddle, self.pong = self.create_sprites()
```

#### `draw_text`

The `draw_text` method draws text on the screen.

```python
    def draw_text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.screen.blit(img, (x, y))
```

#### `draw_board`

The `draw_board` method draws the game board on the screen along with the appropriate text needed and the game start and ending text.

```python
def draw_board(self):
    self.screen.fill(self.bg)
    pyg.draw.line(self.screen, self.white, (0, self.margin), (self.screen_width, self.margin))
    self.draw_text('AI: ' + str(self.ai_score), self.font, self.white, 20, 15)
    self.draw_text('Player: ' + str(self.player_score), self.font, self.white, self.screen_width - 125, 15)
    self.draw_text('BALL SPEED: ' + str(abs(self.pong.speedX)), self.font, self.white, self.screen_width // 2 - 100, 15)

    self.player_paddle.draw(self.screen)
    self.ai_paddle.draw(self.screen)

    if self.live_ball and self.winner == 0:
        # if game not start and no winners
        self.pong.draw(self.screen)
    elif not self.live_ball:
        if self.winner == 0:
            self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 100)
        if self.winner == 1:
            self.draw_text('YOU SCORED!', self.font, self.white, 220, self.screen_height // 2 - 100)
            self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 50)
        if self.winner == -1:
            self.draw_text('AI SCORED!', self.font, self.white, 220, self.screen_height // 2 - 100)
            self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 50)

```

#### `create_sprites`

The `create_sprites` method creates game sprites (paddles and ball).

```python
def create_sprites(self):
    # Instantiate the paddles and pong
    player_paddle = Paddle(self.screen_width - 40, self.screen_height // 2)
    ai_paddle = Paddle(20, self.screen_height // 2)
    pong = Ball(self.screen_width // 2, self.screen_height // 2 + 50)

    return player_paddle, ai_paddle, pong
```

#### `reset_ball`

The `reset_ball` method resets the ball to its initial position.

```python
def reset_ball(self):
    self.pong.reset(self.screen_width - 60, self.screen_height // 2 + 50)
```

#### `handle_input`

The `handle_input` method processes user input for the game window.

```python
def handle_input(self, event):
    if event.type == pyg.QUIT:
        self.run = False
    elif event.type == pyg.MOUSEBUTTONDOWN and not self.live_ball:
        self.live_ball = True
        self.reset_ball()
```

#### `update_speed`

The `update_speed` method is run every round, incrementing the speed of both the X and Y velocity by 1.

```python
def update_speed(self):
    pong = self.pong
    if self.speed_increase > 500:
        self.speed_increase = 0
        pong.speedX += 1 if pong.speedX > 0 else -1
        pong.speedY += 1 if pong.speedY > 0 else -1
        pong.max_Y_vel += 1
```

#### `handle_paddle_movement`

The `handle_paddle_movement` method controls the movement of the paddles. It checks on if either the left or right paddle is being passed and depending on which paddle, it moves said paddle. This opens up to the possibility of the implementation of a player vs. player mode rather than with an AI.

```python
def handle_paddle_movement(self, left_paddle, right_paddle):
    key = pyg.key.get_pressed()
    if left_paddle:
        if key[pyg.K_w] and left_paddle.rect.top > self.margin:
            left_paddle.move(True)  # x,y
        if key[pyg.K_s] and left_paddle.rect.bottom < self.screen_height:
            left_paddle.move(False)  # x,y
    if right_paddle:
        if key[pyg.K_UP] and right_paddle.rect.top > self.margin:
            right_paddle.move(True)  # x,y
        if key[pyg.K_DOWN] and right_paddle.rect.bottom < self.screen_height:
            right_paddle.move(False)  # x,y
```

#### `loop`

The `loop` method is the main game loop. It checks if the game is still ongoing, increses the speed and checks if the ball has passed through either side of the screen, thus checking for a winner. If there is no winner, it continues the game. If there is a winner, it stops the game and increments the points accordingly.

```python
def loop(self):
    if self.live_ball:
    self.speed_increase += 1
    self.winner = self.pong.move(self.margin, self.screen_width, self.screen_height, self.player_paddle, self.ai_paddle)
    if self.winner == 0:
        # self.handle_paddle_movement(self.ai_paddle, False)
        self.handle_paddle_movement(False, self.player_paddle)
    else:
        self.live_ball = False
        if self.winner == 1:
            self.player_score += 1
        else:
            self.ai_score += 1

    self.update_speed()
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
