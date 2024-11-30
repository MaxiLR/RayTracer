from povview.math.utils import handle_value
from povview.math.vector import Vec3
from povview.elements.objects.base import Object3D


class Box(Object3D):
    def __init__(self, box_data, **kwargs):
        self.corner1 = Vec3(handle_value(box_data["corner_1"]))
        self.corner2 = Vec3(handle_value(box_data["corner_2"]))

        super().__init__(box_data, **kwargs)

    def __str__(self):
        return f"Box(corner1: {self.corner1}, corner2: {self.corner2})"

    def __repr__(self):
        return self.__str__()

    def get_center(self):
        return (self.corner1 + self.corner2) / 2

    def create_wireframe(self):
        self.vertices = [
            Vec3(self.corner1[0], self.corner1[1], self.corner1[2]),
            Vec3(self.corner2[0], self.corner1[1], self.corner1[2]),
            Vec3(self.corner2[0], self.corner2[1], self.corner1[2]),
            Vec3(self.corner1[0], self.corner2[1], self.corner1[2]),
            Vec3(self.corner1[0], self.corner1[1], self.corner2[2]),
            Vec3(self.corner2[0], self.corner1[1], self.corner2[2]),
            Vec3(self.corner2[0], self.corner2[1], self.corner2[2]),
            Vec3(self.corner1[0], self.corner2[1], self.corner2[2]),
        ]
        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 2),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (4, 6),
            (0, 4),
            (4, 1),
            (1, 0),
            (1, 5),
            (5, 2),
            (2, 1),
            (2, 6),
            (6, 3),
            (3, 2),
            (3, 7),
            (7, 0),
            (0, 3),
        ]
