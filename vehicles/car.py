import pygame


class Car:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.angle = 0
        self.angular_velocity = 0

        self.original_image = pygame.image.load(
            "assets/images/nigel_mobile.png"
        ).convert_alpha()

        self.size = (50, 30)

        # -------------------
        # Core Stats
        # -------------------
        self.acceleration = 420
        self.brake_force = 2400
        self.turn_speed = 320
        self.max_speed = 1200

        self.drag = 0.992
        self.grip = 3.2
        self.drift_grip = 0.5
        self.angular_damping = 0.97

        self.drift_assist_force = 1600
        self.oversteer_strength = 6.0

        # -------------------
        # Gear System (Restored)
        # -------------------
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
        speed_ratio = min(speed / self.max_speed, 1)

        # -------------------
        # Acceleration
        # -------------------
        accel_factor = min(max(0, 1 - speed_ratio) * 1.5, 1)

        if keys[pygame.K_w]:
            self.velocity += forward * self.acceleration * accel_factor * dt

        if keys[pygame.K_s]:
            self.velocity -= forward * self.brake_force * dt

        # -------------------
        # Steering Input
        # -------------------
        steer_input = 0
        if keys[pygame.K_a]:
            steer_input = 1
        if keys[pygame.K_d]:
            steer_input = -1

        # Stronger steering at speed (arcade style)
        steering_factor = 0.6 + speed_ratio * 0.8

        self.angular_velocity += (
            steer_input * self.turn_speed * steering_factor * dt
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
        # DRIFT MODE (Now Actually Works)
        # -------------------
        drifting = keys[pygame.K_SPACE] and speed > 180

        if drifting:
            grip = self.drift_grip

            # Big outward kick
            self.velocity += right * steer_input * self.drift_assist_force * dt

            # Heavy oversteer
            self.angular_velocity += slip_angle * self.oversteer_strength * dt

            # Slight forward push so drift doesn't stall
            self.velocity += forward * 400 * dt
        else:
            grip = self.grip

        # Apply grip
        lateral_velocity *= max(0, 1 - grip * dt)

        self.velocity = forward_velocity + lateral_velocity


        # -------------------
        # Drag + Speed Cap
        # -------------------
        self.velocity *= self.drag

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # -------------------
        # Angular Motion
        # -------------------
        self.angular_velocity *= self.angular_damping
        self.angle += self.angular_velocity * dt

        # -------------------
        # Position
        # -------------------
        self.position += self.velocity * dt

        # ======================================================
        # AUTOMATIC GEAR SYSTEM
        # ======================================================
        speed = self.velocity.length()
        speed_ratio = min(speed / self.max_speed, 1)

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
    # ACCESSORS (Game Requires These)
    # ==========================================================
    def get_engine_rpm(self):
        return self.engine_rpm

    def get_rect(self):
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.position
        return rect
