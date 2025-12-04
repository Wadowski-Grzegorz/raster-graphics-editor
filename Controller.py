from PyQt6.QtWidgets import QWidget

from core.Paint import Paint
from gui.Canvas import Canvas
from gui.palette.Palette import Palette
from gui.layersPanel.LayersPanel import LayersPanel
from gui.tool.ToolsPanel import ToolsPanel
from gui.starting_window import Starting_window
from gui.ImageCaretaker import ImageCaretaker

from core.layer.DataCenter import data_center
from core.brush.BrushManager import brush_manager

class Controller(QWidget):

    def __init__(self, canvas: Canvas, palette: Palette, tools_panel: ToolsPanel, image_caretaker: ImageCaretaker,
                 layers_panel: LayersPanel, paint: Paint,
                 starting_window: Starting_window):
        super().__init__()
        self.canvas = canvas
        self.palette = palette
        self.layers_panel = layers_panel
        self.paint = paint
        self.starting_window = starting_window
        self.tools_panel = tools_panel
        self.image_caretaker = image_caretaker

        self.palette.signal_color_changed.connect(self.canvas.set_color)

        self.layers_panel.signal_layer_create_order.connect(self.layer_create)
        self.layers_panel.signal_layer_choose.connect(self.idx_chosen)
        self.layers_panel.signal_layer_reorder_order.connect(self.layer_reorder_order)

        self.starting_window.signal_layer_temp_create_order.connect(self.layer_temp_create)

        self.canvas.signal_paint_masking.connect(self.paint.paint_masking)
        self.canvas.signal_paint_masking_line.connect(self.paint.paint_masking_line)
        self.canvas.signal_blend.connect(self.paint.blend)

        self.tools_panel.signal_brush_changed_size.connect(brush_manager.changed_brush_size)
        self.tools_panel.signal_brush_changed_opacity.connect(brush_manager.changed_brush_opacity)
        self.tools_panel.signal_brush_changed_flow.connect(brush_manager.changed_brush_flow)
        self.tools_panel.signal_brush_changed_hardness.connect(brush_manager.changed_brush_hardness)
        self.tools_panel.signal_brush_selected.connect(self.brush_selected)

        self.image_caretaker.signal_image_read_order.connect(self.image_read)


    def layer_create(self):
        image, idx = data_center.create_empty()
        self.layers_panel.added_new_layer(image, idx)
        self.canvas.refresh_data()
        self.paint.added_new_layer(image, idx)

    def layer_temp_create(self):
        layer = data_center.create_temp()
        self.canvas.added_temp_layer(layer)
        self.paint.added_temp_layer(layer)

        if data_center.get_layers_len() == 0:
            self.layer_create()

    def layer_reorder_order(self, new_order: list):
        data_center.reorder(new_order)
        self.layers_panel.layers_order_changed()
        self.canvas.layers_order_changed()

    def idx_chosen(self, idx: int):
        data_center.set_current_idx(idx)
        self.canvas.changed_image()
        self.paint.changed_layer()

    def image_read(self, file_path: str):
        data_center.add_image(file_path)
        self.canvas.refresh_data()

    def brush_selected(self, idx):
        brush_manager.set_curr_brush(idx)
        self.paint.changed_brush()
        self.tools_panel.changed_brush()