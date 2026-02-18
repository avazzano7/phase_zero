import random
from core.upgrades.base_upgrade import (
    Upgrade,
    EngineUpgrade,
    TopSpeedUpgrade,
    GripUpgrade,
    DriftUpgrade,
    NewCarUpgrade,
    Rarity,
    RARITY_WEIGHTS,
)


UPGRADE_TYPES = [
    EngineUpgrade,
    TopSpeedUpgrade,
    GripUpgrade,
    DriftUpgrade,
    NewCarUpgrade,
]


def roll_rarity():
    total = sum(RARITY_WEIGHTS.values())
    roll = random.uniform(0, total)

    cumulative = 0
    for rarity, weight in RARITY_WEIGHTS.items():
        cumulative += weight
        if roll <= cumulative:
            return rarity

    return Rarity.COMMON


def generate_upgrade():
    rarity = roll_rarity()
    upgrade_class = random.choice(UPGRADE_TYPES)

    name_map = {
        EngineUpgrade: "Engine Upgrade",
        TopSpeedUpgrade: "Top Speed Upgrade",
        GripUpgrade: "Grip Kit",
        DriftUpgrade: "Drift Tuning",
        NewCarUpgrade: "New Car",
    }

    return upgrade_class(name_map[upgrade_class], rarity)


def generate_upgrade_choices(count=3):
    return [generate_upgrade() for _ in range(count)]
