import pyparsing as pp
import json
import sys

from povview.elements.objects.box import Box
from povview.elements.objects.cone import Cone
from povview.elements.objects.sphere import Sphere
from povview.elements.objects.ovus import Ovus
from povview.elements.camera import Camera
from povview.elements.light_source import LightSource


class Parser:
    def __init__(self):
        include_line = pp.Suppress(pp.LineStart() + "#" + pp.restOfLine)

        comma = pp.Suppress(",")
        open_brace = pp.Suppress("{")
        close_brace = pp.Suppress("}")

        sign = pp.Optional(pp.oneOf("+ -"))

        uinteger = pp.Word("123456789", pp.nums) ^ "0"
        sinteger = pp.Combine(sign + uinteger)
        expon = pp.oneOf("e E") + sinteger

        ufloat = pp.Combine(
            uinteger + pp.Optional("." + pp.Word(pp.nums)) + pp.Optional(expon)
        )
        sfloat = pp.Combine(
            sinteger + pp.Optional("." + pp.Word(pp.nums)) + pp.Optional(expon)
        )

        uinteger.setParseAction(lambda t: int(t[0]))
        sinteger.setParseAction(lambda t: int(t[0]))
        ufloat.setParseAction(lambda t: float(t[0]))
        sfloat.setParseAction(lambda t: float(t[0]))

        vector3 = pp.Group(
            pp.Suppress("<")
            + sfloat("x")
            + comma
            + sfloat("y")
            + comma
            + sfloat("z")
            + pp.Suppress(">")
        )

        color_vector3 = (
            pp.Suppress("<")
            + sfloat("r")
            + comma
            + sfloat("g")
            + comma
            + sfloat("b")
            + pp.Suppress(">")
        )

        rgb_vector3 = pp.Group(
            pp.Suppress(pp.Keyword("color"))
            + pp.Suppress(pp.Keyword("rgb"))
            + color_vector3
        )

        light = (
            pp.Keyword("light_source")
            + open_brace
            + vector3("location")
            + comma
            + rgb_vector3("color")
            + close_brace
        ).setResultsName("lights", listAllMatches=True)
        light.set_parse_action(lambda t: LightSource(t.as_dict()))

        lights = light.setResultsName("lights", listAllMatches=True)

        camera = (
            pp.Keyword("camera")
            + open_brace
            + pp.Keyword("location")
            + vector3("location")
            + pp.Keyword("look_at")
            + vector3("look_at")
            + pp.Keyword("angle")
            + ufloat("angle")
            + close_brace
        )
        camera.set_parse_action(lambda t: Camera(t.as_dict()))

        cameras = camera.setResultsName("cameras", listAllMatches=True)

        pigment = pp.Group(
            pp.Keyword("pigment")("type")
            + open_brace
            + rgb_vector3("color")
            + close_brace
        )

        rotation = pp.Group(
            pp.Keyword("rotate")("type") + (vector3("value") | sfloat("value"))
        )

        translation = pp.Group(
            pp.Keyword("translate")("type") + (vector3("value") | sfloat("value"))
        )

        scale = pp.Group(
            pp.Keyword("scale")("type") + (vector3("value") | sfloat("value"))
        )

        object_modifiers = pp.Group(
            pp.ZeroOrMore(pigment | rotation | translation | scale)
        ).setResultsName("object_modifiers", listAllMatches=False)

        ovus_parser = (
            pp.Keyword("ovus")("type")
            + open_brace
            + ufloat("bottom_radius")
            + comma
            + ufloat("top_radius")
            + object_modifiers
            + close_brace
        )
        ovus_parser.set_parse_action(lambda t: Ovus(t.as_dict()))

        sphere_parser = (
            pp.Keyword("sphere")("type")
            + open_brace
            + vector3("center")
            + comma
            + ufloat("radius")
            + object_modifiers
            + close_brace
        )
        sphere_parser.set_parse_action(lambda t: Sphere(t.as_dict()))

        cone_parser = (
            pp.Keyword("cone")("type")
            + open_brace
            + vector3("bottom_center")
            + comma
            + ufloat("bottom_radius")
            + comma
            + vector3("top_center")
            + comma
            + ufloat("top_radius")
            + object_modifiers
            + close_brace
        )
        cone_parser.set_parse_action(lambda t: Cone(t.as_dict()))

        box_parser = (
            pp.Keyword("box")("type")
            + open_brace
            + vector3("corner_1")
            + comma
            + vector3("corner_2")
            + object_modifiers
            + close_brace
        )
        box_parser.set_parse_action(lambda t: Box(t.as_dict()))

        object_list = [ovus_parser, cone_parser, sphere_parser, box_parser]

        objects = (
            pp.Or(object_list)
            .add_parse_action(lambda t: t[0])
            .setResultsName("objects", listAllMatches=True)
        )

        element = lights | cameras | objects

        self.parser = pp.ZeroOrMore(include_line | element)

    def parse(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            file_contents = f.read()

        try:
            res = self.parser.parse_string(file_contents, parse_all=True)
        except pp.ParseException as pe:
            print("Parsing failed:", pe)
            sys.exit(1)

        result_dict = res.as_dict()

        return result_dict


def main(args):
    if len(args) < 2:
        print("Uso: python parser.py <archivo_entrada.pov>")
        return 1

    result = Parser().parse(args[1])

    try:
        print(json.dumps(result, indent=4))
    except:
        print(result)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
