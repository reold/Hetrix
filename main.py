from Compositor import OpenCanvas
import cv2
from cv2 import circle, putText, FONT_HERSHEY_SIMPLEX

font = FONT_HERSHEY_SIMPLEX

canvas = OpenCanvas((500, 500), (0, 0, 255), 5, 15)

canvas.all_layers = [
    {
        "data": lambda t, f_r, f_v: putText(
            f_r,
            str(int(t * 15)),
            (int(f_v[str(int(t * 15 + 1))]["x"]), int(f_v[str(int(t * 15 + 1))]["y"])),
            font,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
    },
]

canvas.create_keyframe(1, 1, {"x": 10, "y": 30})
canvas.create_keyframe(1, 75, {"x": 400, "y": 490})

canvas.all_layers.reverse()

canvas.render("test", "gif")
