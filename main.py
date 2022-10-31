from plantcv import plantcv as pcv
import cv2
import numpy as np


class options:
    def __init__(self):
        self.image = "./seedling_imgs/top_2.jpeg"
        self.debug = "plot"
        self.writeimg= False
        self.result = "res2.json"
        self.outdir = "." # Store the output to the current directory


def load_image(args):
    """
    Load the plant image and convert it into LAB colorspace

    Returns: the loaded image, and the LAB A channel of the image
    """
    img, _, _ = pcv.readimage(filename=args.image)
    #   channel- Split by 'l' (lightness), 'a' (green-magenta), or 'b' (blue-yellow) channel
    return img, pcv.rgb2gray_lab(rgb_img=img, channel='a')


def find_plants(img, gray_img):
    """
    Apply a binary threshold to the gray_img and filtering.
    Using the binary create rois around marking each plant
    """
    a_thresh = pcv.threshold.binary(gray_img=gray_img, threshold=120, max_value=255, 
                                    object_type='dark')
    mask =  filter(a_thresh)
    roi_contour, roi_hierarchy = pcv.roi.from_binary_image(img=img, bin_img=mask)
    return roi_contour, roi_hierarchy, mask


def filter(gray_img):
    """
    Apply median blur, fill and dilation to grayscale image

    Returns: filtered img
    """
    s_mblur = pcv.median_blur(gray_img=gray_img, ksize=10)
    fill_image = pcv.fill(bin_img=s_mblur, size=1000)
    return pcv.dilate(gray_img=fill_image, ksize=2, i=1)


def view_plants(img, mask):
    """
    View to plant image with mask applied
    """
    masked = pcv.apply_mask(img=img, mask=mask, mask_color='black')
    pcv.plot_image(masked)


def polyarea(x, y):
    """
    https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    Calculate the area of a polygon given x, y coordinates using shoelace algorithm
    """
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


def calculate_roi_area(roi_contours):
    """
    Calculate the area of rois contours

    roi_contours: list of rois
    Returns: dict with contour index keying to area in pixels
    """
    plant_areas = {}
    for i, contour in enumerate(roi_contours):
        x = [p[0][0] for p in contour]
        y = [p[0][1] for p in contour]
        plant_areas[i] = polyarea(x, y)
    return plant_areas

def find_squares(img):
    """""
    Get the area of the squares

    Returns: area in pixels
    """
    # proccess image
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #get threshold image
    ret,thresh_img = cv2.threshold(img_grey, 100, 255, cv2.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #create an empty image for contours
    img_contours = np.zeros(img.shape)

    max_contour = contours[0]
    for contour in contours:
        if cv2.contourArea(contour)>cv2.contourArea(max_contour) and cv2.contourArea(contour) < 100000:
          max_contour=contour

    contour=max_contour
    approx=cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    x,y,w,h=cv2.boundingRect(approx)

    square_area = (x-w) * (y-h)
    return square_area


if __name__ == "__main__":
    args = options()
    img, gray_img = load_image(args)
    roi_contours, _, mask = find_plants(img, gray_img)
    sizes = calculate_roi_area(roi_contours)
    print(sizes)
    view_plants(img, mask)

    square_area = find_squares(img)
    print(square_area)