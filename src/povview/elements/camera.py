from povview.math.vector import Vec3
from povview.math.utils import handle_value, sign


class Camera:
    def __init__(self, camera_data):
        self.location = Vec3(handle_value(camera_data["location"]))
        self.look_at = Vec3(handle_value(camera_data["look_at"]))

        self.forward = Vec3(self.look_at - self.location).normalized()

        global_up = Vec3(0, 1, 0)
        self.right = -self.forward.cross(global_up).normalized()
        if self.right == Vec3(0, 0, 0):
            global_up = Vec3(0, 0, 1)
            self.right = -self.forward.cross(global_up).normalized()

        up = self.forward.cross(self.right).normalized()
        self.up = up * -sign(up.dot(global_up))

        self.angle = camera_data["angle"]

    def __str__(self):
        return f"Camera(location={self.location}, look_at={self.look_at}, up={self.up})"

    def __repr__(self):
        return self.__str__()
