import random
from turtle import position
from pycat.core import Sprite, Window, Color, KeyCode, Scheduler, Point, Label

window = Window(width=1200,height=600,enforce_window_limits=False)

score_a=0
score_b=0

class WrapSprite(Sprite):
    def wrap(self):
        if self.y > 600+self.height/2:
            self.y -= 600+self.height
        if self.y < 0-self.height/2:
            self.y += 600+self.height
        if self.x > 1200+self.width/2:
            self.x -= 1200+self.width
        if self.x < 0-self.width/2:
            self.x += 1200+self.width
class Score_plus(Label):
    def on_update(self, dt):
        self.font = "Consolas"
        self.x+=0.3
        self.y+=0.6
        self.opacity-=7
        self.font_size = 50
        if self.opacity<=50:
            self.delete()
class Ship(WrapSprite):
    def on_create(self):
        self.image = "ship.png"
        self.position = window.center
        self.color = Color.CYAN
        self.rotation+=180
        self.x=200
        self.speed=0
        self.key_up : KeyCode
        self.key_down : KeyCode
        self.key_left : KeyCode
        self.key_right : KeyCode
        self.mybullettag : str
        self.shootkey : KeyCode
        self.enemybullettag : str
    def setup(self,key_up,key_down,key_left,key_right,mybullettag,shootkey,enemybullettag):
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        self.mybullettag = mybullettag
        self.shootkey = shootkey
        self.enemybullettag = enemybullettag
    def on_update(self, dt):
        if self.is_touching_any_sprite_with_tag(self.enemybullettag):
            self.delete()
        # if self.is_touching_any_sprite_with_tag("ast"):

        if window.is_key_pressed(self.key_left):
            self.rotation+=3
        if window.is_key_pressed(self.key_right):
            self.rotation-=3
        if window.is_key_pressed(self.key_up):
            self.speed=min(self.speed+0.1,10)
            self.image = "ship_thrust.png"
        else:
            self.image = "ship.png"
        if window.is_key_pressed(self.key_down):
            self.speed=max(self.speed-0.1,0)
        self.move_forward(self.speed)
        self.wrap()
        if window.is_key_down(self.shootkey):
            bullet = window.create_sprite(Bullet,x=self.x,y=self.y,tag=self.mybullettag)
            bullet.rotation = self.rotation
class Scorea(Label):
    def on_create(self):
        self.font = "Consolas"
    def on_update(self, dt):
        self.text = "Score1 : "+str(score_a)
class Scoreb(Label):
    def on_create(self):
        self.y = 575
        self.font = "Consolas"
    def on_update(self, dt):
        self.text = "Score2 : "+str(score_b)
        

class Bullet(Sprite):
    def on_create(self):
        self.image = "bullet.png"
        self.scale = 2
    def on_update(self, dt):
        self.move_forward(20)
        if self.is_touching_window_edge():
            self.delete()

class Asteroid(WrapSprite):
    def on_create(self):
        self.add_tag("ast")
        self.color = Color.GREEN
    def on_update(self, dt):
        self.move_forward(3)
        self.wrap()
        for bullet in self.get_touching_sprites_with_tag("bulleta"):
            global score_a
            bullet.delete()
            for rotation in [90,-90]:
                if "big" in self.image:
                    a = window.create_sprite(Asteroid, x=self.x, y=self.y, image = random.choice(["med1.png", "med2.png", "med3.png"]))
                    a.rotation = self.rotation+rotation
                    score_a+=200
                    texta = window.create_label(Score_plus, text="+400", position = self.position)
                    texta.color = Color.YELLOW
                elif "med" in self.image:
                    a = window.create_sprite(Asteroid, x=self.x, y=self.y, image = random.choice(["small1.png", "small2.png", "small3.png"]))
                    a.rotation = self.rotation+rotation
                    score_a+=100
                    texta = window.create_label(Score_plus, text="+200", position = self.position)
                    texta.color = Color.YELLOW
                else:
                    score_a+=50
                    texta = window.create_label(Score_plus, text="+100", position = self.position)
                    texta.color = Color.YELLOW
                
            self.delete()
        
        for bullet in self.get_touching_sprites_with_tag("bulletb"):
            global score_b
            bullet.delete()
            for rotation in [90,-90]:
                if "big" in self.image:
                    a = window.create_sprite(Asteroid, x=self.x, y=self.y, image = random.choice(["med1.png", "med2.png", "med3.png"]))
                    a.rotation = self.rotation+rotation
                    score_b+=200
                    texta = window.create_label(Score_plus, text="+400", position = self.position)
                    texta.color = Color.CYAN
                elif "med" in self.image:
                    a = window.create_sprite(Asteroid, x=self.x, y=self.y, image = random.choice(["small1.png", "small2.png", "small3.png"]))
                    a.rotation = self.rotation+rotation
                    score_b+=100
                    texta = window.create_label(Score_plus, text="+200", position = self.position)
                    texta.color = Color.CYAN
                else:
                    score_b+=50
                    texta = window.create_label(Score_plus, text="+100", position = self.position)
                    texta.color = Color.CYAN
                
            self.delete()

def create_asteroid():
    ast = window.create_sprite(Asteroid)
    ast.image = random.choice(["big1.png", "big2.png", "big3.png"])
    i = random.randint(1,4)
    if i == 1:
        ast.x -= ast.width/2
        ast.y = random.random()*600
        ast.rotation = -45 + random.random()*90
    if i == 2:
        ast.x = 1200+ast.width/2
        ast.y = random.random()*600
        ast.rotation = 135 + random.random()*90
    if i == 3:
        ast.y -= ast.height/2
        ast.x = random.random()*1200
        ast.rotation = 45 + random.random()*90
    if i == 4:
        ast.y = 600+ast.height/2
        ast.x = random.random()*1200
        ast.rotation = 225 + random.random()*90
    
Scheduler.update(create_asteroid, 5)


        
        


ship = window.create_sprite(Ship)
ship.setup(KeyCode.UP,KeyCode.DOWN,KeyCode.LEFT,KeyCode.RIGHT,"bulleta",KeyCode.M,"bulletb")
ship.x = 1000
ship.rotation += 180
ship.color = Color.YELLOW
window.create_label(Scorea)
window.create_label(Scoreb)
ship = window.create_sprite(Ship)
ship.setup(KeyCode.W,KeyCode.S,KeyCode.A,KeyCode.D,"bulletb",KeyCode.SPACE,"bulleta")     
window.run()