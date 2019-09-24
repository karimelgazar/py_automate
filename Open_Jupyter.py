'''  
Use The Line Below At The Beginning Of The Script
Then Save It As .bat To Open It In The Original CMD

  @py.exe E:\karim\Py_Automate\Open_Jupyter.py %*
'''
import sys
from subprocess import Popen as pop

BASE_PATH = sys.path[0]

COMMAND = "pushd %s && jupyter notebook" % BASE_PATH

pop(COMMAND, shell=True)
