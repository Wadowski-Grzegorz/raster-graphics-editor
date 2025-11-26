from core.brush.BrushTip import BrushTip

class Brush():
    def __init__(self, opacity=1, flow=1, spacing=0.25, size=1):
        self.opacity = opacity
        self.flow = flow
        self.spacing = spacing
        self.brush_tip = BrushTip(size=size)

    def get_opacity(self):
        return self.opacity

    def get_size(self):
        return self.brush_tip.size

    def get_tip(self):
        return self.brush_tip.mask

    def get_spacing(self):
        return self.spacing

    def get_flow(self):
        return self.flow

    def set_tip(self, brush_tip: BrushTip):
        self.brush_tip = brush_tip

    def set_size(self, size):
        self.brush_tip.resize(int(size))

    def set_opacity(self, opacity):
        self.opacity = opacity

    def set_flow(self, flow):
        self.flow = flow

    def get_radius(self):
        return self.brush_tip.radius