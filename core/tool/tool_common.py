import resources.settings as settings

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