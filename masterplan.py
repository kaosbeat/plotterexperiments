from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


import math
import random
import numpy as np
from scipy import signal

plotsize = [10, 10]
objects = []

#helpers
def fib(n):
    return ((1+math.sqrt(5))**n-(1-math.sqrt(5))**n)/(2**n*math.sqrt(5))

def addobject1(x,y,size):
	g = shapes.group([])
	g.append(shapes.rectangle(size,size))
	transforms.offset(g, (size/2,size/2))
	g.append(shapes.line((size/2,0),(size/2,size/2)))
	g.append(shapes.line((0,size/2),(size/10,size/2)))
	g.append(shapes.line((size/10*9,size/2),(size,size/2)))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'connections' : 3, 'size':size })
	plotter.write(g)



def plot(start, end): #(left 0; bottom 0; right 16158; top 11040)
	plotter.clear()
	plotter.set_origin_center()
	# plotter.select_pen(1)
	plotter.write(shapes.rectangle(16158,11040))
	offsetx = -2000
	offsety = 0	
	for x in xrange(1,10):
		addobject1(random.randint(16000),random.randint(10000),random.randint(2000))
	io.view(plotter)


plot(0,1)
