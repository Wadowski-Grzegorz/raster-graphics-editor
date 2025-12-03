import numpy as np

arr = np.array([[[1, 2, 3, -1], [0, 0, 0, 0], [4, 5, 6, 7]],
                [[0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 2, 2]],
                [[-1, -2, -3, -4], [5, 5, 5, 5], [1, 1, 1, 1]]])


opacity = 0.4
where_is_painted = (self.temp_layer.sum(axis=2) > 0).astype(np.float32) # 2D array

real_opacity = (self.temp_layer[:, :, 3].astype(np.float32) * opacity * where_is_painted) / 255. # 2D array
real_opacity = real_opacity[:, :, None]

self.layers[self.curr_idx][:] = (
        self.layers[self.curr_idx].astype(np.float32) * (1 - real_opacity) +
        self.temp_layer.astype(np.float32) * real_opacity
).astype(np.uint8)