import numpy as np
from math import cos, pi, sin, sqrt
from sympy import symbols, Eq, solve, re, im, N

from povview.math.vector import Vec3
from povview.elements.objects.base import Object3D


class Ovus(Object3D):
    def __init__(self, ovus_data, **kwargs):
        self.base_point = Vec3(0, 0, 0)
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

    def get_center(self):
        return self.base_point + Vec3(0, max(self.bottom_radius, self.top_radius), 0)

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
                        y,
                        self.base_point[2] + radius * sin(circ_sub * j),
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
