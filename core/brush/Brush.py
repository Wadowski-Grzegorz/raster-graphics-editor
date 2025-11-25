from core.brush.Brush_tip import Brush_tip

class Brush():
    def __init__(self, opacity=1, flow=1, spacing=0.25, size=1):
        self.opacity = opacity
        self.flow = flow
        self.spacing = spacing
        self.brush_tip = Brush_tip(size=size)

    def get_opacity(self):
        return self.opacity

    def get_size(self):
        return self.brush_tip.size

    def get_mask(self):
        return self.brush_tip.mask

    def get_spacing(self):
        return self.spacing

    def get_flow(self):
        return self.flow
