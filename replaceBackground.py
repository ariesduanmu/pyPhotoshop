# -*- coding: utf-8 -*-
'''Three pictures needed
1. picture need to change background
2. background of picture 1
3. background to be changed
'''
import numpy as np
from PIL import Image

def replace_background(original_pic, background_pic, replace_pic, output, level=50):
    original_img = Image.open(original_pic)
    background_img = Image.open(background_pic)
    replace_img = Image.open(replace_pic)

    original_data = np.asarray(original_img, dtype="int32")
    background_data = np.asarray(background_img, dtype="int32")
    replace_data = np.asarray(replace_img, dtype="int32")

    distanceMatrix = np.sum(np.absolute(original_data - background_data), axis=2)
    D = distanceMatrix < level
    original_data[D] = replace_data[D]

    img = Image.fromarray(np.asarray(np.clip(original_data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)

if __name__ == "__main__":
    replace_background("original_pic.jpg", "background_pic.jpg", "replace_pic.jpg", "new.jpg")
