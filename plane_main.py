import pygame
from plane_supply import *

# 游戏主体类
class PlaneGame(object):
    def __init__(self):
        # pygame模块开始工作
        pygame.init()

        # 初始化游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 创建结束页面
        self.canvas_over = Canvas_over(self.screen)

        # 初始化游戏时钟
        self.clock = pygame.time.Clock()

        # 初始化游戏分数对象
        self.score = Game_score()

        # 调用私有方法创建精灵和精灵组
        self.__create_sprite()

        # 初始化游戏控制指针
        self.index = 0

        # 游戏bgm
        self.bgm = pygame.mixer.Sound("sound/game_music.ogg")
        self.bgm.set_volume(0.3)
        self.bgm.play(-1)

        # 游戏结束旗帜
        self.game_over_flag = False

        # 初始化游戏定时器
        pygame.time.set_timer(ENEMY1_EVENT,ENEMY1_FRE)      # 一号敌机出现定时器
        pygame.time.set_timer(PLAYER_PLANE_FIRE_EVENT,PLAYER_PLANE_FIRE_FRE)    # 玩家飞机发射子弹定时器
        pygame.time.set_timer(ENEMY_FIRE_EVENT,ENEMY_FIRE_FRE)  # 敌机发射子弹定时器


    # 创建游戏方法
    def __create_sprite(self):
        # 创建背景精灵和精灵组
        bg1 = Background_sprite()
        bg2 = Background_sprite(is_alt=True)
        self.background_sprite_group = pygame.sprite.Group(bg1,bg2)

        # 创建敌机精灵组
        self.enemy_plane_group = pygame.sprite.Group()

        # 创建玩家飞机和支援飞机精灵和精灵组
        self.player_plane = Player_plane_sprite()
        self.blood_group = pygame.sprite.Group()
        self.player_plane_group = pygame.sprite.Group(self.player_plane)

        # 创建敌机子弹精灵组
        self.enemy_bullet_group = pygame.sprite.Group()

        # 创建buff精灵组
        self.buff_group = pygame.sprite.Group()

        # 创建假性boom精灵组
        self.enemy_boom_group = pygame.sprite.Group()

        # 创建boom列表
        self.booms = []

    # 开始游戏方法
    def __start_game(self):
        print("游戏开始！")

        # 游戏循环
        while True:
            # 设置游戏刷新率
            self.clock.tick(FRAME_FRE_SEC)

            # 事件监听
            self.__event_handler()

            # 碰撞检测
            self.__check_collider()

            # 更新/绘制精灵组
            self.__update()

            # 判断是否结束游戏
            if self.game_over_flag:
                self.canvas_over.update()

            # 更新显示
            pygame.display.update()

    # 事件监视器方法
    def __event_handler(self):
        # 判断Boss是否出场
        if self.score.getvalue() > 100 * self.index + 0:
            boss = Boss_sprite(player_plane_rect=self.player_plane.rect)
            self.enemy_plane_group.add(boss)
            self.index += 1

        for event in pygame.event.get():
            # 判断游戏是否退出
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 判断是否敌机出场
            if event.type == ENEMY1_EVENT:
                # 若分数小于20分则只刷新一号敌人
                if self.score.getvalue() < 20*self.index+20:
                    enemy1 = Enemy_plane_sprite(plane_type=1,player_plane_rect=self.player_plane.rect)
                    self.enemy_plane_group.add(enemy1)
                else :
                    if random.randint(0,100) <= 50:
                        enemy2 = Enemy_plane_sprite(plane_type=2,player_plane_rect=self.player_plane.rect)
                        self.enemy_plane_group.add(enemy2)
                    else:
                        enemy1 = Enemy_plane_sprite(plane_type=1)
                        self.enemy_plane_group.add(enemy1)
                pass

            # 判断敌机是否发射子弹
            if event.type == ENEMY_FIRE_EVENT:
                for enemy in self.enemy_plane_group:
                    enemy.fire()
                    for bullet in enemy.bullet_group:
                        self.enemy_bullet_group.add(bullet)

            # 判断玩家飞机是否开火
            if event.type == PLAYER_PLANE_FIRE_EVENT:
                for player_plane in self.player_plane_group:
                    player_plane.fire()


        # 获取键盘事件
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.player_plane.speed = [2,0]
        elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.player_plane.speed = [-2,0]
        elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.player_plane.speed = [0,-2]
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.player_plane.speed = [0,2]
        else:
            self.player_plane.speed = [0, 0]


    # 碰撞检测方法
    def __check_collider(self):
        for player_plane in self.player_plane_group:
            for enemy in self.enemy_plane_group:
                for bullet in self.player_plane.bullet_group:

                    # 子弹与敌机碰撞
                    if pygame.sprite.collide_mask(bullet,enemy):
                        bullet.kill()
                        enemy.lives -= 1
                        if enemy.plane_type == 2 or enemy.plane_type == 3:
                            enemy.is_hit = True


    # 更新/绘制精灵组方法
    def __update(self):
        self.background_sprite_group.update()
        self.background_sprite_group.draw(self.screen)
        self.enemy_plane_group.update()
        self.enemy_plane_group.draw(self.screen)
        self.enemy_boom_group.update()
        self.enemy_boom_group.draw(self.screen)
        self.player_plane.update()
        self.player_plane_group.draw(self.screen)
        for player_plane in self.player_plane_group:
            player_plane.bullet_group.update()
            player_plane.bullet_group.draw(self.screen)
        # self.buff1_group.update()
        # self.buff1_group.draw(self.screen)
        # self.bars_update()
        # self.bombs_update()
        self.enemy_bullet_group.update()
        self.enemy_bullet_group.draw(self.screen)

        pass



    @staticmethod
    def __start__():
        # 创建游戏对象
        game = PlaneGame()
        # 启动游戏
        game.__start_game()

if __name__ == '__main__':
    PlaneGame.__start__()
