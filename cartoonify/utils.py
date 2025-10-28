# cartoonify/utils.py
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import time

def compute_ssim(img1_rgb, img2_rgb):
    img1_gray = cv2.cvtColor(img1_rgb, cv2.COLOR_RGB2GRAY)
    img2_gray = cv2.cvtColor(img2_rgb, cv2.COLOR_RGB2GRAY)
    score = ssim(img1_gray, img2_gray)
    return score

def color_histogram(image_rgb):
    # returns hist arrays for 3 channels
    chans = cv2.split(image_rgb)
    hist_data = [cv2.calcHist([c],[0],None,[256],[0,256]).flatten() for c in chans]
    return hist_data

def timeit(func, *args, **kwargs):
    t0 = time.time()
    res = func(*args, **kwargs)
    t1 = time.time()
    return res, (t1-t0)