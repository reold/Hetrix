![Hetrix Logo Large](https://user-images.githubusercontent.com/65646799/145385431-bef31636-948e-494d-9d49-38e2446ee857.png)

---

# 🎞Hetrix - Animation Engine

It is an **open-source animation engine** made using **Python** based on **Moviepy**
###### This is the python library version of Hetrix, to see the front-end source code, go to [HetrixWeb Github page](https://github.com/reold/hetrixWeb)
## 🔽 Installation

Clone the repository and use the module

## 💊 Usage

For a brief introduction to Hetrix, please refer the tutorials in the documentation.

#### 🦴 Barebones(template)

Create `main.py` in the root

```python
from Hetrix import OpenCanvas
from cv2 import putText

duration, fps = 5, 15
canvas_size, canvas_color = (500, 500), (0, 0, 255)
canvas = OpenCanvas(canvas_size, canvas_color, duration, fps)

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
]


canvas.create_keyframe(0, 1, {"x": 10, "y": 30})
canvas.create_keyframe(0, 45, {"x": 50, "y": 50})
canvas.create_keyframe(0, 75, {"x": 400, "y": 490})

canvas.render("test", "gif")
```

# 📚API

The API is made similar to other apps available on the market. **It uses Layers which represent Objects**. These _Layers get composited into a single layer_. And gets rendered.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
