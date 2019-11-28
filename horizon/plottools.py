from chiplotle import *
import numpy as np
import freetype
import math
import pickle
import random
#from texttools  import *
from svgpathtools import svg2paths, Path, Line, Arc, CubicBezier, QuadraticBezier
# from texttools import *


def plotchar(char, size, font, xpos, ypos):
#code adapted from freetype-py vector example
  global plotter
  face = freetype.Face(font)
  face.set_char_size( size*64 )
  face.load_char(char)
  slot = face.glyph
  outline = slot.outline
  points = np.array(outline.points, dtype=[('x',float), ('y',float)])
  x, y = points['x'], points['y']
  start, end = 0, 0
  VERTS, CODES = [], []
  # Iterate over each contour
  for i in range(len(outline.contours)):
      end    = outline.contours[i]
      points = outline.points[start:end+1]
      points.append(points[0])
      tags   = outline.tags[start:end+1]
      tags.append(tags[0])

      segments = [ [points[0],], ]
      for j in range(1, len(points) ):
          segments[-1].append(points[j])
          if tags[j] & (1 << 0) and j < (len(points)-1):
              segments.append( [points[j],] )
      verts = [points[0], ]
      # codes = [Path.MOVETO,]
      for segment in segments:
          if len(segment) == 2:
              verts.extend(segment[1:])
              # codes.extend([Path.LINETO])
          elif len(segment) == 3:
              verts.extend(segment[1:])
              # codes.extend([Path.CURVE3, Path.CURVE3])
          else:
              verts.append(segment[1])
              # codes.append(Path.CURVE3)
              for i in range(1,len(segment)-2):
                  A,B = segment[i], segment[i+1]
                  C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                  verts.extend([ C, B ])
                  # codes.extend([ Path.CURVE3, Path.CURVE3])
              verts.append(segment[-1])
              # codes.append(Path.CURVE3)
      VERTS.extend(verts)
      # CODES.extend(codes)
      start = end+1
  g = shapes.group([])
  g.append(shapes.path(VERTS))
  transforms.offset(g, (xpos, ypos))
  print "size is ", g.width
  plotter.write(g)
  return g.width




  # print VERTS
def writeword(textstring, size, font, xpos, ypos):
	print (textstring)
	tt = xpos
	for char in textstring:
		tt = tt + plotchar(char, size, font, tt, ypos)






def plotzonebounds(zone):
#	plotter.select_pen(1)
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	r = shapes.rectangle((x2-x1), (y2-y1))
	transforms.offset(r,((x2-x1)/2,(y2-y1)/2))
	transforms.offset(r,(x1,y1))
	plotter.write(r)


def calculatesvggroup(svg):
	print "PLOTTING stuff"
	# plotter.select_pen(pen)
	g = shapes.group([])
	paths, attributes = svg2paths(svg)
	# print dir(paths[0][0].start.real)
	for path in paths:
		for segment in path:
			if isinstance(segment, Line):
				# print "Line found"
				g.append(shapes.line((segment.start.real,segment.start.imag),(segment.end.real,segment.end.imag)))
			if isinstance(segment, CubicBezier):
				g.append(shapes.bezier_path([(segment.start.real,segment.start.imag),(segment.control1.real,segment.control1.imag),(segment.control2.real,segment.control2.imag),(segment.end.real,segment.end.imag)],0))
	bb = get_bounding_rectangle(g)
	bb = get_minmax_coordinates(bb.points)
	print bb
	print (svg + " is " + str(g.width*plotunit) + "mm")
	print (svg + " is " + str(g.height*plotunit) + "mm")
	# plotter.write(g)
	transforms.offset(g, (-bb[0][0], -bb[0][1] ))
	return({'group': g, 'bounds': bb})
	# io.view(g)

def plotgroup(g,paddingfactor,zone,noisexy,pen):
	plotter.select_pen(pen)
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	maxx = abs(x2-x1)
	maxy = abs(y2-y1)
	xfactor = maxx / g.width/paddingfactor
	yfactor = maxy / g.height/paddingfactor
	if (yfactor <= xfactor):
		scale = yfactor
		transforms.scale(g, scale)
		transforms.offset(g,((recordsize/plotunit - g.width)/2 , (recordsize/plotunit - g.height)/2))

	else:
		scale = xfactor
		transforms.scale(g, scale)
		# transforms.offset(g,(0,(y2-y1+g.height)/2))

	print ("SCALE = " + str(scale))
	transforms.offset(g, (x1,y1))
	if not noisexy == (0,0):
		transforms.noise(g,noisexy)
	# plotter.write(g)
	return g
