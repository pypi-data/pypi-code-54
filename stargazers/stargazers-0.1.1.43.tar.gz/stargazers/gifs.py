import cv2
import numpy as np


from PIL import Image


def make_gif(path, frames, *, duration=1000/30):
    gframes = [Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) for f in frames]
    gif = gframes[0]
    gif.save(
        path,
        save_all=True,
        append_images=gframes[1:],
        duration=duration,
        loop=loop
    )
    pass
