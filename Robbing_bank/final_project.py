from pycat.core import Window, Sprite, Color, Scheduler, KeyCode, RotationMode, Label
from pycat.experimental.spritesheet import SpriteSheet
import pyglet
import random

from sympy import Point

window = Window(width=1280, height=900)

spritesheet_healer = SpriteSheet('Sprite/healer_m.png',32,36)
spritesheet_ninja = SpriteSheet('Sprite/ninja_m.png',32,36)
spritesheet_mage = SpriteSheet('Sprite/mage_m.png',32,36)
spritesheet_ranger = SpriteSheet('Sprite/ranger_m.png',32,36)
spritesheet_townfolk1 = SpriteSheet('Sprite/townfolk1_m.png',32,36)
spritesheet_warrior = SpriteSheet('Sprite/warrior_m.png',32,36)
spritesheet_healer_f = SpriteSheet('Sprite/healer_f.png',32,36)
spritesheet_ninja_f = SpriteSheet('Sprite/ninja_f.png',32,36)
spritesheet_fage_F = SpriteSheet('Sprite/mage_f.png',32,36)
spritesheet_townfolk1_f = SpriteSheet('Sprite/townfolk1_f.png',32,36)
spritesheet_warrior_f = SpriteSheet('Sprite/warrior_f.png',32,36)
spritesheet1 = [spritesheet_healer, spritesheet_ninja, spritesheet_mage, spritesheet_ranger, spritesheet_townfolk1, spritesheet_warrior, spritesheet_healer_f, spritesheet_ninja_f, spritesheet_fage_F, spritesheet_townfolk1_f, spritesheet_warrior_f]
stop = False
start = False
money_num = 0

class Money(Sprite):
    def on_create(self):
        self.image = "money.png"
        self.place = None
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
            if self.owner.dizzy == True:
                self.owner.have_money = False
                self.owner = None
                self.rotation = 0
                self.y-=65
            if self.owner:
                if window.is_key_down(self.owner.controller[4]):
                    self.owner.have_money = False
                    self.owner = None
                    self.rotation = 0
            

        elif self.is_touching_any_sprite_with_tag("player"):
            if self.get_touching_sprites_with_tag("player")[0].have_money == False and window.is_key_down(self.get_touching_sprites_with_tag("player")[0].controller[4]):
                if self.get_touching_sprites_with_tag("player")[0].placenumber != self.place:
                    self.owner = self.get_touching_sprites_with_tag("player")[0]
                    self.owner.have_money = True
        else:
            self.layer = -1000

