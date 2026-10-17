import cv2 as cv

from core.layer.Layer import Layer
from core.layer.RasterLayer import RasterLayer
from core.layer.LosslessLayer import LosslessLayer
from core.layer.LayerHistory import LayerHistory

class LayerManager:

    def __init__(self, event_provider):
        self._event_provider = event_provider
        self._layers = {} # id : layer
        self._layers_order = [] # first in order - first to draw, saved as IDs
        self._current_idx = None
        self._temp_layer = None

        self._history = LayerHistory()
        self._event_provider.subscribe(
            'paint_started', lambda data: self.register_action(data['layer'], 'layer_changed')
        )

    def create_empty(self):
        layer = RasterLayer()
        self._append_layer(layer)
        self._event_provider.notify({"type": "layer_created", "idx": layer.get_idx(), "layer": layer})
        self.set_current_idx(layer.get_idx())

        self.register_action(layer, 'layer_created')

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
        self._event_provider.notify({"type": "layer_created", "idx": img.get_idx(), "layer": img})
        self.set_current_idx(img.get_idx())
        self.register_action(img, 'layer_created')

    def _append_layer(self, layer: Layer):
        idx = layer.get_idx()
        self._layers[idx] = layer
        self._layers_order.append(idx)

    def create_temp(self):
        layer = RasterLayer()
        self._temp_layer = layer
        self._event_provider.notify({"type": "layer_temp_created", "layer": layer})

    def layer_init(self):
        self.create_temp()
        self.create_empty()

    def set_current_idx(self, idx):
        self._current_idx = idx
        self._event_provider.notify({"type": "layer_current_idx_changed", "idx": idx, "layer": self._layers.get(idx)})

    def reorder(self, new_order: list, internal_call=False):
        if len(new_order) != self.get_layers_len():
            return

        old_order = self._layers_order
        self._layers_order = new_order.copy()

        if internal_call:
            self._event_provider.notify({"type": "layer_order_restored", "order": self._layers_order.copy()})
        else:
            self.register_action(old_order, 'order')
            self._event_provider.notify({"type": "layer_order_changed", "order": self._layers_order.copy()})


    def switch_visibility(self, idx: int):
        self._layers[idx].switch_visible()
        self._event_provider.notify({"type": "layer_visibility_switched", "idx": idx})

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
            self._event_provider.notify({"type": "layer_changed_type", "idx": idx, "layer": new_layer})

    def delete(self, idx: int, internal_call=False):
        if idx not in self._layers:
            return

        if not internal_call:
            self.register_action({
                'layer': self._layers[idx],
                'order': self._layers_order
            }, 'layer_deleted')

        del self._layers[idx]
        idx_pos = self._layers_order.index(idx)
        self._layers_order.remove(idx)
        if self._current_idx == idx:
            new_idx = self._layers_order[min(idx_pos, len(self._layers_order) - 1)] if self._layers_order else 0
            self.set_current_idx(new_idx)

        self._event_provider.notify({"type": "layer_deleted", "idx": idx})

    def register_action(self, data, action):
        self._history.push(data, action)

    def pop_action(self):
        data, action = self._history.pop()
        match action:
            case 'order':
                self.reorder(data, internal_call=True)
            case 'layer_created':
                self.delete(data.get_idx(), internal_call=True)
            case 'layer_changed':
                self.restore_layer(data)
            case 'layer_deleted':
                self.recreate_layer(data['layer'], data['order'])

    def restore_layer(self, layer: Layer):
        self._layers[layer.get_idx()] = layer
        self._event_provider.notify({"type": "layer_restored", "layer": layer})

    def recreate_layer(self, layer: Layer, order: list[int]):
        self._layers[layer.get_idx()] = layer
        self._layers_order = order
        self._event_provider.notify({"type": "layer_recreated", "layer": layer, "order": order})

    def set_name(self, idx: int, name: str):
        if self._layers[idx]:
            self._layers[idx].set_name(name)
            self._event_provider.notify({"type": "layer_changed_name", "idx": idx})

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