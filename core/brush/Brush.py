from core.brush.BrushTip import BrushTip

class Brush:
    id_counter = 0
    def __init__(self, name='Brush', opacity=1, flow=1, spacing=0.25, size=1, hardness=1, shape='circle'):
        Brush.id_counter += 1
        self._idx = self.id_counter
        self._name = name
        self._opacity = opacity
        self._flow = flow
        self._spacing = spacing
        self._brush_tip = BrushTip(size=size, hardness=hardness, shape=shape)

    def get_opacity(self):
        return self._opacity

    def get_size(self):
        return self._brush_tip.size

    def get_tip(self):
        return self._brush_tip.mask

    def get_spacing(self):
        return self._spacing

    def get_flow(self):
        return self._flow

    def set_tip(self, brush_tip: BrushTip):
        self._brush_tip = brush_tip

    def set_size(self, size):
        self._brush_tip.resize(int(size))

    def set_opacity(self, opacity):
        self._opacity = opacity

    def set_flow(self, flow):
        self._flow = flow

    def get_radius(self):
        return self._brush_tip.radius

    def get_id(self):
        return self._idx

    def get_name(self):
        return self._name

    def set_hardness(self, hardness):
        self._brush_tip.hardness = hardness

    def get_hardness(self):
        return self._brush_tip.hardness