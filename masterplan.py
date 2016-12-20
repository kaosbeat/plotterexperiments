from __future__ import division
from chiplotle import *

from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")


# interesting https://en.wikipedia.org/wiki/3D_projection#Perspective_projection

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
	transforms.offset(g, (x, y))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'size':size, 'connections' : 3, 'dots' : {(size/2,0),(0,size/2),(size,size/2) } })
	plotter.write(g)

def addobject2(x,y,size):
	g = shapes.group([])
	g.append(shapes.circle(size/2))
	transforms.offset(g, (size/2,size/2))
	g.append(shapes.line((size/2,0),(size/2,size/2)))
	g.append(shapes.line((0,size/2),(size/10,size/2)))
	g.append(shapes.line((size/10*9,size/2),(size,size/2)))
	transforms.offset(g, (x, y))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'size':size, 'connections' : 3, 'dots' : {(size/2,0),(0,size/2),(size,size/2) } })
	plotter.write(g)



def connectthedots(object1,object2):
	x1 = object1.get('x') + object1.get('size')/2
	y1 = object1.get('y') + object1.get('size')/2
	x2 = object2.get('x') + object2.get('size')/2
	y2 = object2.get('y') + object2.get('size')/2
	kartelconnect((x1,y1),(x2,y2),10)
	# plotter.write(g)

def kartelconnect(p1,p2,size,log):
	#p1 = np.array([1,1])
	g = shapes.group([])
	length = np.linalg.norm(np.array(p2)-np.array(p1))
	sublength = (p2[1]-p1[1])/size
	parts = int(abs(math.floor(length/sublength)))
	partsspace = np.logspace(0.23 ,2, parts)
	partsYspace = np.linspace(p1[1], p2[1], parts+1)
	print(parts)
	for i in xrange(0,parts):
		print i
		yoffset = random.randint(0,1000)
		y1 = partsYspace[i] + yoffset
		#y1 = random.uniform(partsYspace[i]-1000,partsYspace[i]+1000)
		if (i % 2 == 0):
			y1= partsYspace[i] - yoffset
		if (log == False):
			g.append(shapes.line((i*sublength,partsYspace[i]),(i*sublength,y1)))
			g.append(shapes.line((i*sublength,y1),((i+1)*sublength,y1)))
			g.append(shapes.line(((i+1)*sublength,y1),((i+1)*sublength,partsYspace[i+1])))
	plotter.write(g)

def plot(start, end): #(left 0; bottom 0; right 16158; top 11040)
	plotter.clear()
	plotter.set_origin_center()
	# plotter.select_pen(1)
	plotter.write(shapes.rectangle(16158,11040))
	offsetx = -2000
	offsety = 0	
	kartelconnect((1000,000), (300,13000),100, False)

	# for x in xrange(1,10):
	# 	addobject2(random.randint(-8000,8000),random.randint(-5000,5000),random.randint(220,2000))
	# 	print(len(objects))
	# plotter.select_pen(2)

	# for x in xrange(0,len(objects)-1):
	#  	print(objects[x].get('x'))
	#  	connectthedots(objects[x],objects[x+1])

	io.view(plotter)


plot(0,1)
