
import pathlib


class Setting:
    MAP_INIT = 'map_1'
    MODEL_INIT = 'car_v1'

    CWD = pathlib.Path(__file__).parent

    CAR_IMG_PATH = CWD / "data/car_img.png"
    MARKER_IMG_PATH = CWD / "data/marker_img.png"

    MARKER_SIZE = 16

    FRAME_FREQ = 5

    ACCELERATIOR_SENSITIVITY = 1
    BREAKS_SENSITIVITY = 1

    TIC = 1

