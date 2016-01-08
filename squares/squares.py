from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
plotter.margins.hard.draw_outline()

b = 0

viewport = (10320,7920)
horizon = (viewport[0] / 2, viewport[1] / 2)

import math
import random
import numpy as np

#additive syths, 
#	plot a sine wave using a shape (circle)
#	plot a saw wave using a shape (triangle)
# 	plot the results using a combination shape
# first wave

rez = 200
size = 200
interval = 50
randpointer = 0
randpointerjump = 5
wav1 = np.linspace(0,2*np.pi,rez)
wav2 = np.linspace(0,np.pi,rez)
randwavesize = size/10
g = shapes.group([])
# help(shapes.cross)
# help(random)


def getrandompoint(wave, table, Vsize):	
	global randpointer
	# global randpointerjump
	randpointer = randpointer + random.randint(0, randpointerjump)
	if randpointer >= rez:
		randpointer = rez-1
	print randpointer
	if table == "sin":
		return (randpointer*interval, np.sin(wave[randpointer])*Vsize)
	if table == "cos":
		return (randpointer*interval, np.cos(wave[randpointer])*Vsize)


def somewaves(waves,wavtype = [],subwaves):
	for i in range(0,rez):
		# print wav1[i]
		plotter.select_pen(1)
		sq = shapes.cross(size,np.cos(wav1[i])*size)
		transforms.offset(sq, (i*interval, np.sin(wav1[i])*1500 )) 
		if waves:
			g.append(sq)
		plotter.select_pen(2)
		tr = shapes.rectangle(size,np.cos(wav1[i])*size)
		transforms.offset(tr, (i*interval, np.cos(wav1[i])*3500 )) 
		if waves:
			g.append(tr)
		plotter.select_pen(3)
		tr = shapes.circle(np.cos(wav2[i])*size)
		transforms.offset(tr, (i*interval, np.cos(wav1[i])*2500 )) 
		if waves:
			g.append(tr)

	if subwaves:
		p1 = getrandompoint(wav1, "sin", 1500)
		p2 = getrandompoint(wav1, "sin", 1500)
		print p1
		while randpointer < rez-1:
			# print randpointer
		# for i in range(int(randwavesize)):
			p2 = getrandompoint(wav1, "sin", 1500)
			l = shapes.line(p1, p2)
			g.append(l)
			p1 = p2
			p2 = getrandompoint(wav2, "cos", 2500)
			l = shapes.line(p1, p2)
			g.append(l)
			p1 = p2
			p2 = getrandompoint(wav1, "cos", 500)
			l = shapes.line(p1, p2)
			g.append(l)



somewaves(True, True)

io.view(g)





