import pygame
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
winner = 0
live_ball = False


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

    def ai(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)


class Ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        if self.rect.top < margin:
            self.speedY *= -1

        if self.rect.bottom > screen_height:
            self.speedY *= -1

        ####
        # Add proper collision detection HERE
        
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(ai_paddle):
            self.speedX *= -1
            
        ####

        if self.rect.left < 0:
            self.winner = 1

        if self.rect.right > screen_width:
            self.winner = -1

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.winner

    def draw(self):
        pyg.draw.circle(screen, white, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.rect = pyg.Rect((self.x, self.y, self.radius * 2, self.radius * 2))
        self.speedX = -4
        self.speedY = 4
        self.winner = 0  # 0 = player, -1 = ai


player_paddle = Paddle(screen_width - 40, screen_height // 2)
ai_paddle = Paddle(20, screen_height // 2)

pong = Ball(screen_width - 60, screen_height // 2 + 50)


run = True
while run:

    clock.tick(FPS)

    draw_board()
    draw_text('AI: ' + str(ai_score), font, white, 20, 15)
    draw_text('Player: ' + str(player_score), font, white, screen_width -125, 15)

    player_paddle.draw()
    ai_paddle.draw()

    if live_ball:
        winner = pong.move()
        if winner == 0:
            player_paddle.move()
            ai_paddle.ai()
            pong.draw()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            else:
                ai_score += 1

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            pong.reset(screen_width - 60, screen_height // 2 + 50)

    pyg.display.update()

pyg.quit()
