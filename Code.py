# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OQrtkkfw9L410bc_pbbmdZMBXGfVyeYx
"""

!git clone https://github.com/udacity/CarND-LaneLines-P1.git

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
from moviepy.editor import VideoFileClip
from IPython.display import HTML
# %matplotlib inline

import math

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(image, lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
           x1, y1, x2, y2 = line.reshape(4)
           cv2.line(line_image, (x1, y1), (x2, y2), [255,0,0], 2)
    return line_image

def draw_lines1(image, lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
           x1, y1, x2, y2 = line.reshape(4)
           cv2.line(line_image, (x1, y1), (x2, y2), [255,0,0], 30)
    return line_image

def weighted_img(initial_img, img, α=0.8, β=1., γ=1.):
    return cv2.addWeighted(initial_img, α, img, β, γ)


def process_image(image):
    blur=gaussian_blur(image,5)
    cany=canny(blur,50,150)
    blur1=gaussian_blur(cany,5)
    height=blur1.shape[0]
    triangle=np.array([[(120,height),(910,height),(490,300)]])
    roi=region_of_interest(blur1,triangle)
    lines=cv2.HoughLinesP(roi, 1, np.pi/180, 30, maxLineGap=250 )
    line_image=draw_lines(blur,lines)
    combo_image=weighted_img(blur, line_image)
    return combo_image

def process_image1(image):
    blur=gaussian_blur(image,5)
    cany=canny(blur,100,200)
    blur1=gaussian_blur(cany,5)
    height=blur1.shape[0]
    triangle=np.array([[(700,height),(4800,height),(2500,2200)]])
    roi=region_of_interest(blur1,triangle)
    lines=cv2.HoughLinesP(roi, 1, np.pi/180, 30, maxLineGap=260 )
    line_image=draw_lines1(blur,lines)
    combo_image=weighted_img(blur, line_image)
    return combo_image

def process_image2(image):
    blur=gaussian_blur(image,5)
    cany=canny(blur,100,200)
    blur1=gaussian_blur(cany,5)
    height=blur1.shape[0]
    triangle=np.array([[(100,height),(2000,height),(1100,600)]])
    roi=region_of_interest(blur1,triangle)
    lines=cv2.HoughLinesP(roi, 1, np.pi/180, 30, maxLineGap=250 )
    line_image=draw_lines1(blur,lines)
    combo_image=weighted_img(blur, line_image)
    return combo_image

#reading in an image
image = mpimg.imread('/content/CarND-LaneLines-P1/test_images/solidWhiteCurve.jpg')

#printing out some stats and plotting
print('This image is:', type(image),  'with dimensions:', image.shape)
plt.imshow(image)
plt.title('Original Image')  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')

blur=gaussian_blur(image,5)
print('This image is:', type(image), 'with dimensions:', blur.shape)
plt.imshow(blur,cmap='gray')
plt.title('Blured Image')

cany=canny(blur,50,150)
print('This image is:', type(image), 'with dimensions:', cany.shape)
plt.imshow(cany,cmap='gray')
plt.title('Canny Edge Detected Image')

blur1=gaussian_blur(cany,5)
print('This image is:', type(image), 'with dimensions:', blur1.shape)
plt.imshow(blur1,cmap='gray')
plt.title('Blurred Edge Detected Image')

height=blur1.shape[0]
triangle=np.array([[(120,height),(910,height),(490,300)]])
roi=region_of_interest(blur1,triangle)
print('This image is:', type(image), 'with dimensions:', roi.shape)
plt.imshow(roi,cmap='gray')
plt.title('Region of Interest')

lines=cv2.HoughLinesP(roi, 1, np.pi/180, 30, maxLineGap=250 )
line_image=draw_lines(blur,lines)
print('This image is:', type(image), 'with dimensions:', line_image.shape)
plt.imshow(line_image,cmap='gray')
plt.title('Drawn Lines on ROI')

combo_image=weighted_img(blur, line_image)
print('This image is:', type(image), 'with dimensions:', combo_image.shape)
plt.imshow(combo_image,cmap='gray')
plt.title('Combined Image')

import os
i=1
for filename in os.listdir('/content/CarND-LaneLines-P1/test_images'):
    img=cv2.imread(os.path.join('/content/CarND-LaneLines-P1/test_images',filename))
    im2=process_image(img)
    plt.subplot(3,3,i)
    plt.imshow(im2,cmap='gray')
    i=i+1

# Commented out IPython magic to ensure Python compatibility.
white_output = '/content/CarND-LaneLines-P1/test_videos_output/solidWhiteRight.mp4'
clip1 = VideoFileClip("/content/CarND-LaneLines-P1/test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
# %time white_clip.write_videofile(white_output, audio=False)

# Commented out IPython magic to ensure Python compatibility.
challenge_output = '/content/CarND-LaneLines-P1/test_videos_output/challenge.mp4'
clip1 = VideoFileClip("/content/CarND-LaneLines-P1/test_videos/challenge.mp4")
white_clip = clip1.fl_image(process_image2) #NOTE: this function expects color images!!
# %time white_clip.write_videofile(challenge_output, audio=False)

# Commented out IPython magic to ensure Python compatibility.
yellow_output = '/content/CarND-LaneLines-P1/test_videos_output/yellow.mp4'
clip1 = VideoFileClip("/content/CarND-LaneLines-P1/test_videos/solidYellowLeft.mp4")
white_clip = clip1.fl_image(process_image) #NOTE: this function expects color images!!
# %time white_clip.write_videofile(yellow_output, audio=False)

image = mpimg.imread('/content/CarND-LaneLines-P1/examples/NEWOWN/IMG_20191229_150401.jpg')
image=process_image1(image)
#printing out some stats and plotting
print('This image is:', type(image), 'with dimensions:', image.shape)
plt.imshow(image,cmap='gray')  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')

# Commented out IPython magic to ensure Python compatibility.
own_output = '/content/CarND-LaneLines-P1/test_videos_output/own1.mp4'
clip1 = VideoFileClip("/content/CarND-LaneLines-P1/test_videos/VID_20191229_150517.mp4").subclip(0,15)
white_clip = clip1.fl_image(process_image2) #NOTE: this function expects color images!!
# %time white_clip.write_videofile(own_output, audio=False)