import pygame
from settings import *

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_position, dt):
        target_offset = target_position - pygame.Vector2(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2
        )

        # Smooth follow
        self.offset += (target_offset - self.offset) * 5 * dt
