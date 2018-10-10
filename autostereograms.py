# -*- coding: utf-8 -*-
import os
import sys
import argparse
import random
from PIL import Image, ImageDraw

def createRandomTile(dims, n=100):
    image = Image.new('RGB', dims)
    draw = ImageDraw.Draw(image)
    r = max(1,min(*dims) // 100)
    for i in range(n):
        x, y = random.randint(r, dims[0]-r), random.randint(r, dims[1]-r)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        draw.ellipse((x-r, y-r, x+r, y+r), color)
    return image

def createTiledImage(tile, dims):
    image = Image.new('RGB', dims)
    W, H = dims
    w, h = tile.size

    cols = W//w + 1
    rows = H//h + 1

    for i in range(rows):
        for j in range(cols):
            image.paste(tile,(j*w, i*h))
    return image

def createAutostereograms(depth, tile, radio):
    W, H = depth.size
    if tile is not None:
        tile = Image.open(os.path.abspath(args.tile))
        w, h = tile.size
        if min(W//w, H//h) < 10:
            tile.thumbnail(min((W//10, (H*w)//(10*h)), ((W*h)//(10*w), H//10)))
    else:
        size = min((W//10, H//10), (100, 100))
        tile = createRandomTile(size, min(*size)*3)
    image = createTiledImage(tile, depth.size)
    sImage = image.copy()

    pixD = depth.load()
    pixS = sImage.load()

    cols, rows = sImage.size
    for j in range(rows):
        for i in range(cols):
            #明暗交界处的变化最为明显,所以矢量图的效果更好
            xshift = pixD[i, j]//radio
            xpos = i - tile.size[0] + xshift
            if xpos > 0 and xpos < cols:
                pixS[i, j] = pixS[xpos, j]
    return sImage

def parse_arguments():
    parser = argparse.ArgumentParser(description="Autosterograms...")

    parser.add_argument('-d', '--depth', required=True, help="depth image path")
    parser.add_argument('-r', '--ratio', type=int, default=10, required=False, help="tile image")
    parser.add_argument('-t', '--tile', required=False, help="tile image")
    parser.add_argument('-o', '--out', default="auto.png", required=False, help="")

    args = parser.parse_args()

    if not os.path.exists(args.depth):
        print("[-] Depth Image Path Not Exist")
        sys.exit(1)

    if args.tile is not None and not os.path.exists(args.tile):
        print("[-] Tile Image Path Not Exist")
        sys.exit(1)

    return args

if __name__ == "__main__":
    args = parse_arguments()
    depth_path = os.path.abspath(args.depth)
    depth = Image.open(depth_path).convert('L')

    autoImage = createAutostereograms(depth, args.tile, args.ratio)
    autoImage.save(args.out)

