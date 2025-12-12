import numpy as np
import cv2 as cv
from PyQt6.QtGui import QImage
import resources.settings as settings


def np_to_q_ptr(arr: np.ndarray):
    return QImage(
        arr.data,
        arr.shape[1],
        arr.shape[0],
        4 * arr.shape[1],
        QImage.Format.Format_RGBA8888
    )

def np_to_q(arr: np.ndarray):
    if arr.ndim == 2:
        np_img = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
        np_img[..., :3] = 255
        np_img[..., 3] = arr
        arr = np_img
    elif arr.ndim == 3 and arr.shape[2] == 3:
        h, w, _ = arr.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        rgba[..., :3] = arr
        rgba[..., 3] = 255
        arr = rgba

    h, w, _ = arr.shape
    q_img = QImage(arr.data, w, h, w * 4, QImage.Format.Format_RGBA8888)
    return q_img.copy()

def default_arr():
    return np.zeros((settings.layer_height, settings.layer_width, 4), dtype=np.uint8)

def arr_as(arr: np.ndarray):
    return np.zeros((arr.shape[0], arr.shape[1], arr.shape[2]), dtype=np.uint8)