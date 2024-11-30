from povview.parser import Parser
from povview.tracer import Tracer


def main(args):
    parsed_file = Parser().parse(args[1])
    tracer = Tracer(
        parsed_file["lights"],
        parsed_file["cameras"][0],
        parsed_file["objects"],
        (1920, 1080),
        model="ray_tracer" if not int(args[2]) else "path_tracer",
    )
    tracer.trace_scene()
    tracer.to_png(f"{tracer.model}.png")


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
