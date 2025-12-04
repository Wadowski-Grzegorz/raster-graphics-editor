import numpy as np
from PyQt6.QtCore import pyqtSlot

from core.layer.DataCenter import data_center
from core.brush.BrushManager import brush_manager

from resources import settings


class Paint:
    def __init__(self):
        super().__init__()

        self.layers = {} # as numpy
        self.curr_idx = None
        self.temp_layer = None # as numpy

        self.curr_brush = brush_manager.get_curr_brush()

    def paint_masking(self, x, y, brush_color: np.ndarray):
        brush_radius = self.curr_brush.get_radius()

        img_y_s = max(y - brush_radius, 0)
        img_y_e = min(y + brush_radius, settings.layer_height)
        img_x_s = max(x - brush_radius, 0)
        img_x_e = min(x + brush_radius, settings.layer_width)

        paint_image = self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        mask = self.curr_brush.get_tip().astype(np.float32) / 255.0

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + (img_y_e - img_y_s)
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + (img_x_e - img_x_s)

        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]

        flow = self.curr_brush.get_flow()
        alpha_add = (mask * flow * 255.0).astype(np.float32)

        paint_image[..., :3] = brush_color[:3]

        current_alpha = paint_image[..., 3]
        new_alpha = current_alpha + alpha_add
        paint_image[..., 3] = np.clip(new_alpha, 0, 255)

        self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e] = paint_image.astype(np.uint8)

    def paint_masking_line(self, start_x, start_y, end_x, end_y, brush_color):
        # ----- calculating pixel position -----
        # check which value has more to grow
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        # steps - how many pixel to color
        steps = dx if dx >= dy else dy
        step_x = dx / steps if end_x >= start_x else -dx / steps
        step_y = dy / steps if end_y >= start_y else -dy / steps

        brush_radius = self.curr_brush.get_radius()
        spacing = self.curr_brush.get_spacing()

        space = (brush_radius * spacing)
        points = np.arange(0, steps, space)
        for i in points:
            a = start_x + step_x * i
            b = start_y + step_y * i
            self.paint_masking(int(a), int(b), brush_color)

    def blend(self):
        opacity = self.curr_brush.get_opacity()

        # Mask of where brush has painted
        src_where_is_painted = (self.temp_layer.sum(axis=2) > 0).astype(np.float32)
        # take alpha from brush stroke from temp
        src_stroke_alpha = (self.temp_layer[..., 3].astype(np.float32) * opacity * src_where_is_painted) / 255.0
        src_stroke_alpha_extended = src_stroke_alpha[:, :, None]

        dst = self.layers[self.curr_idx].astype(np.float32)
        src = self.temp_layer.astype(np.float32)

        out_a = (dst[..., 3] + src_stroke_alpha * 255.0)
        out_a = np.clip(out_a, 0, 255)

        self.layers[self.curr_idx][..., :3] = (
            (dst[..., :3] * (1 - src_stroke_alpha_extended)
            + src[..., :3] * src_stroke_alpha_extended)
            .astype(np.uint8))
        self.layers[self.curr_idx][..., 3] = out_a.astype(np.uint8)

        self.temp_layer.fill(0)

    def set_curr_idx(self, idx: int):
        self.curr_idx = idx

    def added_new_layer(self, layer: np.ndarray, idx: int):
        self.layers[idx] = layer
        self.set_curr_idx(idx)

    def added_temp_layer(self, layer: np.ndarray):
        self.temp_layer = layer

    @pyqtSlot()
    def changed_layer(self):
        idx = data_center.get_idx()
        self.set_curr_idx(idx)

    def changed_brush(self):
        self.curr_brush = brush_manager.get_curr_brush()