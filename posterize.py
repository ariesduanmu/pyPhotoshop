# -*- coding: utf-8 -*-
import numpy as np
from pprint import pprint
from PIL import Image
from scipy.cluster.vq import kmeans, vq

'''modify color depends on light(gray) degree, can be used as heat map
'''

def sepearte_by_lights(gray_data, number=3):
    data = np.asarray(gray_data, dtype="float")
    w, h = data.shape
    data = np.reshape(data, w*h)
    centroids,_ = kmeans(data, number)
    idx,_ = vq(data, centroids)
    return idx

def posterize(image_path, modification, number, extra_colors, output):
    img = Image.open(image_path)
    gray = img.convert("L")
    data = np.asarray(img, dtype="int32")
    w, h, k = data.shape
    data = np.reshape(data, (w*h, k))
    gray_idx = sepearte_by_lights(gray, number)
    for i in range(number):
        data[gray_idx == i] = modification(data[gray_idx == i], extra_colors[i])
    data = np.reshape(data, (w, h, k))
    img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)


if __name__ == "__main__":
    def modification(data, extra_color):
        return data + extra_color
    number = 5
    extra_colors = [[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255]]
    posterize("test.jpg", modification, number, extra_colors, "new_test.jpg")


