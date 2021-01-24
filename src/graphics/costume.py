from PIL import Image as PIL_Image
from PIL import ImageTk


class Costume:
    __slots__ = ("image", "temp_image", "width", "height", "tkimage", "photoimage", "changed", "_resized", "_rotation", "changable", "initialised", "hidden", "canvas")

    def __init__(self, size=None, changable=False, hidden=True):
        self.canvas = None
        self.hidden = hidden
        self.changable = changable
        if size is not None:
            self.image = PIL_Image.new("RGBA", size)
            self.width, self.height = self.image.size
            self.initialised = True
        else:
            self.initialised = False
        # Just for reference
        self.tkimage = None
        self.photoimage = None
        # Changes to the picture that will be executed on redraw
        self.changed = True
        self._resized = True
        self._rotation = 0

    def destroy(self):
        del self.image
        del self.photoimage

    def get_details(self):
        return {"bbox": ("x1", "y1", "x2", "y2")}

    @classmethod
    def from_pil(cls, pil_image, changable=False):
        img = Costume(changable=changable)
        img.image = pil_image
        img.initialised = True
        img.width, img.height = pil_image.size
        return img

    @classmethod
    def open(cls, filename):
        return Costume(PIL_Image.open(filename))

    @classmethod
    def from_file(cls, filename):
        return Costume.open(filename)

    def set_canvas(self, canvas):
        self.canvas = canvas

    def __del__(self):
        del self.photoimage

    def resize(self, scale):
        assert self.initialised, "This image hasn't been initialised yet."
        self.width *= scale
        self.height *= scale
        self._resized = True
        self.changed = True

    def rotate(self, angle):
        assert self.initialised, "This image hasn't been initialised yet."
        self._rotation += angle
        self.changed = True

    def reset_image(self):
        assert self.initialised, "This image hasn't been initialised yet."
        # Undo all of the changes we made to the sprite:
        self._resized = False
        self._rotation = 0
        self.changed = True
        self.width, self.height = self.image.size

    def hide(self):
        # Deletes the sprite from the screen
        # but can be restored with `Costume.show()`
        if self.canvas is not None:
            self.canvas.delete(self.tkimage)
        self.tkimage = None
        self.changed = False
        self.hidden = True

    def show(self):
        # Restores a hidden image on the canvas
        self.changed = True
        self.hidden = False

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def draw(self, position):
        assert self.canvas is not None, "This image doesn't have a canvas."
        if (not self.hidden) and self.changed:
            # self.canvas.after(100, self.)
            image = self._update()
            if self.tkimage is not None:
                self.canvas.delete(self.tkimage)
            self.temp_image = image # Keep the image alive
            self.photoimage = ImageTk.PhotoImage(image)
            self.tkimage = self.canvas.create_image(position, image=self.photoimage)
            self.changed = False

    def _update(self):
        # Rotate the image
        image_copy = self.image.rotate(self._rotation) # If _rotation is 0, it will only copy the image :D

        # Resize image
        if self._resized:
            image_copy.resize((self.width, self.height), PIL_Image.ANTIALIAS)

        return image_copy