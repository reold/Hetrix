![HetrixGithubBannerSized (1)](https://user-images.githubusercontent.com/65646799/132937683-ba02e72d-e829-4b46-a73b-ee7cd6333273.png)

---

# 🎞Hetrix - Animation Engine

It is an **open-source animation engine** made using **Python** based on **Moviepy**

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
]

canvas.all_layers.reverse()

canvas.create_keyframe(2, 1, {"x": 10, "y": 30})
canvas.create_keyframe(2, 45), {"x": 50, "y": 50})
canvas.create_keyframe(2, 75, {"x": 400, "y": 490})

canvas.render("test", "gif")
```

# 📚API

The API is made similar to other apps available on the market. **It uses Layers which represent Objects**. These _Layers get composited into a single layer_. And gets rendered.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
