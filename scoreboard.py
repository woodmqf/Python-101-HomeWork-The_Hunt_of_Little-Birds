import pygame.font
from pygame.sprite import Group

from hunter import Hunter

class Scoreboard:
    """显示得分信息的类"""

    def __init__(self,hb_game):
        """初始化显示得分涉及的属性。"""
        self.hb_game = hb_game
        self.screen = hb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = hb_game.settings
        self.stats = hb_game.stats
        self.stats = hb_game.stats

        # 显示得分信息时使用的字体设置。
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        # 准备初始得分图像和当前最高得分。
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_hunters()



    def prep_score(self):
        """将得分转换为一幅渲染的图像。"""
        rounded_score = round(self.stats.score, -1)
        score_str ="Score:" + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str,True,
                    self.text_color,self.settings.bg_color)

        # 在屏幕右上角显示得分。
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str ="High Score:" + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,
                self.text_color,self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央。
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx =self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染的图像。"""
        level_str = "Lv:"+ str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.settings.bg_color)

        # 将等级放在得分下方。
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_hunters(self):
        """显示还余下多少个猎人"""
        self.hunters = Group()
        for hunter_number in range(self.stats.hunters_exist):
            hunter = Hunter(self.hb_game)
            hunter.rect.x = self.settings.screen_width-hunter.rect.width - 10
            hunter.rect.y = self.settings.screen_height - (hunter_number+1) * (hunter.rect.height+10) - 10
            self.hunters.add(hunter)



    def show_score(self):
        """在屏幕上显示得分、等级和余下的猎人数。"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.hunters.draw(self.screen)

    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
