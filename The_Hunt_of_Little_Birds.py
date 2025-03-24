import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from text_display import Text_Display
from scoreboard import Scoreboard
from hunter import Hunter
from bullet import Bullet,Enemy_Bullet
from bird import Bird
from random import randint

class Hunt_Birds:
    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("The_Hunt_of_Little-Birds")
        self.stats = GameStats(self)
        self.stats.high_score_read()

        self.sb = Scoreboard(self)

        self.hunter =Hunter(self)

        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.birds = pygame.sprite.Group()
        self._create_fleet()

        #设置背景色
        self.bg_color = (self.settings.bg_color)

        # 创建一组按钮（PLAY的简单，一般，困难）。
        self.play_button = Button(self, "开始游戏", -200)
        self.easy_button = Button(self, "简单", -100)
        self.normal_button = Button(self, "一般", 0)
        self.hard_button = Button(self, "困难", 100)
        self.quit_button = Button(self, "退出游戏", 200)

        self.texts = Text_Display(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()

            if self.stats.game_active and not self.stats.paused:
                self.hunter.update()
                self._update_bullets()
                self._update_birds()
                self._update_bird_bullets()


            self._update_screen()


    def clear_groups(self):
        """清空相关精灵组"""
        self.birds.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()

    def _check_birds_left(self):
        """检查是否有小鸟到达了屏幕的左侧。"""
        screen_rect = self.screen.get_rect()
        for bird in self.birds.sprites():
            if bird.rect.left <= screen_rect.left:
                # 像飞机被撞到一样处理。
                self._hunter_hit()
                break

    def _hunter_hit(self):
        """响应猎人被小鸟撞到。"""
        if self.stats.hunters_exist >1:
            self.stats.hunters_exist -= 1
            self.sb.prep_hunters()
            # 清空余下的小鸟和子弹。
            self.clear_groups()

            # 创建一群新的小鸟，并将猎人放到屏幕底端的中央。
            self._create_fleet()
            self.hunter.center_hunter()

            # 暂停。
            sleep(0.5)
        else:
            self.stats.hunters_exist -= 1
            self.sb.prep_hunters()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)



    def _create_fleet(self):
        """创建小鸟群。"""
        # 创建一个小鸟并计算一行可容纳多少个小鸟。
        # 小鸟的间距为小鸟的宽度。
        bird = Bird(self)
        bird_width, bird_height =bird.rect.size
        available_space_y = self.settings.screen_height - (1 * bird_height)
        number_birds_y = available_space_y // (2 * bird_height)
        #计算屏幕可容纳多少列小鸟。
        hunter_width = self.hunter.rect.width
        available_space_x = (self.settings.screen_width -
                             (4 * bird_width) - hunter_width)
        number_columns = available_space_x // (2 * bird_width)

        #创建小鸟群
        for column_number in range(number_columns):
            for bird_number in range(number_birds_y):
                self._create_bird(bird_number,column_number)

    def _create_bird(self, bird_number, column_number):
        # 创建一个小鸟,并将其加入当前行。
        bird = Bird(self)
        bird_width, bird_height = bird.rect.size
        bird.y = bird_height + 2 * bird_height * bird_number + randint(-20,20)
        bird.rect.y = bird.y
        bird.x = bird.rect.x - bird_width - 2 * bird.rect.width * column_number + randint(-20,20)
        bird.rect.x = bird.x
        self.birds.add(bird)

    def _check_fleet_edges(self):
        """小鸟到达边缘时采取相应的措施"""
        for bird in self.birds.sprites():
            if bird.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群小鸟左移，并改变他们的方向"""
        for bird in self.birds.sprites():
            bird.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_events(self):
        """响应键盘和鼠标事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.high_score_save()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_buttons(self, mouse_pos):
        """玩家单击具体按钮时开始新游戏"""
        if self.easy_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game("easy")
        elif self.normal_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game("normal")
        elif self.hard_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._start_game("hard")
        elif self.quit_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.high_score_save()
            sys.exit()

    def _start_game(self, difficulty):
        # 重置游戏设置
        self.settings.initialize_dynamic_settings(difficulty)
        # 重置游戏统计信息。
        self.stats.reset_stats()
        self.stats.game_active = True
        # 清空余下的小鸟和子弹。
        self.clear_groups()

        # 创建一群新的小鸟并让猎人居中。
        self._create_fleet()
        self.hunter.center_hunter()
        # 隐藏鼠标光标
        self.sb.prep_hunters()
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):
        """响应按键"""
        if event.key == pygame.K_UP:
            self.hunter.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.hunter.moving_down = True
        elif event.key == pygame.K_q:
            self.stats.high_score_save()
            sys.exit()
        elif event.key == pygame.K_p:  # 新增按 P 键暂停
            self.stats.paused = not self.stats.paused
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """按键送开"""
        if event.key == pygame.K_UP:
            self.hunter.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.hunter.moving_down = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""
        self.screen.fill(self.bg_color)
        self.hunter.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.birds.draw(self.screen)
        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()
        # 显示得分。
        self.sb.show_score()
        # 如果游戏处于非活动状态，就显示Play按钮。
        if not self.stats.game_active:
            self.easy_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()
            self.play_button.draw_button()
            self.quit_button.draw_button()
            self.texts.draw_instructions()
        if self.stats.paused:  # 显示暂停提示
            self.texts.draw_pause_text()
        pygame.display.flip()


    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)



    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_bird_collisions()

    def _check_bullet_bird_collisions(self):
        """响应子弹和小鸟碰撞"""
        #删除发生碰撞的子弹和小鸟。
        collisions = pygame.sprite.groupcollide(self.bullets,self.birds,True,True)

        if collisions:
            for birds in collisions.values():
                self.stats.score += self.settings.bird_points * len(birds)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.birds:
            # 删除现有的子弹并新建一群小鸟。
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_birds(self):
        """
        检查是否有小鸟位于屏幕边缘，
        并更新整群小鸟的位置。
        """
        self._check_fleet_edges()
        self.birds.update()

        # 检测小鸟和猎人之间的碰撞。
        if pygame.sprite.spritecollideany(self.hunter, self.birds):
            self._hunter_hit()

        # 检查是否有小鸟到达了屏幕左端。
        self._check_birds_left()

        # 随机让小鸟发射子弹
        for bird in self.birds.sprites():
            if randint(1, 10000) < self.settings.bird_fire_rate:
                new_bullet = Enemy_Bullet(self,bird)
                new_bullet.rect.midright = bird.rect.midleft
                self.enemy_bullets.add(new_bullet)

    def _update_bird_bullets(self):
        """更新小鸟子弹的位置并删除消失的子弹"""
        self.enemy_bullets.update()
        for bullet in self.enemy_bullets.copy():
            if bullet.rect.left < 0:
                self.enemy_bullets.remove(bullet)

        # 检测小鸟子弹和猎人的碰撞
        if pygame.sprite.spritecollideany(self.hunter, self.enemy_bullets):
            if self.stats.hunters_exist > 1:
                self.stats.hunters_exist -= 1
                self.sb.prep_hunters()
                # 清空余下的小鸟和子弹。
                self.bullets.empty()
                self.enemy_bullets.empty()
                # 暂停。
                sleep(0.5)
            else:
                self.stats.hunters_exist -= 1
                self.sb.prep_hunters()
                self.stats.game_active = False
                pygame.mouse.set_visible(True)

if __name__ == '__main__':
    hb = Hunt_Birds()
    hb.run_game()