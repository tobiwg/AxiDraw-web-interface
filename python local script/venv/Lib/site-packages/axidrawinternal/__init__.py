# Bail out if python is less than 3.5
import sys
MIN_VERSION = (3, 6)
if sys.version_info < MIN_VERSION:
    sys.exit("AxiDraw software must be run with python 3.6 or greater.")
