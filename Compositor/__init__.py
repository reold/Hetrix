from .settings import *

# from .main import *


class OpenCanvas:
    def __init__(self, resolution_dim, bg_color, duration, fps) -> None:
        """
        # Create a new Canvas:
        --- \n

        ```python
        resolution_dim = (int, int) # height, width of all frames
        bg_color = (int, int, int) # background color of all frames, RGB values
        duration = int # duration of the clip
        fps = int # frames per second of the clip
        ```
        ## Example:
        --- \n
        ```python
        OpenCanvas((500, 500), (0, 0, 255), 5, 15)
        ```

        """
        self.resolution = resolution_dim
        self.bg_color = bg_color[::-1]
        self.duration = duration
        self.fps = fps
        self.all_layers = []
        self.layer_variables = {}
        self._create_bg_image()

    def _composite(self, t):
        final_array = self.background_image

        for no, layer in enumerate(self.all_layers, start=1):
            variable_table = {}
            try:
                if self.layer_variables[str(no)]:
                    variable_table = self.layer_variables[str(no)]
            except:
                pass

            final_array = layer["data"](
                t, np.array(final_array, dtype=np.uint8), variable_table
            )

        final_array = cv2.cvtColor(final_array, cv2.COLOR_BGR2RGB)

        return final_array

    def render(self, name, type):
        self._normalize_frame_vars()
        print(self.layer_variables)
        clip = mpy.VideoClip(self._composite, duration=self.duration)

        if type == "gif":
            clip.write_gif(f"{name}.gif", fps=self.fps)

    def create_keyframe(self, layer_no, frame, props):
        self._create_frame_var(layer_no, frame, props)
        print(self.layer_variables)

    def _create_frame_var(self, layer_no, frame, data):
        try:
            self.layer_variables[str(layer_no)][str(frame)] = data
        except:
            self.layer_variables[str(layer_no)] = {}
            self.layer_variables[str(layer_no)][str(frame)] = data

    def _normalize_frame_vars(self):
        for layer_itr in range(len(self.all_layers)):
            layer_itr += 1
            layer = self.layer_variables[str(layer_itr)]
            print(f"Layer {layer_itr}")

            no_frames = len(layer)

            if no_frames > 1:
                key1, key2 = 0, 0
                key1_data, key2_data = NotImplemented, NotImplemented
                for frame_itr in range(no_frames):
                    print("I")
                    if not key1:
                        key1 = str(list(layer.keys())[frame_itr])
                        key1_data = layer[str(list(layer.keys())[frame_itr])]

                    elif not key2:
                        key2 = str(list(layer.keys())[frame_itr])

                        key2_data = layer[str(list(layer.keys())[frame_itr])]

                print(key1, key2)
                print(key1_data, key2_data)

                slope_value = int(key2_data["x"]) - int(key1_data["x"])
                slope_value_y = int(key2_data["y"]) - int(key1_data["y"])
                slope_value = slope_value / (
                    int(key2_data["x"]) - int(key1_data["x"]) - 1
                )
                slope_value_y = slope_value_y / (
                    int(key2_data["y"]) - int(key1_data["y"]) - 1
                )
                print(f"SLOPE Value: {slope_value}")
                print(f"Y SLOPE Value: {slope_value_y}")
                for frame_itr in range(int(key2) - int(key1) - 1):
                    frame_itr += int(key1) + 1
                    layer[str(frame_itr)] = {
                        "x": key1_data["x"] + slope_value * frame_itr,
                        "y": key1_data["y"] + slope_value_y * frame_itr,
                    }

                last_data = NotImplemented
                for frame_itr in range(self.fps * self.duration):
                    frame_itr += 1
                    try:

                        temp = layer[str(frame_itr)]
                        last_data = temp

                    except:

                        print("Not found")
                        layer[str(frame_itr)] = last_data

            else:
                frame_data = self.layer_variables[str(layer_itr)]
                keys_in_layer = list(frame_data.keys())
                frame_data = frame_data[str(keys_in_layer[0])]
                for frame_itr in range(self.duration * self.fps):
                    self.layer_variables[str(layer_itr)][str(frame_itr)] = frame_data

    def _create_layer_var(self, layer_no, data):
        self.layer_variables[str(layer_no)] = data

    def _create_bg_image(self):
        self.background_image = []

        for row in range(self.resolution[1]):

            row_data = []

            for pixel in range(self.resolution[0]):
                row_data.append(self.bg_color)

            self.background_image.append(row_data)
