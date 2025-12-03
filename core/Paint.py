import numpy as np
from PyQt6.QtCore import pyqtSlot

from core.brush.Brush import Brush
from data.DataCenter import data_center

import settings

class Paint():
    def __init__(self):
        super().__init__()

        self.layers = {} # as numpy
        self.curr_idx = None
        self.temp_layer = None # as numpy

        self.curr_brush = Brush(size=10, opacity=1)

    def paint_masking(self, x, y, brush_color: np.ndarray):
        brush_radius = self.curr_brush.get_radius()

        img_y_s = max(y - brush_radius, 0)
        img_y_e = min(y + brush_radius, settings.layer_height)
        img_x_s = max(x - brush_radius, 0)
        img_x_e = min(x + brush_radius, settings.layer_width)

        # Wycinamy region temp_layer (RGBA)
        paint_image = self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        # Maska 0..1
        mask = self.curr_brush.get_tip().astype(np.float32) / 255.0

        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + (img_y_e - img_y_s)
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + (img_x_e - img_x_s)

        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]

        # Maska wpływa TYLKO NA ALFA
        flow = self.curr_brush.get_flow()
        alpha_add = (mask * flow * 255.0).astype(np.float32)

        # -----------------------------
        # RGB: kolor nakładamy 1:1 (bez maski)
        # -----------------------------
        paint_image[..., :3] = brush_color[:3]

        # -----------------------------
        # ALPHA: dodajemy maskę
        # -----------------------------
        current_alpha = paint_image[..., 3]
        new_alpha = current_alpha + alpha_add
        paint_image[..., 3] = np.clip(new_alpha, 0, 255)

        # Zapis do temp layer
        self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e] = paint_image.astype(np.uint8)

    def paint_maskingn(self, x, y, brush_color: np.ndarray):
        brush_radius = self.curr_brush.get_radius()

        # Obliczamy granice, w których malujemy na obrazie
        img_y_s, img_y_e = max(y - brush_radius, 0), min(y + brush_radius, settings.layer_height)
        img_x_s, img_x_e = max(x - brush_radius, 0), min(x + brush_radius, settings.layer_width)

        # Wycinamy fragment obrazu, na którym będziemy malować
        paint_image = self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e].astype(np.float32)

        # Pobieramy maskę i przekształcamy ją na zakres [0, 1]
        mask = self.curr_brush.get_tip().astype(np.float32) / 255.

        # Dopasowujemy maskę do obszaru malowania
        mask_y_s = max(brush_radius - y, 0)
        mask_y_e = mask_y_s + img_y_e - img_y_s
        mask_x_s = max(brush_radius - x, 0)
        mask_x_e = mask_x_s + img_x_e - img_x_s

        # Dopasowanie maski do odpowiednich wymiarów
        mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]

        # Rozszerzamy maskę do 3 kanałów RGB i 1 kanału alfa
        # Jeżeli maska ma wartości tylko dla RGB, ustawiamy kanał alfa na 1 (pełna przezroczystość)
        mask_rgb = np.stack([mask] * 3, axis=-1)  # Zmienia maskę 2D na 3D (h, w, 3)
        mask_alpha = mask[:, :, None]  # Rozszerzamy maskę do kształtu (h, w, 1) dla alfa
        mask_rgba = np.concatenate([mask_rgb, mask_alpha], axis=-1)  # Łączymy maskę RGB + Alfa

        # Używamy przepływu (flow) do dostosowania intensywności maski
        adjusted_mask = mask_rgba * self.curr_brush.get_flow()

        # Mieszamy kolor z obrazem w zależności od maski i przepływu
        paint_image = paint_image * (1 - adjusted_mask) + brush_color * adjusted_mask

        # Zaktualizuj temp_layer w wybranym obszarze
        self.temp_layer[img_y_s:img_y_e, img_x_s:img_x_e] = paint_image.astype(np.uint8)

    def paint_masking_line(self, start_x, start_y, end_x, end_y, brush_color):
        # ----- calculating pixel position -----
        # check which value has more to grow
        dx = abs(end_x - start_x)
        dy = abs(end_y - start_y)

        # steps - how many pixel to color
        steps = dx if dx >= dy else dy
        step_x = dx / steps if end_x >= start_x else -dx / steps
        step_y = dy / steps if end_y >= start_y else -dy / steps

        brush_radius = self.curr_brush.get_radius()
        spacing = self.curr_brush.get_spacing()

        space = (brush_radius * spacing)
        points = np.arange(0, steps, space)
        for i in points:
            a = start_x + step_x * i
            b = start_y + step_y * i
            self.paint_masking(int(a), int(b), brush_color)

    def blend(self):
        opacity = self.curr_brush.get_opacity()

        # Gdzie pędzel faktycznie dotknął (żeby uniknąć smug alpha = 0)
        where_is_painted = (self.temp_layer.sum(axis=2) > 0).astype(np.float32)

        # Realna przezroczystość pędzla (0–1)
        real_opacity = (self.temp_layer[:, :, 3].astype(np.float32) *
                        where_is_painted *
                        opacity) / 255.0
        real_opacity_3 = real_opacity[:, :, None]  # do RGB

        dst = self.layers[self.curr_idx].astype(np.float32)
        src = self.temp_layer.astype(np.float32)

        # RGB blendowane klasycznie
        out_rgb = dst[..., :3] * (1 - real_opacity_3) + src[..., :3] * real_opacity_3

        # -------------------------------
        # Alpha: TYLKO dodajemy wartość z temp
        # -------------------------------
        dst_a = dst[..., 3]
        src_a = (src[..., 3] * opacity * where_is_painted).astype(np.float32)

        out_a = dst_a + src_a
        out_a = np.clip(out_a, 0, 255)  # zabezpieczenie aby nie wyjść poza zakres uint8

        # Zapis wyniku do warstwy
        self.layers[self.curr_idx][..., :3] = out_rgb.astype(np.uint8)
        self.layers[self.curr_idx][..., 3] = out_a.astype(np.uint8)

        # Wyczyść temp layer
        self.temp_layer.fill(0)

    def blendo(self):
        opacity = self.curr_brush.get_opacity()

        # check where were something drawn
        where_is_painted = (self.temp_layer.sum(axis=2) > 0).astype(np.float32)
        # multi = (where_is_painted[:, :, None] * opacity)
        # self.layers[self.curr_idx][:] = (self.layers[self.curr_idx].astype(np.float32) * multi).astype(np.uint8)
        # self.temp_layer[:] = (self.temp_layer.astype(np.float32) * multi).astype(np.uint8)

        real_opacity = opacity * where_is_painted

        # mask is [a, b] while image is [a, b, 4], so resize with None
        real_opacity = real_opacity[:, :, None]

        self.layers[self.curr_idx][:] = (
                self.layers[self.curr_idx].astype(np.float32) * (1 - real_opacity)+
                self.temp_layer.astype(np.float32) * real_opacity
        ).astype(np.uint8)

        self.temp_layer.fill(0)


    def set_curr_idx(self, idx: int):
        self.curr_idx = idx

    def added_new_layer(self, layer: np.ndarray, idx: int):
        self.layers[idx] = layer
        self.set_curr_idx(idx)

    def added_temp_layer(self, layer: np.ndarray):
        self.temp_layer = layer

    @pyqtSlot()
    def changed_layer(self):
        idx = data_center.get_idx()
        self.set_curr_idx(idx)

    def changed_brush_size(self, size: float):
        self.curr_brush.set_size(size)

    def changed_brush_opacity(self, opacity: float):
        self.curr_brush.set_opacity(opacity)

    def changed_brush_flow(self, flow: float):
        self.curr_brush.set_flow(flow)