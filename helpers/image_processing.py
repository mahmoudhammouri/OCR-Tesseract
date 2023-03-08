import cv2
import numpy as np


def invert_image(image):
    """
    invert image black and white colors in order to highlight all possible texts
        Parameters:
            image (cv2.Mat): the image array read using opencv that need to perform processing on
        Returns:
            inverted_image (cv2.Mat): the result image after performing inverting on it
    """
    arr = np.array(image)
    invert = ~arr
    return invert


def detect_blur(image, threshold=300) -> bool:
    """
    detects blur on the image based on specific threshold
        Parameters:
            image (cv2.Mat): the image array read using opencv that need to perform processing on

            threshold (int): the median value which used to decide if the image is blurred or not(default:300)
        Returns:
            is_blurred (bool): the result of blur detection
    """
    laplace_measure = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplace_measure > threshold
