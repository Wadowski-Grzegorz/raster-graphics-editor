from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtWidgets import QWidget

from adapters.BrushAdapter import BrushAdapter
from adapters.LayerAdapter import LayerAdapter
from adapters.ToolAdapter import ToolAdapter
from core.brush.Brush import Brush
from core.layer.Layer import Layer


class Controller(QWidget):

    def __init__(self, core=None, gui=None):
        super().__init__()
        self.gui = gui
        self.core = core
        self._executor = ThreadPoolExecutor(max_workers=1)

        self.gui.starting_window.signal_initial_pulse.connect(self.initial)
        self.gui.palette.signal_color_changed.connect(self._wrap(self.core.tool.change_color))

        self.gui.layer_panel.signal_layer_create_order.connect(self._wrap(self.core.layer.create_empty))

        self.gui.layer_panel.signal_layer_choose.connect(self._wrap(self.core.layer.set_current_idx))
        self.gui.layer_panel.signal_layer_reorder_order.connect(self._wrap(self.core.layer.reorder))
        self.gui.layer_panel.signal_layer_visibility_switch.connect(self._wrap(self.core.layer.switch_visibility))
        self.gui.layer_panel.signal_layer_convert.connect(self._wrap(self.core.layer.convert_to_editable))
        self.gui.layer_panel.signal_layer_name_change.connect(self._wrap(self.core.layer.set_name))


        self.gui.tool.signal_brush_change_parameter.connect(self._wrap(self.core.brush.set_brush_parameter))
        self.gui.tool.signal_brush_select.connect(self._wrap(self.core.brush.set_curr_brush))
        self.gui.tool.signal_tool_select.connect(self.tool_select)

        self.gui.file_manager.signal_image_read.connect(self._wrap(self.core.layer.create_from_image))

        self._current_manager = self.core.tool

        self.gui.canvas.signal_cursor_pressed.connect(self.on_press)
        self.gui.canvas.signal_cursor_moved.connect(self.on_move)
        self.gui.canvas.signal_cursor_released.connect(self.on_release)

    def _wrap(self, func):
        return lambda *args, **kwargs: self._executor.submit(func, *args, **kwargs)

    def initial(self):
        self.core.brush.init()
        self.core.layer.layer_init()
        self.core.tool.init()

    def tool_select(self, name:str):
        if self._executor.submit(self.core.tool.tool_select, name).result():
            self._current_manager = self.core.tool
        elif self.gui.tool.tool_select(name):
            self._current_manager = self.gui.tool

    def on_press(self, *args):
        if self._current_manager is self.core.tool:
            self._executor.submit(self.core.tool.on_press, *args)
        else:
            self.gui.tool.on_press(x, y)

    def on_move(self, *args):
        if self._current_manager is self.core.tool:
            self._executor.submit(self.core.tool.on_move, *args)
        else:
            self.gui.tool.on_move(*args)

    def on_release(self, *args):
        if self._current_manager is self.core.tool:
            self._executor.submit(self.core.tool.on_release(*args))
        else:
            self.gui.tool.on_release(*args)

    # Adapters
    def convert_layer_gui(self, layer: Layer):
        return LayerAdapter.layer_to_dto(layer)

    def get_layers_gui(self):
        layers = self.core.layer.get_layers()
        return LayerAdapter.layers_to_dto(layers)

    def get_layers_order(self):
        return self.core.layer.get_order()

    def convert_brush_to_gui(self, brush: Brush):
        return BrushAdapter.brush_to_gui(brush)

    def get_brushes_selectable(self):
        brushes = self.core.brush.get_brushes()
        return BrushAdapter.brushes_to_selectable(brushes)

    def get_current_brush(self):
        brush = self.core.brush.get_current_brush()
        return BrushAdapter.brush_to_gui(brush)

    def get_tools_selectable(self):
        core_tools = self.core.tool.get_tools()
        return ToolAdapter.tools_to_selectable(core_tools)

    def convert_tools_to_selectable(self, tools):
        return ToolAdapter.tools_to_selectable(tools)