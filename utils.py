import numpy as np
import cv2 as cv
from PyQt6.QtGui import QImage

import settings

def np_to_q_ptr(arr: np.ndarray):
    return QImage(
        arr.data,
        settings.layer_width,
        settings.layer_height,
        4 * settings.layer_width,
        QImage.Format.Format_RGBA8888
    )

def np_to_q_ptr_irr(arr: np.ndarray, width: int, height: int):
    return QImage(
        arr.data,
        width,
        height,
        4 * width,
        QImage.Format.Format_RGBA8888
    )
