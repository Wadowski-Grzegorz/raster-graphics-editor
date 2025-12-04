import os
import json

from core.brush.Brush import Brush


class BrushManager:
    brush_specs_path = os.path.join(os.path.dirname(__file__), "..//..//resources//brush//initial_brush.json")

    def __init__(self):
        self._brushes = None
        self._curr_brush = None

        self.fetch_brushes()

    def fetch_brushes(self):
        with open(self.brush_specs_path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        brushes = []
        for d in data:
            brushes.append(
                Brush(
                    name=d['name'],
                    size=d['size'],
                    shape=d['shape'],
                    opacity=d['opacity'],
                    flow=d['flow'],
                    spacing=d['spacing'],
                    hardness=d['hardness'],
                )
            )
        self._brushes = brushes
        self._curr_brush = self._brushes[0]

    def get_brushes(self):
        return self._brushes.copy()

    def get_curr_brush(self):
        return self._curr_brush

    def set_curr_brush(self, idx: int):
        brush = next((b for b in self._brushes if b.get_id() == idx), None)
        if brush is not None:
            self._curr_brush = brush

    def changed_brush_size(self, size: float):
        self._curr_brush.set_size(size)

    def changed_brush_opacity(self, opacity: float):
        self._curr_brush.set_opacity(opacity)

    def changed_brush_flow(self, flow: float):
        self._curr_brush.set_flow(flow)

    def changed_brush_hardness(self, hardness: float):
        self._curr_brush.set_hardness(hardness)


brush_manager = BrushManager()
