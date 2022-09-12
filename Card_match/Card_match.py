from pycat.core import Window, Sprite, Point, RotationMode, Color, KeyCode
from pycat.math import get_distance
import random

window = Window(draw_sprite_rects=True, background_image="bg1.png",width=950, height=600)

score = 0
sprites = []
cards = ["1.png","2.png","3.png","4.png"]*4
random.shuffle(cards)

class Card(Sprite):
    def on_create(self):
        self.opacity = 250
        self.scale = 1.3
        self.time = 0
        self.movingcnt = 0
        self.state = 0
        self.rotation_mode = RotationMode.NO_ROTATION
        self.is_animate = False
        self.sx = self.x
        self.sy = self.y
        self.checktime = 0
    def on_left_click(self):
        if len(sprites)<2 and self not in sprites:
            self.opacity = 255
            sprites.append(self)
    def on_update(self,dt):
        if self.movingcnt < 99:
            self.movingcnt += 1
            self.move_forward(get_distance(Point(self.sx, self.sy), Point(700, 460))/100)
            if self.movingcnt == 98:
                self.opacity = 0
        else:
            self.time += dt
            if self.time > self.checktime:
                self.movingcnt += 1
                self.point_toward(Point(self.sx,self.sy))
                if self.movingcnt < 197:
                    self.move_forward(get_distance(Point(self.sx, self.sy), Point(700, 460))/100)
                else:
                    self.rotation_mode = RotationMode.ALL_AROUND
                    self.rotation = 0

        if self.is_animate == True:
            self.opacity += dt/2
            self.scale -= dt/1.5
            self.rotation += dt*30
            if self.scale < 0.1:
                self.delete()
class Check(Sprite):
    def on_create(self):
        self.x = 700
        self.y = 300
        self.image = "Check_box.png"
        self.rx = 0
        self.ry = 0
        self.rc = Color.RED
        self.time = 0
        
    def on_left_click(self):
        global sprites, score
        if len(sprites) == 2:
            if sprites[0].image == sprites[1].image:
                sprites[0].is_animate = True
                sprites[1].is_animate = True
                score += 2
            else:
                sprites[0].opacity = 0
                sprites[1].opacity = 0
            sprites = []
    def on_update(self, dt):
        global score
        self.time += dt
        if score == 16 and self.time >= 2:
            score = 0
            self.rx=random.randint(300,600)
            self.ry=random.randint(200,400)
            self.rc = Color.random_rgb()
            for i in range(0,360,10):
                firework = window.create_sprite(Firework, x=self.rx,y=self.ry)
                firework.rotation = i
                firework.color = self.rc
                firework.scale = 10
            
            
            
        if window.is_key_down(KeyCode.SPACE):
            score = 16 

class Firework(Sprite):
    def on_create(self):
        self.time = 0
        self.speed = 20
    def on_update(self, dt):
        self.time += dt
        self.speed -= dt
        self.opacity -= dt*(255/2)
        self.move_forward(self.speed)
        if self.time >= 0.5:
            self.delete()


t=0
for x in range(100, 461, 120):
    for y in range(100, 461, 120):
        t+=0.7
        card = window.create_sprite(Card, x=x, y=y, image = cards.pop())
        card.point_toward(Point(700, 460))
        card.sx = card.x
        card.sy = card.y
        card.checktime = t




window.create_sprite(Check)


window.run()