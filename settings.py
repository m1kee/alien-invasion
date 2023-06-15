class Settings:
    """All the configurations of the game"""

    def __init__(self):
        """Initialize all the game configurations"""
        self.alien_points = None
        self.ship_speed = None
        self.bullet_speed = None
        self.alien_speed = None
        self.fleet_direction = None
        self.fleet_drop_speed = None

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (24, 32, 48)

        # Ship settings
        self.ship_lives = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_cadence = 10

        # Max difficult settings
        self.max_ship_speed = 7.0
        self.max_bullet_speed = 7.0
        self.max_alien_speed = 3.5
        self.max_alien_points = 10000
        self.max_fleet_drop_speed = 40

        # Game speed scale
        self.speedup_scale = 1.3
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the dynamic settings that changes during the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 0.4
        self.alien_points = 50
        self.fleet_drop_speed = 10

        # 1 = right; -1 = left
        self.fleet_direction = 1

    def increase_speed(self):
        ship_speed = self.ship_speed * self.speedup_scale
        if ship_speed >= self.max_ship_speed:
            ship_speed = self.max_ship_speed

        self.ship_speed = ship_speed

        bullet_speed = self.bullet_speed * self.speedup_scale
        if bullet_speed >= self.max_bullet_speed:
            bullet_speed = self.max_bullet_speed

        self.bullet_speed = bullet_speed

        alien_speed = self.alien_speed * self.speedup_scale
        if alien_speed >= self.max_alien_speed:
            alien_speed = self.max_alien_speed

        self.alien_speed = alien_speed

        alien_points = int(self.alien_points * self.score_scale)
        if alien_points >= self.max_alien_points:
            alien_points = self.max_alien_points

        self.alien_points = alien_points

