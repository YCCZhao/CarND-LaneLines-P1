# Reflection

## My pipeline description:

My pipeline consisted of 5 steps: 

* First, I filtered all colors and only keep white and yellow; 
* Second, I converted the filtered images to grayscale; 
* After that, I applied Canny edage detection to find all edges; 
* Then I only keep the edges in the area where the lanes are located at the images; 
* Finally I perform Hough Line Tranformation to find the left lanes and the right lanes.

### Summary of Modification In My Pipeline 

**1. Created `HSV_flt()` to filter colors except for yellow or white. It turned a image with color in ranges list below.**
* A helper function `to_HSV()` converted RBG image to HSV image. Since the lanes are mainly in yellow or white, 
  it filtered objects that are not lanes. 
```
yellow_min = np.array([20, 0, 100], np.uint8)
yellow_max = np.array([50, 255, 255], np.uint8)
white_min = np.array([0, 0, 180], np.uint8)    
white_max = np.array([255, 50, 255], np.uint8)
```

**2. Modified `draw_lines()` to draw a single line on the left and right lanes.**
* In order to do so, first I filtered lines that with angle less than 15 degree with the X-axis. 

* Then I categorized lines into left lines or right lines base on their slope - negative slope represents left lines, 
  and positive one represents right lines. 
  
* I also filtered lines that appeared too outside. Only lines with parameter passing the following logic were kept
  '(img.shape[0] - b)/m >= 0' or 'img.shape[0] - b)/m <= img.shape[1]'
  
* Finally I averaged for all the right line parameters and all the left parameters. With the two sets of line paramters, 
  a left line and a right line were mapped from the bottom of the image up until the area of interest. 

**3. Tuned Hough Line Transform paramters and automated parameter update when `hough_lines()` return zero lines**
* The followings are the paramters I started to use for Hour Line Transform
```
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180*1 # angular resolution in radians of the Hough grid
threshold = 100    # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10 #minimum number of pixels making up a line
max_line_gap =  5  # maximum gap in pixels between connectable line segments
```
* Large threshold filtered edges that weren't belong the lanes. However when some lanes weren't visible
  or missing, `hough_lines` returned zero lines and the pipeline returned an error. To solove this issue, I add
  steps to decrease threshold automatically until lines are returned

``` while True:
  try:
    line_im = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)
    break
  except:
    threshold -= 10 
```
 
## Shortcomings with my current pipeline:

One potential shortcoming would be incorrect lines would be returned if there no lines between lanes.
For older cities like Philadelphia, some lines on freeways were totally worn out. The pipeline would continue
decrease the threshold until it picks up some random irrelevent lines. 

Another shortcoming could be the computation time. Unlike processing a video on file, the pipeline would process live
video. A car would need the imformation provided by the pipeline while the car is moving. Thus short computation time
is important. 

One other shortcoming could be when lines are out of interets region. A car would make a sudden turn to avoid hazard 
condition. That could cause lanes out of interest region, and the pipeline would have troubles detect the lanes. The
pipeline wouldn't work when the car is changing lanes either.


## Possible improvements to my pipeline:

A possible improvement would be to include history while extrapolate lines

Another potential improvement could be to ...



**Finding Lane Lines on the Road**

Project deliverables are the following:
* A pipeline that finds lane lines on the road in [a Jupyter Notebook](./P1.ipynb)
* Reflection on the pipeline in a  written report.
