#output stored at /var/folders/b5/9zpmpr953hqfzs4mtm43d3q80000gp/T/com.apple.Preview/PreviewTemp-RFLZVu

from chiplotle import *
from chiplotle.tools.plottertools import instantiate_virtual_plotter
plotter =  instantiate_virtual_plotter(type="DXY1300")
plotter.margins.hard.draw_outline()
plotter.select_pen(2)


import freetype
face = freetype.Face("poir.ttf")
face.set_char_size( 48*64 )
face.load_char('S')
bitmap = face.glyph.bitmap
print bitmap.buffer




b = 0
# while b < 10:
#   a = b * 100
#   plotter.goto(a,0)
#   plotter.pen_down()
#   plotter.goto(1000,1000)
#   plotter.pen_up()
#   b = b + 1
#   print a, b
# plotter.select_pen(2)
# plotter.goto( 500 , 500)
# plotter.pen_down()

import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

dotproduct((2,2) , (1,1))
length((1,1))





import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


# def turnAndGo((originX,originY), angle,distance):
#   a*a + b*b = c*c

#   cos(angle) = (0,0)

# c = shapes.circle(1000)
# p = shapes.random_walk_polar(100, 500 )
# r = shapes.rectangle(500, 1000)
# g = shapes.group([c, r, p])

#reset the group
# g = shapes.group([ ])

# for r in range(100, 1000, 100):
#   c = shapes.circle( r, 100 )
#   transforms.offset ( c , (r,50))
#   g.append(c)
# #   print r
#   print g[r/100 - 1].center
# #   print g[1].center
#   # g = shapes.group( [ a ] )
# io.view(g)

g = shapes.group([])

# for seg in [4, 6, 8]:
#   c1 = shapes.circle(1000, seg)
#   g.append(c1)


#dumb version of http://geometrydaily.tumblr.com/post/58058180988/504-rumour
# c1 = shapes.circle(1000)
# c2 = shapes.circle(1000)
# transforms.offset(c2, (2000,0))
# r1 = shapes.rectangle(2000,2000)
# transforms.offset(r1, (1000,0))
# c3 = shapes.circle(2000)
# transforms.offset(c3, (2000,1000))
# c4 = shapes.circle(2000)
# transforms.offset(c4, (0,-1000))
# c5 = shapes.circle(4000)
# transforms.offset(c5, (2000,-1000))
# c6 = shapes.circle(4000)
# transforms.offset(c6, (0,1000))
# g.append(c1)
# g.append(c2)
# g.append(r1)
# g.append(c3)
# g.append(c4)
# g.append(c5)
# g.append(c6)
# io.view(g)



#smart version but not so smart
# baseradius = 1000
# v1 = 0
# currentoffset = 0
# for x in range (0,5,1):
#   v1 = 2**x * baseradius
#   c1 = shapes.circle(v1)
#   currentoffset = 2**x * baseradius
#   previousoffset = 2**(x-1) * baseradius
#   if x%2 == 0:
#     transforms.offset( c1, (0,currentoffset))
#     g.append(c1)
# #     print "bored"
#   else:
# #     print "bored"
#     transforms.offset( c1, (0, 1/4*previousoffset))
#     g.append(c1)

# #   c2 = shapes.circle(x * baseradius)
# #   g.append(c2)
# io.view(g)



d1 = shapes.line( (1000,1000),(300,100))
g.append(d1)


help (shapes.line)



g = shapes.group([])
rlist = [0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,0,4,2,5,2,6,8,3,1,5,3,8,0,6,5,3,2,1,5,7,2,5,3,2,2,5,9]

for r in range (10, 100, 1):
  l = shapes.line( (r*10, 0), (r*rlist[r/10]*10, 1000) )
  g.append(l)
  l = shapes.line( (r*rlist[r/10]*10, 1000), (r,2000) )
  g.append(l)
# io.view(g)
# io.view(plotter)

# help(shapes.path)

# help(transforms)
