def sign(num):
    num = float(num)
    return (num > 0) - (num < 0)


def handle_value(value) -> tuple:
    if isinstance(value, list) or isinstance(value, tuple):
        return tuple(value)
    elif isinstance(value, dict):
        return (value["x"], value["y"], value["z"])
    else:
        return (value, value, value)
