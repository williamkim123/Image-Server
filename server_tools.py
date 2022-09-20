import cv2
import numpy as np
import functools
import image_pb2
import itertools

def decode_image(image):
    """ Return numpy matrix from NLImage
    """
    w = image.width
    h = image.height
    c = image.color
    data = image.data
    params = (w, h)
    # if image has color
    if c:
        params = (w, h, 3)

    # create matrix buffer to store image
    total_elements = functools.reduce(lambda x, y: x*y, params)
    i = np.arange(total_elements, dtype=np.uint8).reshape(*params)
    return np.frombuffer(data, dtype=i.dtype).reshape(*params)

def rotate_image(img, rotation=None):
    """ Return img rotated clockwise given param rotation
    """
    if rotation == image_pb2.NLImageRotateRequest.NINETY_DEG:
        return np.rot90(img, k=3)
    elif rotation == image_pb2.NLImageRotateRequest.ONE_EIGHTY_DEG:
        return np.rot90(img, k=2)
    elif rotation == image_pb2.NLImageRotateRequest.TWO_SEVENTY_DEG:
        return np.rot90(img, k=1)
    return img

def mean_filter(img):
    """ 
    // if you have an image with 9 pixels:
    //   A B C
    //   D E F
    //   G H I
    // Then a few examples of pixels from the mean filter of this
    // image are:
    //    A_mean_filter = (A + B + E + D) / 4
    //    D_mean_filter = (D + A + B + E + G + H) / 6
    //    E_mean_filter = (E + A + B + C + D + F + G + H + I) / 9
    // For color images, the mean filter is the image with this filter
    // run on each of the 3 channels independently.
    """
    result = []

    # increase int range to store up till 2036 (256 * 9)
    img = img.astype(np.int16)
    height, width = img.shape[0], img.shape[1]
    result = [[0 for _ in range(width)] for _ in range(height)]
    for r in range(height):
        for c in range(width):
            # group each value of r with c
            values = itertools.product([r-1, r, r+1], [c-1 , c, c+1])
            total_sum = 0
            total_valid = 0
            for r_next, c_next in values:
                # print(r, c)
                if r_next < 0 or r_next >= height or c_next < 0 or c_next >= width:
                    continue
                # print(total_sum)
                total_sum += img[r_next][c_next]

                total_valid += 1
            val = 0
            if len(img.shape) == 3:
                val = [0, 0, 0]
            if total_valid > 0:
                val = list(total_sum / total_valid)
            result[r][c] = val

    # flatten
    result = np.array(result)
    params = (height, width)
    # color image
    if len(img.shape) == 3:
        params = (height, width, 3)

    # insert each value in params list as argument in reshape function
    return result.reshape(*params).astype(np.uint8)
    




