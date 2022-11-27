from pycat.core import Window, Sprite, Point, Color, KeyCode
from pycat.extensions.ldtk import LdtkLayeredLevel
from bfs import Bfs


window = Window()


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
    for cell in window.get_sprites_with_tag("cell"):
        if cell.distance_to(position) < 2:
            return cell
    return None

class Pac_box(Sprite):
    def on_create(self):
        self.scale = 50
        self.layer = 1000
        self.target = None
    def on_update(self, dt):
        if self.target != None:
            self.point_toward_sprite(self.target)
            self.move_forward(8)
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


window.create_sprite(Pac_box, x=96, y=96)

class Cell(Sprite):
    def on_create(self):
        self.scale = 32
        self.layer = -1
        self.add_tag("cell")
    def get_neighbors(self):
        neighbors = []
        for i in [Point(64,0), Point(-64,0), Point(0,64), Point(0,-64)]:
            if get_cell(self.position+i):
                if get_cell(self.position+i).image == "ground.png":
                    neighbors.append(get_cell(self.position+i))
        return neighbors
    def __str__(self):
        return str(int((self.x-32)/64))+","+str(int((self.y-32)/64))

for i in range(32, 1280, 64):
    for j in range(32, 640, 64):
        cell = window.create_sprite(Cell, x=i, y=j)
        if cell.is_touching_any_sprite_with_tag('ldtk_wall'):
            cell.delete()
        


window.run()