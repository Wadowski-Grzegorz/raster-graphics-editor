from core.brush.BrushManager import BrushManager
from core.layer.LayerManager import LayerManager
from core.tool.CoreToolManager import CoreToolManager


class CoreApp:
    def __init__(self, event):
        self.event = event
        self.brush = BrushManager(event)
        self.layer = LayerManager(event)
        self.tool = CoreToolManager(event)

