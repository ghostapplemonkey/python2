from pycat.core import Sprite, Window, Label, Scheduler, Color
from pycat.base.event import KeyEvent
import random

from sklearn.preprocessing import scale

window = Window(width=1200, height=600)
enemytexts = []

window.create_sprite(y=500, x=80, image = "castle.png", scale = 0.3)

class Particlesystem(Sprite):
    def on_create(self):
        self.sy = 5+random.random()*6
        self.sx = -2+random.random()*4
        self.scale = 10
    def on_update(self, dt):
        self.sy -= 0.5
        self.y += self.sy
        self.x += self.sx
        self.opacity -= dt*500
        if self.opacity < 10:
            self.delete()

class textbg(Sprite):
    def on_create(self):
        self.x = 1125
        self.y = 650
        self.wl = 0
        self.speed = -3
        self.scale_x = 150
        self.scale_y = 100
        self.color = Color.random_rgb()
    def on_update(self, dt):
        self.wl += 3
        self.y += self.speed
        if self.wl == 600:
            self.x -= 150
            self.speed *= -1
            self.wl = 0
        if self.x == 75 and self.y > 350:
            self.delete()
    
class TypeableText(Label):   
    def on_create(self):
        self.wl = 0
        self.x = 1050
        self.y = 600
        self.speed = -3
        self.font_size = 30
        window.subscribe(on_key_press=self.on_key_press_handler)
        self.text = random.choice(["apple","dog","cat","king","orange","monkey","sheep","lion","energy","pycat","yong"])
    def on_key_press_handler(self, key_event : KeyEvent):
        global enemytexts
        if len(enemytexts)>0 and self == enemytexts[0]:
            if len(self.text)>1:
                if self.text[0] == key_event.character:
                    self.text = self.text[1:]
            elif self.text[0] == key_event.character:
                for _ in range(20):
                    window.create_sprite(Particlesystem, x = self.x, y = self.y)
                enemytexts = enemytexts[1:]
                self.delete()
                
    def on_update(self, dt: float):
        self.wl += 3
        self.y += self.speed
        if self.wl == 600:
            self.x -= 150
            self.speed *= -1
            self.wl = 0
        if self.x == 0 and self.y > 400:
            print("you lose")
            window.close()        
class EnemyControllor(Sprite):
    def on_create(self):
        self.time = 100
        self.speed = 1.2
    def on_update(self, dt):
        self.speed -= dt/100
        self.time += dt
        if self.time >= self.speed:
            self.time = 0
            enemytexts.append(window.create_label(TypeableText))
            window.create_sprite(textbg)
            print(enemytexts)
        
        
        
window.create_sprite(EnemyControllor)

window.run()