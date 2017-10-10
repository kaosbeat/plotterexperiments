##emacs instructions
## C-c C-c evaluates whole file


from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label

import random
import math

# import pickle
# from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
# from texttools import *

plotter = instantiate_virtual_plotter(type="DXY1300")
# plotter = instantiate_plotters( )[0]
pltmax = [10320, 7920]
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
# plotunits = (10320/432, 7920/297)
# print plotunits
plotter.select_pen(1)
# plotter.margins.hard.draw_outline()




objects = []
def addAndPlotObject(soort, x, y, size, maxsize, data):
	# g = shapes.group([])
	if (soort == 'text'):
		g = Label(str(data.encode('utf-8')), size, size)
		# check https://github.com/drepetto/chiplotle/blob/master/chiplotle/hpgl/label.py
	transforms.offset(g, (x, y))
	if (g.width > maxsize):
		transforms.scale(g, maxsize/g.width)
	objects.append({'class': soort, 'x': x, 'y': y, 'size':size, 'data': data })
	plotter.write(g)




def plotSquare(size,x,y,depth, random):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.rectangle(size, size))
		# transforms.rotate(t, random.randint(0,30))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)

def plotCircles(size, x, y, depth, rdm):
        '''
        circles get drawn in a certain SIZE at X,Y with a recursion of DEPTH and random range of RDM
        '''
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.circle(size/depth*d))
		transforms.offset(t, (random.randint(0,rdm),0))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)

def plotPolygons(size, x, y, depth, rdm):
	g = shapes.group([])
	for d in xrange(1,depth):
		t = shapes.group([])
		t.append(shapes.symmetric_polygon_side_length(depth,size/depth*d))
		transforms.offset(t, (random.randint(0,rdm),random.randint(0,rdm)))
		g.append(t)
	print ("offsetting" + str(x))
	transforms.offset(g,(x,y))
	plotter.write(g)
	
inputdata = [0,0,1,3,4,3,5,3,6,3,0,0,0,0,0,0,0,0,2,4,2,4,3,5,4,6,7,9,7,5,3,1,0,0,0]
modulationdata = [0,0,3,4,4,4,3,2,1,0,0,0,0,1,2,3,4,5,4,3,4,5,0,0,3,4,4,4,3,2,1,0,0,0,0,1,2,3,4,5,4,3,4,5]
def renderline(data, y):
	print(len(data))
	g = shapes.group([])
	# //do perspective correction
	for x in xrange(1,len(inputdata)-1):
		for y in xrange(1,len(modulationdata)-1):
			g.append(shapes.line(
				(x*6*y,
					(60+y)*y+(y*50+(inputdata[x]*5 * modulationdata[y]))), 
				((x+1)*6*y, 
					(60+y)*y+(y*50+inputdata[x+1]*5 * modulationdata[y])
					)))
	plotter.write(g)


# for x in xrange(1,2):
# 	for y in xrange(1,2):
		# plotPolygons(700,x*1800, -y*1800, x+3, y*100)
		# plotCircles(1000, x*900, -y*1800, 50, 0)
		# plotCircles(900, x*1800, -y*1800, 25, 0)
        # plotSquare(1000, x*1800, -y*1800, x*10, y*100)

renderline(inputdata, 80)




io.view(plotter)
