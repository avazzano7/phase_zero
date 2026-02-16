import pygame
from settings import WORLD_WIDTH, WORLD_HEIGHT


class Player:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.speed = 600  # fast for testing

    def update(self, dt):
        keys = pygame.key.get_pressed()

        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1

        if direction.length() > 0:
            direction = direction.normalize()

        self.position += direction * self.speed * dt
        self.position.x = max(0, min(self.position.x, WORLD_WIDTH))
        self.position.y = max(0, min(self.position.y, WORLD_HEIGHT))

