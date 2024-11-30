import numpy as np
from numbers import Number
from math import cos, log, pi, sqrt
import random

from povview.math.utils import sign


# __     __        ____
# \ \   / /__  ___|___ \
#  \ \ / / _ \/ __| __) |
#   \ V /  __/ (__ / __/
#    \_/ \___|\___|_____|
#


class Vec2:
    def __init__(self, new_x, new_y=None):
        if isinstance(new_x, Vec2):
            assert new_y == None

            self._x, self._y = new_x._x, new_x._y

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
            assert len(new_x) == 2
            assert new_y == None

            self._x, self._y = new_x

        else:
            assert new_y != None
            self._x, self._y = new_x, new_y

    def __str__(self):
        return f"Vec2({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return [self._x, self._y][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case _:
                raise IndexError

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y])


# __     __        _____
# \ \   / /__  ___|___ /
#  \ \ / / _ \/ __| |_ \
#   \ V /  __/ (__ ___) |
#    \_/ \___|\___|____/
#


class Vec3:
    def __init__(self, new_x, new_y=None, new_z=None):
        if isinstance(new_x, Vec3):
            assert new_y == None
            assert new_z == None

            self._x, self._y, self._z = new_x._x, new_x._y, new_x._z

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
            assert len(new_x) == 3
            assert new_y == None
            assert new_z == None

            self._x, self._y, self._z = new_x[0], new_x[1], new_x[2]

        else:
            assert new_y != None
            assert new_z != None

            self._x, self._y, self._z = new_x, new_y, new_z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    def __str__(self):
        return f"Vec3({self._x}, {self._y}, {self._z})"

    def __repr__(self):
        return self.__str__()

    def __neg__(self):
        return Vec3(-self._x, -self._y, -self._z)

    def __getitem__(self, index):
        return [self._x, self._y, self._z][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case 2:
                self._z = value
            case _:
                raise IndexError

    def __eq__(self, v2):
        if v2:
            return self._x == v2._x and self._y == v2._y and self._z == v2._z
        else:
            return False

    def __abs__(self):
        return self.mag()

    def __sub__(self, v2):  # Operator overload (*)
        assert isinstance(v2, Vec3)
        return Vec3(self._x - v2._x, self._y - v2._y, self._z - v2._z)

    def __add__(self, v2):  # Operator overload (+)
        assert isinstance(v2, Vec3)
        return Vec3(self._x + v2._x, self._y + v2._y, self._z + v2._z)

    def __mul__(self, v2):  # Operator overload (* = dot)
        if isinstance(v2, Number):
            return Vec3(self._x * v2, self._y * v2, self._z * v2)
        else:
            return Vec3(self._x * v2._x, self._y * v2._y, self._z * v2._z)

    def __rmul__(self, v2):  # Operator overload (* = dot)
        if isinstance(v2, Number):
            return Vec3(v2 * self._x, v2 * self._y, v2 * self._z)
        else:
            return Vec3(v2._x * self._x, v2._y * self._y, v2._z * self._z)

    def __truediv__(self, v2):  # Operator overload (/)
        if isinstance(v2, Number):
            return Vec3(self._x / v2, self._y / v2, self._z / v2)
        else:
            return Vec3(self._x / v2._x, self._y / v2._y, self._z / v2._z)

    def __rtruediv__(self, v2):  # Operator overload (/)
        if isinstance(v2, Number):
            return Vec3(v2 / self._x, v2 / self._y, v2 / self._z)
        else:
            return Vec3(v2._x / self._x, v2._y / self._y, v2._z / self._z)

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y, self._z])

    def add(self, v2):
        assert isinstance(v2, Vec3)
        self._x += v2.x
        self._y += v2.y
        self._z += v2.z
        return self

    def sub(self, v2):
        assert isinstance(v2, Vec3)
        self._x -= v2.x
        self._y -= v2.y
        self._z -= v2.z
        return self

    def dot(self, v2):
        assert isinstance(v2, Vec3)
        return self._x * v2.x + self._y * v2.y + self._z * v2.z

    def cross(self, v2):
        assert isinstance(v2, Vec3)
        return Vec3(
            self._y * v2.z - self._z * v2.y,
            self._z * v2.x - self._x * v2.z,
            self._x * v2.y - self._y * v2.x,
        )

    def normalized(self):
        d = self.mag()
        if not d:
            return Vec3(0, 0, 0)
        return Vec3(self._x / d, self._y / d, self._z / d)

    def inverted(self):
        return Vec3(-self._x, -self._y, -self._z)

    def mag(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)

    def round(self, ndigits):
        return Vec3(
            round(self._x, ndigits), round(self._y, ndigits), round(self._z, ndigits)
        )

    @staticmethod
    def min(v1, v2):
        return Vec3(min(v1.x, v2.x), min(v1.y, v2.y), min(v1.z, v2.z))

    @staticmethod
    def max(v1, v2):
        return Vec3(max(v1.x, v2.x), max(v1.y, v2.y), max(v1.z, v2.z))

    @staticmethod
    def random_value_normal_distribution():
        theta = 2 * pi * random.random()
        rho = sqrt(-2 * log(random.random()))
        return rho * cos(theta)

    @staticmethod
    def random_direction():
        x = Vec3.random_value_normal_distribution()
        y = Vec3.random_value_normal_distribution()
        z = Vec3.random_value_normal_distribution()
        return Vec3(x, y, z).normalized()

    @staticmethod
    def random_hemisphere_direction(normal):
        direction = Vec3.random_direction()
        return direction * sign(direction.dot(normal))


# __     __        _  _
# \ \   / /__  ___| || |
#  \ \ / / _ \/ __| || |_
#   \ V /  __/ (__|__   _|
#    \_/ \___|\___|  |_|
#


class Vec4:
    def __init__(self, new_x, new_y=None, new_z=None, new_w=None):
        if isinstance(new_x, Vec4):
            assert (new_y == None) and (new_z == None) and (new_w == None)

            self._x, self._y, self._z, self._w = new_x._x, new_x._y, new_x._z, new_x.w

        elif (
            isinstance(new_x, list)
            or isinstance(new_x, tuple)
            or isinstance(new_x, np.ndarray)
        ):
            assert len(new_x) == 4
            assert (new_y == None) and (new_z == None) and (new_w == None)

            self._x, self._y, self._z, self._w = new_x

        else:
            assert (new_y != None) and (new_z != None) and (new_w != None)

            self._x, self._y, self._z, self._w = new_x, new_y, new_z, new_w

    def __str__(self):
        return f"Vec4({self._x}, {self._y}, {self._z}, {self._w})"

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, index):
        return [self._x, self._y, self._z, self._w][index]

    def __setitem__(self, index, value):
        match index:
            case 0:
                self._x = value
            case 1:
                self._y = value
            case 2:
                self._z = value
            case 3:
                self._w = value
            case _:
                raise IndexError

    @property
    def __array__(self) -> np.ndarray:
        return np.array([self._x, self._y, self._z, self._w])

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def w(self):
        return self._w
