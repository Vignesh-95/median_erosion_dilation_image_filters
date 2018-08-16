import numpy as np
import cv2 as cv
import math


def calculate_template_space(temp_side_length):
        return int(temp_side_length/2)


def median_filter(image, template_side_length):
    new_image = np.zeros(image.shape, image.dtype)
    # Coordinates are provided as (y,x), where the origin is at the top left of the image
    # So always remember that (-) is used instead of (+) to iterate
    template_space = calculate_template_space(template_side_length)
    template = []
    half_template = int((template_side_length-1)/2)

    for x in range(template_space, new_image.shape[1] - template_space):
        a = x + half_template
        for y in range(template_space, new_image.shape[0] - template_space):
            b = y + half_template
            # a and b basically imply that from any center point always start iterating at the top left of the template
            # Iteration:
            for c in range(0, template_side_length):
                for d in range(0, template_side_length):
                    template.append(image[b - d, a - c])
            template.sort()
            new_image[y, x] = template[int((int(math.pow(template_side_length, 2)) - 1) / 2)]
            template = []
    return new_image


if __name__ == "__main__":
    img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/images/rotated_fence.png", cv.IMREAD_GRAYSCALE)
    filter_size = 7
    new_img = median_filter(img, filter_size)
    cv.imwrite("/home/vignesh/PycharmProjects/COS791_Ass1/images/rotated_fence_" + str(filter_size) + "_.png", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# NOTES
# Still need to implement median filter to calculate border pixels
# Still need to explain effects of different template sizes by referring to the resulting images and book theory
# Still need to save images
# Powerpoint presentation
# Explain Salt and Pepper Noise for rotated fence
