import pygame as pyg

pyg.init()

screen_width = 600
screen_height = 500

clock = pyg.time.Clock()

screen = pyg.display.set_mode((screen_width, screen_height))
pyg.display.set_caption('Pong')


font = pyg.font.SysFont('Constantia', 30)


margin = 50
ai_score = 0
player_score = 0
FPS = 60


bg = (50, 25, 50)
white = (255, 255, 255)


def draw_board():
    screen.fill(bg)
    pyg.draw.line(screen, white, (0, margin), (screen_width, margin))


def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pyg.Rect((self.x, self.y, 20, 100))
        self.speed = 5

    def move(self):
        key = pyg.key.get_pressed()

        if key[pyg.K_w] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)  # x,y
        if key[pyg.K_s] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)  # x,y

    def draw(self):
        pyg.draw.rect(screen, white, self.rect)


player_paddle = Paddle(screen_width - 40, screen_height // 2)
ai_paddle = Paddle(20, screen_height // 2)




run = True
while run:

    clock.tick(FPS)

    draw_board()
    draw_text('AI: ' + str(ai_score), font, white, 20, 15)
    draw_text('Player: ' + str(player_score), font, white, screen_width -125, 15)

    player_paddle.draw()
    ai_paddle.draw()

    player_paddle.move()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

    pyg.display.update()

pyg.quit()
