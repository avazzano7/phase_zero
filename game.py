import pygame
from settings import *
from camera import Camera
from vehicles.car import Car


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.camera = Camera()
        self.car = Car(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset car state
                    self.car.position = pygame.Vector2(
                        WORLD_WIDTH // 2,
                        WORLD_HEIGHT // 2
                    )
                    self.car.velocity = pygame.Vector2(0, 0)
                    self.car.angle = 0

    def update(self):
        self.car.update(self.dt)
        self.camera.update(self.car.position, self.dt)

    def draw(self):
        # Grass background
        self.screen.fill((30, 150, 30))

        # Draw open arena (asphalt test area)
        arena_rect = pygame.Rect(1000, 1000, 2000, 2000)

        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            arena_rect.move(-self.camera.offset)
        )

        # --- Draw Car ---
        car_surface = pygame.Surface(self.car.size, pygame.SRCALPHA)
        car_surface.fill((200, 0, 0))

        rotated_surface = pygame.transform.rotate(
            car_surface,
            self.car.angle
        )

        rotated_rect = rotated_surface.get_rect(
            center=self.car.position - self.camera.offset
        )

        self.screen.blit(rotated_surface, rotated_rect)

        pygame.display.flip()
