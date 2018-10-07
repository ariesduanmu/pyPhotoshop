# -*- coding: utf-8 -*-
import os
import random
from PIL import Image

def genrateTile(size, folder):
    if not os.path.exists(folder):
        os.mkdir(os.path.abspath(folder))
    for i in range(256):
        r, g, b = random.choices(range(256),k=3)
        color = ((max(0,r-100),r), (max(0,g-100),g), (max(0,b-100),b))
        generateRandonPicture(size, color, folder, "{:03d}.jpg".format(i))

def generateRandonPicture(size, color_range, folder, output):
    img = Image.new("RGB", size)
    for color, i, j in randomColor(size, color_range):
        img.paste(color, [i,j,i+1,j+1])
    img.save(os.path.abspath(os.path.join(folder, output)))

def randomColor(size, color_range):
    r_range, g_range, b_range = color_range
    r_min, r_max = r_range
    g_min, g_max = g_range
    b_min, b_max = b_range
    for i in range(size[0]):
        for j in range(size[1]):
            color = (random.randint(r_min, r_max), random.randint(g_min, g_max), random.randint(b_min, b_max))
            yield color, i, j

def removeTile(folder):
    if os.path.exists(folder):
        for file in os.listdir(folder):
            path = os.path.abspath(os.path.join(folder, file))
            os.remove(path)
