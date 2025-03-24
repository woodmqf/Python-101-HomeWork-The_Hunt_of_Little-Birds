import pygame
from pygame.sprite import Sprite
class BaseBullet(pygame.sprite.Sprite):
    def __init__(self, hb_game):
        super().__init__()
        self.screen = hb_game.screen
        self.settings = hb_game.settings

    def update(self):
        pass  # 具体的更新逻辑在子类中实现

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Bullet(BaseBullet):
    """管理猎人所发射子弹的类"""

    def __init__(self,hb_game):
        """在猎人当前位置创建一个子弹对象"""
        super().__init__(hb_game)
        self.color = self.settings.bullet_color

        # 在（0,0）处创建一个表示子弹的矩形，再设置正确的位置。
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midright = hb_game.hunter.rect.midright

        # 存储用小数表示的子弹位置。
        self.x = float(self.rect.x)

    def update(self):
        """向右移动子弹"""
        # 更新表示子弹位置的小数值
        self.x += self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.x = self.x

class Enemy_Bullet(BaseBullet):
    """管理小鸟所发射子弹的类"""

    def __init__(self,hb_game,bird):
        """在猎人当前位置创建一个子弹对象"""
        super().__init__(hb_game)
        self.color = self.settings.enemy_bullet_color

        # 在（0,0）处创建一个表示子弹的矩形，再设置正确的位置。
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midright = bird.rect.midleft

        # 存储用小数表示的子弹位置。
        self.x = float(self.rect.x)

    def update(self):
        """向左移动子弹"""
        # 更新表示子弹位置的小数值
        self.x -= self.settings.enemy_bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.x = self.x