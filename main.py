from Hetrix import OpenCanvas
import cv2
from cv2 import circle, putText, FONT_HERSHEY_SIMPLEX

font = FONT_HERSHEY_SIMPLEX

duration, fps = 5, 60
canvas = OpenCanvas((500, 500), (0, 0, 255), duration, fps)

canvas.all_layers = [
    {
        "data": lambda t, f_r, f_v: putText(
            f_r,
            str(int(t * 15)),
            (int(f_v["x"]), int(f_v["y"])),
            font,
            1,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
    },
    {
        "data": lambda t, f_r, f_v: circle(
            f_r,
            (int(f_v["x"]), int(f_v["y"])),
            30,
            (0, 0, 255),
            thickness=-1,
        )
    },
]

canvas.all_layers.reverse()

canvas.create_keyframe(2, 1, {"x": 10, "y": 30})
canvas.create_keyframe(2, int((duration * fps) / 2), {"x": 50, "y": 50})
canvas.create_keyframe(2, int(duration * fps), {"x": 400, "y": 490})
canvas.create_keyframe(1, 1, {"x": 0, "y": 0})
canvas.create_keyframe(1, int(duration * fps), {"x": 500, "y": 500})

canvas.render("test", "gif")
print(int((duration * fps) / 2))
