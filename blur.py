# -*- coding: utf-8 -*-
'''I love Blur LOL
'''
import copy
import numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans, vq

from pprint import pprint

def sepearte_by_lights(gray_data, number=3):
    data = np.asarray(gray_data, dtype="float")
    w, h = data.shape
    data = np.reshape(data, w*h)
    centroids,_ = kmeans(data, number)
    idx,_ = vq(data, centroids)
    return idx

def simple_blur(image_path, output, level=1):
    img = Image.open(image_path)
    data = np.asarray(img, dtype="int32")
    w, h, _ = data.shape
    level = min(max(1, level), w, h)
    blur_data = (np.concatenate((data[:,level:], data[:,-1*level:]), axis=1) + 
                np.concatenate((data[:,:level], data[:,:-1*level]), axis=1) +
                np.concatenate((data[level:,:], data[-1*level:,:]), axis=0) +
                np.concatenate((data[:level,:], data[:-1*level,:]), axis=0)) / 4
    img = Image.fromarray(np.asarray(np.clip(blur_data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)

def gray_degree_blur(image_path, output, level=1):
    '''blur depends on gray degree
    '''
    img = Image.open(image_path)
    gray = img.convert('L')
    gray_idx = sepearte_by_lights(gray)
    data = np.asarray(img, dtype="int32")
    w, h, _ = data.shape
    level = min(max(1, level), w, h)
    gray_idx = np.reshape(gray_idx, (w, h))
    blur_data = np.asarray(img, dtype="float")

    dirleft_gray = np.concatenate((gray_idx[:, level:], gray_idx[:,-1*level:]), axis=1) == gray_idx
    dirleft_data = np.concatenate((data[:, level:], data[:,-1*level:]), axis=1)[dirleft_gray]
    blur_data[dirleft_gray] += dirleft_data

    dirright_gray = np.concatenate((gray_idx[:,:level], gray_idx[:,:-1*level]), axis=1) == gray_idx
    dirright_data = np.concatenate((data[:,:level], data[:,:-1*level]), axis=1)[dirright_gray]
    blur_data[dirright_gray] += dirright_data

    dirup_gray = np.concatenate((gray_idx[level:,:], gray_idx[-1*level:,:]), axis=0) == gray_idx
    dirup_data = np.concatenate((data[level:,:], data[-1*level:,:]), axis=0)[dirup_gray]
    blur_data[dirup_gray] += dirup_data

    dirdown_gray = np.concatenate((gray_idx[:level,:], gray_idx[:-1*level,:]), axis=0) == gray_idx
    dirdown_data = np.concatenate((data[:level,:], data[:-1*level,:]), axis=0)[dirdown_gray]
    blur_data[dirdown_gray] += dirdown_data

    gray_levels = np.asarray(dirleft_gray, dtype="float") +\
                  np.asarray(dirright_gray, dtype="float") +\
                  np.asarray(dirup_gray, dtype="float") +\
                  np.asarray(dirdown_gray, dtype="float") +\
                  np.asarray(gray_idx == gray_idx, dtype="float")
    gray_levels = np.reshape(gray_levels, (w,h,1))
    blur_data /= gray_levels
    img = Image.fromarray(np.asarray(np.clip(blur_data, 0, 255), dtype="uint8"), "RGB")
    img.save(output)

if __name__ == "__main__":
    gray_degree_blur("test.jpg", "new_test.jpg", 10)
