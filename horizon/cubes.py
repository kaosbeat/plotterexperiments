from chiplotle import *
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
import random
import math


plotter = instantiate_virtual_plotter(type="DXY1300")

plotter.select_pen(1)



def plotCube(size, x, y):
    points = [(x,y),
              (x + (0.8*size), y - (0.2*size)),
              (x - (0.2*size), y + (0.8*size)),
              (x + (0.3*size), y + (0.5*size)),
              (x + (1.1*size), y + (0.3*size)),
              (x + (0.6*size),y + (0.6*size)),
              (x + (0.9*size),y + (1.1*size)),
              (x + (0.1*size),y + (1.3*size))
    ]
    g = shapes.group([])
    for i in range(1000):
        print(random.randint(0,7))
        g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))
    plotter.write(g)

def connectPoints(g,points,p1,p2):
  g.append(shapes.line(points[p1], points[p2]))
  print (points[p1][0], points[p1][1])

def fillSquare(p1,p2,p3,p4, density):  #parallel lines p1,p2 & p3,p4
  f =  shapes.group([])
  for i in range(density):
    f.append(shapes.line( (p1[0] + (p2[0] - p1[0])/density*i, p1[1] + (p2[1] - p1[1])/density*i), (p3[0] + (p4[0] - p3[0])/density*i, p3[1] + (p4[1] - p3[1])/density*i)))
  plotter.write(f)


def plotDynamicCube(size, x, y, a1, a2, a3):  ## xf, yf, zf normalized vector
    a1x = math.cos(a1)
    a1y = math.sin(a1)
    a2x = math.sin(a2)
    a2y = math.cos(a2)
    a3x = math.sin(a3)
    a3y = math.cos(a3)

    points = [(x,y),
              (x + (a3x*size), y + (a3y*size)),
              (x + ((a2x+a3x)*size), y + ((a2y+a3y)*size)),
              (x + (a2x*size), y + (a2y*size)),
              (x + (a1x*size), y + (a1y*size)),
              (x + ((a1x+a3x)*size),y + ((a1y+a3y)*size)),
              (x + ((a3x+a2x+a1x)*size),y + ((a1y+a2y+a3y)*size)),
              (x + ((a1x+a2x)*size),y + ((a1y+a2y)*size))
    ]
    g = shapes.group([])

    # for i in range(100):

    #     g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))

    connectPoints(g,points,0,1)
    connectPoints(g,points,1,2)
    connectPoints(g,points,2,3)
    connectPoints(g,points,3,0)
    connectPoints(g,points,0,4)
    connectPoints(g,points,1,5)
    connectPoints(g,points,2,6)
    connectPoints(g,points,3,7)
    connectPoints(g,points,4,5) 
    connectPoints(g,points,5,6)
    connectPoints(g,points,6,7)
    connectPoints(g,points,4,7)

    fillSquare(points[0],points[1],points[3],points[2], 100)

    plotter.write(g)





plotDynamicCube(1000, 0, 0, 230, 15, 2300)
plotDynamicCube(1000, 0, 0, 23, 45, 30)
# plotCube(300, 500, 600)
io.view(plotter)
