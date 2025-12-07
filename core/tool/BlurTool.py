import numpy as np
import cv2 as cv

from core.tool.CoreTool import CoreTool

import resources.settings as settings

class BlurTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Blur'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        brush_radius = brush.get_radius()

        img_y_s = max(y - brush_radius, 0)
        img_y_e = min(y + brush_radius, settings.layer_height)
        img_x_s = max(x - brush_radius, 0)
        img_x_e = min(x + brush_radius, settings.layer_width)

        paint_image = temp_layer[img_y_s:img_y_e, img_x_s:img_x_e, 3]

        mask = brush.get_tip()

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + (img_y_e - img_y_s)
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + (img_x_e - img_x_s)

        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]

        paint_image = paint_image + mask
        paint_image[paint_image > 0] = 160
        temp_layer[img_y_s:img_y_e, img_x_s:img_x_e][..., 3] = paint_image

    def on_move(self, start_x, start_y, end_x, end_y, layer=None, temp_layer=None, brush=None, color=None):
        # check which value has more to grow
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        # steps - how many pixel to color
        steps = dx if dx >= dy else dy
        step_x = dx / steps if end_x >= start_x else -dx / steps
        step_y = dy / steps if end_y >= start_y else -dy / steps

        brush_radius = brush.get_radius()
        spacing = brush.get_spacing()

        space = (brush_radius * spacing)
        points = np.arange(0, steps, space)
        for i in points:
            a = start_x + step_x * i
            b = start_y + step_y * i
            self.on_press(int(a), int(b), layer, temp_layer, brush, color)

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        # blend temp layer with real layer
        where_blur = temp_layer[..., 3] > 0

        blurred_rgb = cv.GaussianBlur(layer[..., :3], (11, 11), 0)
        layer[..., :3][where_blur] = blurred_rgb[where_blur]

        temp_layer.fill(0)