import numpy as np

from core.tool.CoreTool import CoreTool

import core.tool.tool_common as common

class EraserTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Eraser'

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        brush_x, brush_y = common.get_brush_cut(brush, x, y)
        mask = common.cut_mask(brush, brush_x, brush_y, x, y)

        paint_image = temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1], 3].astype(np.float32)

        flow = brush.get_flow()
        alpha_add = (mask * flow * 255.0).astype(np.float32)

        paint_image = np.clip(paint_image + alpha_add, 0, 255)

        temp_layer[brush_y[0]:brush_y[1], brush_x[0]:brush_x[1], 3] = paint_image.astype(np.uint8)

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        # blend temp layer with real layer
        layer.adjust_size()

        (l_range_h, l_range_w), (t_range_h, t_range_w) = common.get_intersection(layer.get_layer(),
                                                                                 layer.get_position())
        dst = layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1]].astype(np.float32)
        dst_a = dst[..., 3] / 255.0

        src = temp_layer[t_range_h[0]: t_range_h[1], t_range_w[0]: t_range_w[1]].astype(np.float32)
        opacity = brush.get_opacity()
        src_a = src[..., 3] * (opacity / 255.0)

        # blend
        out_a = dst_a - src_a
        out_a = np.clip(out_a, 0.0, 1.0) * 255.0

        layer.get_layer()[l_range_h[0]: l_range_h[1], l_range_w[0]: l_range_w[1], 3] = out_a.astype(np.uint8)

        temp_layer.fill(0)