from core.layer.Layer import Layer
from dto.LayerGui import LayerGui

from core.layer.LayerManager import layer_manager

class LayerAdapter:

    @staticmethod
    def layer_to_dto(l: Layer):
        return LayerGui(l.get_id(), l.get_layer_q(), l.get_visible(), l.get_position(), l.get_name(), l.is_editable())

    @staticmethod
    def layers_to_dto(layers: list[Layer]):
        return {l.get_id(): LayerAdapter.layer_to_dto(l) for l in layers}

    @staticmethod
    def get_layers_gui():
        layers = layer_manager.get_layers()
        return LayerAdapter.layers_to_dto(layers)

    @staticmethod
    def get_layer_gui(idx: int):
        return LayerAdapter.layer_to_dto(layer_manager.get_layer(idx))

    @staticmethod
    def get_order():
        return layer_manager.get_order()

layer_adapter = LayerAdapter()