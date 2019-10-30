#The Script Should Be Added To 
#C:\Users\karim\.ipython\profile_default\startup



# To make the plot background DARK

from jupyterthemes import jtplot
from IPython.core.interactiveshell import InteractiveShell

jtplot.style(theme='onedork', context='notebook', ticks=True, grid=False)
InteractiveShell.ast_node_interactivity = "all"


# %matplotlib notebook

# %config InlineBackend.figure_format = 'retina' 
# this magic command above make plot in high resolution
# use it just below %matplotlib notebook


"""
********************* VERY IMPORTANT *********************

How to get more space for your plots in the Jupyter notebook:

Jupyter has a nice feature that automatically converts long outputs into a
box with a scrollbar. Unfortunately many times you don’t actually want it,
especially when you want to compare several plots.

One way to disable the feature is to put the following in a separate cell
and run it before you run the cell that generates long output

####################################################
%%javascript

 IPython.OutputArea.prototype.should_scroll = function(lines){
     return false;
}
####################################################

"""
