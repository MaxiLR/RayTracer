import numpy as np

from povview.math.utils import sign
from povview.math.vector import Vec3

#  ____
# |  _ \ __ _ _   _
# | |_) / _` | | | |
# |  _ < (_| | |_| |
# |_| \_\__,_|\__, |
#             |___/


class Ray:
    def __init__(self, origin, direction):
        assert isinstance(origin, Vec3)
        assert isinstance(direction, Vec3)

        self.origin = origin
        self.direction = direction.normalized()

    def __str__(self):
        return f"Ray(origin: {self.origin}, direction: {self.direction})"

    def __repr__(self):
        return self.__str__()

    def at(self, t):
        return self.origin + self.direction * t


#   _    _ _ _
#  | |  | (_) |
#  | |__| |_| |_
#  |  __  | | __|
#  | |  | | | |_
#  |_|  |_|_|\__|


class Hit:
    def __init__(self, obj, t, normal):
        self.obj, self.t, self.normal = obj, t, normal

    def __str__(self):
        return f"Hit(obj: {self.obj}, t: {self.t})"

    def __repr__(self):
        return self.__str__()


#   _    _ _ _   _      _     _
#  | |  | (_) | | |    (_)   | |
#  | |__| |_| |_| |     _ ___| |_
#  |  __  | | __| |    | / __| __|
#  | |  | | | |_| |____| \__ \ |_
#  |_|  |_|_|\__|______|_|___/\__|


class HitList:
    def __init__(self):
        self.clear()

    def __str__(self):
        return f"HitList[{', '.join(str(hit) for hit in self.hits)}]"

    def __repr__(self):
        return self.__str__()

    def append(self, hit):
        self.hits.append(hit)

    def extend(self, hitlist):
        self.hits.extend(hitlist.hits)

    def empty(self):
        return self.hits == []

    def nearest_hit(self):
        return min(self.hits, key=lambda x: x.t)

    def clear(self):
        self.hits = []


#   _______   _                   _
#  |__   __| (_)                 | |
#     | |_ __ _  __ _ _ __   __ _| | ___
#     | | '__| |/ _` | '_ \ / _` | |/ _ \
#     | | |  | | (_| | | | | (_| | |  __/
#     |_|_|  |_|\__,_|_| |_|\__, |_|\___|
#                            __/ |
#                           |___/


class Triangle:
    def __init__(self, new_a, new_b=None, new_c=None):
        if isinstance(new_a, Triangle):
            assert new_b == None
            assert new_c == None

            self._a, self._b, self._c = new_a._a, new_a._b, new_a._c

        elif isinstance(new_a, list) or isinstance(new_a, tuple):
            assert len(new_a) == 3
            assert new_b == None
            assert new_c == None

            self._a, self._b, self._c = new_a[0], new_a[1], new_a[2]

        else:
            assert new_b != None
            assert new_c != None

            self._a, self._b, self._c = new_a, new_b, new_c

        self._normal = (self._b - self._a).cross(self._c - self._a).normalized()

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c(self):
        return self._c

    @property
    def normal(self):
        return self._normal

    @property
    def centroid(self):
        return (self._a + self._b + self._c) / 3

    def __str__(self):
        return f"Triangle(a: {self._a}, b: {self._b}, c: {self._c})"

    def __repr__(self):
        return self.__str__()

    def intersection(self, ray: Ray):
        edge1 = self._b - self._a
        edge2 = self._c - self._a
        h = ray.direction.cross(edge2)
        a = edge1.dot(h)

        if -1e-5 < a < 1e-5:  # Rayo paralelo al triángulo
            return None

        f = 1 / a
        s = ray.origin - self._a
        u = f * s.dot(h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.cross(edge1)
        v = f * ray.direction.dot(q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * edge2.dot(q)
        if t > 1e-5:
            return t
        return None


#  ____                        _ _             ____
# | __ )  ___  _   _ _ __   __| (_)_ __   __ _| __ )  _____  __
# |  _ \ / _ \| | | | '_ \ / _` | | '_ \ / _` |  _ \ / _ \ \/ /
# | |_) | (_) | |_| | | | | (_| | | | | | (_| | |_) | (_) >  <
# |____/ \___/ \__,_|_| |_|\__,_|_|_| |_|\__, |____/ \___/_/\_\
#                                        |___/


class BoundingBox:
    def __init__(self, vertices=None):
        self.min = Vec3(np.array([np.inf, np.inf, np.inf]))
        self.max = Vec3(np.array([-np.inf, -np.inf, -np.inf]))

        if vertices:
            for vertex in vertices:
                self.update(vertex)

    def update(self, vertex):
        self.min = Vec3.min(self.min, vertex)
        self.max = Vec3.max(self.max, vertex)

    @property
    def centre(self):
        return (self.min + self.max) / 2

    def intersection(self, ray: Ray) -> bool:
        t_min = (
            (self.min[0] - ray.origin[0]) / ray.direction[0]
            if ray.direction[0] != 0
            else float("-inf")
        )
        t_max = (
            (self.max[0] - ray.origin[0]) / ray.direction[0]
            if ray.direction[0] != 0
            else float("inf")
        )
        if t_min > t_max:
            t_min, t_max = t_max, t_min

        ty_min = (
            (self.min[1] - ray.origin[1]) / ray.direction[1]
            if ray.direction[1] != 0
            else float("-inf")
        )
        ty_max = (
            (self.max[1] - ray.origin[1]) / ray.direction[1]
            if ray.direction[1] != 0
            else float("inf")
        )
        if ty_min > ty_max:
            ty_min, ty_max = ty_max, ty_min

        # Check for overlap between X and Y intervals
        if (t_min > ty_max) or (ty_min > t_max):
            return False

        # Combine intervals
        t_min = max(t_min, ty_min)
        t_max = min(t_max, ty_max)

        tz_min = (
            (self.min[2] - ray.origin[2]) / ray.direction[2]
            if ray.direction[2] != 0
            else float("-inf")
        )
        tz_max = (
            (self.max[2] - ray.origin[2]) / ray.direction[2]
            if ray.direction[2] != 0
            else float("inf")
        )
        if tz_min > tz_max:
            tz_min, tz_max = tz_max, tz_min

        # Check for overlap between X, Y, and Z intervals
        if (t_min > tz_max) or (tz_min > t_max):
            return False

        return True
