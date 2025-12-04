from core.layer.Layer import Layer
from dto.LayerGui import LayerGui


class LayerAdapter:

    @staticmethod
    def layer_to_dto(l: Layer):
        return LayerGui(l.get_layer_q(), l.get_visible(), l.get_position())

    @staticmethod
    def layers_to_dto(layers: list[Layer]):
        return {l.get_id(): LayerAdapter.layer_to_dto(l) for l in layers}

layer_adapter = LayerAdapter()