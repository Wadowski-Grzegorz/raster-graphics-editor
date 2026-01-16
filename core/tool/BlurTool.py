import numpy as np
import cv2 as cv

from core.tool.CoreTool import CoreTool

import core.tool.tool_common as common
import resources.settings as settings

class BlurTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Blur'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        brush_x, brush_y = common.get_brush_cut(brush, x, y)
        mask = common.cut_mask(brush, brush_x, brush_y, x, y)

        paint_image = temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1], 3]

        paint_image = paint_image + mask
        paint_image[paint_image > 0] = 160
        temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1], 3] = paint_image

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        # blend temp layer with real layer
        layer.adjust_size()

        (l_range_h, l_range_w), (t_range_h, t_range_w) = common.get_intersection(
                                                                 layer.get_layer(),
                                                                 layer.get_position()
        )
        dst = layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1]].astype(np.float32)

        dst_rgb = dst[..., :3]
        where_blur = temp_layer[t_range_h[0]: t_range_h[1], t_range_w[0]: t_range_w[1], 3] > 0
        blurred_rgb = cv.GaussianBlur(dst_rgb, (11, 11), 0)
        dst_rgb[where_blur] = blurred_rgb[where_blur]

        layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1], :3] = dst_rgb.astype(np.uint8)

        temp_layer.fill(0)