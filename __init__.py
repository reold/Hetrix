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
        self.layer_variables = []
        self.taken_layers_for_variables = []

        for _ in range(26):
            self.layer_variables.append(KeyframeMapper(self.duration * self.fps))

        self._create_bg_image()

    def _composite(self, t):
        final_array = self.background_image

        for no, layer in enumerate(self.all_layers):

            if str(no) in self.taken_layers_for_variables:
                variables = self.layer_variables[no].mapped_values[int(t * self.fps)]
            else:
                variables = {}

            final_array = layer["data"](
                t, np.array(final_array, dtype=np.uint8), variables
            )

        final_array = cv2.cvtColor(final_array, cv2.COLOR_BGR2RGB)

        return final_array

    def render(self, name, type):
        for layer_no in self.taken_layers_for_variables:
            self.layer_variables[int(layer_no)].fill_keyframes()

        clip = mpy.VideoClip(self._composite, duration=self.duration)

        if type == "gif":
            clip.write_gif(f"{name}.gif", fps=self.fps)

    def create_keyframe(self, layer_no, frame_no, data):
        self.layer_variables[layer_no].create_key(frame_no, data)
        if str(layer_no) not in self.taken_layers_for_variables:
            self.taken_layers_for_variables.append(str(layer_no))

    def _create_bg_image(self):
        self.background_image = []

        for row in range(self.resolution[1]):

            row_data = []

            for pixel in range(self.resolution[0]):
                row_data.append(self.bg_color)

            self.background_image.append(row_data)
