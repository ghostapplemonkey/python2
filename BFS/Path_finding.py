from pycat.core import Window, Sprite, Color, Point, KeyCode
import random
from bfs import Bfs
from pycat.base.event import MouseEvent, MouseButton

window = Window(width=1280, height=640) 

def get_cell(position : Point):
    for cell in window.get_all_sprites():
        if cell.distance_to(position) < 2:
            return cell
    return None

class Runningbox(Sprite):
    def on_create(self):
        self.scale = 30
        self.index = 1
        self.running = False
        self.time = 0
        self.layer = 1000
    def on_update(self, dt):
        if self.running == True:
            self.point_toward_sprite(solveman.path[self.index])
            self.move_forward(10)
            if self.distance_to(solveman.path[self.index]) <= 20:
                self.index += 1
            if self.index == len(solveman.path):
                self.running = False

runningbox = window.create_sprite(Runningbox)

class SolveMan(Sprite):
    def on_create(self):
        self.bfs = Bfs()
        self.start : Sprite
        self.end : Sprite
        self.result : bool
        self.time = 0
        self.solving = False
        self.path : list[Sprite]
    def on_update(self, dt):
        if window.is_key_pressed(KeyCode.B):
            self.solve(0)
            self.display_path()
        if window.is_key_pressed(KeyCode.D):
            self.solve(1)
            self.display_path()
        self.time += dt
        if window.is_key_pressed(KeyCode.N):
            self.slowsolving(sw=0)
            self.solving = True
        if window.is_key_pressed(KeyCode.F):
            self.slowsolving(sw=1)
            self.solving = True
        if self.solving == True:
            if self.time > 0.05:
                self.result = self.bfs.step()
                self.time = 0
                if self.bfs.v != self.bfs.start and self.bfs.v != self.bfs.end:
                    self.bfs.v.color = Color.YELLOW
                if self.bfs.v == self.bfs.end:
                    self.solving = False
                    self.display_path()
        if window.is_key_pressed(KeyCode.P):
            self.solve(0)
            self.path = self.bfs.path()
            runningbox.position = self.start.position
            runningbox.running = True
                    


    def slowsolving(self, sw):
        self.setup_cells()
        self.bfs.setup(start=self.start, end=self.end, sw=sw)
        
    def solve(self, sw):
        self.setup_cells()
        self.bfs.setup(start=self.start, end=self.end, sw=sw)
        self.result = self.bfs.solve()
    def setup_cells(self):
        for cell in window.get_all_sprites():
            if cell.color != Color.RED and cell.color != Color.GREEN:
                cell.clear_tags()
                cell.color = Color.WHITE
        
        for cell in window.get_sprites_with_tag("start"):
            self.start = cell
        for cell in window.get_sprites_with_tag("end"):
            self.end = cell
    def display_path(self):
        if self.result == True:
            for i in self.bfs.path():
                if i!=self.start and i!=self.end:
                    i.color = Color.AZURE


class Cell(Sprite):
    def get_neighbors(self):
        neighbors = []
        for i in [Point(64,0), Point(-64,0), Point(0,64), Point(0,-64)]:
            if get_cell(self.position+i):
                if get_cell(self.position+i).image == "ground.png":
                    neighbors.append(get_cell(self.position+i))
        return neighbors
    def __str__(self):
        return str(int((self.x-32)/64))+","+str(int((self.y-32)/64))
    def on_click(self, mouse_event: MouseEvent):
        if(mouse_event.button == MouseButton.LEFT and self.image == "ground.png"):
            for cell in window.get_all_sprites():
                if cell.color != Color.GREEN:
                    cell.clear_tags()
                    cell.color = Color.WHITE
            self.add_tag("end")
            self.color = Color.RED
        if(mouse_event.button == MouseButton.RIGHT and self.image == "ground.png"):
            for cell in window.get_all_sprites():
                if cell.color != Color.RED:
                    cell.clear_tags()
                    cell.color = Color.WHITE
            self.add_tag("start")
            self.color = Color.GREEN
        

for i in range(0,640,64):
    for j in range(0,1280,64):
        k=random.random()
        if k>0:
            cell = window.create_sprite(Cell,x=j+32,y=i+32)
            cell.image = "ground.png"
        else:
            cell = window.create_sprite(Cell,x=j+32,y=i+32)
            cell.image = "block.png"

solveman = window.create_sprite(SolveMan)




window.run()

