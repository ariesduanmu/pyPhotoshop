# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image

def edge(image_path, output, level=80, edge_color=[255,255,255], blackground_color=[0,0,0]):
    img = Image.open(image_path)
    data = np.asarray(img, dtype="int32")

    w, h, k = data.shape
    dirright_data = np.concatenate((data[:, 1:], data[:,-1:]), axis=1)
    dirdown_data = np.concatenate((data[1:,:], data[-1:,:]), axis=0)

    disRight = np.absolute(np.sum(data - dirright_data, axis=2))
    disDown = np.absolute(np.sum(data - dirdown_data, axis=2))

    level = min(max(1,level), 255)
    D_right = np.asarray(disRight<=level, dtype="int32")
    D_down = np.asarray(disDown<=level, dtype="int32")

    D = (D_right+D_down) > 1
    neg_D = (D_right+D_down) <= 1
    data[D] = edge_color
    data[neg_D] = blackground_color

    img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)

if __name__ == "__main__":
    edge("images/bob.png", "new_test.jpg")

