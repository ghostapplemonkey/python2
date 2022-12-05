import random
from pycat.core import Window, Sprite, Point, Color, KeyCode, Label, Scheduler
from pycat.extensions.ldtk import LdtkLayeredLevel
from bfs import Bfs
from enum import Enum

window = Window()

map = {}

level = LdtkLayeredLevel.from_file(
    ldtk_file_path="level.ldtk",
    level_id='Level_0',
    image_path='level/png/',
    layer_ordering={
        'Tiles' : 0,
    }
)

level.render(window, debug_entities=False)

def get_cell(position : Point):
    return map.get((int(position.x), int(position.y)), None)

bfs = Bfs()

class Ghost_state(Enum):
    CHASING = 1
    IDLE = 2
    RUNAWAY = 3
    GOHOME = 4

class Dot(Sprite):
    def on_create(self):
        self.scale = 15
        self.layer = 100
    def on_update(self, dt):
        if self.is_touching_sprite((pacpac)):
            pacpac.score += 1
            self.delete()


class Ghost(Sprite):
    def on_create(self):
        self.image = "ghost1.png"
        self.add_tag("ghost")
        self.scale = 0.9
        self.fcolor = self.color
        self.path = []
        self.layer = 1000
        self.target = None
        self.time = 0
        self.ttarget = None
        self.wait_time : int
        self.index = 0
        self.home : Point
        self.state = Ghost_state.IDLE
    def on_update(self, dt):
        if pacpac.lose == False:
            if self.state == Ghost_state.IDLE:
                self.idle(dt)
            if self.state == Ghost_state.CHASING:
                self.chasing()
            if self.state == Ghost_state.RUNAWAY:
                self.runaway(dt)
            if self.state == Ghost_state.GOHOME:
                self.gohome()
    def idle(self, dt):
        self.time += dt
        self.color = self.fcolor
        if self.time >= self.wait_time:
            self.state = Ghost_state.CHASING
            self.wait_time = 5
            self.time = 0
        if self.target == None:
            if get_cell(self.position+Point(0,64)):
                self.target = get_cell(self.position+Point(0,64))
            else:
                self.target = get_cell(self.position+Point(0,-64))
        else:
            self.point_toward_sprite(self.target)
            self.move_forward(4)
            if self.distance_to(self.target)<2:
                self.target = None
    def chasing(self):
        self.color = self.fcolor
        if self.target == None:
            bfs.setup(start = get_cell(self.position),end = pacpac.get_pacell(),sw = 0)
            bfs.solve()
            self.path = bfs.path()
            if len(self.path)>1:
                self.target = self.path[1]
        else:
            self.point_toward_sprite(self.target)
            self.move_forward(4)
            if self.distance_to(self.target)<2:
                self.target = None
        if self.is_touching_sprite(pacpac) and pacpac.usingp == True:
            self.position = self.target.position
            bfs.setup(get_cell(self.position), get_cell(self.home), sw=0)
            bfs.solve()
            self.path = bfs.path()
            self.index = 1
            self.state = Ghost_state.GOHOME
    def runaway(self, dt):
        if self.target == None:
            while(self.ttarget == None):
                self.ttarget = get_cell(Point(32+64*random.randint(1, 19), 32+64*random.randint(1, 9)))
            bfs.setup(start = get_cell(self.position),end = self.ttarget,sw = 0)
            bfs.solve()
            self.ttarget = None
            self.path = bfs.path()
            if len(self.path)>1:
                self.target = self.path[1]
        else:
            self.point_toward_sprite(self.target)
            self.move_forward(4)

            if self.distance_to(self.target)<2:
                self.target = None
        self.color = Color.BLUE
        self.time += dt
        if self.time>=5:
            self.state = Ghost_state.CHASING
        if self.is_touching_sprite(pacpac):
            self.position = self.target.position
            bfs.setup(get_cell(self.position), get_cell(self.home), sw=0)
            bfs.solve()
            self.path = bfs.path()
            self.index = 1
            self.state = Ghost_state.GOHOME
    def gohome(self):
            self.color = Color.BLACK
            self.target = self.path[self.index]
            self.point_toward_sprite(self.target)
            self.move_forward(8)
            if self.distance_to(self.target)<2:
                self.index += 1
            if self.index == len(self.path):
                self.state = Ghost_state.IDLE
                self.time = 0

            
class AmazingDot(Sprite):
    def on_create(self):
        self.scale = 25
        self.layer = 100
    def on_update(self, dt):
        if self.is_touching_sprite(pacpac):
            if ghost1.state == Ghost_state.CHASING:
                ghost1.state = Ghost_state.RUNAWAY
                ghost1.time = 0
            if ghost2.state == Ghost_state.CHASING:
                ghost2.state = Ghost_state.RUNAWAY
                ghost2.time = 0
            if ghost3.state == Ghost_state.CHASING:
                ghost3.state = Ghost_state.RUNAWAY
                ghost3.time = 0
            if ghost4.state == Ghost_state.CHASING:
                ghost4.state = Ghost_state.RUNAWAY
                ghost4.time = 0
            self.delete()

