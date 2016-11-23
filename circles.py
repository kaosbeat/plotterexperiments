from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


import math
import random
import numpy as np
from scipy import signal

plotsize = [10, 10]


def plot(start, end):
	plotter.select_pen(1)
	t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
	transforms.offset(t,(-2500, -plotsize[1]/2 + 200))
	plotter.write(t)
	io.view(plotter)

plot(0,1)