class Chest(Sprite):
    def on_create(self):
        self.image = "chest.png"
        self.place = None
        self.scale = 0.3
        self.owner : Player = None
        self.layer = -1000
        self.add_tag("money")
    def on_update(self, dt):
        if self.owner:
            self.position = self.owner.position
            if self.owner.state == 1:
                self.y -= 60
                self.layer = 10000
                self.rotation = 0
            if self.owner.state == 3:
                self.y += 80
                self.rotation = 0
                self.layer = -1000
            if self.owner.state == 0:
                self.x -= 60
                self.layer = -1000
            if self.owner.state == 2:
                self.x += 60
                self.layer = -1000
            if window.is_key_down(self.owner.controller[4]):
                self.owner.have_money = False
                self.owner.have_chest = False
                self.owner = None
                self.rotation = 0
            if self.owner:
                if self.owner.dizzy == True:
                    self.owner.have_money = False
                    self.owner.have_chest = False
                    self.owner = None
                    self.rotation = 0
                    self.y-=65
            
            

        elif self.is_touching_any_sprite_with_tag("player"):
            if self.get_touching_sprites_with_tag("player")[0].have_money == False and window.is_key_down(self.get_touching_sprites_with_tag("player")[0].controller[4]):
                if self.get_touching_sprites_with_tag("player")[0].placenumber != self.place:
                    self.owner = self.get_touching_sprites_with_tag("player")[0]
                    self.owner.have_chest = True
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
        self.time = 181
        self.moneystart = False
    def on_update(self, dt: float):
            
        if start==True:
            self.time -= dt
            if self.moneystart == False:
                self.moneystart = True
                Scheduler.update(create_money, 4)
                Scheduler.update(create_chest, 40)
        if self.time <= 0.3:
            global stop
            stop = True
        if self.time > 0.2:
            if int(self.time%60<10):
                self.text = str(int(self.time//60))+" : 0"+str(int(self.time%60))
            else:
                self.text = str(int(self.time//60))+" : "+str(int(self.time%60))

timer = window.create_label(Time, x=570, y=70)
class ChoiceSprite(Sprite):
    def on_create(self):
        self.num = 0
        self.player : Player = None
        self.spritesheet = spritesheet1[self.num]
        self.layer = 1000000
        self.k=0
        self.time=0
    def on_update(self, dt):
        self.time+=dt
        if window.is_key_down(self.player.controller[3]):
            self.num+=1
            self.spritesheet = spritesheet1[self.num%11]
            self.player.spritesheet = self.spritesheet
        if self.time > 0.2:
            self.time = 0
            self.k+=1
        self.texture = self.spritesheet.get_texture(self.k%3, 1)
        if start==True:
            self.delete()
        
class Start(Sprite):
    def on_create(self):
        self.image = "start.png"
        self.scale = 1
        self.layer = 1000000
    def on_left_click(self):
        global start
        start = True
        black.delete()
        text.delete()
        playertext.delete()
        self.delete()
text=window.create_sprite(x=640, y=800, image="text.png", layer=1000000, scale = 2)
window.create_sprite(Start, x=640, y=130)
playertext=window.create_sprite(x=640, y=275, image="playertext.png", layer=1000000, scale = 1.15)

    
class Score(Label):
    def on_create(self):
        self.font = 'Consolas'
        self.ownerplace : Player = None
        self.font_size = 35
        self.place = None
        self.score = 0
    def on_update(self, dt: float):
        self.score = 0
        for money in window.get_sprites_with_tag("money"):
            if money.distance_to(self.ownerplace) < self.ownerplace.width/2:
                self.score+=1
                money.place = self.place
                if money.image == "chest.png":
                    self.score+=19
            elif money.place == self.place:
                money.place = None
        self.text = str(self.score)
class Fist(Sprite):
    def on_create(self):
        self.player = None
class Player(Sprite):
    def on_create(self):
        self.placenumber = 0
        self.have_money = False
        self.spritesheet = None
        self.controller = []
        self.speed = 5
        self.add_tag("player")
        self.can_punch = True
        self.state_horizantal = 0
        self.fist:Sprite = None
        self.time = 0
        self.scale = 3
        self.dizzy = False
        self.dizzysprite:Sprite = None
        self.state = 1
        self.have_chest = False
    def not_dizzy(self):
        self.dizzy = False
        self.dizzysprite.delete()
        self.dizzysprite = None
    def on_update(self, dt):
        for fist in self.get_touching_sprites_with_tag('fist'):
            if fist.player != self:
                if self.dizzy == False:
                    self.dizzy = True
                    self.dizzysprite = window.create_sprite(image = "dizzy.png",position=self.position,y = self.y+70)
                    self.dizzysprite.scale = 0.4
                    self.state = 1
                    self.state_horizantal = 1
                    self.have_money = False
                    self.have_chest = False
                    Scheduler.wait(2, self.not_dizzy)
        if timer.time > 30:
            if self.have_money:
                if self.have_chest == False:
                    self.speed = 3.5
                else:
                    self.speed = 1
            else:
                self.speed = 5
        else:
            if self.have_money:
                self.speed = 9
            else:
                self.speed = 10
        if stop==False and self.dizzy == False and start==True:
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
        if window.is_key_down(self.controller[5]) and self.have_money==False and self.can_punch==True:
            self.fist = window.create_sprite(Fist, image = "fist.png", position=self.position)
            self.can_punch = False
            Scheduler.wait(6, self.setpunch)
            self.fist.scale = 0.35
            self.fist.layer = 100000
            self.fist.player = self
            self.fist.add_tag("fist")
            if self.state == 3:
                self.fist.rotation = 270
                self.fist.y+=100
            if self.state == 1:
                self.fist.rotation = 90
                self.fist.y-=100
            if self.state == 0:
                self.fist.rotation = 0
                self.fist.x-=100
            if self.state == 2:
                self.fist.rotation = 180
                self.fist.x+=100
        if self.fist:
            self.fist.scale*=1.01
            self.fist.opacity-=20
            if self.fist.opacity < 60:
                self.fist.delete()
                self.fist = None
        

        if window.is_key_pressed(self.controller[0]) == False and window.is_key_pressed(self.controller[1]) == False and window.is_key_pressed(self.controller[2]) == False and window.is_key_pressed(self.controller[3]) == False:
            self.state = 1
            self.state_horizantal = 1
    def setpunch(self):
        self.can_punch = True
    # def imageback(self):
    #     self.punch.delete()
    #     self.punch = None
player1 = window.create_sprite(Player, x=60, y=120)
player1.controller = [KeyCode.W, KeyCode.A, KeyCode.S, KeyCode.D, KeyCode.E, KeyCode.Q]
player1.placenumber = 0
player1.spritesheet = spritesheet_healer
label1 = window.create_label(PlayerLabel, text="P1", color = Color.RED)
label1.owner = player1
player2 = window.create_sprite(Player, x=60, y=840)
player2.controller = [KeyCode.T, KeyCode.F, KeyCode.G, KeyCode.H, KeyCode.Y, KeyCode.R]
player2.placenumber = 1
player2.spritesheet = spritesheet_healer
label2 = window.create_label(PlayerLabel, text="P2", color = Color.GREEN)
label2.owner = player2
player3 = window.create_sprite(Player, x=1220, y=120)
player3.controller = [KeyCode.I, KeyCode.J, KeyCode.K, KeyCode.L, KeyCode.O, KeyCode.U]
player3.placenumber = 2
player3.spritesheet = spritesheet_healer
label3 = window.create_label(PlayerLabel, text="P3", color = Color.BLUE)
label3.owner = player3
player4 = window.create_sprite(Player, x=1220, y=840)
player4.controller = [KeyCode.UP, KeyCode.LEFT, KeyCode.DOWN, KeyCode.RIGHT, KeyCode.NUM_0, KeyCode.NUM_1]
player4.placenumber = 3
player4.spritesheet = spritesheet_healer
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
    money_num = 0
    for money in window.get_sprites_with_tag("money"):
        if money.place != None:
            money_num+=1
    if money_num <= 25:
        window.create_sprite(Money, x=random.randint(200, 1080), y=random.randint(200,700))
        money_num+=1
def create_chest():
    window.create_sprite(Chest, x=random.randint(200, 1080), y=random.randint(200,700))
k=0
for location, placelocate, color in [(Point(450, 70),Point(0, 0),Color.RED),(Point(450, 880),Point(0, 900),Color.GREEN),(Point(830, 70),Point(1280, 0),Color.BLUE),(Point(830, 880),Point(1280, 900),Color.YELLOW)]:
    place = window.create_sprite(image = "place.png", position = placelocate, layer = -10000, scale = 0.7, opacity = 150)
    score = window.create_label(Score)
    square = window.create_sprite(scale = 100)
    score.ownerplace = place
    score.place = k
    place.color = color
    score.position = location
    score.color = place.color
    square.color = score.color
    square.opacity = 50
    square.position = score.position+Point(10,-30)
    k+=1
    
for location, player in [(160, player1),(160+320,player2),(160+320*2,player3),(160+320*3,player4)]:
    choice = window.create_sprite(ChoiceSprite, position=Point(location, 520))
    choice.player = player
    choice.scale = 8
black = window.create_sprite(layer = 100001, position = window.center, scale_x = window.width, scale_y = window.height, color=Color.BLACK)

for i in range(10):
    create_money()

window.run()

