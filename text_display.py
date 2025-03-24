import pygame.font

class Text_Display:
    def __init__(self, hb_game):
        self.game = hb_game
        self.screen = hb_game.screen
        self.pause_font = pygame.font.Font("font/msyh.ttc", 74)
        self.instruction_font = pygame.font.Font("font/msyh.ttc", 30)
        self.pause_text = self.pause_font.render("游戏暂停", True, (255, 255, 255))
        self.pause_text_rect = self.pause_text.get_rect(center=self.screen.get_rect().center)
        self.instructions = [
            "操作指南:",
            "↑ 键: 向上移动飞船",
            "↓ 键: 向下移动飞船",
            "空格键: 发射子弹",
            "P 键: 暂停/继续游戏",
            "Q 键: 退出游戏"
        ]

    def draw_pause_text(self):
        self.screen.blit(self.pause_text, self.pause_text_rect)

    def draw_instructions(self):
        y_offset = 100
        for instruction in self.instructions:
            text = self.instruction_font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (20, y_offset))
            y_offset += 30