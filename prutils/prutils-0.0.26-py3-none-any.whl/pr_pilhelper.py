from PIL import Image


def get_im_size(im_path):
    im = Image.open(im_path).convert("RGBA")
    return im.size  # w, h
