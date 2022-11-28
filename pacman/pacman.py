from pycat.core import Window, Sprite, Point, Color, KeyCode
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


class Ghost(Sprite):
    def on_create(self):
        self.image = "ghost1.png"
        self.add_tag("ghost")
        self.fcolor = self.color
        self.path = []
        self.layer = 1000
        self.target = None
        self.time = 0
        self.wait_time : int
        self.index = 0
        self.home : Point
        self.state = Ghost_state.IDLE
    def on_update(self, dt):
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
        if window.is_key_down(KeyCode.R):
            self.state = Ghost_state.RUNAWAY
            self.time = 0
    def runaway(self, dt):
        if self.target != None:
            self.position = self.target.position
        self.color = Color.BLUE
        self.time += dt
        if self.time>=5:
            self.state = Ghost_state.CHASING
        if self.is_touching_sprite(pacpac):
            bfs.setup(get_cell(self.position), get_cell(self.home), sw=0)
            bfs.solve()
            self.path = bfs.path()
            self.index = 1
            self.state = Ghost_state.GOHOME
    def gohome(self):
            self.color = Color.BLACK
            self.target = self.path[self.index]
            self.point_toward_sprite(self.target)
            self.move_forward(16)
            if self.distance_to(self.target)<2:
                self.index += 1
            if self.index == len(self.path):
                self.state = Ghost_state.IDLE
                self.time = 0

            
        

class Pac_box(Sprite):
    def on_create(self):
        self.image = "pacman.png"
        self.layer = 1000
        self.target = None
    def on_update(self, dt):
        if self.target != None:
            self.point_toward_sprite(self.target)
            self.move_forward(16)
            if self.distance_to(self.target) < 2:
                self.target = None
        else:
            if window.is_key_pressed(KeyCode.A):
                self.target = get_cell(self.position + Point(-64,0))
            if window.is_key_pressed(KeyCode.D):
                self.target = get_cell(self.position + Point(64,0))
            if window.is_key_pressed(KeyCode.W):
                self.target = get_cell(self.position + Point(0,64))
            if window.is_key_pressed(KeyCode.S):
                self.target = get_cell(self.position + Point(0,-64))
            if self.target == None:
                self.move_forward(64)
                self.target = get_cell(self.position)
                self.move_forward(-64)
    def get_pacell(self):
        if self.target != None:
            return self.target
        else:
            return get_cell(self.position)


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