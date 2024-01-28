import sys, os, pygame, random, math

pygame.init()
pygame.display.set_caption("Nsnake v1.0")
pygame.font.init()
random.seed()

SPEED = 0.36
SNAKE_SIZE = 9
GHOST_SIZE = 12
SEPARATION = 10
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200
FPS = 37
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE)


score_font = pygame.font.Font(None, 38)
HP_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 46)
play_again_font = HP_numb_font
HP_msg = score_font.render("HP:", 1, pygame.Color("green"))
HP_msg_size = score_font.size("HP")

background_color = pygame.Color(152,229,254)
black = pygame.Color(0, 0, 0)


gameClock = pygame.time.Clock()


def checkCollision(posA, As, posB, Bs):
    # As size of a | Bs size of B
    if (posA.x < posB.x + Bs and posA.x + As > posB.x and posA.y < posB.y + Bs and posA.y + As > posB.y):
        return True
    return False


def checkLimits(entity):
    if (entity.x > SCREEN_WIDTH):
        entity.x = SNAKE_SIZE
    if (entity.x < 0):
        entity.x = SCREEN_WIDTH - SNAKE_SIZE
    if (entity.y > SCREEN_HEIGHT):
        entity.y = SNAKE_SIZE
    if (entity.y < 0):
        entity.y = SCREEN_HEIGHT - SNAKE_SIZE


class Ghost:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("black")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, GHOST_SIZE, GHOST_SIZE), 0)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Zevs.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, 50)


