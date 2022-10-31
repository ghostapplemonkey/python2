from pycat.core import Sprite, Window, Color, Label
import random

window = Window(width=600, height=900)

colorcycle = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.CYAN, Color.PURPLE, Color.ORANGE]
ans = [Color.RED, Color.GREEN, Color.YELLOW, Color.BLUE, Color.CYAN, Color.PURPLE, Color.ORANGE]
random.shuffle(ans)
colorbutton = [None]*4
asset = input("which shape do you want?")
class Button(Sprite):
    def on_create(self):
        self.image = str(asset)+".png"
        self.color = Color.WHITE
        self.colorn = 0
        self.scale = 1.2
    def on_left_click(self):
        self.color = colorcycle[self.colorn%len(colorcycle)]
        self.colorn+=1
        
class Check(Sprite):
    def on_create(self):
        self.scale_x = 100
        self.createl = 860
        self.scale_y = 50
        self.x = 500
        self.y = 90
        self.correct = 0
        self.hcorrect = 0
        self.cx = 0
    def clonepeg(self):
        self.correct = 0
        self.hcorrect = 0
        for i in range(4):
                box = window.create_sprite()
                box.image = str(asset)+".png"
                box.color = colorbutton[i].color
                box.x = colorbutton[i].x
                box.y = self.createl
                box.scale = 1.2
                if colorbutton[i].color == ans[i]:
                    self.correct+=1
                for j in range(4):
                    if colorbutton[i].color == ans[j] and colorbutton[i].color != ans[i]:
                        self.hcorrect+=1
                
    def scoretext(self):
        score = window.create_label()
        score.text = str(self.correct)
        score.y = self.createl+20
        score.x = 470
        score.font = "Consolas"
        score.font_size = 30
    def hscoretext(self):
        hscore = window.create_label()
        hscore.text = str(self.hcorrect)
        hscore.y = self.createl+20
        hscore.x = 520
        hscore.font = "Consolas"
        hscore.font_size = 30
    def scorepeg(self):
        self.cx = 0
        for i in range(self.correct):
            circle = window.create_sprite(image = "circle.png", x=480+self.cx%60, y=self.createl+10-30*int(self.cx/60))
            circle.color = Color.RED
            circle.scale = 0.8
            self.cx += 30
        for i in range(self.hcorrect):
            circle = window.create_sprite(image = "circle.png", x=480+self.cx%60, y=self.createl+10-30*int(self.cx/60))
            circle.scale = 0.8
            self.cx += 30
    def on_left_click(self):
        if self.createl>100:
            self.clonepeg()
            print("correct : "+str(self.correct))
            # self.scoretext()
            # self.hscoretext()
            self.scorepeg()
            self.createl -= 70
            if self.correct == 4:
                print("you win")
                self.delete()
        else:
            print("you lose")
            self.delete()
        
        

for i in range(100, 420, 80):
    colorbutton[int((i-100)/80)] = window.create_sprite(Button, x=i, y=90)
window.create_sprite(Check)
        

window.run()