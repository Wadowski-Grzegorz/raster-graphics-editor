from core.brush.BrushManager import BrushManager
from core.layer.LayerManager import LayerManager
from core.tool.CoreToolManager import CoreToolManager


class CoreApp:
    def __init__(self, event_provider):
        self.event_provider = event_provider
        self.brush = BrushManager(event_provider)
        self.layer = LayerManager(event_provider)
        self.tool = CoreToolManager(event_provider)

