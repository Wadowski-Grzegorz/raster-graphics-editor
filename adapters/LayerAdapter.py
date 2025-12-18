from core.layer.Layer import Layer
from dto.LayerGui import LayerGui
import utils

class LayerAdapter:

    @staticmethod
    def layer_to_dto(l: Layer):
        return LayerGui(
            l.get_idx(),
            utils.np_to_q_ptr(l.get_layer()),
            l.get_visible(),
            l.get_position(),
            l.get_name(),
            l.is_editable()
        )

    @staticmethod
    def layers_to_dto(layers: list[Layer]):
        return {l.get_idx(): LayerAdapter.layer_to_dto(l) for l in layers}

    # @staticmethod
    # def get_layers_gui():
    #     layers = layer_manager.get_layers()
    #     return LayerAdapter.layers_to_dto(layers)

    # @staticmethod
    # def get_layer_gui(idx: int):
    #     return LayerAdapter.layer_to_dto(layer_manager.get_layer(idx))

    # @staticmethod
    # def get_order():
    #     return layer_manager.get_order()