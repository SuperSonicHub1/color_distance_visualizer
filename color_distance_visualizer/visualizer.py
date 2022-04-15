import av
import numpy as np
from typing import BinaryIO, Tuple

class Progress:
    def __init__(self, total: int):
        self.total = total
        self.amount = 0
    
    def __iadd__(self, other: int):
        self.amount += other
        print(f"{(self.amount/self.total):%}  ({self.amount}/{self.total})")
        return self

def distance(a: int, b: int) -> int:
    # RuntimeWarning: overflow encountered in ubyte_scalars
    # I don't think I can resolve this...
    return abs(a - b)

def pixel_distance(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return tuple(
        map(
            lambda x: distance(x[0], x[1]),
            zip(a, b)
        )
    )

def visualize(
    input: BinaryIO,
    output: BinaryIO,
    show_unchanged_pixels: bool = False,
    vcodec: str | None = None
):
    with av.open(input) as input:
        with av.open(output) as output:
            # Get input video frames
            input_stream: av.stream.Stream = input.streams.video[0]
            frames = tuple(input.decode(input_stream))
            
            # Copy over audio streams
            # https://pyav.org/docs/stable/cookbook/basics.html#remuxing
            for audio_input_stream in input.streams.audio:
                audio_output_stream = output.add_stream(template=audio_input_stream)
                for packet in input.demux(audio_input_stream):
                    # We need to skip the "flushing" packets that `demux` generates.
                    if packet.dts is None:
                        continue
                    packet.stream = audio_output_stream
                    output.mux(packet)

            

            progress = Progress(input_stream.frames)

            # DON'T USE `template`! IT'S BUGGED!
            # output_stream = output.add_stream(template=input_stream)
            # https://github.com/PyAV-Org/PyAV/issues/507
            # Just recreate the stream yourself.
            output_stream: av.stream.Stream = output.add_stream(
                vcodec or input_stream.codec_context.codec.name,
                rate=input_stream.base_rate
            )
            output_stream.width = input_stream.width
            output_stream.height = input_stream.height
            output_stream.pix_fmt = input_stream.pix_fmt

            input_stream_ctx = input_stream.codec_context
            height, width = input_stream_ctx.height, input_stream_ctx.width

            # Visualize color difference

            # Our first frame lacks a previous one, so we'll
            # leave it unchanged.
            for packet in output_stream.encode(frames[0]):
                output.mux(packet)
            progress += 1

            for frame, previous_frame in zip(frames[1:], frames[:-1]):
                frame_array = frame.to_rgb().to_ndarray()
                previous_array = previous_frame.to_rgb().to_ndarray()

                new_frame_array = np.zeros((height, width, 3), np.uint8)

                for y in range(height):
                    for x in range(width):
                        pixel = frame_array[y][x]
                        previous_pixel = previous_array[y][x]
                        new_pixel = np.array(
                            pixel_distance(
                                pixel,
                                previous_pixel
                            ),
                            np.uint8
                        )

                        # If our new pixel is (0, 0, 0),
                        # that means the pixel in the previous
                        # frame and in the current is the same. 
                        if show_unchanged_pixels and not np.all(new_pixel):
                            new_frame_array[y][x] = pixel
                        else:
                            new_frame_array[y][x] = new_pixel

                new_frame = av.VideoFrame.from_ndarray(new_frame_array)
                for packet in output_stream.encode(new_frame):
                    output.mux(packet)

                progress += 1

            # Flush stream
            for packet in output_stream.encode():
                output.mux(packet)
