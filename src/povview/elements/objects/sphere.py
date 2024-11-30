from math import cos, pi, sin, sqrt
from numbers import Number

from povview.math.utils import handle_value
from povview.math.vector import Vec3
from povview.math.tracing import Hit, HitList
from povview.elements.objects.base import Object3D


class Sphere(Object3D):
    def __init__(self, sphere_data, **kwargs):
        self.center = Vec3(handle_value(sphere_data["center"]))
        self.radius = sphere_data["radius"]

        super().__init__(sphere_data, **kwargs)

    def __str__(self):
        return f"Sphere(center: {self.center}, radius: {self.radius})"

    def __repr__(self):
        return self.__str__()

    def get_center(self):
        return self.center

    def get_radius(self, initial_radius: float, relative_height: float):
        return sqrt(initial_radius**2 - relative_height**2)

    def apply_scale(self, scale_vector):
        super().apply_scale(scale_vector)

        if isinstance(scale_vector, tuple):
            self.radius *= scale_vector[0]
        elif isinstance(scale_vector, Number):
            self.radius *= scale_vector
        else:
            raise TypeError("scale_vector must be Vec3 or Number")

    def intersection(self, ray):
        hitlist = HitList()

        b = ray.direction.dot(ray.origin - self.center) * 2
        c = abs(ray.origin - self.center) ** 2 - self.radius**2

        if b**2 < 4 * c:
            return hitlist
        elif b**2 == 4 * c:
            t = -b / 2
            normal = ((ray.origin + ray.direction * t) - self.center).normalized()
            hitlist.append(Hit(self, t, normal))
        else:
            t = (-b - sqrt(b**2 - 4 * c)) / 2
            normal = ((ray.origin + ray.direction * t) - self.center).normalized()
            hitlist.append(Hit(self, t, normal))
            t = (-b + sqrt(b**2 - 4 * c)) / 2
            normal = ((ray.origin + ray.direction * t) - self.center).normalized()
            hitlist.append(Hit(self, t, normal))

        return hitlist

    def create_wireframe(self):
        # Vertices
        circ_sub = 2 * pi / self._subdiv

        bottom_point = [
            self.center[0],
            self.center[1] - self.radius,
            self.center[2],
        ]
        top_point = [
            self.center[0],
            self.center[1] + self.radius,
            self.center[2],
        ]

        for i in range(1, self._subdiv):
            y = (abs(top_point[1] - bottom_point[1]) / self._subdiv) * i + bottom_point[
                1
            ]
            radius = self.get_radius(self.radius, y - self.center[1])

            for j in range(self._subdiv):
                self.vertices.append(
                    Vec3(
                        self.center[0] + radius * cos(circ_sub * j),
                        y,
                        self.center[2] + radius * sin(circ_sub * j),
                    )
                )

        self.vertices.insert(0, Vec3(bottom_point))
        self.vertices.append(Vec3(top_point))

        # Edges
        for i in range(self._subdiv):
            self.edges.append((0, (i + 1)))
            for j in range(self._subdiv - 2):
                self.edges.append(
                    ((i + 1) + j * self._subdiv, (i + 1) + (j + 1) * self._subdiv)
                )
            self.edges.append(((i + 1) + (j + 1) * self._subdiv, -1))

        for j in range(self._subdiv - 1):
            for i in range(self._subdiv - 1):
                self.edges.append((i + 1 + j * self._subdiv, i + 2 + j * self._subdiv))
            self.edges.append(((j + 1) * self._subdiv, 1 + j * self._subdiv))

        # -- Triangulation
        for j in range(self._subdiv - 2):
            for i in range(self._subdiv - 1):
                self.edges.append(
                    ((i + 1) + j * self._subdiv, (i + 2) + (j + 1) * self._subdiv)
                )
            self.edges.append(((i + 2) + j * self._subdiv, 1 + (j + 1) * self._subdiv))
