
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

class Ball(pygame.sprite.Sprite):
    """ This class represents a simple ball class. """

    def __init__(self, surface, color, center, width):
        """ Create a new instance of a ball """
        super().__init__()
        self.surface = surface
        self.color = color
        self.center = center
        self.width = width

    def display(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.width)


class Paddle:
    """ This class represents a simple paddle class. """

    def __init__(self, surface, color, rect):
        """ Create a new instance of a paddle """
        self.surface = surface
        self.color = color
        self.rect = rect

    def display(self):
        pygame.draw.rect(self.surface, self.color, self.rect)


class Game(object):
    """This class represents an instance of the game. If we need to
    reset the game we'd just need to create a new instance of this
    class. """

    def __init__(self, screen, ball, player_one, player_two):
        self.screen = screen
        self.ball = ball
        self.player_one = player_one
        self.player_two = player_two
        self.game_over = False

    def load(self):
        self.ball.display()
        self.player_one.display()
        self.player_two.display()
        pygame.draw.line(self.screen, RED, (SCREEN_WIDTH / 2, 40), (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40), 3)

    def process_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()
        return False

    def display_frame(self, screen):
        screen.fill(BLACK)
        self.load()
        pygame.display.flip()

def main():

    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Pong")
    pygame.mouse.set_visible(False)

    done = False
    clock = pygame.time.Clock()

    ball = Ball(screen, WHITE, [int(SCREEN_WIDTH / 2), 20], 10)
    player_one = Paddle(screen, WHITE, [20, SCREEN_HEIGHT / 2 - 150, 10, 150])
    player_two = Paddle(screen, WHITE, [SCREEN_WIDTH - 30, SCREEN_HEIGHT / 2 - 150, 10, 150])
    game = Game(screen, ball, player_one, player_two)

    while not done:

        done = game.process_events()

        game.display_frame(screen)

        clock.tick(20)

    pygame.quit()

if __name__ == '__main__':
    main()