class Mountain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("oblaka.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 1200), random.randint(100, 800))


class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = pygame.color.Color("green")


class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack = []

        self.stack.append(self)

        blackBox = Segment(self.x, self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)

    def move(self):
        last_element = len(self.stack) - 1
        while (last_element != 0):
            self.stack[last_element].direction = self.stack[last_element - 1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        if (len(self.stack) < 2):
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if (self.stack[0].direction == KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED * FPS)
        elif (self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED * FPS)
        elif (self.stack[0].direction == KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED * FPS)
        elif (self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x + (SPEED * FPS)
        self.stack.insert(0, last_segment)

    def getHead(self):
        return (self.stack[0])

    def grow(self):
        last_element = len(self.stack) - 1
        self.stack[last_element].direction = self.stack[last_element].direction
        if (self.stack[last_element].direction == KEY["UP"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y - SNAKE_SIZE)
            blackBox = Segment(newSegment.x, newSegment.y - SEPARATION)

        elif (self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y + SNAKE_SIZE)
            blackBox = Segment(newSegment.x, newSegment.y + SEPARATION)

        elif (self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = Segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x - SEPARATION, newSegment.y)

        elif (self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = Segment(self.stack[last_element].x + SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x + SEPARATION, newSegment.y)

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def setDirection(self, direction):
        if (self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY[
            "LEFT"] and direction == KEY["RIGHT"]):
            pass
        elif (self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["DOWN"] and direction ==
              KEY["UP"]):
            pass
        else:
            self.direction = direction

    def get_rect(self):
        rect = (self.x, self.y)
        return rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def checkCrash(self):
        counter = 1
        while (counter < len(self.stack) - 1):
            if (checkCollision(self.stack[0], SNAKE_SIZE, self.stack[counter], SNAKE_SIZE) and self.stack[
                counter].color != "NULL"):
                return True
            counter += 1
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.color.Color("yellow"),
                         (self.stack[0].x, self.stack[0].y, SNAKE_SIZE, SNAKE_SIZE), 0)
        counter = 1
        while (counter < len(self.stack)):
            if (self.stack[counter].color == "NULL"):
                counter += 1
                continue
            pygame.draw.rect(screen, pygame.color.Color("green"),
                             (self.stack[counter].x, self.stack[counter].y, SNAKE_SIZE, SNAKE_SIZE), 0)
            counter += 1


def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
        if event.type == pygame.QUIT:
            sys.exit()


def respGhost(ghost, index, sx, sy):
    radius = math.sqrt((SCREEN_WIDTH / 2 * SCREEN_WIDTH / 2 + SCREEN_HEIGHT / 2 * SCREEN_HEIGHT / 2)) / 2
    angle = 999
    while (angle > radius):
        angle = random.uniform(0, 800) * math.pi * 2
        x = SCREEN_WIDTH / 2 + radius * math.cos(angle)
        y = SCREEN_HEIGHT / 2 + radius * math.sin(angle)
        if (x == sx and y == sy):
            continue
    newGhost = Ghost(x, y, 1)
    ghost[index] = newGhost

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


def respGhosts(ghosts, quantity, sx, sy):
    counter = 0
    del ghosts[:]
    radius = math.sqrt((SCREEN_WIDTH / 2 * SCREEN_WIDTH / 2 + SCREEN_HEIGHT / 2 * SCREEN_HEIGHT / 2)) / 2
    angle = 999
    while (counter < quantity):
        while (angle > radius):
            angle = random.uniform(0, 800) * math.pi * 2
            x = SCREEN_WIDTH / 2 + radius * math.cos(angle)
            y = SCREEN_HEIGHT / 2 + radius * math.sin(angle)
            if ((x - GHOST_SIZE == sx or x + GHOST_SIZE == sx) and (
                    y - GHOST_SIZE == sy or y + GHOST_SIZE == sy) or radius - angle <= 10):
                continue
        ghosts.append(Ghost(x, y, 1))
        angle = 999
        counter += 1


def gameover():
    exit()

def endGame():
    sys.exit()


def drawHp(HP):
    HP_numb = HP_numb_font.render(str(HP), 1, pygame.Color("black"))
    screen.blit(HP_msg, (SCREEN_WIDTH - HP_msg_size[0] - 60, 10))
    screen.blit(HP_numb, (SCREEN_WIDTH - 45, 14))


def drawGameTime(gameTime):
    game_time = score_font.render("Time:", 1, pygame.Color("green"))
    game_time_numb = HP_numb_font.render(str(gameTime / 1000), 1, pygame.Color("black"))
    screen.blit(game_time, (30, 10))
    screen.blit(game_time_numb, (105, 14))



def main():
    hp = 100

    mySnake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    mySnake.setDirection(KEY["UP"])
    mySnake.move()
    all_sprites = pygame.sprite.Group()
    boss = Boss()
    for i in range(10):
        mount = Mountain()
        all_sprites.add(mount)
    all_sprites.add(boss)
    start_segments = 18
    while (start_segments > 0):
        mySnake.grow()
        mySnake.move()
        start_segments -= 1

    max_ghost = 1
    destghost = False
    ghosts = [Ghost(random.randint(60, SCREEN_WIDTH), random.randint(60, SCREEN_HEIGHT), 1)]
    respGhosts(ghosts, max_ghost, mySnake.x, mySnake.y)

    startTime = pygame.time.get_ticks()
    endgame = 0

    while (endgame != 1):
        gameClock.tick(FPS)

        keyPress = getKey()
        if keyPress == "exit":
            endgame = 1

        checkLimits(mySnake)
        if (mySnake.checkCrash() == True):
            gameover()

        for myGhost in ghosts:
            if (myGhost.state == 1):
                if (checkCollision(mySnake.getHead(), SNAKE_SIZE, myGhost, GHOST_SIZE) == True):
                    mySnake.grow()
                    myGhost.state = 0
                    hp -= 5
                    destghost = True

        if (keyPress):
            mySnake.setDirection(keyPress)
        mySnake.move()

        if (destghost == True):
            destghost = False
            respGhost(ghosts, 0, mySnake.getHead().x, mySnake.getHead().y)

        if hp == 0:
            endGame()

        screen.fill(background_color)
        all_sprites.draw(screen)
        for myGhost in ghosts:
            if (myGhost.state == 1):
                myGhost.draw(screen)

        mySnake.draw(screen)
        drawHp(hp)
        gameTime = pygame.time.get_ticks() - startTime
        drawGameTime(gameTime)
        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    main()