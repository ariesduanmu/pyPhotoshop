# -*- coding: utf-8 -*-
import argparse
import numpy as np

from PIL import Image
from scipy.cluster.vq import kmeans, vq

from tile import generateRandonPicture
from helper import splitImage, createImageGrid
'''
Create Mosaic effect using kmeans
I think the effect can't be called mosaic...
'''

def creatTile(image):
    image = np.array(image)
    w, h, d = image.shape
    image = image.reshape(w*h, d)
    centroids,_ = kmeans(image.astype(float), 2)
    idx,_ = vq(image, centroids)

    for i in range(len(idx)):
        image[i] = centroids[idx[i]].astype(int)

    image = image.reshape(w,h,d)
    return Image.fromarray(image)

def createMosaic(target_image, grid_size):
    target_images = splitImage(target_image, grid_size)
    tiles = [creatTile(image) for image in target_images]
    return createImageGrid(tiles, grid_size, 0)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    parser.add_argument('-t', '--target_image', required=True)
    parser.add_argument('-g', '--grid_size', nargs=2, type=int, required=True)
    parser.add_argument('-o', '--output_file',  default="magic.jpg", required=False)

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    target_image = Image.open(args.target_image)
    print('[*] Starting photomosaic creation...')
    mosaic_image = createMosaic(target_image, args.grid_size)
    mosaic_image.save(args.output_file)
    print(f"[+] Saved output to {args.output_file}")
    print('[+] Done.')

if __name__ == "__main__":
    main()
    
