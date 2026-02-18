import pygame
from settings import *
from camera import Camera
from vehicles.car import Car
from audio.engine import EngineSound
from core.run_manager import RunManager
from core.upgrades.base_upgrade import RARITY_COLORS


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        self.camera = Camera()
        self.car = Car(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

        self.run_manager = RunManager()

        self.walls = [
            pygame.Rect(1100, 1700, 1800, 20),
            pygame.Rect(1100, 2000, 1800, 20),
        ]

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
                    self.reset_car()

                if self.run_manager.in_upgrade_phase:
                    if event.key == pygame.K_1:
                        self.select_upgrade(0)
                    if event.key == pygame.K_2:
                        self.select_upgrade(1)
                    if event.key == pygame.K_3:
                        self.select_upgrade(2)

    def reset_car(self):
        self.car.position = pygame.Vector2(
            WORLD_WIDTH // 2,
            WORLD_HEIGHT // 2
        )
        self.car.velocity = pygame.Vector2(0, 0)
        self.car.angle = 0

    def select_upgrade(self, index):
        if index < len(self.run_manager.available_upgrades):
            upgrade = self.run_manager.available_upgrades[index]
            self.run_manager.apply_upgrade(self.car, upgrade)

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self):
        self.run_manager.update(self.dt)

        if not self.run_manager.in_upgrade_phase:
            self.car.update(self.dt)

        self.camera.update(self.car.position, self.dt)

        rpm = self.car.get_engine_rpm()
        self.engine.update(rpm, self.dt)

    # ==========================================================
    # DRAW
    # ==========================================================
    def draw(self):
        self.screen.fill((30, 150, 30))

        # -------- Track Geometry --------
        straight_rect = pygame.Rect(1200, 1800, 1600, 200)
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            straight_rect.move(-self.camera.offset)
        )

        hairpin_rect = pygame.Rect(2600, 1400, 400, 400)
        pygame.draw.rect(
            self.screen,
            (60, 60, 60),
            hairpin_rect.move(-self.camera.offset)
        )

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

        if speed_mph > 120:
            speed_color = (255, 0, 0)
        elif speed_mph > 90:
            speed_color = (255, 200, 0)
        else:
            speed_color = (0, 255, 0)

        hud_rect = pygame.Rect(15, 15, 260, 140)
        pygame.draw.rect(self.screen, (0, 0, 0), hud_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), hud_rect, 2)

        speed_text = self.font.render(
            f"{speed_mph} MPH",
            True,
            speed_color
        )
        self.screen.blit(speed_text, (30, 25))

        gear_text = self.small_font.render(
            f"GEAR: {self.car.current_gear}",
            True,
            (200, 200, 255)
        )
        self.screen.blit(gear_text, (30, 65))

        rpm_text = self.small_font.render(
            f"RPM: {int(self.car.get_engine_rpm() * 100)}%",
            True,
            (180, 180, 180)
        )
        self.screen.blit(rpm_text, (130, 65))

        level_text = self.small_font.render(
            f"LEVEL: {self.run_manager.current_level}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(level_text, (30, 100))

        if not self.run_manager.in_upgrade_phase:
            time_left = int(
                self.run_manager.level_duration -
                self.run_manager.level_timer
            )

            timer_text = self.small_font.render(
                f"TIME: {time_left}",
                True,
                (255, 255, 255)
            )
            self.screen.blit(timer_text, (150, 100))

        # ======================================================
        # UPGRADE PHASE
        # ======================================================

        if self.run_manager.in_upgrade_phase:
            overlay = pygame.Surface(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render(
                "CHOOSE AN UPGRADE",
                True,
                (255, 255, 255)
            )
            self.screen.blit(
                title,
                (SCREEN_WIDTH // 2 - 220, 200)
            )

            for i, upgrade in enumerate(
                self.run_manager.available_upgrades
            ):
                color = RARITY_COLORS[upgrade.rarity]

                text = self.small_font.render(
                    f"{i+1}. {upgrade.get_display_name()}",
                    True,
                    color
                )

                self.screen.blit(
                    text,
                    (SCREEN_WIDTH // 2 - 220, 260 + i * 40)
                )

        pygame.display.flip()
