# **Reflection**

## My pipeline description:

My pipeline consisted of 5 steps: 

* Filtered all colors and only keep white and yellow; 
* Converted the filtered images to grayscale; 
* Applied Canny Edage Detection to find all edges; 
* Only kept the edges in the area where the lanes are located at the images; 
* Perfomred Hough Line Tranform to map the left lanes and the right lanes.

### Summary of Modification In My Pipeline 

**1. Created `HSV_flt()` to filter colors except for yellow or white.**
A helper function `to_HSV()` converted RBG image to HSV image. Then pixels with color outside of the range below were filtered.
```
yellow_min = np.array([20, 0, 100], np.uint8)
yellow_max = np.array([50, 255, 255], np.uint8)
white_min = np.array([0, 0, 180], np.uint8)    
white_max = np.array([255, 50, 255], np.uint8)
```

**2. Modified `draw_lines()` to draw a single line on the left and right lanes.**
* In order to do so, first I filtered lines that are less than 15 degree from the X-axis. 

* Then I categorized lines into left lines or right lines based on their slope: negative slope = left lines, 
  and positive one = right lines. 
  
* I also filtered lines that appeared too "outside". Lines were only kept if the following is true
  `(img.shape[0] - b)/m >= 0' or 'img.shape[0] - b)/m <= img.shape[1]`
  
* Finally I averaged for all the right lines and all the left lines. With averaged paramters for both lines, 
  a left line and a right line were mapped from the bottom of the image up to the end of the area of interest. 

**3. Tuned Hough Line Transform paramters and automated parameter update when `hough_lines()` return zero lines**
* The followings are the paramters I started to use for Hour Line Transform
```
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180*1 # angular resolution in radians of the Hough grid
threshold = 100    # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10 #minimum number of pixels making up a line
max_line_gap =  5  # maximum gap in pixels between connectable line segments
```
* Large threshold filtered edges that weren't belong the lanes. However when some lanes weren not clearly visible
  or missing, `hough_lines()` returned zero lines and the pipeline threw an error. To solove this issue, I added
  steps to decrease threshold automatically until lines were returned.

``` while True:
  try:
    line_im = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)
    break
  except:
    threshold -= 10 
```
 
## Shortcomings with my current pipeline:

One potential shortcoming could be that incorrect lines would be returned if there no lines between lanes.
For older cities like Philadelphia, some lines on freeways were totally worn out. The pipeline would continue
decrease the threshold until it picks up some random irrelevent lines. 

Another shortcoming could be the computation time. Unlike processing a video saved locally, the pipeline would process live
video. A moving car would need the imformation very fast so it can make its decision right away. The while loop i added to find thresholds could slow the process down.

One other shortcoming could be when lines are out of interets region. A car would make a sudden turn to avoid hazard 
condition. That could cause lanes out of interest region, and the pipeline would have troubles detect the lanes. The
pipeline wouldn't work when the car is changing lanes either.


## Possible improvements to my pipeline:

A possible improvement would be to include line changing trends while extrapolating left and right lanes. For example combine gradient of line paramters and output of `hough_lines()` to find the left and right lanes.

Another potential improvement could be to change Hough line Transform parameters based on number of edges identified, insteady of starting at a fixed value and change incrementally. 

Also if I had more time, I would look into how I could use other methods to better process images before edge detection. Making the lane lines pop out more and filter noise such as tire marks would increase the accuracy.  




