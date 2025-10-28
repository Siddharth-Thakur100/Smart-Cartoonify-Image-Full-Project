# cartoonify/classic.py
import cv2
import numpy as np

def classic_cartoonify(image_rgb, resize_to=(960,540)):
    # image_rgb: numpy array in RGB
    img = image_rgb.copy()
    # Convert to BGR for OpenCV operations that expect BGR if needed
    # but we'll convert internally where required
    # 1. Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 2. Median blur
    blur = cv2.medianBlur(gray, 5)
    # 3. Edge detection (adaptive threshold)
    edges = cv2.adaptiveThreshold(blur, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    # 4. Bilateral filter on color image
    color = cv2.bilateralFilter(img, 9, 300, 300)
    # 5. Combine
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(color, edges_colored)
    # resize for consistent display
    cartoon = cv2.resize(cartoon, resize_to)
    return cartoon
