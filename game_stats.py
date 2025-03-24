class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self,hb_game):
        """初始化统计信息。"""
        self.settings = hb_game.settings
        self.reset_stats()

        # 游戏刚启动时处于非活动状态。
        self.game_active = False
        self.paused = False

        # 任何情况下都不应重置最高得分。
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息。"""
        self.hunters_exist = self.settings.hunter_limit
        self.score = 0
        self.level = 1

    def high_score_save(self):
        # 存储最高分
        with open("high_score_save.csv",'w') as file_object:
            high_score = self.high_score
            file_object.write(str(high_score))

    def high_score_read(self):
        # 读取最高分
        with open("high_score_save.csv") as file_object:
            self.high_score = int(file_object.read())
