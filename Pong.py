
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

class Ball(pygame.sprite.Sprite):
    """ This class represents a simple ball class. """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-2, -1, 1, 2])

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Constraints
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.dy *= -1

class Score():
    def __init__(self, ball, screen):
        self.screen = screen
        self.ball = ball
        self.score_one = 0
        self.score_two = 0
        self.score_font = pygame.font.SysFont(None, 100)

    def update(self):
        if self.ball.rect.right < 0:
            self.score_two += 1
            self.ball.__init__()
        if self.ball.rect.left > SCREEN_WIDTH:
            self.score_one += 1
            self.ball.__init__()
        self.player_one_score = self.score_font.render(str(self.score_one), True, WHITE, BLACK)
        self.player_two_score = self.score_font.render(str(self.score_two), True, WHITE, BLACK)

    def draw(self):
        self.screen.blit(self.player_one_score, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8))
        self.screen.blit(self.player_two_score, (SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 8))


class Player1(pygame.sprite.Sprite):
    """ This class represents a simple paddle class. """

    def __init__(self):
        """ Create a new instance of a paddle """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = 25
        self.rect.centery = SCREEN_HEIGHT / 2
        self.dy = 0

    def update(self):
        self.dy = 0
        # movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.dy = -3
        if keystate[pygame.K_s]:
            self.dy = 3
        self.rect.y += self.dy

        # Contraints -w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Player2(pygame.sprite.Sprite):
    """ This class represents a simple paddle class. """

    def __init__(self):
        """ Create a new instance of a paddle """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.right = SCREEN_WIDTH - 25
        self.rect.centery = SCREEN_HEIGHT / 2
        self.dy = 0

    def update(self):
        self.dy = 0
        # movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.dy = -3
        if keystate[pygame.K_DOWN]:
            self.dy = 3
        self.rect.y += self.dy

        # Contraints -w
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Game(object):
    """This class represents an instance of the game. If we need to
    reset the game we'd just need to create a new instance of this
    class. """

    def __init__(self, screen, ball, player_one, player_two, score):
        self.screen = screen
        self.ball = ball
        self.player_one = player_one
        self.player_two = player_two
        self.game_over = False
        self.screen_rect = self.screen.get_rect()
        self.score = score

        # Create a list to add all sprites
        self.all_sprites = pygame.sprite.Group()

        # Create a list to add only the ball sprite
        self.ball_sprite = pygame.sprite.GroupSingle()

        self.all_sprites.add(self.player_one)
        self.all_sprites.add(self.player_two)
        self.ball_sprite.add(self.ball)

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
        return False

    def run_logic(self):
        if not self.game_over:
            self.all_sprites.update()
            self.ball_sprite.update()
            self.score.update()

            # Collision with paddle
            collision = pygame.sprite.spritecollideany(self.ball, self.all_sprites)
            if collision:
                if collision == self.player_one:
                    self.ball.rect.x -= self.ball.dx
                    self.ball.dx *= -1
                    self.ball.dx += random.choice([0, 1])
                if collision == self.player_two:
                    self.ball.rect.x -= self.ball.dx
                    self.ball.dx *= -1
                    self.ball.dx += random.choice([0, 1])
                if self.ball.dy == 0:
                    self.ball.dy += random.choice([-1, 1])
                if self.ball.dy <= 0:
                    self.ball.dy += random.choice([-1, 0, 1])
                if self.ball.dy >= 0:
                    self.ball.dy += random.choice([-1, 0, 1])


    def display_frame(self):
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        pygame.draw.circle(self.screen, RED, (SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2), 80, 1)
        self.all_sprites.draw(self.screen)
        self.ball_sprite.draw(self.screen)
        self.score.draw()
        pygame.display.flip()

def main():

    # intiialize pygame and music
    pygame.init()
    pygame.mixer.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pong")
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()
    fps = 120

    player_one = Player1()
    player_two = Player2()
    ball = Ball()
    score = Score(ball, screen)

    game = Game(screen, ball, player_one, player_two, score)

    while not done:

        done = game.process_events()

        game.run_logic()

        game.display_frame()

        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    main()

