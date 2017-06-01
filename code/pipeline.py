'''
Created on May 29, 2017

@author: Yunshi_Zhao
'''
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2


def grayscale(img):
    """Applies the Grayscale transform"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def to_HSV(img):
    """Transform image from RGB format to HSV
    to better filter for lanes"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

def HSV_flt(img, yellow_min,yellow_max, white_min, white_max):
    """Filter the HSV image besides yellow and white colors"""
    HSV = to_HSV(img)
    yellow_mask = cv2.inRange(HSV, yellow_min, yellow_max)
    white_mask = cv2.inRange(HSV, white_min, white_max)
    return cv2.bitwise_and(img, img, mask=cv2.bitwise_or(yellow_mask, white_mask))
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
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
    return cv2.bitwise_and(img, mask)

def draw_lines(img, lines, color=[255, 0, 0], thickness=20):
    """
    The function average the line parameters and extrapolate two lines: 
    one on the left, and the other on the right.
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.

    """
    y_min = int(img.shape[0]*3/5)
    r_b, r_m, l_b, l_m = 0, 0, 0, 0
    rbc, rmc, lbc, lmc = 0, 0, 0, 0
    for line in lines:
        for x1,y1,x2,y2 in line:
            m = (y2 - y1)/(x2 - x1)
            b = y1 - m * x1
            # Filter horizontal lines
            if math.atan(abs(m)) < (15 * np.pi / 180):
                continue
            # Determine if a line represents the left lane or the right lane
            else:
                m = (y2 - y1)/(x2 - x1)
                b = y1 - m * x1
                # When slope ((y2-y1)/(x2-x1)) is negative the line is on the left
                if m < 0: #left
                    if (y_min - b)/m >= 0:
                        l_b += b
                        lbc += 1
                        l_m += m
                        lmc += 1
                # When slope ((y2-y1)/(x2-x1)) is positive the line is on the left        
                else: 
                    if (y_min - b)/m <= img.shape[1]:
                        r_b += b
                        rbc += 1
                        r_m += m
                        rmc += 1
    # average the coefficient        
    left_m = l_m / lmc 
    left_b = l_b / lbc
    right_m = r_m / rmc 
    right_b = r_b / rbc 
    # extrapolate two lines to map out the full extent of the lanes
    x_bl = int((img.shape[0] - left_b) / left_m)
    x_br = int((img.shape[0] - right_b) / right_m)
    x_ul = int((y_min - left_b) / left_m)
    x_ur = int((y_min - right_b) / right_m)
            
    cv2.line(img, (x_ur, y_min), (x_br, img.shape[0]), color, thickness)
    cv2.line(img, (x_ul, y_min), (x_bl, img.shape[0]), color, thickness)
    
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    function performs a Canny transform and         
    returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    it is a blank image (all black) with lines drawn on it.
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)


#read the image
image = mpimg.imread('solidYellowLeft.jpg')
imshape = image.shape
print('This image is:', type(image), 'with dimensions:', image.shape)
#define HSV filter range
yellow_min = np.array([15, 0, 0], np.uint8)
yellow_max = np.array([50, 255, 255], np.uint8)
white_min = np.array([0, 0, 150], np.uint8)
white_max = np.array([255, 80, 255], np.uint8)
color_flt = HSV_flt(image,yellow_min,yellow_max, white_min, white_max)
#plt.imshow(color_flt)
#plt.show()
#tranform image to grayscale
gray = grayscale(color_flt)
#plt.imshow(gray, cmap = 'gray')
#plt.show()
#filter image and only keep area of interet
low_threshold, high_threshold = 50, 150
kernel_size = 3
vertices =np.array([[(0,imshape[0]),(imshape[1]*5/11, imshape[0]*3/5), 
                     (imshape[1]*6/11, imshape[0]*3/5), (imshape[1],imshape[0])]], 
                   dtype=np.int32)

mask = region_of_interest(gray, vertices)

filtered = gaussian_blur(gray, kernel_size)
edge = canny(filtered, low_threshold, high_threshold)

masked_edges = cv2.bitwise_and(edge, mask)
#plt.imshow(masked_edges)
#plt.show()
#find lines 
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180*1 # angular resolution in radians of the Hough grid
threshold = 20    # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10 #minimum number of pixels making up a line
max_line_gap =  50  # maximum gap in pixels between connectable line segments

line_im = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)
final_im = weighted_img(line_im, image)
#process image
plt.imshow(final_im)
plt.show()
