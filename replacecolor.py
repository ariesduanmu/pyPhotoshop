# -*- coding: utf-8 -*-
import argparse
import numpy as np
from PIL import Image
from scipy.spatial.distance import cdist

def replace_color(image, original_corlor, modification, area=None, distance=10, output="new_test.jpg"):
    print(f"[*] START Replace Color: {original_corlor}")
    img = Image.open(image)
    data = np.asarray(img, dtype="int32")
    w,h,k = data.shape
    data = np.reshape(data, (w*h,k))
    distMatrix = cdist(data, np.array([original_corlor]))
    dist = distance - distMatrix
    distRatio = (dist >= 0) * dist / distance
    D = distMatrix<=distance
    D = np.reshape(D,w*h)
    if area is None:
        data[D] = modification(data[:,:][D], distRatio[D])
    else:
        (c1, r1), (c2, r2) = area
        for i in range(r1, r2+1):
            l, r = i*h+c1, i*h+c2+1
            data[l:r,:][D[l:r]] = modification(data[l:r,:][D[l:r]], distRatio[l:r,:][D[l:r]])
    data = np.reshape(data, (w,h,k))
    img = Image.fromarray(np.asarray(np.clip(data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)
    print("[*] DONE Replace Color")

# TODO: change color to target color, predefined modification modes

def parse_options():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <filename>',
                                     description='Replace color Tool @Qin')
    parser.add_argument('filename', type=str, help='image file path')
    parser.add_argument('-c','--color', type=str, help='color need to be modified')
    parser.add_argument('-t','--target', type=str, help='target color to be')
    parser.add_argument('-r','--range', type=str, help='image pixel range to be changed')
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    def modification(color, ratio):
        return color * ratio.dot([[2,0,0]])
        # return [255,0,0]
    replace_color("test.jpg",(36,35,30), modification, ((0,0),(400,400)))
