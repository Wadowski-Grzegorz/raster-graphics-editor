from core.layer.Layer import Layer
from dto.LayerGui import LayerGui
from dto.ObjectGui import ObjectGui


class Adapter:

    @staticmethod
    def layer_to_dto(l: Layer):
        objects_gui = []
        for ob in l.get_images():
            ob_gui = ObjectGui(ob.get_qImage(), ob.get_size(), ob.get_position())
            objects_gui.append(ob_gui)

        return LayerGui(l.get_qLayer(), l.get_visible(), objects_gui)

    @staticmethod
    def layers_to_dto(layers: list[Layer]):
        return {l.get_id(): Adapter.layer_to_dto(l) for l in layers}

adapter = Adapter()