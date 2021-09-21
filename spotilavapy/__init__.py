import sys
assert sys.version_info[0] == 3
from spotilavapy.spotilava import SpotiLava
from spotilavapy.exceptions import Forbidden, NotFound, InvalidPlayer

__author__ = "Lysander12"
__url__ = "https://github.com/xlysander12/spotilava.py"
__description__ = "A Python wrapper that converts spotify songs to be played through LavaLink"
__license__ = "MIT"
__version__ = "1.0.0"