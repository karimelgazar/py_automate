import sys
from subprocess import Popen as pop

BASE_PATH = sys.path[0]
ORIGINAL_JUPYTER_THEME = 'jt -r '
DARK_THEME = 'jt -t onedork -fs 140 -altp -tfs 150 -dfs 120 -ofs 120 -nfs 115 -cellw 88% -T'
# COMMAND = "pushd %s && %s && jupyter notebook" % (BASE_PATH, DARK_THEME)
COMMAND = "pushd %s && jupyter notebook" % BASE_PATH
pop(COMMAND, shell=True)
