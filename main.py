import pygame as pyg
from Pong import Game
import neat
import os
import pickle


class PongGame:
    def __init__(self, screen, width, height):
        self.game = Game(width, height, screen)
        self.left_paddle = self.game.ai_paddle
        self.right_paddle = self.game.player_paddle
        self.ball = self.game.pong

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

    def calculate_fitness(self, genome1, genome2):
        genome1.fitness += self.game.ai_score
        genome2.fitness += self.game.player_score


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


def run_neat(config):
    # Setting up the population

    p = neat.Checkpointer.restore_checkpoint("ai_checkpoints/neat-checkpoint-49")
    # For restoring checkpoints, comment out the next line
    # p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Saves a checkpoint after X generations
    p.add_reporter(neat.Checkpointer(1, filename_prefix='ai_checkpoints/neat-checkpoint-'))

    # Takes all genomes in the population and give a fitness.
    # The winner is the best fitness
    winner = p.run(eval_genomes, 50)

    with open("ai_checkpoints/best.pickle", "wb") as f:
        print("Saved winner")
        pickle.dump(winner, f)


def test_ai(config):
    screen_width, screen_height = 600, 500
    screen = pyg.display.set_mode((screen_width, screen_height))

    with open("ai_checkpoints/best.pickle", "rb") as f:
        winner = pickle.load(f)

    game = PongGame(screen, screen_width, screen_height)
    game.test_ai(winner, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    configs = neat.Config(neat.DefaultGenome,
                          neat.DefaultReproduction,
                          neat.DefaultSpeciesSet,
                          neat.DefaultStagnation,
                          config_path)

    # Once best is picked, comment line below out
    # run_neat(configs)
    test_ai(configs)
