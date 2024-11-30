from numbers import Number

#  ____   ____ ____
# |  _ \ / ___| __ )
# | |_) | |  _|  _ \
# |  _ <| |_| | |_) |
# |_| \_\\____|____/
#


class RGB:
    def __init__(self, r, g=None, b=None):
        if isinstance(r, list) or isinstance(r, tuple):
            self._rgb = r
        elif (g is None) and (b is None):
            self._rgb = [r, r, r]
        else:
            self._rgb = [r, g, b]

    def __str__(self):
        return f"RGB({self._rgb[0]}, {self._rgb[1]}, {self._rgb[2]})"

    def __repr__(self):
        return self.__str__()

    def limit(self):
        self._rgb = [min(max(c, 0), 1) for c in self._rgb]
        return self

    def __eq__(self, c2):
        return self._rgb == c2.rgb

    def __add__(self, c2):
        if isinstance(c2, Number):
            return RGB(self._rgb[0] + c2, self._rgb[1] + c2, self._rgb[2] + c2)
        else:
            return RGB(self._rgb[0] + c2.r, self._rgb[1] + c2.g, self._rgb[2] + c2.b)

    def __sub__(self, c2):
        if isinstance(c2, Number):
            return RGB(self._rgb[0] - c2, self._rgb[1] - c2, self._rgb[2] - c2)
        else:
            return RGB(self._rgb[0] - c2.r, self._rgb[1] - c2.g, self._rgb[2] - c2.b)

    def __mul__(self, f):
        if isinstance(f, Number):
            return RGB(self._rgb[0] * f, self._rgb[1] * f, self._rgb[2] * f)
        else:
            return RGB(self._rgb[0] * f.r, self._rgb[1] * f.g, self._rgb[2] * f.b)

    def __rmul__(self, f):
        if isinstance(f, Number):
            return RGB(f * self._rgb[0], f * self._rgb[1], f * self._rgb[2])
        else:
            return RGB(f.r * self._rgb[0], f.g * self._rgb[1], f.b * self._rgb[2])

    def __truediv__(self, f):
        if isinstance(f, Number):
            return RGB(self._rgb[0] / f, self._rgb[1] / f, self._rgb[2] / f)
        else:
            return RGB(self._rgb[0] / f.r, self._rgb[1] / f.g, self._rgb[2] / f.b)

    def __rtruediv__(self, f):
        if isinstance(f, Number):
            return RGB(f / self._rgb[0], f / self._rgb[1], f / self._rgb[2])
        else:
            return RGB(f.r / self._rgb[0], f.g / self._rgb[1], f.b / self._rgb[2])

    @property
    def r(self):
        return self._rgb[0]

    @property
    def g(self):
        return self._rgb[1]

    @property
    def b(self):
        return self._rgb[2]

    @property
    def rgb(self):
        return self._rgb

    def as_rgb8(self):
        return (
            int(self._rgb[0] * 255),
            int(self._rgb[1] * 255),
            int(self._rgb[2] * 255),
        )


#
#  ____   ____ ____    _
# |  _ \ / ___| __ )  / \
# | |_) | |  _|  _ \ / _ \
# |  _ <| |_| | |_) / ___ \
# |_| \_\\____|____/_/   \_\
#


class RGBA:
    def __init__(self, r, g=None, b=None, a=None):
        if isinstance(r, list) or isinstance(r, tuple):
            assert len(r) == 4
            assert g is None
            assert b is None
            assert a is None
            self._rgba = r
        else:
            assert g is not None
            assert b is not None
            assert a is not None
            self._rgba = [r, g, b, a]

    def __str__(self):
        return (
            f"RGBA({self._rgba[0]}, {self._rgba[1]}, {self._rgba[2]}, {self._rgba[3]})"
        )

    def __repr__(self):
        return self.__str__()

    def limit(self):
        self._rgba = [min(max(c, 0), 1) for c in self._rgba]
        return self

    def __add__(self, c2):
        for c in range(4):
            self._rgba[c] += c2._rgba[c]
        return self

    def __sub__(self, c2):
        for c in range(4):
            self._rgba[c] -= c2._rgba[c]
        return self

    def __mul__(self, f):
        for c in range(4):
            self._rgba[c] *= f
        return self

    @property
    def r(self):
        return self._rgba[0]

    @property
    def g(self):
        return self._rgba[1]

    @property
    def b(self):
        return self._rgba[2]

    @property
    def a(self):
        return self._rgba[3]

    @property
    def rgba(self):
        return self._rgba
