import resources.settings as settings
import numpy as np

def get_cut_as(orig, example, orig_pos):
    h, w = get_borders_as(example, orig_pos)
    return orig[h[0]: h[1], w[0]: w[1]]

def get_borders_as(example, orig_pos):
    ex_h, ex_w = example.shape[:2]
    pos_x, pos_y = orig_pos
    start_h, start_w = abs(pos_y), abs(pos_x)
    return (start_h, start_h + ex_h), (start_w, start_w + ex_w)

def replace(orig, matrix, orig_pos):
    h, w = get_borders_as(matrix, orig_pos)
    if matrix.ndim == 2:
        orig[h[0]: h[1], w[0]: w[1], 3] = matrix
    if matrix.ndim == 3:
        orig[h[0]: h[1], w[0]: w[1], :3] = matrix

def get_intersection(orig, orig_pos):
    # returns intersection of temp_layer and orig_layer
    orig_h, orig_w = orig.shape[:2]
    pos_x, pos_y = orig_pos

    world_start_h = max(0, pos_y)
    world_start_w = max(0, pos_x)
    world_end_h = min(settings.layer_height, orig_h + pos_y)
    world_end_w = min(settings.layer_width, orig_w + pos_x)

    temp_range = ((world_start_h, world_end_h), (world_start_w, world_end_w))
    orig_range = ((world_start_h - pos_y, world_end_h - pos_y), (world_start_w - pos_x, world_end_w - pos_x))

    return orig_range, temp_range

def base_move(on_press, start_x, start_y, end_x, end_y, layer, temp_layer, brush, color):
    # check which value has more to grow
    dx = abs(end_x - start_x)
    dy = abs(end_y - start_y)

    # steps - how many pixel to color
    steps = dx if dx >= dy else dy
    step_x = dx / steps if end_x >= start_x else -dx / steps
    step_y = dy / steps if end_y >= start_y else -dy / steps

    brush_radius = brush.get_radius()
    spacing = brush.get_spacing()

    space = (brush_radius * spacing)
    points = np.arange(0, steps, space)
    for i in points:
        a = start_x + step_x * i
        b = start_y + step_y * i
        on_press(int(a), int(b), layer, temp_layer, brush, color)

def get_brush_cut(brush, x, y):
    brush_radius = brush.get_radius()

    brush_y_s = max(y - brush_radius, 0)
    brush_y_e = min(y + brush_radius, settings.layer_height)
    brush_x_s = max(x - brush_radius, 0)
    brush_x_e = min(x + brush_radius, settings.layer_width)

    return (brush_x_s, brush_x_e), (brush_y_s, brush_y_e)
    
def cut_mask(brush, brush_x, brush_y, x, y):
    brush_radius = brush.get_radius()
    mask = brush.get_tip().astype(np.float32) / 255.0

    mask_y_s = max(brush_radius - y, 0)
    mask_y_e = mask_y_s + (brush_y[1] - brush_y[0])
    mask_x_s = max(brush_radius - x, 0)
    mask_x_e = mask_x_s + (brush_x[1] - brush_x[0])

    mask = mask[mask_y_s:mask_y_e, mask_x_s:mask_x_e]
    
    return mask