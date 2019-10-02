from jupyterthemes import jtplot
from IPython.core.interactiveshell import InteractiveShell

jtplot.style(theme='onedork', context='notebook', ticks=True, grid=False)
InteractiveShell.ast_node_interactivity = "all"
line = '%'*80
