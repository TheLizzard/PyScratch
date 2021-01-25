from math import sqrt


class Vector:
    def __init__(self, *args):
        self.data = args

    def __repr__(self) -> str:
        return "Vector(%s)" % (", ".join(map(str, self.data)))

    def __str__(self) -> str:
        return "Vector(%s)" % (", ".join(map(str, self.data)))

    def __len__(self) -> int:
        """
        Returns the length of the Vector
        """
        return len(self.data)

    def __abs__(self) -> int:
        """
        Returns the magnitude of self
        """
        return sqrt(self.dot(self))

    def __getitem__(self, idx: int) -> float:
        assert isinstance(idx, int), "The idx must be an int."
        """
        Idexes self
        """
        return self.data[idx]

    def __eq__(self, other) -> bool:
        assert isinstance(other, Vector), "Other must be a Vector."
        return not (False in (self.data[i] == other[i] for i in range(len(self))))

    def __add__(self, other):
        assert isinstance(other, Vector), "Other must be a Vector."
        assert len(self) == len(other), "Vectors must have same sizes."
        """
        Adds self to the other vector and returns the result
        """
        return Vector(*map(sum, zip(self, other)))

    def __mul__(self, other: int):
        assert isinstance(other, int), "Other must be an int."
        """
        Multiplies self by the integer and returns the result
        """
        return Vector(*(i*other for i in self.data))

    def __rmul__(self, other: int):
        assert isinstance(other, int), "Other must be an int."
        """
        Multiplies self by the integer and returns the result
        """
        return Vector(*(i*other for i in self.data))

    def __truediv__(self, other: int):
        assert isinstance(other, int), "Other must be an int."
        """
        Divides self by the integer and returns the result
        """
        return Vector(*(i/other for i in self.data))

    def add(self, other):
        """
        Adds self to the other vector and returns the result
        """
        return self+other

    def direction(self):
        """
        Returns the direction of self
        """
        return self/abs(self)

    def dot(self, other) -> int:
        assert isinstance(other, Vector), "Other must be a Vector."
        assert len(self) == len(other), "Vectors must have same sizes."
        """
        Calculates and returns the dot product of self and the other vector
        """
        return sum(self.data[i]*other[i] for i in range(len(self)))