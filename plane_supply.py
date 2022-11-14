import math
import sys
import random
import pygame

# 定义分数
SCORE = 0

# 定义颜色
color_blue = (30, 144, 255)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_purple = (148, 0, 211)
color_gray = (251, 255, 242)

# 定义屏幕刷新率
FRAME_FRE_SEC = 90

# 定义屏幕rect常量
SCREEN_RECT = pygame.rect.Rect(0,0,480,700)

# 定义一号敌人出现事件
ENEMY1_EVENT = pygame.USEREVENT
# 一号敌人出现频率
ENEMY1_FRE = 1000

# 定义玩家飞机发射子弹事件
PLAYER_PLANE_FIRE_EVENT = pygame.USEREVENT + 1
# 玩家飞机发射子弹频率
PLAYER_PLANE_FIRE_FRE = 200

# 定义敌机发射子弹事件
ENEMY_FIRE_EVENT = pygame.USEREVENT + 2
# 敌机发射子弹频率
ENEMY_FIRE_FRE = 1300



# 敌机精灵类
class Enemy_plane_sprite(pygame.sprite.Sprite):
    def __init__(self,player_plane_rect=0,plane_type=1):
        super(Enemy_plane_sprite, self).__init__()
        self.plane_type = plane_type
        self.speed = 0
        self.lives = 0
        self.is_hit = False
        self.bullet_group = pygame.sprite.Group()
        self.player_plane_rect = player_plane_rect

        # 爆炸效果
        self.is_boom = False
        self.index = 0
        self.index_hit = 0
        # 根据敌机类型初始化敌机属性
        if self.plane_type == 1:
            self.image = pygame.image.load("images/enemy1.png")
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, SCREEN_RECT.width-self.rect.width)
            self.rect.bottom = SCREEN_RECT.top
            self.music_boom = pygame.mixer.Sound("./sound/enemy1_down.wav")
            self.speed = 2
            self.lives = 2
            self.score =self.lives
        if self.plane_type == 2:
            self.image = pygame.image.load("images/enemy2.png")
            self.rect = self.image.get_rect()
            self.music_boom = pygame.mixer.Sound("./sound/enemy2_down.wav")
            self.rect.centerx = self.player_plane_rect.centerx
            self.rect.bottom = SCREEN_RECT.top
            self.speed = 1
            self.lives = 5
            self.score = self.lives
            self.index2 = 0

    def update(self):
        global SCORE
        # 判断敌机是否在屏幕以内，未在则销毁敌机
        if self.rect.y >= SCREEN_RECT.bottom:
            self.kill()

        # 根据敌机类型设置不同的飞行轨迹
        if self.plane_type == 1:
            self.rect.y += self.speed
        if self.plane_type == 2:
            # 使玩家飞机始终在屏幕内
            # x轴方向
            if self.rect.right >= SCREEN_RECT.right - self.rect.width / 2 \
                    and self.rect.left <= SCREEN_RECT.left + - self.rect.width / 2:
                if self.rect.right >= SCREEN_RECT.right:
                    self.rect.right = SCREEN_RECT.right
                else:
                    self.rect.left = SCREEN_RECT.rect.left

            else:
                # 二号敌机跟随玩家飞机x轴方向上移动
                if self.rect.bottom <= SCREEN_RECT.top:
                    self.center_x = self.player_plane_rect.centerx
                    self.rect.y += self.speed
                else:
                    self.rect.centerx = math.sin(1 / 50 * (self.index2)) * 50 + self.center_x
                    self.rect.y += self.speed
                    self.index2 += 1
                    self.rect.y += self.speed

            # 判断二号敌机是否被击中
            if self.is_hit and self.is_boom is False:
                if self.index_hit < 15:
                    self.image = pygame.image.load("images/enemy2_hit.png")
                    self.index_hit += 1
                else:
                    self.image = pygame.image.load("images/enemy2.png")
                    self.is_hit = False
                    self.index_hit = 0

        # 判断敌机是否爆炸
        if self.lives <= 0:
            if self.index == 0:
                self.music_boom.play()
            self.image = pygame.image.load("./images/enemy" + str(self.plane_type) + "_down" + str(self.index // 4% 4 + 1) + ".png")
            self.index += 1
            print(str(self.index // 4% 4 + 1))
            if (self.index // 4% 4 + 1)>=4:
                SCORE += self.score
                self.kill()



    def fire(self):
        if self.plane_type == 2:
            bullet = Bullet_sprite(bullet_type=2)
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.top = self.rect.bottom
            self.bullet_group.add(bullet)

# 玩家飞机精灵类
class Player_plane_sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 初始化玩家飞机属性
        self.speed = [0,0]
        self.lives = 5
        self.music_down = pygame.mixer.Sound("./sound/me_down.wav")
        self.music_upgrade = pygame.mixer.Sound("./sound/upgrade.wav")
        self.music_degrade = pygame.mixer.Sound("./sound/supply.wav")
        self.image = pygame.image.load("images/me1.png")
        self.index1 = 1     #玩家飞机喷气动画控制参数
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()
        # 创建血量精灵组
        self.blood_group = pygame.sprite.Group()

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-20

    def update(self):
        # 使玩家飞机始终在屏幕内
        # x轴方向
        if self.rect.right >= SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        else:
            self.rect.x += self.speed[0]
        if self.rect.x <= SCREEN_RECT.x:
            self.rect.x = SCREEN_RECT.x
        else:
            self.rect.x += self.speed[0]
        # y轴方向
        if self.rect.bottom >= SCREEN_RECT.bottom + 24:
            self.rect.bottom = SCREEN_RECT.bottom + 24
        else:
            self.rect.y += self.speed[1]
        if self.rect.y <= SCREEN_RECT.y:
            self.rect.y = SCREEN_RECT.y
        else:
            self.rect.y += self.speed[1]

        # 玩家飞机喷气动画
        self.image = pygame.image.load("./images/me" + str((self.index1 // 20) % 2 + 1) + ".png")
        self.index1 += 1

    def fire(self):
        for i in (-1,1):
            bullet = Bullet_sprite()
            bullet.rect.centerx = self.rect.centerx + i*10
            bullet.rect.bottom = self.rect.top
            self.bullet_group.add(bullet)

    def blood(self):
        for i in range(1,self.lives):
            blood = Supply_sprite()
            blood.rect.y = SCREEN_RECT.top + 10* i
            self.bullet_group.add(blood)

# 背景精灵类
class Background_sprite(pygame.sprite.Sprite):
    def __init__(self,is_alt=False):
        super().__init__()
        # 初始化背景对象属性
        self.image = pygame.image.load("images/background.png")
        self.rect = self.image.get_rect()
        self.is_alt = is_alt
        self.speed = 2

        # 判断创建背景对象是否为替换背景，是则更改对象rect.y位置
        if self.is_alt:
            self.rect.y = self.rect.height

    def update(self):
        # 判断背景对象是否移出屏幕，是则将其移至屏幕顶端
        if self.rect.y >= SCREEN_RECT.bottom:
            self.rect.y = -SCREEN_RECT.height
        else:
            self.rect.y += self.speed
# 子弹精灵类
class Bullet_sprite(pygame.sprite.Sprite):
    def __init__(self,bullet_type=1,bullet_trans = 0):
        super(Bullet_sprite, self).__init__()
        self.bullet_type = bullet_type
        self.speed = [0,0]
        self.bullet_trans = bullet_trans

        # 判断子弹类型并根据类型初始化子弹对象属性
        if self.bullet_type == 1:
            self.image = pygame.image.load("images/bullet1.png")
            self.rect = self.image.get_rect()
            self.speed = [0,-4]
        if self.bullet_type == 2:
            self.image = pygame.image.load("images/bullet2.png")
            self.rect = self.image.get_rect()
            self.speed = [3, 3]

    def update(self):
        # 判断子弹对象是否在屏幕内，不在则销毁
        if (self.rect.bottom < SCREEN_RECT.top or self.rect.left > SCREEN_RECT.right
                or self.rect.right < SCREEN_RECT.left):
            self.kill()
        else:
            self.rect.y += self.speed[1]
            self.rect.x += self.bullet_trans
# 游戏结束类
class Canvas_over():
    def __init__(self,screen):
        # 初始化游戏结束对象属性
        self.again_image = pygame.image.load("images/again.png")
        self.over_image = pygame.image.load("images/gameover.png")
        self.again_rect = self.again_image.get_rect()
        self.over_rect = self.over_image.get_rect()
        self.again_rect.centerx = self.over_rect.centerx = SCREEN_RECT.centerx
        self.again_rect.bottom = SCREEN_RECT.centery
        self.over_rect.y = self.again_rect.bottom + 20
        self.screen = screen

    # 事件监听方法
    def event_handler(self):
        pass

    # 更新按钮位置
    def update(self):
        self.screen.blit(self.again_image, self.again_rect)
        self.screen.blit(self.over_image, self.over_rect)
        score_font = pygame.font.Font("./STCAIYUN.ttf", 50)
        image = score_font.render("SCORE:" + str(int(SCORE)), True, color_gray)
        rect = image.get_rect()
        rect.centerx, rect.bottom = SCREEN_RECT.centerx, self.again_rect.top - 20
        self.screen.blit(image, rect)
# 游戏分数类
class Game_score():
    global SCORE

    def __init__(self):
        self.score = 0
        pass

    def getvalue(self):
        self.score = SCORE
        return self.score
# BOSS类
class Boss_sprite(pygame.sprite.Sprite):
    def __init__(self,player_plane_rect):
        super().__init__()
        self.image = pygame.image.load("images/enemy3_n1.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.top
        self.bullet_group = pygame.sprite.Group()
        self.lives = 6
        self.speed = [1,1]
        self.is_hit = False
        self.index_hit = 0
        self.is_boom = False
        self.index = 1
        self.plane_type = 3
        self.player_plane_rect = player_plane_rect
        self.first_show = True
        self.index2 = 0
        self.music_boom = pygame.mixer.Sound("sound/enemy3_down.wav")
        self.music_fly = pygame.mixer.Sound("sound/enemy3_flying.wav")
        self.music_fly.play(-1)
        self.score = self.lives
        self.index3 = 0

    def update(self):
        global SCORE
        # Boss动画
        self.image = pygame.image.load("images/enemy3_n"+str((self.index // 20)%2+1)+".png")
        self.index += 1
        if self.rect.top+90 <= SCREEN_RECT.top and self.first_show:
            self.rect.y += self.speed[1]
            if self.rect.top+90 == SCREEN_RECT.top:
                self.first_show = False
        if self.first_show is False:
            self.rect.top = math.sin(1/25*self.index2)*25 - 90
            self.rect.centerx = math.sin(1/120*(self.index2+1/2*self.index2*math.pi))*100 + SCREEN_RECT.centerx
            self.index2 += 1/2

        # 判断BOSS是否被击中
        if self.is_hit and self.is_boom is False:
            if self.index_hit < 10:
                self.image = pygame.image.load("images/enemy3_hit.png")
                self.index_hit += 1
            else:
                self.image = pygame.image.load("images/enemy3_n1.png")
                self.is_hit = False
                self.index_hit = 0

        # 判断敌机是否爆炸
        if self.lives <= 0:
            if self.index3 == 0:
                self.music_fly.stop()
                self.music_boom.play()
            self.image = pygame.image.load("./images/enemy" + str(self.plane_type) + "_down" + str(self.index3 // 6 % 6 + 1) + ".png")
            self.index3 += 1
            if (self.index3 // 6 % 6 + 1) >= 6:
                SCORE += self.score
                self.kill()


    def fire(self):
        for i in (-1,0,1):
            bullet = Bullet_sprite(bullet_type=2,bullet_trans=i)
            bullet.image = pygame.transform.rotate(bullet.image,45*i)
            bullet.rect.centerx = self.rect.centerx + i * 50
            bullet.rect.top = self.rect.bottom - math.fabs(i * 20)
            self.bullet_group.add(bullet)



# 血量显示/支援飞机类
class Supply_sprite(Player_plane_sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/life.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 1/10*SCREEN_RECT.centerx
        self.rect.y = SCREEN_RECT.top + 10
        # self.player_plane_life = player_plane_life
        self.is_supply = False

    def update(self):
        if self.is_supply:
            pass

