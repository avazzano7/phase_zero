import pygame


class Car:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.angle = 0

        # Core stats
        self.acceleration = 1200
        self.brake_force = 2000
        self.turn_speed = 180
        self.max_speed = 900

        self.drag = 0.995
        self.grip = 8  # higher = tighter handling

        self.size = (50, 30)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        forward = pygame.Vector2(1, 0).rotate(-self.angle)
        right = pygame.Vector2(0, 1).rotate(-self.angle)

        # -------------------
        # Acceleration
        # -------------------
        if keys[pygame.K_w]:
            self.velocity += forward * self.acceleration * dt

        if keys[pygame.K_s]:
            self.velocity -= forward * self.brake_force * dt

        # -------------------
        # Speed-Based Steering
        # -------------------
        speed = self.velocity.length()
        speed_factor = max(0.3, min(speed / self.max_speed, 1))

        if keys[pygame.K_a]:
            self.angle += self.turn_speed * speed_factor * dt

        if keys[pygame.K_d]:
            self.angle -= self.turn_speed * speed_factor * dt

        # -------------------
        # Separate Velocities
        # -------------------
        forward_velocity = forward * self.velocity.dot(forward)
        lateral_velocity = right * self.velocity.dot(right)

        # -------------------
        # Hand Brake (Drift)
        # -------------------
        if keys[pygame.K_SPACE]:
            lateral_velocity *= 0.5
            self.velocity *= 0.95  # slight speed loss when handbraking

        # Reduce lateral velocity using grip
        lateral_velocity *= max(0, 1 - self.grip * dt)

        # Combine them back
        self.velocity = forward_velocity + lateral_velocity

        # -------------------
        # Drag
        # -------------------
        self.velocity *= self.drag

        # Clamp speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Move
        self.position += self.velocity * dt
