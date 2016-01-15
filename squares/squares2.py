from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
# plotter.margins.hard.draw_outline()
#plotter = instantiate_plotters( )[0]
# real plotter says
#    Drawing limits: (left 0; bottom 0; right 16158; top 11040)
pltmax = [16158, 11040]
#coords = plotter.margins.soft.all_coordinates
# plotter.select_pen(1)
b = 0

# viewport = (10320,7920)
# horizon = (viewport[0] / 2, viewport[1] / 2)

import math
import random
import numpy as np
from scipy import signal

#additive syths, 
#	plot a sine wave using a shape (circle)
#	plot a saw wave using a shape (triangle)
# 	plot the results using a combination shape
# first wave

rez = 200 #keep it below 300 unless you know what you do
size = 120
noise = size*1.5
interval = 120
randpointer = 30
randpointerjump = 2
randpointerbackrange = 0.99 #(number between 0.50-0.99)
wav1 = np.linspace(0,2*np.pi,rez)
wav2 = np.linspace(0,np.pi,rez)
wav3 = np.linspace(0,8*np.pi,rez)
randwavesize = size/10
g = shapes.group([])




def getrandompoint(wave, table, Vsize):	
	global randpointer
	# global randpointerjump
	randpointer = randpointer + int(randpointerjump*randpointerbackrange - random.randint(0, randpointerjump))
	if randpointer < 0:
		randpointer = 0
	if randpointer >= rez:
		randpointer = rez-1
	# print randpointer
	if table == "sin":
		return (randpointer*interval, np.sin(wave[randpointer])*Vsize)
	if table == "cos":
		return (randpointer*interval, np.cos(wave[randpointer])*Vsize)
	if table == "saw":
		return (randpointer*interval, signal.sawtooth(wave[randpointer])*Vsize)


def somewaves(pen,waves, subwaves, wavperiod = [], wavtype = [], wavesize = [], waveshape = []):
	global noise
	global plotter
	global g
	plotter.select_pen(pen)
	for idx, wav in enumerate(wavperiod):
		p1 = getrandompoint(wav, wavtype[idx], wavesize[idx])
		p2 = getrandompoint(wav, wavtype[len(wavtype) - 1], wavesize[len(wavtype) -1])
		# print p1
		while randpointer < rez-1:
			print randpointer
		# for i in range(int(randwavesize)):
			for w in range(len(wavtype)):
				l = shapes.line(p1, p2)
				transforms.noise(l, noise)
				g.append(l)
				p1 = p2
				p2 = getrandompoint(wav, wavtype[w], wavesize[w])

	plotter.write(g)

#somewaves(2,False, True, [wav3, wav1], ["cos", "saw", "saw", "sin", "sin"], [1500, 5100, 500, 2000, 6000], ["rect", "cross", "cross", "rect", "cross"])  

def wavesdown(pen, freq, offset, width, min, max):
	global plotter
	global g
	density = freq
	quantity = width
	g = shapes.group([])
	plotter.select_pen((pen%2)+1)
	#offset = random.randint(0, width)
	offset = density*quantity/5*3*(pen+1) + (pen%2*density/2)
	# maxheight = random.randint(min, max)
	#max = random.randint(min + 100,3000)
	g.append(shapes.line((0+offset,max),(0+offset,0)))
	
	#baseblock
	for f in range(width):
		#set height
		p1 = (f*freq + offset , max)
		p2 = (f*freq + offset, random.randint(int(min),int(max)))
		l = shapes.line(p1, p2)
		g.append(l)
		#random toppings
		if (random.randint(0,2) == 1):
			p1 = (f*freq + offset , max)
			p2 = (width/2*freq +1000 + offset, max + 500)
			l = shapes.line(p1, p2)
			g.append(l)
		#take it up
		p1 = (width/2*freq +1000 + offset, max + 500)
		p2 = (width/2*freq +1000 + offset, max +2000)
		l = shapes.line(p1, p2)
		g.append(l)


	g.append(shapes.line((freq*width,max),(freq*width,0)))
	#goffset = density*quantity/5*3*(pen+1) + (pen%2*density/2)
	#transforms.offset(g, (goffset, 0))
	plotter.write(g)

def simplelines(pen, freq, height, density, densityscale):
	global plotter
	global g
	g = shapes.group([])
	plotter.select_pen(pen+1)
	for f in range(freq):
		l = shapes.line((f*density,0),(f*(pen+1)*density/densityscale,height))
		g.append(l)
	#fitpage(g)
	plotter.write(g)

def simplelines2(pen, density, quantity, height):
	global plotter
	global g
	g = shapes.group([])
	plotter.select_pen(pen+1)
	for f in range(quantity):
		l = shapes.line(((2%(pen+1)*density/4)+quantity+f*density,0) , ((2%(pen+1)*density/4)+quantity+f*density,1000))
		#l = shapes.line((f*density,0),(f*density,height))
		g.append(l)
	#fitpage(g)
	goffset = density*quantity/2*(pen+1) + (pen%2*density/2)
	transforms.offset(g, (goffset, 0))
	plotter.write(g)

def fitpage(shape):		
	if (pltmax[0]/g.width < pltmax[1]/g.height):
		transforms.scale(shape, (pltmax[0]-100)/shape.width)
	else:
		transforms.scale(shape, (pltmax[1]-100)/shape.height)
	# print g.width, g.height
	transforms.offset(shape, (shape.width, shape.height))

size = 30
for i in range(size):
	# width = random.randint(20,30)
	width = 30
	freq= 25
	# print np.sin((wav3[int(rez/size*i)]))
	#wavesdown(i,freq,i*width*freq,width,random.randint(500,1903),3000)
	wavesdown(i+1,freq,i*width*freq,width,random.randint(0,int((np.sin((wav1[int(rez/size*i)])) +1 )*500)),(np.sin((wav1[int(rez/size*i)]))+1)*2000)
	#simplelines(i, 200, 8000, 50, 5)
	#simplelines2(i, 20, 10, 1000)

io.view(plotter)

