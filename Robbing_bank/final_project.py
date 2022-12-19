from pycat.core import Window, Sprite, Color, Scheduler, KeyCode, RotationMode, Label
from pycat.experimental.spritesheet import SpriteSheet
import pyglet
import random
from sklearn.preprocessing import scale

from sympy import Point

window = Window(width=1280, height=900)

spritesheet_healer = SpriteSheet('Sprite/healer_m.png',32,36)
spritesheet_ninja = SpriteSheet('Sprite/ninja_m.png',32,36)
spritesheet_mage = SpriteSheet('Sprite/mage_m.png',32,36)
spritesheet_ranger = SpriteSheet('Sprite/ranger_m.png',32,36)
spritesheet_townfolk1 = SpriteSheet('Sprite/townfolk1_m.png',32,36)
spritesheet_warrior = SpriteSheet('Sprite/warrior_m.png',32,36)

money_num = 0

class Money(Sprite):
    def on_create(self):
        self.image = "money.png"
        self.scale = 0.03
        self.owner : Player = None
        self.layer = -1000
        self.add_tag("money")
    def on_update(self, dt):
        if self.owner:
            self.position = self.owner.position
            if self.owner.state == 1:
                self.y -= 30
                self.layer = 10000
                self.rotation = 0
            if self.owner.state == 3:
                self.y += 80
                self.rotation = 0
                self.layer = -1000
            if self.owner.state == 0:
                self.x -= 60
                self.layer = -1000
                self.rotation = 90
            if self.owner.state == 2:
                self.x += 60
                self.rotation = 90
                self.layer = -1000
            if window.is_key_down(self.owner.controller[4]):
                self.owner.have_money = False
                self.owner = None
                self.rotation = 0

        elif self.is_touching_any_sprite_with_tag("player"):
            if self.get_touching_sprites_with_tag("player")[0].have_money == False and window.is_key_down(self.get_touching_sprites_with_tag("player")[0].controller[4]):
                self.owner = self.get_touching_sprites_with_tag("player")[0]
                self.owner.have_money = True
        else:
            self.layer = -1000
        
            
class PlayerLabel(Label):
    def on_create(self):
        self.font = 'Consolas'
        self.owner : Player = None
        self.font_size = 35
    def on_update(self, dt):
        self.position = self.owner.position+Point(-22, -58)
        
class Time(Label):
    def on_create(self):
        self.font = 'Consolas'
        self.font_size = 35
        self.time = 180
    def on_update(self, dt: float):
        self.time -= dt

class Score(Label):
    def on_create(self):
        self.font = 'Consolas'
        self.ownerplace : Player = None
        self.font_size = 35
        self.score = 0
    def on_update(self, dt: float):
        self.score = 0
        for money in window.get_sprites_with_tag("money"):
            if money.distance_to(self.ownerplace) < self.ownerplace.width/2:
                self.score+=1
        self.text = str(self.score)


class Player(Sprite):
    def on_create(self):
        self.have_money = False
        self.spritesheet = None
        self.controller = []
        self.speed = 4.5
        self.add_tag("player")
        self.state_horizantal = 0
        self.punch = None
        self.time = 0
        self.scale = 3
        self.state = 1
    def on_update(self, dt):
        if self.have_money:
            self.speed = 3
        else:
            self.speed = 4.5
        self.by_keyboard()
        self.animate(dt)
    def animate(self, dt):
        self.time += dt
        self.texture = self.spritesheet.get_texture(self.state_horizantal,self.state)
        if self.time > 0.2:
            self.time = 0
            self.state_horizantal += 1
            if self.state_horizantal >= 3:
                self.state_horizantal = 0
    def by_keyboard(self):
        # if self.punch:
        #     self.punch.position = self.position
        #     self.punch.move_forward(100)
            
        #     self.punch.scale = 0.5
            
            # Scheduler.wait(0.1, self.imageback)
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
    # def imageback(self):
    #     self.punch.delete()
    #     self.punch = None

player1 = window.create_sprite(Player, x=60, y=120)
player1.controller = [KeyCode.W, KeyCode.A, KeyCode.S, KeyCode.D, KeyCode.E]
player1.spritesheet = spritesheet_healer
label1 = window.create_label(PlayerLabel, text="P1", color = Color.RED)
label1.owner = player1
player2 = window.create_sprite(Player, x=60, y=840)
player2.controller = [KeyCode.T, KeyCode.F, KeyCode.G, KeyCode.H, KeyCode.Y]
player2.spritesheet = spritesheet_ninja
label2 = window.create_label(PlayerLabel, text="P2", color = Color.GREEN)
label2.owner = player2
player3 = window.create_sprite(Player, x=1220, y=120)
player3.controller = [KeyCode.I, KeyCode.J, KeyCode.K, KeyCode.L, KeyCode.O]
player3.spritesheet = spritesheet_mage
label3 = window.create_label(PlayerLabel, text="P3", color = Color.BLUE)
label3.owner = player3
player4 = window.create_sprite(Player, x=1220, y=840)
player4.controller = [KeyCode.UP, KeyCode.LEFT, KeyCode.DOWN, KeyCode.RIGHT, KeyCode.SPACE]
player4.spritesheet = spritesheet_townfolk1
label4 = window.create_label(PlayerLabel, text="P4", color = Color.YELLOW)
label4.owner = player4


# for i in range(60, 1300, 120):
#     for j in range(60 ,661, 120):
#         ground = window.create_sprite(x=i, y=j)
#         ground.layer = -1000
#         ground.image = "stone.jpg"
#         ground.scale = 0.1


def create_money():
    global money_num
    if money_num<15:
        window.create_sprite(Money, x=random.randint(200, 1080), y=random.randint(200,700))
        money_num+=1
for location, placelocate, color in [(Point(450, 70),Point(0, 0),Color.RED),(Point(450, 880),Point(0, 900),Color.GREEN),(Point(830, 70),Point(1280, 0),Color.BLUE),(Point(830, 880),Point(1280, 900),Color.YELLOW)]:
    place = window.create_sprite(image = "place.png", position = placelocate, layer = -10000, scale = 0.7, opacity = 150)
    score = window.create_label(Score)
    square = window.create_sprite(scale = 100)
    score.ownerplace = place
    place.color = color
    score.position = location
    score.color = place.color
    square.color = score.color
    square.opacity = 50
    square.position = score.position+Point(10,-30)
    

for i in range(10):
    create_money()

Scheduler.update(create_money, 4)

window.run()