class Pac_box(Sprite):
    def on_create(self):
        self.image = "pacman.png"
        self.layer = 1000
        self.target = None
        self.score = 0
        self.needscore = 0
        self.lose = False
        self.powertime = 2
        self.usingp = False
        self.time = 0
    def on_update(self, dt):
        if self.lose == False:
            if window.is_key_down(KeyCode.P) and self.powertime > 0: 
                self.usingp = True
                self.powertime -= 1
                self.time = 0
            if self.time > 8:
                self.usingp = False
                self.color = Color.WHITE
                self.time = 0
            if self.usingp == True:
                self.time += dt
                self.color = Color.random_rgb()
            if self.target != None:
                self.point_toward_sprite(self.target)
                self.move_forward(16)
                if self.distance_to(self.target) < 2:
                    self.target = None
            else:
                if window.is_key_pressed(KeyCode.LEFT):
                    self.target = get_cell(self.position + Point(-64,0))
                if window.is_key_pressed(KeyCode.RIGHT):
                    self.target = get_cell(self.position + Point(64,0))
                if window.is_key_pressed(KeyCode.UP):
                    self.target = get_cell(self.position + Point(0,64))
                if window.is_key_pressed(KeyCode.DOWN):
                    self.target = get_cell(self.position + Point(0,-64))
                if self.target == None:
                    self.move_forward(64)
                    self.target = get_cell(self.position)
                    self.move_forward(-64)
            if self.is_touching_any_sprite_with_tag("ghost"):
                for ghost in self.get_touching_sprites_with_tag("ghost"):
                    if ghost.state == Ghost_state.CHASING or ghost.state == Ghost_state.IDLE:
                        if self.usingp == False:
                            self.image = "die.gif"
                            self.lose = True
                            self.scale = 0.25
        if self.score == self.needscore:
            print("You win")
            window.close()
        if self.lose == True:
            self.time += dt
            if self.time > 5.5:
                print("You lose")
                window.close()

    def get_pacell(self):
        if self.target != None:
            return self.target
        else:
            return get_cell(self.position)

class Scoretext(Label):
    def on_create(self):
        self.font = "Consolas"
        self.y = 630
        self.x = 20
        self.font_size = 25
        self.color = Color.WHITE
    def on_update(self, dt: float):
        self.text = "Score : "+str(pacpac.score)+"/"+str(pacpac.needscore)+"   Power left : "+str(pacpac.powertime)
text = window.create_label(Scoretext)
text.color = Color.BLUE
text.x += -2
text.y += 2
window.create_label(Scoretext)


pacpac = window.create_sprite(Pac_box, x=96, y=96)

class Cell(Sprite):
    def on_create(self):
        self.scale = 32
        self.layer = -1
        self.add_tag("cell")
    def get_neighbors(self):
        neighbors = []
        for i in [Point(64,0), Point(-64,0), Point(0,64), Point(0,-64)]:
            if get_cell(self.position+i):
                neighbors.append(get_cell(self.position+i))
        return neighbors
    def __str__(self):
        return str(int((self.x-32)/64))+","+str(int((self.y-32)/64))



for i in range(32, 1280, 64):
    for j in range(32, 640, 64):
        cell = window.create_sprite(Cell, x=i, y=j)
        if cell.is_touching_any_sprite_with_tag('ldtk_wall'):
            cell.delete()
        else:
            map[(i, j)] = cell
            window.create_sprite(Dot, x=i, y=j)
            a = random.random()
            pacpac.needscore += 1
            if a>0.9:
                window.create_sprite(AmazingDot, x=i, y=j)
            
        
ghost1 = window.create_sprite(Ghost, x=32+640-64, y=32+320)
ghost1.wait_time = 4
ghost1.home = Point(32+640-64, 32+320)
ghost2 = window.create_sprite(Ghost, x=32+640, y=32+320-64)
ghost2.fcolor = Color.CYAN
ghost2.wait_time = 9
ghost2.home = Point(32+640, 32+320-64)
ghost3 = window.create_sprite(Ghost, x=32+640-64, y=32+320-64)
ghost3.fcolor = Color.GREEN
ghost3.wait_time = 16
ghost3.home = Point(32+640-64, 32+320-64)
ghost4 = window.create_sprite(Ghost, x=32+640, y=32+320)
ghost4.fcolor = Color.YELLOW
ghost4.wait_time = 25
ghost4.home = Point(32+640, 32+320)

window.run()