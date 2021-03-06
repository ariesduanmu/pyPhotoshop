# -*- coding: utf-8 -*-
import os
import sys
import random
import argparse
import numpy as np


from scipy.spatial import KDTree
from PIL import Image

from helper import getImage, getAverageRGB, splitImage, createImageGrid
from tile import genrateTile, removeTile

'''
Create Mosaic effect using tile xD
tiles are generated by random color blocks
'''

#TODO compress image

def safeInputImages(input_folder, dims, resize):
    input_images = getImage(input_folder)
    if input_images == []:
        print(f'[-] No input images found in {input_folder}. Generating.')
        print("[*] Gernating input images...")
        genrateTile(dims, input_folder)
        input_images = getImage(input_folder)
    else:
        if resize:
            print('[*] Resizing images...')
            for img in input_images:
                img.thumbnail(dims)
    random.shuffle(input_images)
    return input_images


def searchTile(target_images, input_images, reuse_image):
    output_images = []
    count = 0
    batch_size = len(target_images) // 10
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))

    avgs = np.array(avgs)
    tree = KDTree(avgs)
    for img in target_images:
        avg = getAverageRGB(img)
        match_index = tree.query(avg)[1]
        output_images.append(input_images[match_index])

        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print(f"[*] Processed {count} of {len(target_images)}")
        count += 1

        if not reuse_image:
            input_images.remove(match_index)
    return output_images


def createPhotomosaic(target_image, input_images, grid_size, reuse_image=True):
    print("[*] Spliting input image...")
    target_images = splitImage(target_image, grid_size)

    print("[*] Finding image matches...")
    output_images = searchTile(target_images, input_images, reuse_image)

    print("[*] Creating mosaic...")

    return createImageGrid(output_images, grid_size, 1)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    parser.add_argument('-t', '--target_image', required=True)
    parser.add_argument('-i', '--input_folder', required=True)
    parser.add_argument('-g', '--grid_size', nargs=2, type=int, required=True)
    parser.add_argument('-o', '--output_file',  default="mosaic.jpg", required=False)
    parser.add_argument('-u', '--reuse',  default=True, required=False)
    parser.add_argument('-s', '--resize',  default=True, required=False)

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    target_image = Image.open(args.target_image)
    print('[*] Reading input folder...')
    
    grid_row, grid_column = args.grid_size

    print('[*] Starting photomosaic creation...')

    # if images can't be reused, ensure m*n <= num_of_images 
    if not args.reuse:
        if grid_row*grid_column > len(input_images):
          print('[-] Grid size less than number of images')
          sys.exit(1)

    dims = (target_image.size[0]//grid_row, 
            target_image.size[1]//grid_column)
    print(f"[*] Max tile dims: {dims}")

    input_images = safeInputImages(args.input_folder, dims, args.resize)

    mosaic_image = createPhotomosaic(target_image, input_images, args.grid_size,
                                     args.reuse)

    mosaic_image.save(args.output_file)

    print(f"[+] Saved output to {args.output_file}")
    print('[+] Done.')
    removeTile(args.input_folder)

if __name__ == "__main__":
    main()

