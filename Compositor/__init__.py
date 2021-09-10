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
                keys = []

                for frame_itr in range(no_frames):
                    print("I")
                    keys.append(
                        {
                            "frame": int(list(layer.keys())[frame_itr]),
                            "data": layer[str(list(layer.keys())[frame_itr])],
                        }
                    )

                print(keys)

                for key_itr in range(len(keys) - 1):
                    a_key, b_key = keys[key_itr], keys[key_itr + 1]
                    print(f"A: {a_key} B: {b_key}")

                    slope_value_x = int(b_key["data"]["x"]) - int(a_key["data"]["x"])
                    slope_value_y = int(b_key["data"]["y"]) - int(a_key["data"]["y"])
                    slope_value_x = slope_value_x / (
                        int(b_key["frame"]) - int(a_key["frame"]) - 1
                    )
                    slope_value_y = slope_value_y / (
                        int(b_key["frame"]) - int(a_key["frame"]) - 1
                    )
                    print(f"X SLOPE Value: {slope_value_x}")
                    print(f"Y SLOPE Value: {slope_value_y}")
                    for frame_itr in range(b_key["frame"] - a_key["frame"] - 1):
                        frame_itr += int(a_key["frame"]) + 1
                        layer[str(frame_itr)] = {
                            "x": a_key["data"]["x"]
                            + slope_value_x * (frame_itr - int(a_key["frame"]) - 1),
                            "y": a_key["data"]["y"]
                            + slope_value_y * (frame_itr - int(a_key["frame"]) - 1),
                        }

                # last_data = NotImplemented
                # for frame_itr in range(self.fps * self.duration):
                #     frame_itr += 1
                #     try:

                #         temp = layer[str(frame_itr)]
                #         last_data = temp

                #     except:

                #         print("Not found")
                #         layer[str(frame_itr)] = last_data

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
