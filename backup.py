import pygame as pyg
from random import randint

pyg.init()

bg = (50, 25, 50)
white = (255, 255, 255)

class Paddle:
    def __init__(self, x, y):
        self.x = x # Start position
        self.y = y # Start position
        self.width = 20
        self.height = 100
        self.rect = pyg.Rect((self.x, self.y, self.width, self.height))
        self.speed = 5

    def move(self, margin, screen_height):
        key = pyg.key.get_pressed()

        if key[pyg.K_w] and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed)  # x,y
        if key[pyg.K_s] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)  # x,y

    def draw(self, screen):
        pyg.draw.rect(screen, white, self.rect)

    def ai(self, margin, screen_height, pong):
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

        # Passes right side, ai wins round
        if self.rect.right > screen_width:
            self.winner = -1

        # Adds speeds to ball
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.winner

    def handle_paddle_collision(self, player_paddle, ai_paddle:
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
        

    def draw(self, screen):
        pyg.draw.circle(screen, white, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


class Game:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 500
        self.margin = 50
        self.screen = pyg.display.set_mode((screen_width, screen_height))
        pyg.display.set_caption('Pong')
        self.live_ball = False
        self.ai_score = 0
        self.player_score = 0
        self.FPS = 60
        self.winner = 0
        self.speed_increase = 0
        self.font = pyg.font.SysFont('Constantia', 30)
        self.run = True

    def draw_text(self, text, font, colour, x, y):
        img = font.render(text, True, colour)
        self.screen.blit(img, (x, y))

    def draw_board(self):
        self.screen.fill(bg)
        pyg.draw.line(self.screen, white, (0, self.margin), (self.screen_width, self.margin))

    def create_sprites(self):
        # Instantiate the paddles and pong
        player_paddle = Paddle(self.screen_width - 40, self.screen_height // 2)
        ai_paddle = Paddle(20, self.screen_height // 2)
        pong = Ball(self.screen_width - 60, self.screen_height // 2 + 50)

        return player_paddle, ai_paddle, pong

    def handle_input(self, event, pong):
        if event.type == pygame.QUIT:
            self.run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.live_ball:
            self.live_ball = True
            self.reset_ball(pong)

    def update_speed(self, pong):
        if self.speed_increase > self.paddle_speed_increase_threshold:
            self.speed_increase = 0
            pong.speedX += 1 if pong.speedX > 0 else -1
            pong.speedY += 1 if pong.speedY > 0 else -1
            pong.max_Y_vel += 1

    def start_game(self):
        player_paddle, ai_paddle, pong = cls.create_sprites()

        while self.run:
            # Ensures this loop runs 60 times per second
            clock.tick(self.FPS)

            # Set board up
            self.draw_board()
            self.draw_text('AI: ' + str(self.ai_score), 20, 15)
            self.draw_text('Player: ' + str(self.player_score), self.screen_width - 125, 15)
            self.draw_text('BALL SPEED: ' + str(abs(pong.speedX)), self.screen_width // 2 - 100, 15)

            player_paddle.draw(self.screen)
            ai_paddle.draw(self.screen)

            if self.live_ball:
                self.speed_increase += 1
                self.winner = pong.move(self.margin, self.screen_width, self.screen_height, player_paddle, ai_paddle)
                if self.winner == 0:
                    player_paddle.move(self.margin, self.screen_height, pong)
                    ai_paddle.move(self.margin, self.screen_height, pong)
                    pong.draw(self.screen)
                else:
                    self.live_ball = False
                    if self.winner == 1:
                        self.player_score += 1
                    else:
                        self.ai_score += 1

            if not self.live_ball:
                if self.winner == 0:
                    self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 100)
                if self.winner == 1:
                    self.draw_text('YOU SCORED!', self.font, self.white, 220, self.screen_height // 2 - 100)
                    self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 50)
                if self.winner == -1:
                    self.draw_text('AI SCORED!', self.font, self.white, 220, self.screen_height // 2 - 100)
                    self.draw_text('CLICK ANYWHERE TO START', self.font, self.white, 100, self.screen_height // 2 - 50)

             for event in pygame.event.get():
                self.handle_input(event, pong)

            self.update_speed(pong)
            pyg.display.update()

        pyg.quit()


"""
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



def draw_board():
    screen.fill(bg)
    pyg.draw.line(screen, white, (0, margin), (screen_width, margin))


def draw_text(text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))
"""



"""
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
"""

game = Game()
game.start_game()
