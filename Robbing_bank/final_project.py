from pycat.core import Window, Sprite, Color, Scheduler, KeyCode, RotationMode
from pycat.experimental.spritesheet import SpriteSheet
import pyglet
import random

window = Window()

spritesheet_healer = SpriteSheet('Sprite/healer_m.png',32,36)
spritesheet_ninja = SpriteSheet('Sprite/ninja_m.png',32,36)
spritesheet_mage = SpriteSheet('Sprite/mage_m.png',32,36)
spritesheet_ranger = SpriteSheet('Sprite/ranger_m.png',32,36)
spritesheet_townfolk1 = SpriteSheet('Sprite/townfolk1_m.png',32,36)
spritesheet_warrior = SpriteSheet('Sprite/warrior_m.png',32,36)

money_num = 0

class money(Sprite):
    def on_create(self):
        self.image = "money.png"
        self.scale = 0.03
        self.player = Player
    def on_update(self, dt):
        if self.player:
            if self.player.state == 1:
                pass

class Player(Sprite):
    def on_create(self):
        self.spritesheet = None
        self.controller = []
        self.speed = 5
        self.add_tag("player")
        self.state_horizantal = 0
        self.punch = None
        self.time = 0
        self.scale = 3
        self.state = 1
    def on_update(self, dt):
        self.by_keyboard()
        self.time += dt
        self.texture = self.spritesheet.get_texture(self.state_horizantal,self.state)
        if self.time > 0.2:
            self.time = 0
            self.state_horizantal += 1
            if self.state_horizantal >= 3:
                self.state_horizantal = 0
    def by_keyboard(self):
        if self.punch:
            self.punch.position = self.position
            self.punch.move_forward(100)
        if self.image != "pick_money" and window.is_key_down(self.controller[4]) and self.punch == None:
            self.punch = window.create_sprite(position = self.position)
            self.punch.move_forward(100)
            self.punch.image = "hit_1.png"
            self.punch.rotation = self.rotation
            
            self.punch.scale = 0.5
            
            Scheduler.wait(0.1, self.imageback)
        if window.is_key_pressed(self.controller[0]):
            self.y += self.speed
            self.state = 3
        if window.is_key_pressed(self.controller[1]):
            self.x -= self.speed
            self.state = 0
        if window.is_key_pressed(self.controller[2]):
            self.y -= self.speed
            self.state = 1
        if window.is_key_pressed(self.controller[3]):
            self.x += self.speed
            self.state = 2
        if window.is_key_pressed(self.controller[0]) == False and window.is_key_pressed(self.controller[1]) == False and window.is_key_pressed(self.controller[2]) == False and window.is_key_pressed(self.controller[3]) == False:
            self.state = 1
            self.state_horizantal = 1
    def imageback(self):
        self.punch.delete()
        self.punch = None

player1 = window.create_sprite(Player)
player1.controller = [KeyCode.W, KeyCode.A, KeyCode.S, KeyCode.D, KeyCode.E]
player1.spritesheet = spritesheet_healer

player2 = window.create_sprite(Player)
player2.controller = [KeyCode.T, KeyCode.F, KeyCode.G, KeyCode.H, KeyCode.Y]
player2.spritesheet = spritesheet_ninja
player3 = window.create_sprite(Player)
player3.controller = [KeyCode.I, KeyCode.J, KeyCode.K, KeyCode.L, KeyCode.O]
player3.spritesheet = spritesheet_mage
player4 = window.create_sprite(Player)
player4.controller = [KeyCode.UP, KeyCode.LEFT, KeyCode.DOWN, KeyCode.RIGHT, KeyCode.SPACE]
player4.spritesheet = spritesheet_townfolk1


# for i in range(60, 1300, 120):
#     for j in range(60 ,661, 120):
#         ground = window.create_sprite(x=i, y=j)
#         ground.layer = -1000
#         ground.image = "stone.jpg"
#         ground.scale = 0.1


def create_money():
    global money_num
    if money_num<15:
        window.create_sprite(money, x=random.randint(1, 1280), y=random.randint(1,640))
        money_num+=1
    

Scheduler.update(create_money, 1)

window.run()

