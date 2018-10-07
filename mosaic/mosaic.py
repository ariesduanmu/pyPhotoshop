# -*- coding: utf-8 -*-
import os
import sys
import random
import argparse
import numpy as np
from PIL import Image

def genrateMosaic(size, folder):
    for i in range(256):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        generateRandonPicture(size, ((max(0,r-100),r), (max(0,g-100),g), (max(0,b-100),b)), folder, "{:03d}.jpg".format(i))

def generateRandonPicture(size, color_range, folder, output):
    r_range, g_range, b_range = color_range
    r_min, r_max = r_range
    g_min, g_max = g_range
    b_min, b_max = b_range
    img = Image.new("RGB", size)
    for i in range(size[0]):
        for j in range(size[1]):
            img.paste((random.randint(r_min, r_max), random.randint(g_min, g_max), random.randint(b_min, b_max)), [i,j,i+1,j+1])
    img.save(os.path.abspath(os.path.join(folder, output)))


def removeMosaic(folder):
    for file in os.listdir(folder):
        path = os.path.abspath(os.path.join(folder, file))
        os.remove(path)

def RGBDistance(color_a, color_b):
    r1, g1, b1 = color_a
    r2, g2, b2 = color_b
    return (r1-r2) ** 2 + (g1-g2) ** 2 + (b1-b2) ** 2

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

def getBestMatchIndex(input_avg, avgs):
    avg = input_avg
    min_index = 0
    min_dist = float("inf")
    for index in range(len(avgs)):
        val = avgs[index]
        distance = RGBDistance(val, avg)
        if distance < min_dist:
            min_dist = distance
            min_index = index
    return min_index

def createImageGrid(images, dims):
    m, n = dims
    assert m*n == len(images)
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])
    grid_img = Image.new('RGB', (n*width+(n+1)*10, m*height+(m+1)*10))

    for index in range(len(images)):
        row = index//n
        col = index%n
        grid_img.paste(images[index], (col*width+(col+1)*10, row*height+(row+1)*10))
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

    for img in target_images:
        avg = getAverageRGB(img)
        match_index = getBestMatchIndex(avg, avgs)
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
    input_images = getImage(args.input_folder)
    if input_images == []:
      print(f'[-] No input images found in {args.input_folder}. Generating.')
      print("[*] Gernating input images...")
      genrateMosaic(args.grid_size, args.input_folder)
      input_images = getImage(args.input_folder)
      # sys.exit(1)
    random.shuffle(input_images)
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

    # resizing input
    if resize_input:
        print('[*] Resizing images...')
        # for given grid size, compute max dims w,h of tiles
        dims = (target_image.size[0]//grid_size[1], 
                target_image.size[1]//grid_size[0])
        print(f"[*] Max tile dims: {dims}")
    # resize
    for img in input_images:
        img.thumbnail(dims)

    mosaic_image = createPhotomosaic(target_image, input_images, grid_size,
                                   reuse_images)

    mosaic_image.save(output_filename, 'PNG')

    print(f"[+] Saved output to {output_filename}")
    print('[+] Done.')
    removeMosaic(args.input_folder)

if __name__ == "__main__":
    main()

