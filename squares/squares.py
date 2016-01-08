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
from scipy import signal

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
wav3 = np.linspace(0,8*np.pi,rez)
randwavesize = size/10
g = shapes.group([])
# help(shapes.cross)
# help(random)
# print (signal.sawtooth(wav3))

def getrandompoint(wave, table, Vsize):	
	global randpointer
	# global randpointerjump
	randpointer = randpointer + random.randint(0, randpointerjump)
	if randpointer >= rez:
		randpointer = rez-1
	# print randpointer
	if table == "sin":
		return (randpointer*interval, np.sin(wave[randpointer])*Vsize)
	if table == "cos":
		return (randpointer*interval, np.cos(wave[randpointer])*Vsize)


def somewaves(waves, subwaves, wavperiod = [], wavtype = [], wavesize = [], waveshape = []):
	for idx, wav in enumerate(wavperiod):
		
		# print wav, idx, wavesize[idx]
		plotter.select_pen(random.randint(1,3))
		for i in range(0,rez):
			print(wav, wavtype[idx], wavesize[idx], waveshape[idx])
			if waveshape[idx] == "cross":
				atom = shapes.cross(size,np.cos(wav[i])*size)
			if waveshape[idx] == "rect":
				atom = shapes.cross(size,np.sin(wav[i])*size)
			if waveshape[idx] == "circle":
				atom = shapes.cross(size,signal.sawtooth(wav[i])*size)				
			if wavtype[idx] == "sin":
				transforms.offset(atom, (i*interval, np.sin(wav[idx])*wavesize[idx] )) 
			if wavtype[idx] == "cos":
				transforms.offset(atom, (i*interval, np.cos(wav[idx])*wavesize[idx] )) 
			if wavtype[idx] == "saw":
				transforms.offset(atom, (i*interval, signal.sawtooth(wav[idx])*wavesize[idx] )) 
			if waves:
				g.append(atom)


		# plotter.select_pen(2)
		# tr = shapes.rectangle(size,np.cos(wav1[i])*size)
		# transforms.offset(tr, (i*interval, np.cos(wav1[i])*3500 )) 
		# if waves:
		# 	g.append(tr)
		# plotter.select_pen(3)
		# tr = shapes.circle(np.cos(wav2[i])*size)
		# transforms.offset(tr, (i*interval, np.cos(wav1[i])*2500 )) 
		# if waves:
		# 	g.append(tr)

		if subwaves:
			p1 = getrandompoint(wav, "sin", 1500)
			p2 = getrandompoint(wav, "sin", 1500)
			# print p1
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



# somewaves(True, True, [wav1, wav2, wav3], ["sin", "saw", "saw"], [2100, 3000, 1500], ["rect", "cross", "circle"])
somewaves(True,False,[wav3],["saw"],[3000],["cross"])

io.view(g)





