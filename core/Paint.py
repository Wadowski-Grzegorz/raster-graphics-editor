import numpy as np

from core.brush.Brush import Brush


class Paint():
    def __init__(self):
        super().__init__()

        self.layers = {} # as numpy
        self.curr_idx = None
        self.temp_layer = None # as numpy

        self.layer_width = None
        self.layer_height = None

        self.curr_brush = Brush(size=100, opacity=1)

    def paint_masking(self, x, y, brush_color):
        brush_radius = self.curr_brush.get_radius()

        img_y_s, img_y_e = max(y - brush_radius, 0), min(y + brush_radius, self.layer_height)
        img_x_s, img_x_e = max(x - brush_radius, 0), min(x + brush_radius, self.layer_width)

        # cut a peace of image which user will paint with a brush
        paint_image = self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        # values 0-255 --> 0-1
        mask = self.curr_brush.get_tip().astype(np.float32) / 255.

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + img_y_e - img_y_s
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + img_x_e - img_x_s

        # mask is [a, b] while image is [a, b, 4], so resize with None
        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e, None]
        adjusted_mask = mask * self.curr_brush.get_flow()
        paint_image = paint_image * (1 - adjusted_mask) + brush_color * adjusted_mask

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

        # ----- order paint -----
        brush_radius = self.curr_brush.get_radius()
        spacing = self.curr_brush.get_spacing()
        flow = self.curr_brush.get_flow()

        space = (brush_radius * spacing)
        points = np.arange(0, steps, space)
        for i in points:
            a = start_x + step_x * i
            b = start_y + step_y * i
            self.paint_masking(int(a), int(b), brush_color)

    def blend(self):
        opacity = self.curr_brush.get_opacity()

        # check where were something drawn
        where_is_painted = (self.temp_layer.sum(axis=2) > 0).astype(np.float32)
        real_opacity = opacity * where_is_painted

        # mask is [a, b] while image is [a, b, 4], so resize with None
        real_opacity = real_opacity[:, :, None]

        self.layers[self.curr_idx][:] = (self.layers[self.curr_idx].astype(np.float32) * (1 - real_opacity) +
                                            self.temp_layer.astype(np.float32) * real_opacity).astype(np.uint8)

        self.temp_layer.fill(0)


    def set_curr_idx(self, idx: int):
        self.curr_idx = idx

    def added_new_layer(self, layer: np.ndarray, idx: int):
        self.layers[idx] = layer
        self.set_curr_idx(idx)

    def added_temp_layer(self, layer: np.ndarray):
        self.layer_height, self.layer_width, _ = layer.shape
        self.temp_layer = layer

    def changed_layer(self, idx: int):
        self.set_curr_idx(idx)

    def changed_brush_size(self, size: float):
        self.curr_brush.set_size(size)

    def changed_brush_opacity(self, opacity: float):
        self.curr_brush.set_opacity(opacity)

    def changed_brush_flow(self, flow: float):
        self.curr_brush.set_flow(flow)