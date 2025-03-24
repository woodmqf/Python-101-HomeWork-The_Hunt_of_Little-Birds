import pygame
from pygame.sprite import Sprite

class Bird(Sprite):
    """表示单个小鸟的类"""

    def __init__(self,hb_game):
        """初始化小鸟并设置其起始位置"""
        super().__init__()
        self.screen = hb_game.screen
        self.settings = hb_game.settings

        # 加载小鸟图像并设置其rect属性
        self.image = pygame.image.load('images/bird.png')
        self.rect = self.image.get_rect()

        #每个小鸟最初都在屏幕右上角附近。
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height

        # 存储小鸟的精确水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def check_edges(self):
        """如果小鸟位于屏幕边缘，就返回True。"""
        screen_rect = self.screen.get_rect()
        if  self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        """向上或下移动小鸟"""
        self.y += (self.settings.bird_speed * self.settings.fleet_direction)
        self.rect.y = self.y





