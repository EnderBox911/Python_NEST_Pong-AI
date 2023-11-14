import pygame
from random import randint

pygame.init()

bg = (50, 25, 50)
white = (255, 255, 255)


class Paddle:
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 100
        self.rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.speed = 5
        self.is_player = is_player

    def move(self, margin, screen_height, pong):
        keys = pygame.key.get_pressed()

        if self.is_player:
            if keys[pygame.K_w] and self.rect.top > margin:
                self.rect.move_ip(0, -1 * self.speed)
            if keys[pygame.K_s] and self.rect.bottom < screen_height:
                self.rect.move_ip(0, self.speed)
        else:
            self.ai(margin, screen_height, pong)

    def ai(self, margin, screen_height, pong):
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed + randint(1, 3))
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
            self.rect.move_ip(0, -1 * self.speed - randint(1, 3))

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect)


class Ball:
    def __init__(self, x, y):
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.rect = pygame.Rect((self.x, self.y, self.radius * 2, self.radius * 2))
        self.speedX = -5
        self.speedY = 5
        self.max_Y_vel = self.speedY
        self.winner = 0

    def move(self, margin, screen_width, screen_height, player_paddle, ai_paddle):
        if self.rect.top < margin or self.rect.bottom > screen_height:
            self.speedY *= -1

        if self.rect.colliderect(player_paddle) or self.rect.colliderect(ai_paddle):
            self.handle_paddle_collision(player_paddle, ai_paddle)

        if self.rect.left < 0:
            self.winner = 1
        elif self.rect.right > screen_width:
            self.winner = -1

        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.winner

    def handle_paddle_collision(self, player_paddle, ai_paddle):
        self.speedX *= -1
        paddle = player_paddle if self.rect.colliderect(player_paddle) else ai_paddle
        middle_y = paddle.rect.y + paddle.height / 2
        diff_in_y = middle_y - self.rect.y
        reducing_factor = (paddle.height / 2) / self.max_Y_vel
        y_vel = diff_in_y / reducing_factor
        self.speedY = -1 * y_vel

    def draw(self, screen):
        pygame.draw.circle(screen, white, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


class Game:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 500
        self.margin = 50
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Pong')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Constantia', 30)
        self.run = True
        self.live_ball = False
        self.ai_score = 0
        self.player_score = 0
        self.speed_increase = 0
        self.winner = 0
        self.paddle_speed_increase_threshold = 500

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, white)
        self.screen.blit(img, (x, y))

    def draw_board(self):
        self.screen.fill(bg)
        pygame.draw.line(self.screen, white, (0, self.margin), (self.screen_width, self.margin))

    def create_sprites(self):
        player_paddle = Paddle(self.screen_width - 40, self.screen_height // 2, is_player=True)
        ai_paddle = Paddle(20, self.screen_height // 2, is_player=False)
        pong = Ball(self.screen_width - 60, self.screen_height // 2 + 50)
        return player_paddle, ai_paddle, pong

    def reset_ball(self, pong):
        pong.reset(self.screen_width - 60, self.screen_height // 2 + 50)

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
        player_paddle, ai_paddle, pong = self.create_sprites()

        while self.run:
            self.clock.tick(60)

            self.draw_board()
            self.draw_text('AI: ' + str(self.ai_score), 20, 15)
            self.draw_text('Player: ' + str(self.player_score), self.screen_width - 125, 15)
            self.draw_text('BALL SPEED: ' + str(abs(pong.speedX)), self.screen_width // 2 - 100, 15)

            player_paddle.draw(self.screen)
            ai_paddle.draw(self.screen)

            for event in pygame.event.get():
                self.handle_input(event, pong)

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
                if self.winner != 0:
                    self.draw_text('YOU SCORED!' if self.winner == 1 else 'AI SCORED!',
                                   220, self.screen_height // 2 - 100)
                    self.draw_text('CLICK ANYWHERE TO START', 100, self.screen_height // 2 - 50)
                else:
                    self.draw_text('CLICK ANYWHERE TO START', 100, self.screen_height // 2 - 100)

            self.update_speed(pong)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.start_game()