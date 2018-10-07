# -*- coding: utf-8 -*-
import os
import sys
import random
import argparse
import numpy as np

from scipy.spatial import KDTree
from PIL import Image

def genrateMosaic(size, folder):
    for i in range(256):
        r, g, b = random.choices(range(256),k=3)
        color = ((max(0,r-100),r), (max(0,g-100),g), (max(0,b-100),b))
        generateRandonPicture(size, color, folder, "{:03d}.jpg".format(i))

def generateRandonPicture(size, color_range, folder, output):
    r_range, g_range, b_range = color_range
    r_min, r_max = r_range
    g_min, g_max = g_range
    b_min, b_max = b_range
    img = Image.new("RGB", size)
    for i in range(size[0]):
        for j in range(size[1]):
            color = (random.randint(r_min, r_max), random.randint(g_min, g_max), random.randint(b_min, b_max))
            img.paste(color, [i,j,i+1,j+1])
    img.save(os.path.abspath(os.path.join(folder, output)))

def removeMosaic(folder):
    for file in os.listdir(folder):
        path = os.path.abspath(os.path.join(folder, file))
        os.remove(path)

def getImage(imageDir):
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
    return tuple(np.average(img.reshape(w*h, d), axis=0))

def splitImage(image, size):
    W, H, *args = image.size
    m, n = size
    w, h = W//n, H//m
    imgs = []
    for j in range(m):
        for i in range(n):
            imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
    return imgs

def createImageGrid(images, dims):
    padding = 10
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

def createPhotomosaic(target_image, input_images, grid_size, reuse_image=True):
    print("[*] Spliting input image...")
    target_images = splitImage(target_image, grid_size)

    print("[*] Finding image matches...")
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

    print("[*] Creating mosaic...")

    mosaic_image = createImageGrid(output_images, grid_size)
    return mosaic_image

def parse_arguments():
    parser = argparse.ArgumentParser(description='Creates a photomosaic from input images')
    parser.add_argument('-t', '--target_image', required=True)
    parser.add_argument('-i', '--input_folder', required=True)
    parser.add_argument('-g', '--grid_size', nargs=2, type=int, required=True)
    parser.add_argument('-o', '--output_file',  default="mosaic.png", required=False)
    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    target_image = Image.open(args.target_image)
    print('[*] Reading input folder...')
    
    
    grid_size = (args.grid_size[0], args.grid_size[1])

    output_filename = args.output_file
    reuse_images = True
    resize_input = True

    print('[*] Starting photomosaic creation...')

    # if images can't be reused, ensure m*n <= num_of_images 
    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
          print('[-] Grid size less than number of images')
          sys.exit(1)

    dims = (target_image.size[0]//grid_size[1], 
            target_image.size[1]//grid_size[0])
    print(f"[*] Max tile dims: {dims}")

    input_images = getImage(args.input_folder)
    if input_images == []:
        print(f'[-] No input images found in {args.input_folder}. Generating.')
        print("[*] Gernating input images...")
        genrateMosaic(dims, args.input_folder)
        input_images = getImage(args.input_folder)
    else:
        if resize_input:
            print('[*] Resizing images...')
            for img in input_images:
                img.thumbnail(dims)
    random.shuffle(input_images)

    mosaic_image = createPhotomosaic(target_image, input_images, grid_size,
                                     reuse_images)

    mosaic_image.save(output_filename, 'PNG')

    print(f"[+] Saved output to {output_filename}")
    print('[+] Done.')
    removeMosaic(args.input_folder)

if __name__ == "__main__":
    main()

