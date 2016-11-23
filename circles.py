from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


import math
import random
import numpy as np
from scipy import signal

plotsize = [10, 10]

# Y = np.linspace(p1[1] ,p2[1], len(spaceX))
# #
# The parametric equation for a circle is

x = cx + r * cos(a)
y = cy + r * sin(a)

def filledcircle(cx,cy,radius,rate):

	x = np.linspace(0, 2*np.pi, rate)
	y = np.sin(x)
	print (x,", ", y)
	for i in xrange(1,100):
		print (y[i]*50)
		
	g = shapes.group([])
	for i in xrange(1,100):
		g.append(shapes.line())
		g.append(shapes.line((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius)))
	plotter.write(g)

def plot(start, end):
	plotter.select_pen(1)
	t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
	transforms.offset(t,(-2500, -plotsize[1]/2 + 200))
	plotter.write(t)
	filledcircle(0,0,1000,100)
	io.view(plotter)

plot(0,1)
