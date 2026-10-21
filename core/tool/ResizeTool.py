from core.layer.LosslessLayer import LosslessLayer
from core.tool.CoreTool import CoreTool
import cv2 as cv
import core.tool.tool_common as common

class ResizeTool(CoreTool):
    def __init__(self):
        super().__init__()
        self._name = 'Resize'
        self._sensitivity = 0.02
        self._mode = 'all'

        self._dx = 0
        self._dy = 0

    def on_press(self, x, y, layer=None, temp_layer=None, brush=None, color=None):
        self._dx = 0
        self._dy = 0

    def on_move(self, start_x, start_y, end_x, end_y, layer=None, temp_layer=None, brush=None, color=None):
        dx = self._dx + end_x - start_x
        dy = self._dy + end_y - start_y

        orig_arr, (w, h), (scale_x, scale_y) = self._get_resize_params(layer, dx, dy)

        self._dx = dx
        self._dy = dy

        resized = cv.resize(
            orig_arr,
            (w, h),
            interpolation=cv.INTER_LINEAR
        )

        (r_range_h, r_range_w), (t_range_h, t_range_w) = common.get_intersection(resized, layer.get_position())
        temp_layer.fill(0)
        temp_layer[t_range_h[0]: t_range_h[1], t_range_w[0]: t_range_w[1]] = \
            resized[r_range_h[0]: r_range_h[1], r_range_w[0]: r_range_w[1]]

    def on_release(self, layer=None, temp_layer=None, brush=None, color=None):
        current_scale = layer.get_scale() if isinstance(layer, LosslessLayer) else None
        orig_arr, (w, h), (scale_x, scale_y) = self._get_resize_params(layer, self._dx, self._dy)

        resized = cv.resize(
            orig_arr,
            (w, h),
            interpolation=cv.INTER_AREA
        )

        if current_scale is not None:
            layer.transform_by(scale_x / current_scale[0], scale_y / current_scale[1])
        
        layer.set_layer(resized)
        self._dx = 0
        self._dy = 0
        temp_layer.fill(0)

    def _get_resize_params(self, layer, dx, dy):
        scale_x = 1 + self._sensitivity * dx
        scale_y = 1 + self._sensitivity * dy

        if isinstance(layer, LosslessLayer):
            orig_arr = layer.get_orig()
            current_scale_x, current_scale_y = layer.get_scale()
            scale_x *= current_scale_x
            scale_y *= current_scale_y
        else:
            orig_arr = layer.get_layer()

        scale_x = max(scale_x, 1 / orig_arr.shape[1])
        scale_y = max(scale_y, 1 / orig_arr.shape[0])
        w = max(1, int(orig_arr.shape[1] * scale_x))
        h = max(1, int(orig_arr.shape[0] * scale_y))
        return orig_arr, (w, h), (scale_x, scale_y)