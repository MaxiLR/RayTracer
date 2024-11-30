from math import cos, sin, pi

from povview.math.utils import handle_value
from povview.math.vector import Vec3
from povview.elements.objects.base import Object3D


class Cone(Object3D):
    def __init__(self, cone_data, **kwargs):
        self.top_center = Vec3(handle_value(cone_data["top_center"]))
        self.top_radius = cone_data["top_radius"]
        self.bottom_center = Vec3(handle_value(cone_data["bottom_center"]))
        self.bottom_radius = cone_data["bottom_radius"]

        super().__init__(cone_data, **kwargs)

    def __str__(self):
        return f"Cone(top_center: {self.top_center}, top_radius: {self.top_radius}, bottom_center: {self.bottom_center}, bottom_radius: {self.bottom_radius})"

    def __repr__(self):
        return self.__str__()

    def get_center(self):
        return (self.top_center + self.bottom_center) / 2

    def create_wireframe(self):
        # Vertices
        circ_sub = 2 * pi / self._subdiv

        for i in range(self._subdiv):
            self.vertices.append(
                Vec3(
                    self.bottom_center[0] + self.bottom_radius * cos(circ_sub * i),
                    self.bottom_center[1],
                    self.bottom_center[2] + self.bottom_radius * sin(circ_sub * i),
                )
            )
            self.vertices.append(
                Vec3(
                    self.top_center[0] + self.top_radius * cos(circ_sub * i),
                    self.top_center[1],
                    self.top_center[2] + self.top_radius * sin(circ_sub * i),
                )
            )

        # Edges
        for i in range(self._subdiv):
            self.edges.append((i * 2, i * 2 + 1))

        for i in range(self._subdiv - 1):
            self.edges.append((i * 2, i * 2 + 2))
            self.edges.append((i * 2 + 1, i * 2 + 3))
        self.edges.append((-1, 1))
        self.edges.append((-2, 0))

        # -- Triangulation
        for i in range(self._subdiv - 1):
            self.edges.append((i * 2, (i + 1) * 2 + 1))
        self.edges.append((-2, 1))
