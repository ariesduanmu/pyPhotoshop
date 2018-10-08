# -*- coding: utf-8 -*-
import sys
import numpy as np
import argparse
from PIL import Image

def getAverageL(image):
    img = np.array(image)
    w, h = img.shape
    return int(np.average(img.reshape(w*h)))

def generateAscii(image, rows, cols, w, h, W, H, morelevels, invert, ascii_map):
    scale1 = r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    scale2 = r"@%#*+=-:. "
    aimg = []
    for j in range(rows):
        aimg.append("")
        for i in range(cols):
            y1 = int(j*h)
            y2 = H if j==rows-1 else int((j+1)*h)
            x1 = int(i*w)
            x2 = W if i==cols-1 else int((i+1)*w)

            img = image.crop((x1,y1,x2,y2))
            avg = getAverageL(img)
            if invert:
                avg = 255-avg
            if ascii_map is None:
                sval = scale1[(avg*69)//255] if morelevels else scale2[(avg*9)//255]
            else:
                sval = ascii_map[(avg*(len(ascii_map)-1))//255]
            aimg[j] += sval
    return aimg

def convertImageToAscii(target_image, cols, scale, morelevels, invert, ascii_map):
    image = Image.open(target_image).convert("L")

    W, H = image.size
    print(f"[*] Input image dims: {W} x {H}")

    w = W/cols
    h = w/scale

    rows = int(H//h)
    print(f"[*] cols: {cols}, rows: {rows}")
    print(f"[*] tile dims: {w} x {h}")

    if cols > W or rows > H:
        print("[-] Image too small for specified cols!")
        sys.exit(1)

    return generateAscii(image, rows, cols, w, h, W, H, morelevels, invert, ascii_map)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Creates a ascii image from input images')
    parser.add_argument('-t', '--target_image', required=True)
    parser.add_argument('-s', '--scale', type=float, default=0.43, required=False)
    parser.add_argument('-o', '--output_file',  default="ascii.txt", required=False)
    parser.add_argument('-c', '--cols', type=int, default=80, required=False)
    parser.add_argument('-m', '--morelevels', action='store_true')
    parser.add_argument('-p', '--map', required=False, help="input ascii")
    parser.add_argument('-i', '--invert', action='store_true', help="invert color")

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()
    print("[*] Generating ASCII art...")
    aimg = convertImageToAscii(args.target_image, args.cols, args.scale, args.morelevels, args.invert ,args.map)
    with open(args.output_file, "w") as f:
        for row in aimg:
            f.write(f"{row}\n")
    print(f"[*] ASCII art written to {args.output_file}")

if __name__ == '__main__':
    main()