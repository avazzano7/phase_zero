import pygame
from vehicles.car_stats import CarStats


class Car:
    def __init__(self, x, y, stats=None):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.angle = 0
        self.angular_velocity = 0

        self.original_image = pygame.image.load(
            "assets/images/corvette_c4_grand_sport.png"
        ).convert_alpha()

        self.size = (50, 30)

        # =============================
        # Stats System (Upgrade-Ready)
        # =============================
        self.base_stats = stats if stats else CarStats()
        self.stats = self.base_stats.copy()

        # =============================
        # Gear System
        # =============================
        self.gear_ratios = [0.0, 0.18, 0.35, 0.55, 0.75, 0.9, 1.0]
        self.current_gear = 1
        self.max_gears = len(self.gear_ratios) - 1
        self.engine_rpm = 0.0

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self, dt):
        keys = pygame.key.get_pressed()

        forward = pygame.Vector2(1, 0).rotate(-self.angle)
        right = pygame.Vector2(0, 1).rotate(-self.angle)

        speed = self.velocity.length()
        speed_ratio = min(speed / self.stats.max_speed, 1)

        # -------------------
        # Acceleration
        # -------------------
        accel_factor = min(max(0, 1 - speed_ratio) * 1.5, 1)

        if keys[pygame.K_w]:
            self.velocity += (
                forward * self.stats.acceleration * accel_factor * dt
            )

        if keys[pygame.K_s]:
            self.velocity -= (
                forward * self.stats.brake_force * dt
            )

        # -------------------
        # Steering
        # -------------------
        steer_input = 0
        if keys[pygame.K_a]:
            steer_input = 1
        if keys[pygame.K_d]:
            steer_input = -1

        steering_factor = 0.6 + speed_ratio * 0.8

        self.angular_velocity += (
            steer_input * self.stats.turn_speed * steering_factor * dt
        )

        # -------------------
        # Separate Velocity
        # -------------------
        forward_velocity = forward * self.velocity.dot(forward)
        lateral_velocity = right * self.velocity.dot(right)

        # -------------------
        # Slip Angle
        # -------------------
        if speed > 5:
            velocity_dir = self.velocity.normalize()
            forward_dir = forward.normalize()
            slip_angle = velocity_dir.angle_to(forward_dir)
        else:
            slip_angle = 0

        # -------------------
        # Drift Mode
        # -------------------
        drifting = keys[pygame.K_SPACE] and speed > 180

        if drifting:
            grip = self.stats.drift_grip

            # Arcade rear kick
            self.velocity += (
                right * steer_input *
                self.stats.drift_assist_force * dt
            )

            # Oversteer rotation
            self.angular_velocity += (
                slip_angle *
                self.stats.oversteer_strength * dt
            )
        else:
            grip = self.stats.grip

        lateral_velocity *= max(0, 1 - grip * dt)
        self.velocity = forward_velocity + lateral_velocity

        # -------------------
        # Drag + Speed Cap
        # -------------------
        self.velocity *= 0.992

        if self.velocity.length() > self.stats.max_speed:
            self.velocity.scale_to_length(self.stats.max_speed)

        # -------------------
        # Angular Motion
        # -------------------
        self.angular_velocity *= self.stats.angular_damping
        self.angle += self.angular_velocity * dt

        # -------------------
        # Position
        # -------------------
        self.position += self.velocity * dt

        # ======================================================
        # Automatic Gear + RPM
        # ======================================================
        speed = self.velocity.length()
        speed_ratio = min(speed / self.stats.max_speed, 1)

        for i in range(1, self.max_gears + 1):
            if speed_ratio < self.gear_ratios[i]:
                self.current_gear = i - 1
                break
        else:
            self.current_gear = self.max_gears

        lower = self.gear_ratios[self.current_gear]
        upper = self.gear_ratios[min(self.current_gear + 1, self.max_gears)]

        gear_span = max(upper - lower, 0.001)
        gear_progress = (speed_ratio - lower) / gear_span
        gear_progress = max(0, min(gear_progress, 1))

        throttle_boost = 0.0
        if keys[pygame.K_w]:
            throttle_boost = 0.15 * (1 - gear_progress)

        self.engine_rpm = min(1.0, gear_progress + throttle_boost)

    # ==========================================================
    # DRAW
    # ==========================================================
    def draw(self, surface, offset):
        shadow_width = int(self.size[0] * 0.8)
        shadow_height = int(self.size[1] * 2)

        shadow_surface = pygame.Surface(
            (shadow_width, shadow_height),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            shadow_surface,
            (0, 0, 0, 100),
            shadow_surface.get_rect()
        )

        rotated_shadow = pygame.transform.rotate(
            shadow_surface,
            self.angle - 90
        )

        shadow_rect = rotated_shadow.get_rect(
            center=self.position - offset + pygame.Vector2(0, 5)
        )

        surface.blit(rotated_shadow, shadow_rect)

        rotated_surface = pygame.transform.rotate(
            self.original_image,
            self.angle - 90
        )

        rotated_rect = rotated_surface.get_rect(
            center=self.position - offset
        )

        surface.blit(rotated_surface, rotated_rect)

    # ==========================================================
    # ACCESSORS
    # ==========================================================
    def get_engine_rpm(self):
        return self.engine_rpm

    def get_rect(self):
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.position
        return rect
