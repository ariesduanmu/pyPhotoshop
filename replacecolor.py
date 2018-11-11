# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from scipy.spatial.distance import cdist

def replace_corlor(image, original_corlor, modification, distance=10, output="new_test.jpg"):
    print("[*] START Replace Color")
    img = Image.open(image)
    data = np.asarray(img, dtype="int32")
    w,h,k = data.shape
    data = np.reshape(data, (w*h,k))
    distMatrix = cdist(data, np.array([original_corlor]))
    D = distMatrix<=distance
    D = np.reshape(D,w*h)
    data[:,:k][D] = modification(data[:,:k][D])
    data = np.reshape(data, (w,h,k))
    img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)
    print("[*] DONE Replace Color")

if __name__ == "__main__":
    def modification(color):
        return color + [50,0,0]
        # return [255,0,0]
    replace_corlor("test.jpg",(36,35,30),modification)

