import numpy as np

from core.tool.CoreTool import CoreTool

import resources.settings as settings

class BrushTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Brush'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        brush_radius = brush.get_radius()

        img_y_s = max(y - brush_radius, 0)
        img_y_e = min(y + brush_radius, settings.layer_height)
        img_x_s = max(x - brush_radius, 0)
        img_x_e = min(x + brush_radius, settings.layer_width)

        paint_image = temp_layer[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        mask = brush.get_tip().astype(np.float32) / 255.0

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + (img_y_e - img_y_s)
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + (img_x_e - img_x_s)

        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]

        flow = brush.get_flow()
        alpha_add = (mask * flow * 255.0).astype(np.float32)

        paint_image[..., :3] = color[:3]

        current_alpha = paint_image[..., 3]
        new_alpha = current_alpha + alpha_add
        paint_image[..., 3] = np.clip(new_alpha, 0, 255)

        temp_layer[img_y_s:img_y_e, img_x_s:img_x_e] = paint_image.astype(np.uint8)

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
        opacity = brush.get_opacity()

        src = temp_layer.astype(np.float32)
        src_rgb = src[..., :3]
        src_a = src[..., 3] * (opacity / 255.0)

        dst = layer.astype(np.float32)
        dst_rgb = dst[..., :3]
        dst_a = dst[..., 3] / 255.0

        dst_where_is_not_painted = (dst_a == 0)

        # blend
        out_rgb = dst_rgb * (1 - src_a[:, :, None]) + src_rgb * src_a[:, :, None]
        out_rgb[dst_where_is_not_painted] = src_rgb[dst_where_is_not_painted]

        out_a = dst_a + src_a
        out_a = np.clip(out_a, 0.0, 1.0)

        layer[..., :3] = out_rgb.astype(np.uint8)
        layer[..., 3] = (out_a * 255).astype(np.uint8)

        temp_layer.fill(0)