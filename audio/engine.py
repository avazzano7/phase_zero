import pygame
import numpy as np


class EngineSound:
    def __init__(self, sound_path):
        self.base_sound = pygame.mixer.Sound(sound_path)
        self.base_array = pygame.sndarray.array(self.base_sound)

        self.layers = []
        self.channels = []

        self.num_layers = 12
        self.min_pitch = 0.5
        self.max_pitch = 1.6

        self.current_rpm = 0.0
        self.rpm_smoothing = 2.0   # higher = faster response


        # Pre-generate pitch layers
        for i in range(self.num_layers):
            ratio = i / (self.num_layers - 1)
            pitch = self.min_pitch + ratio * (self.max_pitch - self.min_pitch)

            pitched = self._resample(self.base_array, pitch)
            sound = pygame.sndarray.make_sound(pitched)

            channel = pygame.mixer.Channel(i)
            channel.play(sound, loops=-1)
            channel.set_volume(0)

            self.layers.append(sound)
            self.channels.append(channel)

    def _resample(self, array, pitch):
        new_length = int(len(array) / pitch)

        indices = np.linspace(
            0,
            len(array) - 1,
            new_length
        ).astype(np.int32)

        return array[indices]

    def update(self, rpm_ratio, dt):
        rpm_ratio = max(0, min(rpm_ratio, 1))

        # Smooth RPM toward target
        self.current_rpm += (rpm_ratio - self.current_rpm) * self.rpm_smoothing * dt

        position = self.current_rpm * (self.num_layers - 1)

        lower = int(position)
        upper = min(lower + 1, self.num_layers - 1)

        blend = position - lower

        for i in range(self.num_layers):
            self.channels[i].set_volume(0)

        self.channels[lower].set_volume(1 - blend)
        self.channels[upper].set_volume(blend)

