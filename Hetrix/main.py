from .settings import *

background_image = []
background_color = [31, 36, 40]
background_color.reverse()
width = height = 500

for row in range(height):

    row_data = []

    for pixel in range(width):
        row_data.append(background_color)

    background_image.append(row_data)


all_layers = []
layer_variables = {}

for row in range(0, 5):
    print(row)
    for c in range(5):
        all_layers.append(
            {
                "data": lambda t, f_r, f_v: cv2.circle(
                    f_r,
                    (
                        ((f_v["c"] - int(f_v["c"] / (t + 1))) * 100) + 30 + 15,
                        (100 * f_v["row"]) + 50,
                    ),
                    int(30),
                    (0, 0, 255),
                    thickness=-1,
                )
            }
        )

        layer_variables[str(len(all_layers))] = {
            "c": c,
            "row": row,
        }

# all_layers.reverse()


def composite(t):
    final_array = background_image

    for no, layer in enumerate(all_layers, start=1):
        variable_table = {}
        try:
            if layer_variables[str(no)]:
                variable_table = layer_variables[str(no)]
        except:
            pass

        final_array = layer["data"](
            t, np.array(final_array, dtype=np.uint8), variable_table
        )

    final_array = cv2.cvtColor(final_array, cv2.COLOR_BGR2RGB)

    return final_array


clip = mpy.VideoClip(composite, duration=2)  # 2 seconds
clip.write_gif("circle.gif", fps=15)

clip.write_videofile("circle_amazing", fps=15)
