"""
Property photo quality analysis using OpenCV.
"""
from typing import Any
import cv2
import numpy as np

def variance_of_laplacian(image: np.ndarray) -> float:
    """
    Compute the Laplacian variance (blurriness detection).

    Args:
        image: Input image array.

    Returns:
        Variance of Laplacian.

    >>> import numpy as np
    >>> img = np.ones((100, 100), dtype=np.uint8) * 255
    >>> variance_of_laplacian(img) == 0.0
    True
    """
    return float(cv2.Laplacian(image, cv2.CV_64F).var())