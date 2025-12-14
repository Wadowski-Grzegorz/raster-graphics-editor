import json

from core.brush.Brush import Brush

import resources.settings as settings


class BrushManager:
    brush_specs_path = settings.program_catalog + "\\resources\\brush\\initial_brushes.json"

    def __init__(self, context):
        self._context = context
        self._brushes = []
        self._curr_brush = None

        with open(BrushManager.brush_specs_path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        for d in data:
            self._brushes.append(
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
        self._curr_brush = self._brushes[0]


    def init(self):
        self._context.event.notify(
            'brush_current_changed',
            {
                "idx": self._curr_brush.get_idx(),
                "brush": self._curr_brush
            }
        )

    def get_brushes(self):
        return self._brushes.copy()

    def get_current_brush(self):
        return self._curr_brush

    def set_curr_brush(self, idx: int):
        brush = next((b for b in self._brushes if b.get_idx() == idx), None)
        if brush is not None:
            self._curr_brush = brush
            self._context.event.notify('brush_current_changed', {"idx": brush.get_idx(), "brush": brush})

    def set_brush_parameter(self, par_name: str, value: float | int):
        self._curr_brush.set_parameter(par_name, value)
        self._context.event.notify('brush_changed_parameter', {"idx": self._curr_brush.get_idx()})