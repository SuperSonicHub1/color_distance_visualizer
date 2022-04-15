from argparse import ArgumentParser, FileType
from .visualizer import visualize
from color_distance_visualizer import __version__

parser = ArgumentParser(prog="color_distance_visualizer", description='Visualize color distance.')

parser.add_argument(
    'input',
    type=FileType('rb'),
    help="The video that we want to analyze."
)
parser.add_argument(
    'output',
    type=FileType('wb'),
    help="Where we want to save the output.",
)
parser.add_argument(
    '--show-unchanged-pixels',
    action='store_true',
    help="For pixels that haven't changed, display the pixel from the orginal frame instead of black.",
)
parser.add_argument(
    '--vcodec',
    default=None,
    help="What codec you want the output to be saved in. FFV1 is the recommended lossless codec. Using lossy codecs like MPEG-4 will result in significant loss of detail. (default: codec of input)"
)
parser.add_argument(
    '--version',
    action='version',
    version='%(prog)s ' + __version__
)

args = parser.parse_args()

visualize(
    args.input,
    args.output,
    show_unchanged_pixels=args.show_unchanged_pixels,
    vcodec=args.vcodec,
)
