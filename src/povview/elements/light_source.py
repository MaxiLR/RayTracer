from povview.math.color import RGB
from povview.math.vector import Vec3
from povview.math.tracing import BoundingBox
from povview.math.utils import handle_value
from povview.elements.objects.box import Box


class LightSource(Box):
    def __init__(self, light_data):
        self._subdiv = None
        self.location = Vec3(handle_value(light_data["location"]))
        self.color = RGB(
            light_data["color"]["r"], light_data["color"]["g"], light_data["color"]["b"]
        )

        self.corner1 = self.location
        self.corner2 = self.location

        self.create_wireframe()
        self.bounding_box = BoundingBox(self.vertices)
        
        self.faces = self.generate_faces()

    def __str__(self):
        return f"LightSource(position={self.location}, color={self.color})"

    def __repr__(self):
        return self.__str__()
