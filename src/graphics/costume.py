from PIL import Image as PIL_Image
from PIL import ImageTk


class Costume:
    __slots__ = ("image", "temp_image", "width", "height", "tkimage", "photoimage", "initialised", "canvas")

    def __init__(self, size=None):
        self.canvas = None
        if size is not None:
            self.image = PIL_Image.new("RGBA", size)
            self.width, self.height = self.image.size
            self.initialised = True
        else:
            self.initialised = False
        # Just for reference
        self.tkimage = None
        self.photoimage = None

    def destroy(self):
        del self.image
        del self.photoimage

    def get_details(self):
        return {"bbox": ("x1", "y1", "x2", "y2")}
        im = np.array(self.temp_image)
        transparent = [0, 0, 0, 0]
        xs, ys = np.where(np.all(im != transparent, axis=2))

    @classmethod
    def from_pil(cls, pil_image):
        img = Costume()
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

    def remove(self):
        # Deletes the sprite from the screen
        # but can be restored with `Costume.show()`
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