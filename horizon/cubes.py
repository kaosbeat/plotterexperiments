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
    for i in range(100):
        g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))


plotCube(1000, 0, 0)
plotter.write(g)
