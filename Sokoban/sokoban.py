from pycat.core import Window, Sprite, Label, Color, Scheduler, KeyCode, RotationMode
from pycat.extensions.ldtk import LdtkLayeredLevel

window = Window()

level = LdtkLayeredLevel.from_file(
    ldtk_file_path="sokoban l1.ldtk",
    level_id='Level_0',
    image_path='sokoban l1/png/',
    layer_ordering={
        'Wall' : -1,
    }
)

level.render(window, debug_entities=False)   

# class Wall(Sprite):
#     def on_create(self):
#         self.scale = 64
#         self.color = Color.MAGENTA
#         self.add_tag("wall")

class Box(Sprite):
    def on_create(self):
        self.image = "box.png"
        self.scale = 60/64
        self.add_tag("box")
        self.rotation_mode = RotationMode.NO_ROTATION
    def try_push(self, dir):
        self.rotation = dir
        self.move_forward(64)
        if self.is_touching_any_sprite():
            if len(self.get_touching_sprites_with_tag("ldtk_wall")):
                self.move_forward(-64)
            if len(self.get_touching_sprites_with_tag("box")):
                self.move_forward(-64)
        if self.is_touching_any_sprite_with_tag("ldtk_target"):
            self.color = Color.GREEN
        else:
            self.color = Color.WHITE


class Player(Sprite):
    def on_create(self):
        self.image = "player.png"
        self.scale = 60/64
        self.rotation_mode = RotationMode.NO_ROTATION
    def on_update(self, dt):
        if window.is_key_down(keycode=KeyCode.W):
            self.rotation = 90
            self.move_forward(64)
        if window.is_key_down(keycode=KeyCode.A):
            self.rotation = 180
            self.move_forward(64)
        if window.is_key_down(keycode=KeyCode.S):
            self.rotation = 270
            self.move_forward(64)
        if window.is_key_down(keycode=KeyCode.D):
            self.rotation = 0
            self.move_forward(64)
        if self.is_touching_any_sprite_with_tag("ldtk_wall"):
            self.move_forward(-64)
        if self.is_touching_any_sprite_with_tag("box"):
            self.get_touching_sprites_with_tag("box")[0].try_push(self.rotation)
            if self.is_touching_any_sprite_with_tag("box"):
                self.move_forward(-64)
        
window.create_sprite(Player, x=32+64*8, y=32+64*5)
window.create_sprite(Box, x=32+64*5, y=32+64*5)
window.create_sprite(Box, x=32+64*5, y=32+64*3)
window.create_sprite(Box, x=32+64*6, y=32+64*6)


window.run()