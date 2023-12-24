import pygame
import sys

class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 50

    def terminate(self):
        pygame.quit()
        sys.exit()


    def run_game(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()


            self.screen.fill(pygame.Color('#1f7515'))

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.run_game()