import pygame


class Car:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.angle = 0

        # Load car image
        self.original_image = pygame.image.load(
            "assets/images/corvette_c4.png"
        ).convert_alpha()

        # Physics size (used for shadow + rect)
        self.size = (50, 30)

        # -------------------
        # Core Stats (arcade tuned)
        # -------------------
        self.acceleration = 400
        self.brake_force = 2200
        self.turn_speed = 220
        self.max_speed = 1200

        self.drag = 0.992
        self.grip = 2.5

        # -------------------
        # Gear System
        # -------------------
        # Normalized speed thresholds (0 → 1 of max_speed)
        self.gear_ratios = [0.0, 0.18, 0.35, 0.55, 0.75, 0.9, 1.0]
        self.current_gear = 1
        self.max_gears = len(self.gear_ratios) - 1

        self.engine_rpm = 0.0  # 0–1 value for sound system

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self, dt):
        keys = pygame.key.get_pressed()

        forward = pygame.Vector2(1, 0).rotate(-self.angle)
        right = pygame.Vector2(0, 1).rotate(-self.angle)

        speed = self.velocity.length()
        speed_ratio = min(speed / self.max_speed, 1)

        # -------------------
        # Speed-Based Acceleration Taper
        # -------------------
        accel_factor = min(max(0, 1 - speed_ratio) * 1.5, 1)

        if keys[pygame.K_w]:
            self.velocity += forward * self.acceleration * accel_factor * dt

        if keys[pygame.K_s]:
            self.velocity -= forward * self.brake_force * dt

        speed = self.velocity.length()
        speed_ratio = min(speed / self.max_speed, 1)

        # -------------------
        # Automatic Gear Selection
        # -------------------
        for i in range(1, self.max_gears + 1):
            if speed_ratio < self.gear_ratios[i]:
                self.current_gear = i - 1
                break
        else:
            self.current_gear = self.max_gears

        # -------------------
        # Calculate RPM Within Current Gear
        # -------------------
        lower = self.gear_ratios[self.current_gear]
        upper = self.gear_ratios[min(self.current_gear + 1, self.max_gears)]

        gear_span = max(upper - lower, 0.001)
        gear_progress = (speed_ratio - lower) / gear_span
        gear_progress = max(0, min(gear_progress, 1))

        # Throttle spike effect
        throttle_boost = 0.0
        if keys[pygame.K_w]:
            throttle_boost = 0.15 * (1 - gear_progress)

        self.engine_rpm = min(1.0, gear_progress + throttle_boost)

        # -------------------
        # Steering (Speed-Based)
        # -------------------
        steering_factor = max(0.4, min(speed_ratio, 1))
        turn_boost = 1.6 if keys[pygame.K_SPACE] else 1.0

        if keys[pygame.K_a]:
            self.angle += self.turn_speed * steering_factor * turn_boost * dt

        if keys[pygame.K_d]:
            self.angle -= self.turn_speed * steering_factor * turn_boost * dt

        # -------------------
        # Separate Velocities
        # -------------------
        forward_velocity = forward * self.velocity.dot(forward)
        lateral_velocity = right * self.velocity.dot(right)

        # -------------------
        # Handbrake Drift
        # -------------------
        if keys[pygame.K_SPACE]:
            lateral_velocity *= 0.05
            grip_multiplier = 0.25
            forward_velocity *= 0.98
        else:
            grip_multiplier = 1.0

        lateral_velocity *= max(0, 1 - self.grip * grip_multiplier * dt)

        self.velocity = forward_velocity + lateral_velocity

        # -------------------
        # Drag
        # -------------------
        self.velocity *= self.drag

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.position += self.velocity * dt

    # ==========================================================
    # DRAW
    # ==========================================================
    def draw(self, surface, offset):

        # ---------- Shadow ----------
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

        shadow_offset = pygame.Vector2(0, 5)
        shadow_rect = rotated_shadow.get_rect(
            center=self.position - offset + shadow_offset
        )

        surface.blit(rotated_shadow, shadow_rect)

        # ---------- Car ----------
        rotated_surface = pygame.transform.rotate(
            self.original_image,
            self.angle - 90
        )

        rotated_rect = rotated_surface.get_rect(
            center=self.position - offset
        )

        surface.blit(rotated_surface, rotated_rect)

    # ==========================================================
    # ENGINE RPM ACCESSOR
    # ==========================================================
    def get_engine_rpm(self):
        return self.engine_rpm

    def get_rect(self):
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.position
        return rect
