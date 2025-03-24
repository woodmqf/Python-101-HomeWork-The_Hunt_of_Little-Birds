class Settings:
    """存储游戏《狩猎小鸟》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (135,206,250)



        # 子弹设置
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (0, 0, 128)
        self.bullets_allowed = 3

        # 敌人子弹设置
        self.enemy_bullet_color = (255, 0, 0)

        # 小鸟设置
        self.fleet_drop_speed = 10

        # 加快游戏节奏速度。
        self.speedup_scale = 1.1

        # 小鸟分数的提高速度。
        self.score_scale = 1.5

        # 设置小鸟射击频率
        self.bird_fire_rate = 5
        self.enemy_bullet_speed = 1.0

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self,difficulty = "normal"):
        """初始化随游戏进行而变化的设置"""
        if difficulty == "easy":
            self.hunter_speed = 1.5
            self.bullet_speed = 3.0
            self.bird_speed = 1.0

            self.bird_fire_rate = 3
            self.enemy_bullet_speed = 1.0

        elif difficulty == "normal":
            self.hunter_speed = 1.0
            self.bullet_speed = 2.0
            self.bird_speed = 1.5

            self.bird_fire_rate = 5
            self.enemy_bullet_speed = 1.3

        elif difficulty == "hard":
            self.hunter_speed = 1.0
            self.bullet_speed = 1.0
            self.bird_speed = 2.0

            self.bird_fire_rate = 7
            self.enemy_bullet_speed = 1.5

        # 猎人设置
        self.hunter_limit = 7

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 记分
        self.bird_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.hunter_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bird_speed *= self.speedup_scale

        self.bird_points = int(self.bird_points * self.score_scale)
