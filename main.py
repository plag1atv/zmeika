import pygame
import sys
import os

class snake(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__(app.all_sprites)
        self.image = app.load_image("snake.png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass


class app:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.all_sprites = pygame.sprite.Group()
        self.hero = snake(self)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run_game(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.hero.rect.x -= 10
            if keys[pygame.K_RIGHT]:
                self.hero.rect.x += 10
            if keys[pygame.K_UP]:
                self.hero.rect.y -= 10
            if keys[pygame.K_DOWN]:
                self.hero.rect.y += 10


            self.screen.fill(pygame.Color('#1f7515'))
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = app()
    app.run_game()