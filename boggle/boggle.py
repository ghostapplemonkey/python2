from pycat.core import Window, Scheduler, Sprite, Label, RotationMode, Color
from pycat.base.event import MouseEvent
import random
window = Window()

dice = [ # new version
    ['A','A','E','E','G','N'],
    ['E','L','R','T','T','Y'],
    ['A','O','O','T','T','W'],
    ['A','B','B','J','O','O'],
    ['E','H','R','T','V','W'],
    ['C','I','M','O','T','U'],
    ['D','I','S','T','T','Y'],
    ['E','I','O','S','S','T'],
    ['D','E','L','R','V','Y'],
    ['A','C','H','O','P','S'],
    ['H','I','M','N','Q','U'],
    ['E','E','I','N','S','U'],
    ['E','E','G','H','N','W'],
    ['A','F','F','K','P','S'],
    ['H','L','N','N','R','Z'],
    ['D','E','I','L','R','X'],
]

English_words = []
words_already = []
with open("words_list.txt","r") as file:
    for word in file.readlines():
        English_words.append(word.strip("\n").upper())


word = []

CELL_SIZE = 128

class Dice(Sprite):
    def on_create(self):
        self.scale = 0.5
        self.color = Color.WHITE
    def on_click(self, mouse_event: MouseEvent):
        if self.color == Color.WHITE:
            if len(word) == 0:
                word.append(self)
                self.color = Color.AMBER
            elif abs(self.x - word[-1].x)<=CELL_SIZE and abs(self.y - word[-1].y)<=CELL_SIZE:
                word.append(self)
                self.color = Color.AMBER
                word[-2].color = Color.RED
                if len(word)>=3:
                    a = ""
                    for cell in word:
                        a+=cell.image[0]
                    if a in English_words:
                        for cell in word:
                            cell.color = Color.GREEN
                    else:
                        for cell in word:
                            if cell != self:
                                cell.color = Color.RED
                            else:
                                cell.color = Color.AMBER
        
class Finished_words(Label):
    def on_create(self):
        self.font = "Consolas"
        self.y = 630
        self.font_size = 25
        self.x = 750

class Finished_words2(Label):
    def on_create(self):
        self.font = "Consolas"
        self.y = 630
        self.font_size = 25
        self.x = 925

class Finished_words3(Label):
    def on_create(self):
        self.font = "Consolas"
        self.y = 630
        self.font_size = 25
        self.x = 1100



class Score(Label):
    def on_create(self):
        self.font = "Consolas"
        self.y = 640
        self.font_size = 25
        self.x = 750
        self.score = 0
    def on_update(self, dt: float):
        self.text = "Score : "+str(self.score)
    
score = window.create_label(Score)

finish_label = window.create_label(Finished_words)
finish_label2 = window.create_label(Finished_words2)
finish_label3 = window.create_label(Finished_words3)

class Check(Sprite):
    def on_create(self):
        self.x = 650
        self.y = 375
        self.scale = 2
        self.image = "check.png"
        self.label : Label = finish_label
    def on_click(self, mouse_event: MouseEvent):
        if len(words_already) > 14 and len(words_already) <= 28:
            self.label = finish_label2
        elif len(words_already)>28:
            self.label = finish_label3
        a = ""
        for text in word:
            a += text.image[0]
        if len(word)>=3 and a not in words_already and a in English_words:
            self.label.text += "\n"
            score.score += (len(word)-2)*2-1
            self.label.text += a
            self.label.text += "  "+str((len(word)-2)*2-1)
            words_already.append(a)
        for text in word:
            text.color = Color.WHITE
        
        word.clear()

class Cross(Sprite):
    def on_create(self):
        self.x = 650
        self.y = 225
        self.scale = 2
        self.image = "cross.png"
    def on_click(self, mouse_event: MouseEvent):
        for text in word:
            text.color = Color.WHITE
        word.clear()

window.create_sprite(Check)

window.create_sprite(Cross)

random.shuffle(dice)
k=0
for i in [CELL_SIZE*1, CELL_SIZE*2, CELL_SIZE*3, CELL_SIZE*4]:
    for j in [CELL_SIZE*1, CELL_SIZE*2, CELL_SIZE*3, CELL_SIZE*4]:
        window.create_sprite(Dice, image = dice[k][random.randint(0,5)]+".png", x=i, y=j)
        k+=1


window.run()