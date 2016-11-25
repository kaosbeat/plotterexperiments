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



def filledcircle(cx,cy,radius,rate):

	a = np.linspace(0, 2*np.pi, rate)
	# y = np.sin(x)
	# print (a)
	# for i in xrange(1,100):
	# 	print (y[i]*50)
		
	g = shapes.group([])
	for i in xrange(1,rate):
		# print((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius))
		# g.append(shapes.line())
		# g.append(shapes.line((x[i-1]*radius,y[i]*radius),(x[i]*radius, y[i]*radius)))
		# g.append(shapes.line(
		# 	( cx + radius * np.cos(a[i-1]) , cy + radius * np.sin(a[i-1]) ),
		# 	( cx + radius * np.cos(a[i]),cy + radius * np.sin(a[i]) )))
		#figure out how to get point at certin y-value
		# x^2 + y^2 = r^2
		x0 = cx + radius * np.cos(a[i-1])
		# y0 = np.sqrt(radius^2 - int(x0)^2)
		y0 = np.sqrt(radius**2 - x0**2)

		# x1 = np.sqrt(radius^2 - y0^2)

		g.append(shapes.line((x0,y0),(-x0,y0)))
		g.append(shapes.line((x0,-y0),(-x0,-y0)))
	plotter.write(g)


def takeawalk(size):
	g = shapes.group([])
	# for x in xrange(1,10):
	g.append(shapes.bezier_path([(0,0),(500,0)], 0.5,1))
	plotter.write(g)

def takeacirclewalk(steps):
	g = shapes.group([])
	g.append(shapes.random_walk_polar(steps, step_size=1000))
	plotter.write(g)

def plot(start, end):
	plotter.select_pen(1)
	t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
	transforms.offset(t,(-2500, -plotsize[1]/2 + 200))
	plotter.write(t)
	filledcircle(0,0,1000,50)
	takeawalk(80)
	io.view(plotter)

plot(0,1)
