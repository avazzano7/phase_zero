import pygame
from settings import *
from camera import Camera
from vehicles.car import Car
from audio.engine import EngineSound


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.camera = Camera()
        self.car = Car(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

        self.walls = [
            pygame.Rect(1100, 1700, 1800, 20),
            pygame.Rect(1100, 2000, 1800, 20),
        ]

        # Engine now reacts to gear-based RPM
        self.engine = EngineSound("assets/sounds/engine_idle.mp3")

        self.font = pygame.font.SysFont("consolas", 32)
        self.small_font = pygame.font.SysFont("consolas", 22)

    # ==========================================================
    # MAIN LOOP
    # ==========================================================
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    # ==========================================================
    # EVENTS
    # ==========================================================
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset car
                    self.car.position = pygame.Vector2(
                        WORLD_WIDTH // 2,
                        WORLD_HEIGHT // 2
                    )
                    self.car.velocity = pygame.Vector2(0, 0)
                    self.car.angle = 0

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self):
        self.car.update(self.dt)
        self.camera.update(self.car.position, self.dt)

        # 🔥 Use real gear-based RPM now
        rpm = self.car.get_engine_rpm()
        self.engine.update(rpm, self.dt)

    # ==========================================================
    # DRAW
    # ==========================================================
    def draw(self):
        self.screen.fill((30, 150, 30))  # grass

        # -------- Straight --------
        straight_rect = pygame.Rect(1200, 1800, 1600, 200)
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            straight_rect.move(-self.camera.offset)
        )

        # -------- Hairpin --------
        hairpin_rect = pygame.Rect(2600, 1400, 400, 400)
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            hairpin_rect.move(-self.camera.offset)
        )

        # -------- Drift Circle --------
        drift_center = pygame.Vector2(1800, 1300)
        pygame.draw.circle(
            self.screen,
            (60, 60, 60),
            drift_center - self.camera.offset,
            300
        )

        # -------- Car --------
        self.car.draw(self.screen, self.camera.offset)

        # ======================================================
        # HUD
        # ======================================================

        PIXELS_TO_MPH = 0.15

        speed = self.car.velocity.length()
        speed_mph = int(speed * PIXELS_TO_MPH)

        # Speed color logic
        if speed_mph > 120:
            speed_color = (255, 0, 0)
        elif speed_mph > 90:
            speed_color = (255, 200, 0)
        else:
            speed_color = (0, 255, 0)

        # Background panel
        hud_rect = pygame.Rect(15, 15, 220, 100)
        pygame.draw.rect(self.screen, (0, 0, 0), hud_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), hud_rect, 2)

        # Speed text
        speed_text = self.font.render(
            f"{speed_mph} MPH",
            True,
            speed_color
        )
        self.screen.blit(speed_text, (30, 25))

        # Gear display
        gear_text = self.small_font.render(
            f"GEAR: {self.car.current_gear}",
            True,
            (200, 200, 255)
        )
        self.screen.blit(gear_text, (30, 65))

        # Optional RPM debug display
        rpm_text = self.small_font.render(
            f"RPM: {int(self.car.get_engine_rpm() * 100)}%",
            True,
            (180, 180, 180)
        )
        self.screen.blit(rpm_text, (130, 65))

        pygame.display.flip()
