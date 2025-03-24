import pygame
from pygame.sprite import Sprite
class Hunter(Sprite):
    """管理猎人的类"""

    def __init__(self,hb_game):
        """初始化猎人并设置其初始位置"""
        super().__init__()
        self.screen = hb_game.screen
        self.settings = hb_game.settings
        self.screen_rect = hb_game.screen.get_rect()

        # 加载猎人图像并获取其外接矩形。
        self.image = pygame.image.load('images/hunter.png')
        self.rect = self.image.get_rect()

        # 对于每艘新猎人，都将其放在屏幕左侧中央。
        self.rect.left = self.screen_rect.left

        # 在猎人的属性x，y中存储小数值。
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志。

        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整猎人的位置"""

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.hunter_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom :
            self.y += self.settings.hunter_speed

        # 根据self.x,self.y更新rect对象。
        self.rect.y = self.y


    def blitme(self):
        """在指定位置绘制猎人"""
        self.screen.blit(self.image,self.rect)

    def center_hunter(self):
        """让猎人在屏幕左端居中"""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)