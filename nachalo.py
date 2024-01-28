import sys, os, pygame, gerkules

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("data\9a49e1c170bd8c1.mp3")
pygame.mixer.music.play()
pygame.display.set_caption("zmeika")
pygame.font.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
FPS = 25



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)
gameClock = pygame.time.Clock()

def load_image(name, colorkey=None):
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


class kartinka(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


def main():
    all_sprites = pygame.sprite.Group()
    a = 1
    pic = kartinka(f"{a}.png")
    all_sprites.add(pic)
    endgame = 0

    while (endgame != 1):
        gameClock.tick(FPS)
        all_sprites.draw(screen)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                a += 1
                if a < 4:
                    pic = kartinka(f"{a}.png")
                    all_sprites.add(pic)
                else:
                    pygame.mixer.music.stop()
                    gerkules.main()
                    exit()


        all_sprites.draw(screen)
        pygame.display.flip()
        pygame.display.update()


main()