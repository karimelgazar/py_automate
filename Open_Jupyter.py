import sys
from subprocess import Popen as pop

BASE_PATH = sys.path[0]

COMMAND = "pushd %s && jupyter notebook" % BASE_PATH

pop(COMMAND, shell=True)
