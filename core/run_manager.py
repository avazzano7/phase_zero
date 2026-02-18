from core.upgrades.upgrade_pool import generate_upgrade_choices


class RunManager:
    def __init__(self):
        # --------------------------
        # Level Timing
        # --------------------------
        self.level_duration = 30.0
        self.level_timer = 0.0

        # --------------------------
        # Level State
        # --------------------------
        self.current_level = 1
        self.in_upgrade_phase = False

        # --------------------------
        # Money
        # --------------------------
        self.money_collected = 0
        self.total_money = 0

        # --------------------------
        # Upgrade System
        # --------------------------
        self.available_upgrades = []

    # ==========================================================
    # UPDATE
    # ==========================================================
    def update(self, dt):
        if self.in_upgrade_phase:
            return

        self.level_timer += dt

        if self.level_timer >= self.level_duration:
            self.start_upgrade_phase()

    # ==========================================================
    # MONEY
    # ==========================================================
    def add_money(self, amount):
        self.money_collected += amount
        self.total_money += amount

    # ==========================================================
    # LEVEL TRANSITIONS
    # ==========================================================
    def start_upgrade_phase(self):
        self.in_upgrade_phase = True
        self.level_timer = 0.0
        self.generate_upgrades()

    def end_upgrade_phase(self):
        self.in_upgrade_phase = False
        self.current_level += 1
        self.money_collected = 0

    # ==========================================================
    # UPGRADES
    # ==========================================================
    def generate_upgrades(self):
        self.available_upgrades = generate_upgrade_choices(3)

    def apply_upgrade(self, car, upgrade):
        upgrade.apply(car)
        self.end_upgrade_phase()
