from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget

from core.Paint import Paint
from gui.Canvas import Canvas
from gui.palette.Palette import Palette
from data.Layers import Layers
from gui.LayersPanel import LayersPanel
from gui.tool.ToolsPanel import ToolsPanel
from gui.starting_window import Starting_window


class Controller(QWidget):

    def __init__(self, canvas: Canvas, palette: Palette, tools_panel: ToolsPanel,
                 layers: Layers, layers_panel: LayersPanel, paint: Paint,
                 starting_window: Starting_window):
        super().__init__()
        self.canvas = canvas
        self.palette = palette
        self.layers = layers
        self.layers_panel = layers_panel
        self.paint = paint
        self.starting_window = starting_window
        self.tools_panel = tools_panel

        self.palette.signal_color_changed.connect(self.canvas.set_color)

        self.layers_panel.signal_layer_create_order.connect(self.layer_create)
        self.layers_panel.signal_layer_choose.connect(self.idx_chosen)
        self.layers_panel.signal_layer_reorder_order.connect(self.layer_reorder_order)

        self.starting_window.signal_layer_temp_create_order.connect(self.layer_temp_create)

        self.canvas.signal_paint_masking.connect(self.paint.paint_masking)
        self.canvas.signal_paint_masking_line.connect(self.paint.paint_masking_line)
        self.canvas.signal_blend.connect(self.paint.blend)

        self.tools_panel.signal_brush_changed_size.connect(self.paint.changed_brush_size)
        self.tools_panel.signal_brush_changed_opacity.connect(self.paint.changed_brush_opacity)
        self.tools_panel.signal_brush_changed_flow.connect(self.paint.changed_brush_flow)


    def layer_create(self):
        image, idx = self.layers.create()
        self.layers_panel.added_new_layer(image, idx)
        self.canvas.added_new_image(image, idx)
        self.paint.added_new_layer(image, idx)

    def layer_temp_create(self, width: int, height: int):
        layer = self.layers.create_temp(width, height)
        self.canvas.added_temp_layer(layer)
        self.paint.added_temp_layer(layer)

        if self.layers.get_layers_size() == 0:
            self.layer_create()

    def layer_reorder_order(self, new_order: list):
        self.layers.reorder(new_order)
        self.layers_panel.layers_order_changed()
        self.canvas.layers_order_changed()

    def idx_chosen(self, idx: int):
        self.canvas.changed_image(idx)
        self.paint.changed_layer(idx)