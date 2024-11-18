import gi

gi.require_version("Gtk", "3.0")
from povview_utils import setup_goocanvas

setup_goocanvas()
from gi.repository import GooCanvas
from sympy import symbols, Eq, solve, re, im, N
import numpy as np
from functools import lru_cache

from math import cos, sin, pi, sqrt, radians
from povview_math import Vec3, Ray, Triangle, Hit, HitList, RGB
from povview_utils import timer

LINE_COLOR = "darkgrey"


class Object3D:
    def __init__(
        self,
        data,
        subdiv=10,
    ):
        self._subdiv = subdiv
        self.svg_scale = 50
        self.modifiers = data["object_modifiers"]

        self.vertices = []
        self.edges = []

        self.color = None

        self.build()

    def build(self):
        self.create_wireframe()
        self.apply_modifiers()

        self.bounding_box = BoundingBox(self.vertices)

        self.faces = self.generate_faces()

    def set_subdiv(self, subdiv):
        self._subdiv = subdiv

    def set_params(self, subdiv):
        if subdiv == self._subdiv:
            return

        self.set_subdiv(subdiv)

        self.vertices.clear()
        self.edges.clear()

        self.build()

    def create_wireframe(self):
        return

    def intersection(self, ray: Ray):
        hitlist = HitList()

        if not self.bounding_box.intersection(ray):
            return hitlist

        for face in self.faces:
            face = Triangle(
                self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]]
            )

            t = face.intersection(ray)
            if not t:
                continue

            hitlist.append(Hit(self, t))

        return hitlist

    def handle_value(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            return value
        elif isinstance(value, dict):
            return (value["x"], value["y"], value["z"])
        else:
            return (value, value, value)

    def apply_rotation(self, angle_vector: tuple[float]):
        angle_vector = [radians(angle) for angle in angle_vector]
        x_rotation_matrix = np.array(
            [
                [1, 0, 0],
                [0, cos(angle_vector[0]), -sin(angle_vector[0])],
                [0, sin(angle_vector[0]), cos(angle_vector[0])],
            ]
        )
        y_rotation_matrix = np.array(
            [
                [cos(angle_vector[1]), 0, sin(angle_vector[1])],
                [0, 1, 0],
                [-sin(angle_vector[1]), 0, cos(angle_vector[1])],
            ]
        )
        z_rotation_matrix = np.array(
            [
                [cos(angle_vector[2]), -sin(angle_vector[2]), 0],
                [sin(angle_vector[2]), cos(angle_vector[2]), 0],
                [0, 0, 1],
            ]
        )
        rotation_matrix = np.matmul(
            np.matmul(x_rotation_matrix, y_rotation_matrix), z_rotation_matrix
        )

        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = Vec3(np.matmul(rotation_matrix, vertex.__array__))

    def apply_translation(self, translation_vector: tuple[float]):
        translation_matrix = np.array(
            [
                [1, 0, 0, translation_vector[0]],
                [0, 1, 0, translation_vector[1]],
                [0, 0, 1, translation_vector[2]],
                [0, 0, 0, 1],
            ]
        )

        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = Vec3(
                np.delete(
                    np.matmul(translation_matrix, np.append(vertex.__array__, 1)), -1
                )
            )

    def apply_scale(self, scale_vector: tuple[float]):
        scale_matrix = np.array(
            [
                [scale_vector[0], 0, 0],
                [0, scale_vector[1], 0],
                [0, 0, scale_vector[2]],
            ]
        )

        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = Vec3(np.matmul(scale_matrix, vertex.__array__))

    def apply_pigment(self, color):
        self.color = RGB(color["r"], color["g"], color["b"])

    def apply_modifiers(self):
        if not self.modifiers:
            return

        for modifier in self.modifiers:
            match modifier["type"]:
                case "translate":
                    self.apply_translation(self.handle_value(modifier["value"]))
                case "rotate":
                    self.apply_rotation(self.handle_value(modifier["value"]))
                case "scale":
                    self.apply_scale(self.handle_value(modifier["value"]))
                case "pigment":
                    self.apply_pigment(modifier["color"])
                case _:
                    raise ValueError("Invalid modifier type")

    # TODO: Slow function, try adding a Cache
    @timer
    def generate_faces(self):
        from collections import defaultdict

        vertex_to_edges = defaultdict(list)

        for i, (v1, v2) in enumerate(self.edges):
            vertex_to_edges[v1].append(i)
            vertex_to_edges[v2].append(i)

        faces = []

        for edge1_idx, (v1, v2) in enumerate(self.edges):
            connected_edges = set(vertex_to_edges[v1] + vertex_to_edges[v2])
            connected_edges.discard(edge1_idx)

            for edge2_idx in connected_edges:
                v3, v4 = self.edges[edge2_idx]

                shared_vertex = None
                for v in (v3, v4):
                    if v == v1 or v == v2:
                        shared_vertex = v
                        break

                if shared_vertex is None:
                    continue

                other_vertex1 = v1 if v2 == shared_vertex else v2
                other_vertex2 = v3 if v4 == shared_vertex else v4

                if (other_vertex1, other_vertex2) in self.edges or (
                    other_vertex2,
                    other_vertex1,
                ) in self.edges:
                    face = tuple(sorted([shared_vertex, other_vertex1, other_vertex2]))
                    if face not in faces:
                        faces.append(face)

        return faces

    def to_svg(self, view):
        svg = ""
        match view:
            case "xy":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][0]*self.svg_scale:g},{self.vertices[edge[0]][1]*self.svg_scale:g} L{self.vertices[edge[1]][0]*self.svg_scale:g},{self.vertices[edge[1]][1]*self.svg_scale:g} "

            case "zy":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][2]*self.svg_scale:g},{self.vertices[edge[0]][1]*self.svg_scale:g} L{self.vertices[edge[1]][2]*self.svg_scale:g},{self.vertices[edge[1]][1]*self.svg_scale:g} "

            case "zx":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][2]*self.svg_scale:g},{self.vertices[edge[0]][0]*self.svg_scale:g} L{self.vertices[edge[1]][2]*self.svg_scale:g},{self.vertices[edge[1]][0]*self.svg_scale:g} "

            case _:
                raise ValueError("Invalid view")

        return svg.strip()

    def draw_on(self, views):
        for view in ["xy", "zy", "zx"]:
            root = views[view]["canvas"].get_root_item()
            GooCanvas.CanvasPath(
                parent=root,
                data=self.to_svg(view),
                line_width=1,
                stroke_color=LINE_COLOR,
                fill_color=None,
            )


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


