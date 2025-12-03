import os
import json

class BrushManager:
    brush_specs_path = os.path.join(os.path.dirname(__file__), "..//..//resources//brush//initial_brush.json")

    def __init__(self):
        brushes = self._init()

    def _init(self):
        with open(self.brush_specs_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        return data


a = BrushManager()
