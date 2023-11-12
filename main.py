import pygame as pyg

pyg.init()

screen_width = 800
screen_height = 600

screen = pyg.display.set_mode((screen_width, screen_height))

player = pyg.Rect((300, 250, 50, 50))  # x,y,width,height

run = True
while run:
    screen.fill((0, 0, 0))

    pyg.draw.rect(screen, (255, 0, 0), player)  # screen,rgb,object

    key = pyg.key.get_pressed()
    if key[pyg.K_a]:
        player.move_ip(-1, 0)  # x,y
    if key[pyg.K_d]:
        player.move_ip(1, 0)  # x,y
    if key[pyg.K_w]:
        player.move_ip(0, -1)  # x,y
    if key[pyg.K_s]:
        player.move_ip(0, 1)  # x,y

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

    pyg.display.update()

pyg.quit()
