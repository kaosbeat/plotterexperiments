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
              (x + ((a1x+a3y)*size),y + ((a1y+a3y)*size)),
              (x + ((a3x+a2x+a1x)*size),y + ((a1y+a2y+a3y)*size)),
              (x + ((a1x+a2x)*size),y + ((a1y+a2y)*size))
    ]
    g = shapes.group([])
    for i in range(100):

        g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))
    plotter.write(g)



plotDynamicCube(1000, 0, 0, 23, 45, 300)
plotCube(300, 500, 600)
io.view(plotter)