class Cone(Object3D):
    """
    tc      self.top_center     vec3    Cone top center
    tr      self.top_radius     float   Cone top radius
    bc      self.bottom_center     vec3    Cone bottom center
    br      self.bottom_radius     float   Cone bottom radius
    """

    def __init__(self, cone_data, **kwargs):
        self.top_center = self.handle_value(cone_data["top_center"])
        self.top_radius = cone_data["top_radius"]
        self.bottom_center = self.handle_value(cone_data["bottom_center"])
        self.bottom_radius = cone_data["bottom_radius"]

        super().__init__(cone_data, **kwargs)

    def __str__(self):
        return f"Cone(top_center: {self.top_center}, top_radius: {self.top_radius}, bottom_center: {self.bottom_center}, bottom_radius: {self.bottom_radius})"

    def __repr__(self):
        return self.__str__()

    def create_wireframe(self):
        # Vertices
        circ_sub = 2 * pi / self._subdiv

        for i in range(self._subdiv):
            self.vertices.append(
                Vec3(
                    self.bottom_center[0] + self.bottom_radius * cos(circ_sub * i),
                    -self.bottom_center[1],
                    self.bottom_center[2] + self.bottom_radius * sin(circ_sub * i),
                )
            )
            self.vertices.append(
                Vec3(
                    self.top_center[0] + self.top_radius * cos(circ_sub * i),
                    -self.top_center[1],
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


class Sphere(Object3D):
    def __init__(self, sphere_data, **kwargs):
        self.center = self.handle_value(sphere_data["center"])
        self.radius = sphere_data["radius"]

        super().__init__(sphere_data, **kwargs)

    def __str__(self):
        return f"Sphere(center: {self.center}, radius: {self.radius})"

    def __repr__(self):
        return self.__str__()

    def get_radius(self, initial_radius: float, relative_height: float):
        return sqrt(initial_radius**2 - relative_height**2)

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
                        -y,
                        self.center[2] + radius * sin(circ_sub * j),
                    )
                )

        bottom_point[1], top_point[1] = (
            -bottom_point[1],
            -top_point[1],
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


class Ovus(Object3D):
    def __init__(self, ovus_data, **kwargs):
        self.base_point = (0, 0, 0)
        self.bottom_radius = ovus_data["bottom_radius"]
        self.top_radius = ovus_data["top_radius"]

        self.is_sphere = not 0 < self.top_radius < 2 * self.bottom_radius

        if not self.is_sphere:
            self.bottom_interval, self.top_interval = self.get_intervals()

        super().__init__(ovus_data, **kwargs)

    def __str__(self):
        return (
            f"Ovus(bottom_radius: {self.bottom_radius}, top_radius: {self.top_radius})"
        )

    def __repr__(self):
        return self.__str__()

    def get_intersection(
        self, *, ctr1: tuple[float], r1: float, ctr2: tuple[float], r2: float
    ):
        x, y = symbols("x y")

        x1, y1, r1 = ctr1[0], ctr1[1], r1
        x2, y2, r2 = ctr2[0], ctr2[1], r2

        circle1 = Eq((x - x1) ** 2 + (y - y1) ** 2, r1**2)
        circle2 = Eq((x - x2) ** 2 + (y - y2) ** 2, r2**2)

        solutions = solve((circle1, circle2), (x, y))
        if any(
            [im(solution[0]) != 0 or im(solution[1]) != 0 for solution in solutions]
        ):
            solutions = [(re(solutions[0][0]), re(solutions[0][1]))]

        solutions = np.array(
            [(float(N(solution[0])), float(N(solution[1]))) for solution in solutions]
        )

        return solutions

    def get_intervals(self):
        self.bottom_center = (self.base_point[0], self.base_point[1])
        self.top_center = (self.base_point[0], self.base_point[1] + self.bottom_radius)
        self.join_curve_centers = self.get_intersection(
            ctr1=self.top_center,
            r1=self.bottom_radius,
            ctr2=self.bottom_center,
            r2=self.top_radius,
        )

        A = self.get_intersection(
            ctr1=self.join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.bottom_center,
            r2=self.bottom_radius,
        )[0]
        B = self.get_intersection(
            ctr1=self.join_curve_centers[1],
            r1=self.bottom_radius + self.top_radius,
            ctr2=self.top_center,
            r2=self.top_radius,
        )[0]

        return A[1], B[1]

    def get_radius(self, initial_radius: float, relative_height: float):
        return sqrt(initial_radius**2 - relative_height**2)

    def get_ovus_radius(self, y: float):
        if y < self.bottom_interval:
            return self.get_radius(self.bottom_radius, y - self.bottom_center[1])
        elif y < self.top_interval:
            return self.get_radius(
                self.bottom_radius + self.top_radius, y - self.join_curve_centers[1][1]
            ) - (self.join_curve_centers[1][0] - self.base_point[0])
        else:
            return self.get_radius(self.top_radius, y - self.top_center[1])

    def create_wireframe(self):
        # Vertices
        circ_sub = 2 * pi / self._subdiv

        if self.is_sphere:
            sphere_radius = max(self.bottom_radius, self.top_radius)

        bottom_point = [
            self.base_point[0],
            (
                self.base_point[1] - self.bottom_radius
                if not self.is_sphere
                else self.base_point[1] - sphere_radius
            ),
            self.base_point[2],
        ]
        top_point = [
            self.base_point[0],
            (
                self.base_point[1] + self.bottom_radius + self.top_radius
                if not self.is_sphere
                else self.base_point[1] + sphere_radius
            ),
            self.base_point[2],
        ]

        for i in range(1, self._subdiv):
            y = (abs(top_point[1] - bottom_point[1]) / self._subdiv) * i + bottom_point[
                1
            ]
            radius = (
                self.get_ovus_radius(y)
                if not self.is_sphere
                else self.get_radius(sphere_radius, y - self.base_point[1])
            )

            for j in range(self._subdiv):
                self.vertices.append(
                    Vec3(
                        self.base_point[0] + radius * cos(circ_sub * j),
                        -y,
                        self.base_point[2] + radius * sin(circ_sub * j),
                    )
                )

        bottom_point[1], top_point[1] = (
            -bottom_point[1],
            -top_point[1],
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
