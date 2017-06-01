# **Udacity Self-Driving Car Nanodegree Term 1 Project 1: Finding Lane Lines on the Road** 


**Finding Lane Lines on the Road**

Project deliverables are the following:
* A pipeline that finds lane lines on the road in [a Jupyter Notebook](./P1.ipynb)
* Reflection on the pipeline in a  written report.


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### My pipeline description:

My pipeline consisted of 5 steps: 

* First, I filtered all colors and only keep white and yellow; 
* Second, I converted the filtered images to grayscale; 
* After that, I applied Canny edage detection to find all edges; 
* Then I only keep the edges in the area where the lanes are located at the images; 
* Finally I perform Hough Line Tranformation to find the left lanes and the right lanes.

#### Below is the summary of what is new in my pipeline compared to the origin master

* Create `to_HSV(img)` and `HSV_flt(img, yellow_min, yellow_max, white_min, white_max)` to filter colors except for yellow or white
  
In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Shortcomings with my current pipeline:


One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Possible improvements to my pipeline:

A possible improvement would be to ...

Another potential improvement could be to ...
