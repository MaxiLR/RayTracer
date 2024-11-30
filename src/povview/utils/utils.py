import gi
import time
import logging
from functools import wraps
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.INFO, format="[%(levelname)s][%(name)s] %(message)s")
logger = logging.getLogger(__name__)


def timer(func):
    """
    Decorator that measures the execution time of a function with high precision.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with timing functionality.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # High-resolution timer
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        logger.info(
            f"Function '{func.__name__}' executed in {elapsed_time:.6f} seconds."
        )
        return result

    return wrapper


def plot_points(points):
    x = [point.x for point in points]
    y = [point.y for point in points]
    z = [point.z for point in points]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(x, y, z)

    ax.set_box_aspect([1, 1, 1])

    max_range = max(max(x) - min(x), max(y) - min(y))
    mid_x = (max(x) + min(x)) / 2
    mid_y = (max(y) + min(y)) / 2

    ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
    ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)

    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_zlabel("Z Label")

    ax.set_title("3D Scatter Plot")

    plt.show()


def plot_vectors_3d(
    origins,
    vectors,
    colors=None,
    length=1.0,
    arrow_length_ratio=0.1,
    title="3D Vector Plot",
):
    origins = np.array(origins)
    vectors = np.array(vectors)

    if origins.shape != vectors.shape:
        raise ValueError(
            f"Origins and vectors must have the same shape. "
            f"Got origins shape {origins.shape} and vectors shape {vectors.shape}."
        )

    if origins.shape[1] != 3:
        raise ValueError(
            f"Each origin and vector must have exactly 3 components (x, y, z). "
            f"Got shape {origins.shape}."
        )

    num_vectors = origins.shape[0]

    if colors is None:
        colors = plt.cm.rainbow(np.linspace(0, 1, num_vectors))
    else:
        if len(colors) != num_vectors:
            raise ValueError(
                f"The number of colors ({len(colors)}) must match the number of vectors ({num_vectors})."
            )

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.quiver(
        origins[:, 0],
        origins[:, 1],
        origins[:, 2],
        vectors[:, 0],
        vectors[:, 1],
        vectors[:, 2],
        length=length,
        normalize=False,
        colors=colors,
        arrow_length_ratio=arrow_length_ratio,
    )

    unique_origins = np.unique(origins, axis=0)
    ax.scatter(
        unique_origins[:, 0],
        unique_origins[:, 1],
        unique_origins[:, 2],
        color="k",
        s=50,
        label="Origin",
    )

    all_points = origins + vectors * length
    max_limit = np.max(all_points)
    min_limit = np.min(origins)

    ax.set_xlim([min_limit, max_limit])
    ax.set_ylim([min_limit, max_limit])
    ax.set_zlim([min_limit, max_limit])

    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_zlabel("Z-axis")

    ax.set_title(title)

    ax.grid(True)

    ax.legend()

    plt.show()


def setup_goocanvas():
    """
    Sets up the GooCanvas library version.
    """
    try:
        gi.require_version("GooCanvas", "3.0")
    except ValueError:
        try:
            gi.require_version("GooCanvas", "2.0")
        except ValueError:
            raise ImportError("No se encontró ninguna versión compatible de GooCanvas.")
