from datetime import datetime
from threading import Thread
from time import sleep

from threadsafe import Tk, Canvas
from physics import Vector
from graphics import Costume


INTERACT_WITH_PHYSICS = True
INTERACT_WITH_GRAVITY = True
INTERACT_WITH_GROUND = True

GRAVITY = 9.81
GROUND = "ground"


class BasicSprite:
    """
    This is the basic sprite widget. It can act using a physics engine (given that PHYSICS is true).
    """

    __slots__ = ("screen", "forces", "pos", "v", "a", "mass", "upper", "lower", "last_t")

    def __init__(self, pos: Vector, v=Vector(0, 0), a=Vector(0, 0), forces=Vector(0, 0), mass=1):
        # We don't know the screen for now
        self.screen = None

        # The physics stuff:
        self.forces = forces    # Vector
        self.pos = pos          # Vector
        self.v = v              # Vector
        self.a = a              # Vector
        self.mass = mass        # Scalar

        # Sprite details:
        self.upper = pos        # Position Vector
        self.lower = pos        # Position Vector

        # Time keeping purposes:
        self.last_t = datetime.now()

    def move(self, delta):
        self.pos += delta

    def tick(self) -> None:
        assert self.screen is not None, "This object hasn't been registered with a screen."
        # If gavity is active:
        #    add weight to the forces acting on the object
        #    assuming the object isn't touching the ground
        now_t = datetime.now()
        delta_t = (self.last_t - now_t).seconds
        self.last_t = now_t
        if INTERACT_WITH_GRAVITY:
            if (not self.is_touching(GROUND)) or (not INTERACT_WITH_GROUND):
                weight = Vector(0, GRAVITY*self.mass)
                self.act(weight)
        # Make the forces act on the object:
        if INTERACT_WITH_PHYSICS:
            self.a = self.forces/self.mass
            # Change the velocity and position accordingly
            self.v += self.a*delta_t
            self.pos += self.v*delta_t

    def is_touching(self, other) -> bool:
        assert self.screen is not None, "This object hasn't been registered with a screen."
        # Check if I am touching the other object.
        # The orther object must be a constant (eg. GROUND) or
        # another Sprite object
        if other is GROUND:
            return self.screen.get_height() <= self.upper[1]
        else:
            self.screen.check_touching(self, other)

    def act(self, force: Vector) -> None:
        self.forces += force

    def draw(self, screen):
        self.screen = screen


class Sprite(BasicSprite):
    def __init__(self, sprite_file_location=None, **kwargs):
        super().__init__(**kwargs)
        self.current_costume_idx = 0
        self.costumes = [Costume(size=(0, 0), changable=False, hidden=True)]
        self.costume_details = [self.costumes[0].get_details()]

    def destroy(self):
        for costume in self.costumes:
            costume.destroy()

    def remove_costume(self, idx):
        assert idx != 0, "You can't remove the 0th costume."
        costume = self.costumes[idx]
        del self.costumes[idx]
        del self.costume_details[idx]

    def add_costume(self, costume):
        self.costumes.append(costume)

    def add_costume_from_file(self, file):
        costume = Costume.from_file(file)
        self.costumes.append(costume)

    def set_costume(self, idx):
        current_costume = self.costumes[self.current_costume_idx]
        current_costume.hide()
        assert isinstance(idx, int), "idx must be an int."
        assert len(self.costumes) > idx, "Index out of range."
        assert idx >= 0, "Must be a +ve int."
        self.current_costume_idx = idx
        new_costume = self.costumes[self.current_costume_idx]
        new_costume.show()

    def draw(self, screen):
        super().draw(screen)
        costume = self.costumes[self.current_costume_idx]
        costume.draw(tuple(self.pos))

    def set_canvas(self, canvas):
        for costume in self.costumes:
            costume.set_canvas(canvas)

    @classmethod
    def from_pil(cls, pillow_image, **kwargs):
        sprite = Sprite(**kwargs)
        sprite.sprite = pillow_image
        return sprite


class Screen:
    def __init__(self, width=400, height=400, bg="#f0f0ed"):
        """
        Creates a window with the height and width given
        """
        # Stop `Screen.mainloop()` when the program is closed
        # to prevent: `Tcl_AsyncDelete: async handler deleted by the wrong thread`
        #self.running = True
        # All of the sprites on the screen:
        self.sprites = []
        # The size of the screen (used with the physics engine)
        self.size = (width, height)
        # Create a window and put a canvas on it.
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Scratch v0.1")
        self.canvas = Canvas(self.root, width=width, height=height, bg=bg, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=1, column=1)

        self.root.after(100, self.mainloop)

    def mainloop(self):
        for sprite in self.sprites:
            sprite.tick()
            sprite.draw(self)
        if not self.root.closed:
            self.root.after(100, self.mainloop)

    # def mainloop(self):
    #     t = Thread(target=self._mainloop, daemon=True)
    #     t.start()

    # def _mainloop(self):
    #     while not self.root.tk_dead:
    #         for sprite in self.sprites:
    #             sprite.draw(self)
    #         sleep(0.1)

    def geometry(self, pos=(None, None)):
        """
        Moves the screen to the location given by pos
        """
        if pos[0] is None:
            pos = (self.root.winfo_x(), pos[1])
        if pos[1] is None:
            pos = (pos[0], self.root.winfo_y())
        self.root.geometry("+%i+%i" % pos)

    def title(self, text):
        self.root.title(text)

    @property
    def bg(self):
        raise ValueError("Can't get the value of Screen.bg")

    @bg.setter
    def bg(self, new_bg):
        self.canvas.config(bg=new_bg)

    def get_width(self):
        return self.size[0]

    def get_height(self):
        return self.size[1]

    def add_sprite(self, sprite):
        """
        Adds the sprite and keeps it alive.
        """
        self.sprites.append(sprite)

    def register_sprite(self, sprite):
        """
        Adds the sprite and keeps it alive.
        """
        sprite.set_canvas(self.canvas)
        self.sprites.append(sprite)


if __name__ == "__main__":
    from PIL import Image as PIL_Image
    from PIL import ImageDraw as PIL_ImageDraw
    from graphics import Costume
    from threadsafe import StackDebug

    from time import sleep

    # Make this easier pls:
    image = PIL_Image.new("RGBA", (700, 700))
    draw = PIL_ImageDraw.Draw(image)
    draw.line((350, 0, 350, 700), fill="white")

    costume = Costume.from_pil(image)
    sprite = Sprite(pos=Vector(200, 200))
    sprite.add_costume(costume)
    sprite.set_costume(1)

    with StackDebug("debug.txt", "all"):
        screen = Screen()
        screen.bg = "black"
        screen.register_sprite(sprite)

        hidden = False

        while not screen.root.closed:
            costume.rotate(1)
            if hidden:
                costume.show()
                hidden = False
            else:
                costume.hide()
                hidden = True
            sleep(0.1)