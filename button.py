import pygame.font

class Button:

    def __init__(self,hb_game,msg,offset = 0):
        """初始化按钮的属性"""
        self.screen = hb_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性。
        self.width, self.height = 200, 50
        self.button_color = (80, 80, 80)
        self.text_color =(255, 182, 193)
        self.font = pygame.font.Font("font/msyh.ttc", 36)

        # 创建按钮的rect对象，并使其居中。
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.centerx =self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery + offset
        # 按钮的标签只需创建一次。
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮上居中。"""
        self.msg_image = self.font.render(msg,True,self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本。
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
