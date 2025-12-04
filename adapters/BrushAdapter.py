from PyQt6.QtGui import QPixmap, QIcon

from core.brush.Brush import Brush
from core.brush.BrushManager import brush_manager
from dto.BrushGui import BrushGui
from dto.SelectableItem import SelectableItem
import utils

class BrushAdapter:

    @staticmethod
    def brush_to_selectable(brush: Brush) -> SelectableItem:
        img = utils.np_to_q(brush.get_tip())
        icon = QIcon(QPixmap().fromImage(img))
        return SelectableItem(idx=brush.get_id(), name=brush.get_name(), icon=icon)


    @staticmethod
    def brushes_to_selectable(brushes: list[Brush]) -> list[SelectableItem]:
        return [BrushAdapter.brush_to_selectable(brush) for brush in brushes]

    @staticmethod
    def get_brushes_selectable() -> list[SelectableItem]:
        brushes = brush_manager.get_brushes()
        return BrushAdapter.brushes_to_selectable(brushes)

    @staticmethod
    def get_curr_brush():
        brush = brush_manager.get_curr_brush()
        return BrushGui(
            idx=brush.get_id(),
            name=brush.get_name(),
            size=brush.get_size(),
            opacity=brush.get_opacity(),
            flow=brush.get_flow(),
            hardness=brush.get_hardness()
        )


brush_adapter = BrushAdapter()