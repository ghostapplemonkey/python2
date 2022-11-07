from pycat.core import Window, Sprite, Color, Point
import random
from bfs import Bfs

window = Window(width=1280, height=640) 

def get_cell(position : Point):
    for cell in window.get_all_sprites():
        if cell.distance_to(position) < 2:
            return cell
    return None


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

for i in range(0,640,64):
    for j in range(0,1280,64):
        k=random.random()
        if k>0.4:
            cell = window.create_sprite(Cell,x=j+32,y=i+32)
            cell.image = "ground.png"
        else:
            cell = window.create_sprite(Cell,x=j+32,y=i+32)
            cell.image = "block.png"

start = get_cell(Point(32+64*0,32+64*0))
end = get_cell(Point(32+64*12,32+64*8))
start.image = "ground.png"
end.image = "ground.png"
start.color = Color.GREEN
end.color = Color.RED

bfs = Bfs()
print(bfs.solve(start=start, end=end))
for i in bfs.path(start=start, end=end):
    if i!=start and i!=end:
        i.color = Color.AZURE

window.run()

