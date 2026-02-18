import random


class Rarity:
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


RARITY_WEIGHTS = {
    Rarity.COMMON: 60,
    Rarity.RARE: 25,
    Rarity.EPIC: 10,
    Rarity.LEGENDARY: 5,
}


RARITY_COLORS = {
    Rarity.COMMON: (200, 200, 200),
    Rarity.RARE: (80, 160, 255),
    Rarity.EPIC: (200, 80, 255),
    Rarity.LEGENDARY: (255, 180, 0),
}


class Upgrade:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity

    def apply(self, car):
        raise NotImplementedError

    def get_display_name(self):
        return f"{self.name} ({self.rarity})"


# ==========================================================
# ENGINE UPGRADE
# ==========================================================

class EngineUpgrade(Upgrade):
    def apply(self, car):
        bonus = {
            Rarity.COMMON: 80,
            Rarity.RARE: 140,
            Rarity.EPIC: 220,
            Rarity.LEGENDARY: 350,
        }[self.rarity]

        car.stats.acceleration += bonus


# ==========================================================
# MAX SPEED UPGRADE
# ==========================================================

class TopSpeedUpgrade(Upgrade):
    def apply(self, car):
        bonus = {
            Rarity.COMMON: 100,
            Rarity.RARE: 180,
            Rarity.EPIC: 300,
            Rarity.LEGENDARY: 450,
        }[self.rarity]

        car.stats.max_speed += bonus


# ==========================================================
# GRIP UPGRADE
# ==========================================================

class GripUpgrade(Upgrade):
    def apply(self, car):
        bonus = {
            Rarity.COMMON: 0.3,
            Rarity.RARE: 0.5,
            Rarity.EPIC: 0.8,
            Rarity.LEGENDARY: 1.2,
        }[self.rarity]

        car.stats.grip += bonus


# ==========================================================
# DRIFT UPGRADE
# ==========================================================

class DriftUpgrade(Upgrade):
    def apply(self, car):
        bonus = {
            Rarity.COMMON: 1.0,
            Rarity.RARE: 1.8,
            Rarity.EPIC: 3.0,
            Rarity.LEGENDARY: 5.0,
        }[self.rarity]

        car.stats.oversteer_strength += bonus


# ==========================================================
# NEW CAR UPGRADE
# ==========================================================

class NewCarUpgrade(Upgrade):
    def apply(self, car):
        # Simple stat reset + buff for now
        car.stats = car.base_stats.copy()

        rarity_bonus = {
            Rarity.COMMON: 1.05,
            Rarity.RARE: 1.10,
            Rarity.EPIC: 1.18,
            Rarity.LEGENDARY: 1.30,
        }[self.rarity]

        car.stats.acceleration *= rarity_bonus
        car.stats.max_speed *= rarity_bonus
