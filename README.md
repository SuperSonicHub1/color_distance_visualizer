# Color Distance Visualizer

The purpose of this project is hard to describe outside of
"visaulize the color distance of pixels between frames," so just go
to the `examples/` folder already.

Generating a 30-second video will likely take a while due
to Python being slow and my code being unoptimized, so get
something to drink and a bite to eat while you wait.

## Installation
Standard `git clone`, `cd`, and `poetry install`.

## Example Credits
The base for `test_video_viz.mp4` series was generated with the following FFmpeg command:
```bash
ffmpeg -f lavfi -i mandelbrot -vf "format=yuv444p,split=4[a][b][c][d],[a]waveform[aa],[b][aa]vstack[V],[c]waveform=m=0[cc],[d]vectorscope=color4[dd],[cc][dd]vstack[V2],[V][V2]hstack" -r 60 -t 1 test_video.mp4
```

The base for the series of `stress` videos comes from
[the Dorkly video *NOT LOFI METAL BEATS TO STRESS/CRAM TO*](https://www.youtube.com/watch?v=wPSWsz2R6Xc).

## Usage
Run `python -m color_distance_visualizer --help` for the most up-to-date help.
```
usage: color_distance_visualizer [-h] [--show-unchanged-pixels]
                                 [--vcodec VCODEC] [--version]
                                 input output

Visualize color distance.

positional arguments:
  input                 The video that we want to analyze.
  output                Where we want to save the output.

options:
  -h, --help            show this help message and exit
  --show-unchanged-pixels
                        For pixels that haven't changed, display the pixel
                        from the orginal frame instead of black.
  --vcodec VCODEC       What codec you want the output to be saved in. FFV1 is
                        the recommended lossless codec. Using lossy codecs
                        like MPEG-4 will result in significant loss of detail.
                        (default: codec of input)
  --version             show program's version number and exit
```
