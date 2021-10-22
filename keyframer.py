import sys


class KeyframeMapper:
    def __init__(self, total_frames):
        self.mapped_values = [{} for _ in range(total_frames)]
        self.no_keyframes = 0
        self.started_maping = False

    def create_key(self, frame_no, data):
        self.no_keyframes += 1
        data["s"] = True
        self.mapped_values[frame_no] = data

    def fill_keyframes(self):
        a_frame_no = a_value = False
        b_frame_no = b_value = False

        for keyframe_no, keyframe in enumerate(self.mapped_values):
            if keyframe != {}:
                if not a_frame_no and not a_value:
                    # a is not defined
                    a_frame_no = keyframe_no
                    a_value = keyframe

                elif not b_frame_no and not b_value:
                    # b is not defined
                    b_frame_no = keyframe_no
                    b_value = keyframe

                    # everything is defined
                    for key in list(keyframe.keys()):
                        if key != "s":
                            for frame_no in range(a_frame_no + 1, b_frame_no):
                                linear_value = self.linear_framer(
                                    a_frame_no,
                                    a_value[key],
                                    b_frame_no,
                                    b_value[key],
                                    frame_no,
                                )
                                self.mapped_values[frame_no][key] = linear_value

                    # After a&b keyframing is done
                    a_frame_no, a_value = b_frame_no, b_value
                    b_frame_no = b_value = False

    def linear_framer(self, a_frame_no, a_value, b_frame_no, b_value, val_frame_no):
        # y = mx + c

        if a_frame_no == b_frame_no:
            slope = sys.maxsize
        else:
            slope = (b_value - a_value) / (b_frame_no - a_frame_no)

        val_value = a_value + (slope * (val_frame_no - a_frame_no))

        return int(val_value)
