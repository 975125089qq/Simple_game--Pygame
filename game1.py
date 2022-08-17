import pygame
from pygame.locals import *
import random


class square():
    def __init__(self):
        self.x, self.y = random.randint(1, NUM_W - 2) * BLOCK_SIZE, random.randint(1, NUM_H - 2) * BLOCK_SIZE
        self.dir_list = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        self.dir = self.dir_list[random.randint(0, 7)]

    # move the obstacle and target
    def move(self):
        self.x += self.dir[0] * BLOCK_SIZE
        self.y += self.dir[1] * BLOCK_SIZE
        if self.x < 0:
            self.x = 0
            self.dir[0] = -self.dir[0]
        if self.y < 0:
            self.y = 0
            self.dir[1] = -self.dir[1]
        if self.x > BORDER_W:
            self.x = BORDER_W
            self.dir[0] = -self.dir[0]
        if self.y > BORDER_H:
            self.y = BORDER_H
            self.dir[1] = -self.dir[1]

    def change_direction(self):
        self.dir = self.dir_list[random.randint(0, 7)]


# GUI parameter
BLOCK_SIZE = 50
SIZE = WIDTH, HEIGHT = (800, 800)
NUM_W, NUM_H = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE  # number of blocks in a row or a column
BORDER_W, BORDER_H = WIDTH - BLOCK_SIZE * 2, HEIGHT - BLOCK_SIZE * 2  # area where target will be generated

# parameters of the game
x, y = WIDTH / 2, HEIGHT / 2
direc = [0, 0]
score = 0
best_score = 0
life = 3
difficulty = 0
speed = 0

# random target and obstacle
target = square()
NUM_OB = 3
obs = [square() for i in range(NUM_OB)]

# window setting
pygame.init()
running = True
screen = pygame.display.set_mode((SIZE))
pygame.display.set_caption("sanke")
screen.fill((60, 220, 0))
clock = pygame.time.Clock()
count = 0

# loop
while running:
    # change direction
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                direc = [-BLOCK_SIZE, 0]
            if event.key in [K_d, K_RIGHT]:
                direc = [BLOCK_SIZE, 0]
            if event.key in [K_w, K_UP]:
                direc = [0, -BLOCK_SIZE]
            if event.key in [K_s, K_DOWN]:
                direc = [0, BLOCK_SIZE]
    x += direc[0]
    y += direc[1]

    # eat food
    if x == target.x and y == target.y:
        score += 1
        target.x, target.y = random.randint(1, NUM_W - 2) * BLOCK_SIZE, random.randint(1, NUM_H - 2) * BLOCK_SIZE

    # collision with obstacle or wall
    for ob in obs[:difficulty]:
        if (x == ob.x and y == ob.y) or x < 0 or x > WIDTH or y < 0 or y > HEIGHT:
            x, y = WIDTH / 2, HEIGHT / 2
            life -= 1
            direc = [0, 0]
            # dead
            if not life:
                if score > best_score:
                    best_score = score
                life = 3
                score = 0
                difficulty = 0
                speed = 0

    # obstacle and target move
    if speed or count % 2 ==0 :
        for ob in obs[:difficulty]:
            ob.move()

    # draw
    pygame.draw.rect(screen, (50, 250, 100), (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, (0, 50, 50,), (x, y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, (255, 0, 0), (target.x, target.y, BLOCK_SIZE, BLOCK_SIZE))
    for ob in obs[:difficulty]:
        pygame.draw.rect(screen, (0, 0, 255), (ob.x, ob.y, BLOCK_SIZE, BLOCK_SIZE))

    # score_font and life
    font = pygame.font.SysFont(None, 50)
    score_font = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_font, (10, 50))
    life_font = font.render(f"Life: {life}", True, (255, 255, 255))
    screen.blit(life_font, (10, 100))
    best_font = font.render(f"best score: {best_score}", True, (255, 255, 255))
    screen.blit(best_font, (10, 150))
    best_font = font.render(f"difficulty: {difficulty + speed}", True, (255, 255, 255))
    screen.blit(best_font, (10, 200))
    pygame.display.update()
    clock.tick(10)
    count += 1
    if count % 100 == 0:
        count = 1
        if difficulty < NUM_OB:
            difficulty += 1
        elif not speed:
            speed = 1
        else:
            obs[random.randint(0,NUM_OB-1)].change_direction()
pygame.quit()
