from random import randint
from pycat.core import Sprite, Window, KeyCode, Label, Scheduler, Player

window = Window(width=1200, height=600)

live = 10
time = [4,6,8,10]

class Score(Label):
    def on_create(self):
        self.font = "Consolas"
    def on_update(self, dt: float):
        self.text = "Live : "+str(live)



class Timer(Label):
    def on_create(self):
        self.font = "Consolas"
        self.timer = 0
        self.y = 570
    def on_update(self, dt: float):
        self.timer += dt
        self.text = "Time : "+str(round(self.timer,2))

window.create_label(Timer)

window.create_label(Score)

class Spawner(Sprite):
    def on_create(self):
        self.x = 100
        
        self.timer = 0
        self.stime = time[randint(0,3)]
        self.scale = 4
        self.layer = 100
    def on_update(self, dt):
        self.timer += dt
        if self.timer >= self.stime:
            self.stime = time[randint(0,3)]
            window.create_sprite(Cars, image = self.image, position = self.position)
            self.timer = 0

class Cars(Sprite):
    def on_create(self):
        self.scale = 3
    def on_update(self, dt):
        global live
        self.x+=3
        if self.x >= 1200:
            live -= 1
            self.delete()

class Tower(Sprite):
    def on_create(self):
        self.y = 50
        self.scale = 3
        self.layer = 100
        self.button : KeyCode
        self.ismoveing = False
        self.bumpcarimage : str
        self.layer = 2
    def on_update(self, dt):
        global live
        if window.is_key_down(self.button) and self.ismoveing ==False:
            self.ismoveing = True
            self.rotation+=90
        if self.ismoveing == True:
            self.y+=40
            if self.y >= 600:
                live -= 1
                self.rotation-=90
                self.y=50
                self.ismoveing = False  
        if len(self.get_touching_sprites())!=0:
            for car in self.get_touching_sprites():
                if car.image == self.bumpcarimage:
                    car.delete()
                    explosion = window.create_sprite(image = "explosion.gif", position = self.position)
                    explosion.y+=150
                    Scheduler.wait(1.7, explosion.delete)
                    # p = Player("Explosion7.wav")
                    # p.play()
                    self.rotation-=90
                    self.y=50
                    self.ismoveing = False
                    break
            
            
        
window.create_sprite(Spawner, y=200, image = "Cars/rounded_green.png")
window.create_sprite(Spawner, y=300, image = "Cars/rounded_yellow.png")
window.create_sprite(Spawner, y=400, image = "Cars/rounded_red.png")
window.create_sprite(Spawner, y=500, image = "Cars/sedan_vintage.png")
truck = window.create_sprite(Tower, x=400, image = "Cars/truckdelivery.png")
truck.button = KeyCode.A
truck.bumpcarimage = "Cars/rounded_green.png"
truck = window.create_sprite(Tower, x=600, image = "Cars/trucktank.png")
truck.button = KeyCode.S
truck.bumpcarimage = "Cars/rounded_yellow.png"
truck = window.create_sprite(Tower, x=800, image = "Cars/towtruck.png")
truck.button = KeyCode.D
truck.bumpcarimage = "Cars/rounded_red.png"
truck = window.create_sprite(Tower, x=1000, image = "Cars/riot.png")
truck.button = KeyCode.F
truck.bumpcarimage = "Cars/sedan_vintage.png"
road = window.create_sprite(x=600, y=200)
road.scale_x = 1200
road.scale_y = 60
road.opacity = 50
road = window.create_sprite(x=600, y=300)
road.scale_x = 1200
road.scale_y = 60
road.opacity = 50
road = window.create_sprite(x=600, y=400)
road.scale_x = 1200
road.scale_y = 60
road.opacity = 50
road = window.create_sprite(x=600, y=500)
road.scale_x = 1200
road.scale_y = 60
road.opacity = 50
road = window.create_sprite(x=400, y=300)
road.scale_y = 600
road.scale_x = 80
road.opacity = 50
road = window.create_sprite(x=600, y=300)
road.scale_y = 600
road.scale_x = 80
road.opacity = 50
road = window.create_sprite(x=800, y=300)
road.scale_y = 600
road.scale_x = 80
road.opacity = 50
road = window.create_sprite(x=1000, y=300)
road.scale_y = 600
road.scale_x = 80
road.opacity = 50


window.run()
