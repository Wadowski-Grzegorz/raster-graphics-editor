from PyQt6.QtWidgets import QWidget

from gui.Canvas import Canvas
from gui.palette.Palette import Palette
from gui.layersPanel.LayersPanel import LayersPanel
from gui.tool.ToolsPanelsController import ToolsPanelsController
from gui.starting_window import Starting_window
from gui.ImageCaretaker import ImageCaretaker

from core.layer.LayerManager import layer_manager
from core.tool.ToolManager import tool_manager
from core.brush.BrushManager import brush_manager

class Controller(QWidget):

    def __init__(self, canvas: Canvas, palette: Palette, tools_panels_controller: ToolsPanelsController, image_caretaker: ImageCaretaker,
                 layers_panel: LayersPanel,
                 starting_window: Starting_window):
        super().__init__()
        self.canvas = canvas
        self.palette = palette
        self.layers_panel = layers_panel
        self.starting_window = starting_window
        self.tools_panels_controller = tools_panels_controller
        self.image_caretaker = image_caretaker

        self.palette.signal_color_changed.connect(tool_manager.changed_color)

        self.layers_panel.signal_layer_create_order.connect(self.layer_create)
        self.layers_panel.signal_layer_choose.connect(self.idx_chosen)
        self.layers_panel.signal_layer_reorder_order.connect(self.layer_reorder_order)

        self.starting_window.signal_layer_temp_create_order.connect(self.layer_temp_create)

        self.canvas.signal_cursor_pressed.connect(tool_manager.on_press)
        self.canvas.signal_cursor_moved.connect(tool_manager.on_move)
        self.canvas.signal_cursor_released.connect(tool_manager.on_release)

        self.tools_panels_controller.signal_brush_change_parameter.connect(self.brush_change_parameter)
        self.tools_panels_controller.signal_brush_selected.connect(self.brush_selected)
        self.tools_panels_controller.signal_tool_selected.connect(tool_manager.tool_selected)

        self.image_caretaker.signal_image_read_order.connect(self.image_read)


    def layer_create(self):
        idx = layer_manager.create_empty()
        self._announce_new_layer(idx)

    def image_read(self, file_path: str):
        idx = layer_manager.add_image(file_path)
        self._announce_new_layer(idx)

    def layer_temp_create(self):
        layer = layer_manager.create_temp()
        self.canvas.added_temp_layer(layer)
        tool_manager.added_temp_layer(layer)

        if layer_manager.get_layers_len() == 0:
            self.layer_create()

    def _announce_new_layer(self, idx: int):
        self.canvas.refresh_data()
        self.layers_panel.added_new_layer(idx)
        tool_manager.refresh_data()

    def layer_reorder_order(self, new_order: list):
        layer_manager.reorder(new_order)
        self.layers_panel.layers_order_changed()
        self.canvas.layers_order_changed()

    def idx_chosen(self, idx: int):
        layer_manager.set_current_idx(idx)
        self.canvas.changed_image()
        tool_manager.changed_layer()

    def brush_selected(self, idx):
        brush_manager.set_curr_brush(idx)
        tool_manager.changed_brush()
        self.tools_panels_controller.changed_brush()

    def brush_change_parameter(self, name: str, value: int|float):
        brush_manager.changed_brush_parameter(name, value)
        self.tools_panels_controller.changed_brush()