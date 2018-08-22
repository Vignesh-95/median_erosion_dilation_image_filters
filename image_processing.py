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


def erosion(image, template_side_length, template):
    new_image = np.zeros(image.shape, image.dtype)
    # Coordinates are provided as (y,x), where the origin is at the top left of the image
    # So always remember that (-) is used instead of (+) to iterate
    template_space = calculate_template_space(template_side_length)
    half_template = int((template_side_length - 1) / 2)

    for x in range(template_space, new_image.shape[1] - template_space):
        for y in range(template_space, new_image.shape[0] - template_space):
            minimum = 256
            for c in range(0, template_side_length):
                for d in range(0, template_side_length):
                    a = x - half_template - 1 + c
                    b = y - half_template - 1 + d
                    sub = image[b, a] - template[d, c]
                    if sub < minimum:
                        if sub > 0:
                            minimum = sub
            new_image[y, x] = int(minimum)
    return new_image


def dilation(image, template_side_length, template):
    new_image = np.zeros(image.shape, image.dtype)
    # Coordinates are provided as (y,x), where the origin is at the top left of the image
    # So always remember that (-) is used instead of (+) to iterate
    template_space = calculate_template_space(template_side_length)
    half_template = int((template_side_length - 1) / 2)

    for x in range(template_space, new_image.shape[1] - template_space):
        for y in range(template_space, new_image.shape[0] - template_space):
            maximum = 0
            for c in range(0, template_side_length):
                for d in range(0, template_side_length):
                    a = x - half_template - 1 + c
                    b = y - half_template - 1 + d
                    sub = image[b, a] - template[d, c]
                    if sub > maximum:
                        if sub > 0:
                            maximum = sub
            new_image[y, x] = int(maximum)
    return new_image


def open_op(image, template_side_length, template):
    new_image = erosion(image, template_side_length, template)
    new_image_2 = dilation(new_image, template_side_length, template)
    return new_image_2


def close_op(image, template_side_length, template):
    new_image = dilation(image, template_side_length, template)
    new_image_2 = erosion(new_image, template_side_length, template)
    return new_image_2


if __name__ == "__main__":
    # Median Filter
    #
    # img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/rotated_fence.png", cv.IMREAD_GRAYSCALE)
    # filter_size = 7
    # new_img = median_filter(img, filter_size)
    # cv.imwrite("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/rotated_fence_" + str(filter_size) + "_.png", new_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    #

    # Erosion
    img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells.png", cv.IMREAD_GRAYSCALE)
    filter_size = 9
    temp = np.zeros(img.shape, img.dtype)
    new_img = erosion(img, filter_size, temp)
    cv.imwrite("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells_eroded_" + str(filter_size) + "_.png", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Dilation
    img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells.png", cv.IMREAD_GRAYSCALE)
    filter_size = 9
    temp = np.zeros(img.shape, img.dtype)
    new_img = dilation(img, filter_size, temp)
    cv.imwrite("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells_dilated_" + str(filter_size) + "_.png", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Opening
    img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells.png",
                    cv.IMREAD_GRAYSCALE)
    filter_size = 9
    temp = np.zeros(img.shape, img.dtype)
    new_img = open_op(img, filter_size, temp)
    cv.imwrite(
        "/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells_opened_" + str(
            filter_size) + "_.png", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # Closing
    img = cv.imread("/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells.png",
                    cv.IMREAD_GRAYSCALE)
    filter_size = 9
    temp = np.zeros(img.shape, img.dtype)
    new_img = close_op(img, filter_size, temp)
    cv.imwrite(
        "/home/vignesh/PycharmProjects/COS791_Ass1/median_erosion_dilation_image_filters/images/cells_closed_" + str(
            filter_size) + "_.png", new_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

# NOTES
# Still need to implement median filter to calculate border pixels
# Still need to explain effects of different template sizes by referring to the resulting images and book theory
# Still need to save images
# Powerpoint presentation
# Explain Salt and Pepper Noise for rotated fence
# Questions on WhatsApp

# CHECK BOOK VS CODE COMPATIBILITY FOR EROSION DILATION OPENING CLOSING
# CHECK MAIN CODE FOR THE ABOVE 4 AS WELL
# UNDERSTAND BOOK ABOVE
# UNDERSTAND EFFECT ON PICTURES
# CHECK TEXTBOOK AND NOTEBOOK FOR UNDERSTANDING OF IMPACT OF DIFFERENT TEMPLATES AND TEMPLATE SIZES
# CHECK ASSIGNMENT INSTRUCTIONS FOR THESE OPERATORS IN TERMS OF WHAT TO PRESENT
# CHOOSE MORE PICTURES
