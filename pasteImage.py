# -*- coding: utf-8 -*-
from PIL import Image
import os

'''
Usage:
    create a tmp directory and put all images init
    name those images like "1","2","3" in order
'''

def _pasted_size(images):
    '''
    Args:
        images: list of image names
    
    Return:
        output image size, composed by the maxwidth in images
        and the sum of height of images
    '''
    max_width = 0
    total_height = 0
    for image in images:
        img = Image.open(image)
        w, h = img.size
        total_height += h
        if w > max_width:
            max_width = w
    return (max_width, total_height)

def _read_images():
    '''
    Returns:
        all sorted images names in tmp directory
    '''
    base_url = "tmp"
    return sorted(os.path.join(base_url, img) \
           for img in os.listdir(base_url) \
           if not os.path.isdir(os.path.join(base_url, img)))

def paste_images():
    images = _read_images()
    base_image = Image.new("RGB", _pasted_size(images), (255,255,255,255))
    next_h = 0
    for image in images:
        img = Image.open(image)
        w, h = img.size
        base_image.paste(img, (0,next_h))
        next_h += h
    base_image.save("out.jpg")

if __name__ == "__main__":
    paste_images()
