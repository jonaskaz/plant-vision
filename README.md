# Plant Detection and Measurement (PDM)
#TODO make a better name

What was the goal of your project? Since everyone is doing a different project, you will have to spend some time setting this context.

How did you solve the problem (i.e., what methods / algorithms did you use and how do they work)? As above, since not everyone will be familiar with the algorithms you have chosen, you will need to spend some time explaining what you did and how everything works.

## Detecting Plants in an Image

There are many different ways to detect a plant from an image. Each method works best in different applications, and for our context we chose the following approach:

- Tranform image into LAB colorspace (lightness, green-red, blue-yellow)
- Apply a binary threshold on the green-red channel to select the plants and remove the background
- Apply a blur, fill, and dilation to reduce noise and cleanup the result
- Apply the resulting pixel map mask to the original image

We used the following image to test our algorithm:
| Original Plant Image |
:----------------------:|
|![Original Plant Image](report_imgs/top_down.png)|

### Transform the Image into LAB
Detecting images in the RGB colorspace is possible, but there are often better ways to represent image data. One common example is the Hue-Saturation-Value (HSV) colorspace, which reduces the impact of lighting on the images color. Another alternative is the LAB (lightness, green-red, blue-yellow) colorspace, which similarly separates lighting from color information. We chose the LAB colorspace as it gave us the highest distinction between our plants and the background. Below is a comparison between the green-red channel (a) in the LAB colorspace and the value channel from the HSV colorspace selected from our image.

LAB A Channel             |  HSV V Channel
:-------------------------:|:-------------------------:
![](report_imgs/a_channel.png)  |  ![](report_imgs/hsv_v_channel.png)


### Binary Threshold
A binary threshold removes all pixels above or below a given value, leaving behind the object you hoped to detect. The effectiveness of this approach depends on a few important factors:
- Does the object have a solid or uniform appearance?
- Does the object differ in appearance to the background?
- What filters or transformations are applied to the image before taking a binary threshold?  

We applied a binary threshold on the A channel of the LAB image to remove the background. This mask could then be applied back to the original image. Results are shown below.  

| Detected Plants |
:----------------------:|
|![Detected Plants](report_imgs/detected_plants.png)|

### Blurring, Fill, and Dilation

Blurring, fill, and dilation are techniques used to reduce noise and separation of objects when detected. To apply these effects a kernel is used. A kernel is a small matrix used to change the pixel values in an image. 
#### Median Blur
In our case, we first applied a median blur filter. This filter works by stepping through the image, looking at a 10x10 area of pixels. It calculates the median pixel value among those 100 pixels, and sets the center pixel to that value. It then repeats, moving throughout the image resulting in a blurred image. 
#### Fill
Fill is used to remove small holes in the image that are the result of noise or misidentified plants. Fill works by going through the image and creating a binary structure from the image. This binary structure changes any pixels in the image that are greater than 0 to a 1. Next, groups (any pixels touching each other) of pixels are labeled. These labeled groups are checked, and those under a certain size have their pixel values set to 0. This final mask is then applied back to the original image. An example of this fill is shown below.

| Unfilled | Filled |
:----------------------:|:----------------------:|
|![Unfilled Image ](report_imgs/unfilled.png)|![Filled Image](report_imgs/filled.png)

The drawback of using a fill is that this sets a minimum size for identifiable plants. For example, small sprouts that are just beginning to show on the image may be falsely filled in.

### Dilation
Dilation is a technique that attempts to fill in the structure of detected elements in an image. To do this a structuring element is used (a kernel). This kernel is moved throughout the binary image, and if any pixels in the kernel are 1, the center pixel is set to 1. This has the effect of smoothing out the edges. The effect of this filter on our image was not visually perceptible, but we kept it in as an additional safety net. Dilation explanation resource: https://www.cs.auckland.ac.nz/courses/compsci773s1c/lectures/ImageProcessing-html/topic4.htm


### Canny Edge Detection
An alternative to the above filtering that we explored is Canny Edge Detection. Our attempts on this are shown below. This method did not work well for a few reasons:
- The plant leaves overlap and are not distinct objects
- There are many other edges present in the image, that also overlap with the plants
- There is no way to distinguish plant edges from other edges in the image

| Canny Edge Detection | Canny Edge on LAB Image |
:----------------------:|:----------------------:|
|![Failed Edge Detection](report_imgs/canny_edge.png)|![Failed Edge Dection on LAB Image](report_imgs/canny_edge_lab.png)

## Measuring Plants

#TODO

Describe a design decision you had to make when working on your project and what you ultimately did (and why)? These design decisions could be particular choices for how you implemented some part of an algorithm or perhaps a decision regarding which of two external packages to use in your project.

What if any challenges did you face along the way?
What would you do to improve your project if you had more time?

Did you learn any interesting lessons for future robotic programming projects? These could relate to working on robotics projects in teams, working on more open-ended (and longer term) problems, or any other relevant topic.