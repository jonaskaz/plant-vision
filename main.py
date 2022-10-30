from plantcv import plantcv as pcv
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


if __name__ == "__main__":
    args = options()
    img, gray_img = load_image(args)
    roi_contours, _, mask = find_plants(img, gray_img)
    sizes = calculate_roi_area(roi_contours)
    print(sizes)
    view_plants(img, mask)