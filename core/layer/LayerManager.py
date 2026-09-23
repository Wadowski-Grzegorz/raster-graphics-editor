import cv2 as cv

from core.layer.Layer import Layer
from core.layer.RasterLayer import RasterLayer
from core.layer.LosslessLayer import LosslessLayer
from time import sleep

class LayerManager:

    def __init__(self, event):
        self._event = event
        self._layers = {} # id : layer
        self._layers_order = [] # first in order - first to draw, saved as IDs
        self._current_idx = None

        self._temp_layer = None

    def create_empty(self):
        # print("LayerManager create_empty start waiting")
        # sleep(3)
        # print("LayerManager create_empty ended waiting")
        layer = RasterLayer()
        self._append_layer(layer)
        self._event.notify({"type": "layer_created", "idx": layer.get_idx(), "layer": layer})

    def create_from_image(self, file_path: str):
        img_file = cv.imread(file_path, cv.IMREAD_UNCHANGED)
        if img_file is None:
            raise FileNotFoundError

        if img_file.shape[2] == 3:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGR2RGBA)
        elif img_file.shape[2] == 4:
            img_file = cv.cvtColor(img_file, cv.COLOR_BGRA2RGBA)

        img = LosslessLayer(img_file)
        self._append_layer(img)
        self._event.notify({"type": "layer_created", "idx": img.get_idx(), "layer": img})

    def _append_layer(self, layer: Layer):
        idx = layer.get_idx()
        self._layers[idx] = layer
        self._layers_order.append(idx)
        self.set_current_idx(idx)

    def create_temp(self):
        layer = RasterLayer()
        self._temp_layer = layer
        self._event.notify({"type": "layer_temp_created", "layer": layer})

    def layer_init(self):
        self.create_temp()
        self.create_empty()

    def set_current_idx(self, idx):
        self._current_idx = idx
        self._event.notify({"type": "layer_current_idx_changed", "idx": idx, "layer": self._layers[idx]})

    def reorder(self, new_order: list):
        if len(new_order) != self.get_layers_len():
            return

        self._layers_order = new_order.copy()
        self._event.notify({"type": "layer_order_changed", "order": self._layers_order})

    def switch_visibility(self, idx: int):
        self._layers[idx].switch_visible()
        self._event.notify({"type": "layer_visibility_switched", "idx": idx})

    def convert_to_editable(self, idx: int):
        l = self._layers[idx]
        if l and not l.is_editable():
            new_layer = RasterLayer(
                idx = l.get_idx(),
                layer = l.get_layer(),
                position = l.get_position(),
                name = l.get_name(),
                visible= l.get_visible(),
            )
            self._layers[idx] = new_layer
            self._event.notify({"type": "layer_changed_type", "idx": idx, "layer": new_layer})

    def set_name(self, idx: int, name: str):
        if self._layers[idx]:
            self._layers[idx].set_name(name)
            self._event.notify({"type": "layer_changed_name", "idx": idx})

    def get_layers(self) -> list[Layer]:
        return list(self._layers.values())

    def get_layer(self, idx: int):
        return self._layers[idx]

    def get_layers_len(self):
        return len(self._layers)

    def get_layers_arr(self):
        return {idx: l.get_layer() for idx, l in self._layers.items()}

    def get_temp_layer(self):
        return self._temp_layer

    def get_current_layer(self):
        return self._layers[self._current_idx]

    def get_order(self):
        return self._layers_order.copy()

    def return_state(self, data):
        d_layer = data["layer"]
        d_idx = data["idx"]
        d_op = data["operation"]

        if d_op == "create":
            for idx, l in self._layers:
                if d_idx == idx:
                    del self._layers[idx]
                    self._layers_order.remove(idx)

        if d_op == "edit":
            for idx, l in self._layers:
                if d_idx == idx:
                    self._layers[idx] = d_layer

        if d_op == "delete":
            for idx, l in self._layers:
                if d_idx == idx:
                    self._layers[idx] = d_layer
                    self._layers_order.append(idx)
