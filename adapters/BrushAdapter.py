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
    def brush_to_gui(b: Brush) -> BrushGui:
        return BrushGui(
            idx=b.get_id(),
            name=b.get_name(),
            size=b.get_size(),
            opacity=b.get_opacity(),
            flow=b.get_flow(),
            hardness=b.get_hardness()
        )

    @staticmethod
    def get_brushes_gui() -> list[BrushGui]:
        brushes = brush_manager.get_brushes()
        return [BrushAdapter.brush_to_gui(b) for b in brushes]

    @staticmethod
    def get_current_brush() -> BrushGui:
        brush = brush_manager.get_current_brush()
        return BrushAdapter.brush_to_gui(brush)


brush_adapter = BrushAdapter()