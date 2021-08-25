from PIL import Image as PIL_Image
from PIL import ImageTk
import numpy as np


class Costume:
    __slots__ = ("image", "temp_image", "width", "height", "tkimage", "photoimage", "initialised", "canvas")

    def __init__(self, size=None):
        self.canvas = None
        if size is not None:
            image = PIL_Image.new("RGBA", size)
            self.init_image(image)
        else:
            self.initialised = False
        # Just for reference
        self.tkimage = None
        self.photoimage = None

    def init_image(self, image):
        self.image = image
        self.temp_image = image
        self.width, self.height = image.size
        self.initialised = True

    def destroy(self):
        del self.image
        del self.photoimage

    def get_details(self):
        if self.width == self.height == 0:
            bbox = (0, 0, 0, 0)
        else:
            image = np.array(self.temp_image)
            transparent = (0, 0, 0, 0)
            xs = []
            ys = []
            for x in range(self.width):
                for y in range(self.height):
                    colour = tuple(image[x, y])
                    if colour != transparent:
                        xs.append(x)
                        ys.append(y)
            max_x = max(xs)
            max_y = max(ys)
            min_x = min(xs)
            min_y = min(ys)
            bbox = (min_x, min_y, max_x, max_y)
        return {"bbox": bbox}

    @classmethod
    def from_pil(cls, pil_image):
        img = Costume()
        img.init_image(pil_image)
        return img

    @classmethod
    def open(cls, filename):
        return Costume.from_pil(PIL_Image.open(filename))

    @classmethod
    def from_file(cls, filename):
        return Costume.open(filename)

    def set_canvas(self, canvas):
        self.canvas = canvas

    def __del__(self):
        del self.photoimage

    def remove(self):
        # Deletes the sprite from the screen
        if self.canvas is not None:
            self.canvas.delete(self.tkimage)
        self.tkimage = None

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def draw(self, position, rotation=0, scale=1):
        assert self.canvas is not None, "This image doesn't have a canvas."

        self._update(rotation, scale)
        if self.tkimage is not None:
            self.canvas.delete(self.tkimage)
        self.photoimage = ImageTk.PhotoImage(self.temp_image)
        self.tkimage = self.canvas.create_image(position, image=self.photoimage)

    def _update(self, rotation, scale):
        # Rotate the image
        self.temp_image = self.image.rotate(rotation) # If rotation is 0, it will only copy the image :D

        # Resize image
        if scale != 1:
            self.temp_image.resize((self.width*scale, self.height*scale), PIL_Image.ANTIALIAS)