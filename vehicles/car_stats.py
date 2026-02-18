class CarStats:
    def __init__(
        self,
        acceleration=420,
        brake_force=2400,
        turn_speed=420,
        max_speed=1200,
        grip=3.2,
        drift_grip=0.4,
        angular_damping=0.97,
        drift_assist_force=1600,
        oversteer_strength=6.0,
    ):
        self.acceleration = acceleration
        self.brake_force = brake_force
        self.turn_speed = turn_speed
        self.max_speed = max_speed
        self.grip = grip
        self.drift_grip = drift_grip
        self.angular_damping = angular_damping
        self.drift_assist_force = drift_assist_force
        self.oversteer_strength = oversteer_strength

    def copy(self):
        return CarStats(
            self.acceleration,
            self.brake_force,
            self.turn_speed,
            self.max_speed,
            self.grip,
            self.drift_grip,
            self.angular_damping,
            self.drift_assist_force,
            self.oversteer_strength,
        )
