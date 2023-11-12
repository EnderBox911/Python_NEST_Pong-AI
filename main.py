import pygame as pyg

pyg.init()

screen_width = 800
screen_height = 600

screen = pyg.display.set_mode((screen_width, screen_height))

run = True
while run:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

pyg.quit()