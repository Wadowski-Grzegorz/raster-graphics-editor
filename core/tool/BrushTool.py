import numpy as np

from core.tool.CoreTool import CoreTool

import core.tool.tool_common as common
import resources.settings as settings

class BrushTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Brush'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        brush_x, brush_y = common.get_brush_cut(brush, x, y)
        mask = common.cut_mask(brush, brush_x, brush_y, x, y)

        paint_image = temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1]].astype(np.float32)

        flow = brush.get_flow()
        alpha_add = (mask * flow * 255.0).astype(np.float32)

        paint_image[..., :3] = color[:3]

        current_alpha = paint_image[..., 3]
        new_alpha = current_alpha + alpha_add
        paint_image[..., 3] = np.clip(new_alpha, 0, 255)

        temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1]] = paint_image.astype(np.uint8)

    def on_move(self, start_x, start_y, end_x, end_y, layer=None, temp_layer=None, brush=None, color=None):
        common.base_move(self.on_press, start_x, start_y, end_x, end_y, layer, temp_layer, brush, color)

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        # blend temp layer with real layer
        layer.adjust_size()

        # cut to temp_layer size
        (l_range_h, l_range_w), (t_range_h, t_range_w) = common.get_intersection(layer.get_layer(), layer.get_position())
        dst = layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1]].astype(np.float32)
        dst_rgb = dst[..., :3]
        dst_a = dst[..., 3] / 255.0
        dst_where_is_not_painted = (dst_a == 0)

        opacity = brush.get_opacity()
        src = temp_layer[t_range_h[0]: t_range_h[1], t_range_w[0]: t_range_w[1]].astype(np.float32)
        src_rgb = src[..., :3]
        src_a = src[..., 3] * (opacity / 255.0)

        # blend
        out_rgb = dst_rgb * (1 - src_a[:, :, None]) + src_rgb * src_a[:, :, None]
        out_rgb[dst_where_is_not_painted] = src_rgb[dst_where_is_not_painted]

        out_a = dst_a + src_a
        out_a = np.clip(out_a, 0.0, 1.0) * 255.0

        layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1], :3] = out_rgb.astype(np.uint8)
        layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1], 3] = out_a.astype(np.uint8)

        temp_layer.fill(0)