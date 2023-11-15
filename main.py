import pygame as pyg
from Pong import Game

screen_width, screen_height = 600, 500
screen = pyg.display.set_mode((screen_width, screen_height))

if __name__ == "__main__":
    game = Game(screen_width, screen_height, screen)

    while game.run:
        game.clock.tick(game.FPS)
        for event in pyg.event.get():
            game.handle_input(event)

        game.loop()
        game.draw_board()
        pyg.display.update()

    pyg.quit()