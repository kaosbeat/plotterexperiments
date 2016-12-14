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
	transforms.offset(g, (x, y))
	objects.append({'class': 'obj1', 'x': x, 'y': y, 'size':size, 'connections' : 3, 'dots' : {(size/2,0),(0,size/2),(size,size/2) } })
	plotter.write(g)

def connectthedots(object1,object2):
	x1 = object1.get('x') + object1.get('size')/2
	y1 = object1.get('y') + object1.get('size')/2
	x2 = object2.get('x') + object2.get('size')/2
	y2 = object2.get('y') + object2.get('size')/2
	g = shapes.group([])
	g.append(shapes.line((x1,y1),(x2,y2)))
	plotter.write(g)

def kerstboom(xpos,ypos,jump,size,number):
	for i in xrange(1,number):
		y = -i*i*size*jump
		x = i*size+jump*jump
		g = shapes.group([])
		g.append(shapes.line((-x,y),(x,y)))
		plotter.write(g)



def plot(start, end): #(left 0; bottom 0; right 16158; top 11040)
	plotter.clear()
	plotter.set_origin_center()
	# plotter.select_pen(1)
	plotter.write(shapes.rectangle(16158,11040))
	offsetx = -2000
	offsety = 0	
	plotter.select_pen(2)
	#chiplotle.geometry.shapes.label(text, charwidth, charheight, charspace=None, linespace=None, origin='bottom-left')
	t = shapes.label("Merel", 1, 1)
	transforms.offset(t,(500, -200))
	plotter.write(t)
	plotter.select_pen(3)
	kerstboom(1000,1000,1.4,50,80)

	for x in xrange(1,10):
		addobject1(random.randint(-8000,8000),random.randint(-5000,5000),random.randint(220,2000))
		print(len(objects))
	plotter.select_pen(2)

	for x in xrange(0,len(objects)-1):
	 	print(objects[x].get('x'))
	 	connectthedots(objects[x],objects[x+1])

	io.view(plotter)


plot(0,1)
