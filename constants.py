import os
from Vector import *

# FIXED CONSTANTS
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
VIRTUAL_SIZE = Vector(1280, 720)

# CHANGEABLE CONSTANTS
SAMPLES = 4				# anti-aliasing