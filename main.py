import pygame
import pygame as pyg
from random import randint

pyg.init()

screen_width = 600
screen_height = 500

clock = pyg.time.Clock()

screen = pyg.display.set_mode((screen_width, screen_height))
pyg.display.set_caption('Pong')


font = pyg.font.SysFont('Constantia', 30)

live_ball = False
margin = 50
ai_score = 0
player_score = 0
FPS = 60
winner = 0
speed_increase = 0


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
        self.x = x # Start position
        self.y = y # Start position
        self.width = 20
        self.height = 100
        self.rect = pyg.Rect((self.x, self.y, self.width, self.height))
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
        # Placeholder AI
        # + randint for some variation
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed + (randint(1,3)))
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed - (randint(1,3)))


class Ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x # Start position
        self.y = y # Start position
        self.radius = 8
        self.rect = pyg.Rect((self.x, self.y, self.radius * 2, self.radius * 2))
        self.speedX = -5
        self.speedY = 5 # Initial Y velocity of the ball
        self.max_Y_vel = self.speedY
        self.winner = 0  # 0 = player, -1 = ai

    def move(self):
        # Top and bottom border check
        if self.rect.top < margin or self.rect.bottom > screen_height:
            self.speedY *= -1

        # Check for paddle collision
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(ai_paddle):
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
            reducing_factor = (paddle.height/2) / self.max_Y_vel

            # Squeezes the difference in y to the range of the max velocity
            y_vel = diff_in_y/reducing_factor

            # Makes that the y velocity
            self.speedY = -1 * y_vel

        # Passes left side, user wins round
        if self.rect.left < 0:
            self.winner = 1

        # Passes right side, ai wins round
        if self.rect.right > screen_width:
            self.winner = -1

        # Adds speeds to ball
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.winner

    def draw(self):
        pyg.draw.circle(screen, white, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


# Instantiate the paddles and pong
player_paddle = Paddle(screen_width - 40, screen_height // 2)
ai_paddle = Paddle(20, screen_height // 2)
pong = Ball(screen_width - 60, screen_height // 2 + 50)


run = True
while run:
    # Ensures this loop runs 60 times per second
    clock.tick(FPS)

    # Set board up
    draw_board()
    draw_text('AI: ' + str(ai_score), font, white, 20, 15)
    draw_text('Player: ' + str(player_score), font, white, screen_width -125, 15)
    draw_text('BALL SPEED: ' + str(abs(pong.speedX)), font, white, screen_width // 2 - 100, 15)

    player_paddle.draw()
    ai_paddle.draw()

    if live_ball:
        speed_increase += 1
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

    if not live_ball:
        if winner == 0:
            draw_text('CLICK ANYWHERE TO START', font, white, 100, screen_height // 2 - 100)
        if winner == 1:
            draw_text('YOU SCORED!', font, white, 220, screen_height // 2 - 100)
            draw_text('CLICK ANYWHERE TO START', font, white, 100, screen_height // 2 - 50)
        if winner == -1:
            draw_text('AI SCORED!', font, white, 220, screen_height // 2 - 100)
            draw_text('CLICK ANYWHERE TO START', font, white, 100, screen_height // 2 - 50)


    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not live_ball:
            live_ball = True
            pong.reset(screen_width - 60, screen_height // 2 + 50)

    if speed_increase > 500:
        speed_increase = 0
        if pong.speedX < 0:
            pong.speedX -= 1
        if pong.speedX > 0:
            pong.speedX += 1

        if pong.speedY < 0:
            pong.speedY -= 1
            pong.max_Y_vel += 1
        if pong.speedY > 0:
            pong.speedY += 1
            pong.max_Y_vel += 1


    pyg.display.update()

pyg.quit()
