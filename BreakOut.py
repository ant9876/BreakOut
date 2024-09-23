from random import randint

import pygame
from pygame import Color
from pygame.draw_py import draw_polygon
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()


class Player(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 15)  # arbitrary values TODO yes
        self.vx = 0

    def draw(self):
        pygame.draw.rect(screen, 'gray', self, 0)  #0 will fill the rectangle
        pygame.draw.rect(screen, 'black', self, 1)  # 1 will outline the rectangle

    def update(self):
        self.x += self.vx
        if self.x < 0:
            self.x = 0
        if self.x + self.width > screen.get_width():
            self.x = screen.get_width() - self.width


class Ball(pygame.Rect):
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.vx = random.randint(3, 6) * random.choice([-1, 1])
        self.vy = random.randint(3, 4)

    def draw(self):
        pygame.draw.ellipse(screen, Color(102, 153, 204), self, 0)
        pygame.draw.ellipse(screen, Color(77, 109, 142), self, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > screen.get_width()-self.width:
            self.vx*=-1
        if self.y < 0:
            self.vy*=-1
        elif self.y > screen.get_height():
            self.y = screen.get_height() // 2



class Brick(pygame.Rect):
    WIDTH = 85
    HEIGHT = 20
    def __init__(self, x, y):
        super().__init__(x, y, Brick.WIDTH, Brick.HEIGHT)
        self.color = Color (randint(0,250), randint(0,250), randint(0,250))

    def draw(self):
        pygame.draw.rect(screen, self.color, self, 0)



player = Player(screen.get_width() / 2 - 30, screen.get_height() - 40)
ball = Ball(screen.get_width() / 2 - 10, screen.get_height() / 2 + 20, 20)
brick_list = []

for x in range(2, screen.get_width()-Brick.WIDTH, Brick.WIDTH):
    for y in range(2, 302, Brick.HEIGHT+2):
        brick_list.append(Brick(x,y))



while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx -= 7
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx += 7
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.vx += 7
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.vx -= 7

    # Do logical updates here.

    player.update()
    ball.update()
    if ball.colliderect(player):
        ball.vy*=-1
        ball.y = player.y - ball.width
        diff = (ball.x +ball.w/2) - (player.x + player.w/2)
        ball.vx += diff // 10

    for b in brick_list[:]:  # iterate over a copy of the list
        if ball.colliderect(b):
            ball.vy *= -1
            brick_list.remove(b)

    screen.fill("light blue")  # Fill the display with a solid color

    # Render the graphics here.
    player.draw()
    ball.draw()
    for b in brick_list:
        b.draw()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)  # wait until next frame (at 60 FPS)
