# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
from timeit import timeit
from scipy.cluster.vq import kmeans

def getImage(imageDir):
    if not os.path.exists(imageDir):
        os.mkdir(imageDir)
        return []
    files = os.listdir(imageDir)
    images = []
    for file in files:
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            with open(filePath, "rb") as f:
                img = Image.open(f)
                images.append(img)
                img.load()
        except:
            print("[-] Invalid image: {filePath}")
    return images

def getAverageRGB(image):
    img = np.array(image)
    
    w, h, d = img.shape
    img = img.reshape(w*h, d)

    '''
    def foo1():
        return kmeans(img.astype(float), 1)[0][0]

    def foo2():
        return np.average(img, axis=0)

    print(timeit(stmt=foo1, number=100))
    print(timeit(stmt=foo2, number=100))

    ---
    output:
    1.9172285870008636
    0.035429636016488075

    kmeans spend way more time...
    '''
    return tuple(np.average(img, axis=0))

def splitImage(image, size):
    W, H, *args = image.size
    m, n = size
    w, h = W//n, H//m
    imgs = []
    for j in range(m):
        for i in range(n):
            imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
    return imgs

def createImageGrid(images, dims, padding=10):
    m, n = dims
    assert m*n == len(images)
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])
    grid_img = Image.new('RGB', (n*(width+padding)+padding, m*(height+padding)+padding))

    for index in range(len(images)):
        row = index//n
        col = index%n
        grid_img.paste(images[index], (col*(width+padding)+padding, row*(height+padding)+padding))
    return grid_img
