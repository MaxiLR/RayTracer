import os
import pickle
import numpy as np
from math import cos, radians, sin
from collections import defaultdict

from povview.utils.utils import setup_goocanvas, timer

setup_goocanvas()
from gi.repository import GooCanvas

from povview.math.tracing import BoundingBox, Ray, Hit, HitList, Triangle
from povview.math.vector import Vec3
from povview.math.color import RGB
from povview.math.utils import handle_value
from povview.math.utils import sign


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
        self.center = self.get_center()

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

    def get_center(self):
        return None

    def create_wireframe(self):
        pass

    def intersection(self, ray: Ray):
        hitlist = HitList()

        if not self.bounding_box.intersection(ray):
            return hitlist

        for face in self.faces:
            face = Triangle(
                self.vertices[face[0]],
                self.vertices[face[1]],
                self.vertices[face[2]],
            )

            t = face.intersection(ray)
            if not t:
                continue

            normal = face.normal * -sign(face.normal.dot(ray.direction))
            hitlist.append(Hit(self, t, normal))

        return hitlist

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

        self.center = Vec3(np.matmul(rotation_matrix, self.center.__array__))

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

        self.center = Vec3(
            np.delete(
                np.matmul(translation_matrix, np.append(self.center.__array__, 1)), -1
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

        self.center = Vec3(np.matmul(scale_matrix, self.center.__array__))

    def apply_pigment(self, color):
        self.color = RGB(color["r"], color["g"], color["b"])

    def apply_modifiers(self):
        if not self.modifiers:
            return

        for modifier in self.modifiers:
            match modifier["type"]:
                case "translate":
                    self.apply_translation(handle_value(modifier["value"]))
                case "rotate":
                    self.apply_rotation(handle_value(modifier["value"]))
                case "scale":
                    self.apply_scale(handle_value(modifier["value"]))
                case "pigment":
                    self.apply_pigment(modifier["color"])
                case _:
                    raise ValueError("Invalid modifier type")

    def generate_faces(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        cache_filename = os.path.join(base_dir, "cache.pickle")

        if os.path.exists(cache_filename):
            with open(cache_filename, "rb") as f:
                cache = pickle.load(f)
        else:
            cache = {}

        key = (self.__class__.__name__, self._subdiv)

        if key in cache:
            return cache[key]

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

        cache[key] = faces

        with open(cache_filename, "wb") as f:
            pickle.dump(cache, f)

        return faces

    def to_svg(self, view):
        svg = ""
        match view:
            case "xy":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][0]*self.svg_scale:g},{-self.vertices[edge[0]][1]*self.svg_scale:g} L{self.vertices[edge[1]][0]*self.svg_scale:g},{-self.vertices[edge[1]][1]*self.svg_scale:g} "

            case "zy":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][2]*self.svg_scale:g},{-self.vertices[edge[0]][1]*self.svg_scale:g} L{self.vertices[edge[1]][2]*self.svg_scale:g},{-self.vertices[edge[1]][1]*self.svg_scale:g} "

            case "zx":
                for edge in self.edges:
                    svg += f"M{self.vertices[edge[0]][2]*self.svg_scale:g},{-self.vertices[edge[0]][0]*self.svg_scale:g} L{self.vertices[edge[1]][2]*self.svg_scale:g},{-self.vertices[edge[1]][0]*self.svg_scale:g} "

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
