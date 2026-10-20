import cv2
import numpy as np
import os

import settings

icons_catalog = os.path.join(settings.program_catalog, "resources", "icons")
alt_icons_catalog = os.path.join(icons_catalog, "alt")
icons = [
    'menu_save.png',
    'menu_open.png',
]

for icon in icons:
    input_path = os.path.join(alt_icons_catalog, icon)
    img = cv2.imdecode(np.fromfile(input_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None:
        continue

    img[:, :, :3] = (204, 204, 206)

    success, encoded = cv2.imencode(".png", img)
    if not success:
        continue

    output_path = os.path.join(icons_catalog, icon)
    encoded.tofile(output_path)