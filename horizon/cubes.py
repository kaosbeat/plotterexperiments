1
from chiplotle.tools.geometrytools.get_minmax_coordinates import get_minmax_coordinates
from chiplotle.tools.geometrytools.get_bounding_rectangle import get_bounding_rectangle
from chiplotle.geometry.core.label import Label
from chiplotle.core.interfaces.interface import _Interface
from chiplotle.plotters.margins.marginssoft import MarginsSoft
from chiplotle.plotters.margins.marginshard import MarginsHard
import random
import math
import plottools
import numpy as np
import freetype

#pltmax = [10320, 7920] # <<<
plotunit = 0.025 # 1 coordinate unit per plotter = 0.025 mm
#plotunits = (10320/432, 7920/297)
# print plotunits
#plotter.select_pen(3)
#plotter.margins.hard.draw_outline()
#plotsizemm = [626,309] #in mm breedte x hoogte maximale plotoppervlakte buitenkant karton, zonder lijmflappen
plotsizemm = [635,315]
plotsize = [plotsizemm[0]/plotunit,plotsizemm[1]/plotunit]
globaloffset = [-plotsize[0]/2,-plotsize[1]/2]  ##deze bijregelen om de plot op een andere plats te plotten
margin = 3
##grootte van de plot en zones
recordsize = 306 ### make this fit next lines sizes!!! (306 + 3 = 309) ### 306 voor een 12"

backflap = [(margin/plotunit,margin/plotunit),((recordsize+margin)/plotunit,(recordsize+margin)/plotunit)] #volledige achterflap
backcubezone = [(15/plotunit, 15/plotunit),(150/plotunit, 150/plotunit)]

frontflap= [((backflap[1][0]*plotunit + 2*margin)/plotunit,margin/plotunit),((plotsizemm[0]-margin)/plotunit, (recordsize+margin)/plotunit)] #volledige voorflap
#record jackect size = 635mm,312mm
fullzone = [(0,0) , (plotsizemm[0]/plotunit,plotsizemm[1]/plotunit)]
squareszonesize = 0.8*frontflap[0][0]*plotunit ### 60% of frontflap
squareszone = [
         ((((frontflap[1][0]*plotunit) - squareszonesize) / plotunit) ,
         (((frontflap[1][1]*plotunit) - squareszonesize) / plotunit)),
        (frontflap[1])]
squareszonemarge = 25
squareszone = [(squareszonemarge/plotunit + frontflap[0][0] , squareszonemarge/plotunit ),(frontflap[1][0] - squareszonemarge/plotunit, frontflap[1][1] - squareszonemarge/plotunit ) ]
tracklistzone = [(175/plotunit,40/plotunit),(backflap[1][0],250/plotunit)]
titlezone = [(20/plotunit,200/plotunit), (175/plotunit,backflap[1][1] - 25/plotunit )]
filldensity = 20
print fullzone
print squareszone
#####configuratieopties
virtualplotting = True  ##False for real plotter, True for virtual
plotbounds = True

#######CONFIG STOP, do not change below


if (virtualplotting == True):
        plotter = instantiate_virtual_plotter(type="DXY1300")
else:
        plotter = instantiate_plotters( )[0]


#plotter = instantiate_plotters()[0]
print(MarginsHard(plotter))
plotter.select_pen(1)
###drawbounds
#plotter.margins.hard.draw_outline()
#bounds = shapes.group([])
#bounds.append(shapes.rectangle(16158,11040))
#plotter.write(bounds)
maingroup = shapes.group([])
cubes = {}





def plotzonebounds(zone):
#	plotter.select_pen(1)
	x1,y1 = zone[0]
	x2,y2 = zone[1]
	r = shapes.rectangle((x2-x1), (y2-y1))
	transforms.offset(r,((x2-x1)/2,(y2-y1)/2))
	transforms.offset(r,(x1,y1))
        transforms.offset(r,globaloffset)
	plotter.write(r)


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
        #print(random.randint(0,7))
        g.append(shapes.line(points[random.randint(0,7)],points[random.randint(0,7)]))
    plotter.write(g)

def connectPoints(g,points,p1,p2):
  g.append(shapes.line(points[p1], points[p2]))
  #print (points[p1][0], points[p1][1])

def fillSquare(p1,p2,p3,p4, density, cubeID):  #parallel lines p1,p2 & p3,p4
    maingroup = shapes.group([])
    cubes[cubeID]["fillType"] = "parallel"
    f =  shapes.group([])
    intervalX = density
    totinterval = (p2[0] - p1[0])/density
#    for i in range(density):
    for i in range(int(totinterval)+1):
 #       vx1 = p1[0] + (p2[0] - p1[0])/density*i
        vx1 = p1[0] + intervalX*i
#        vy1 = p1[1] + (p2[1] - p1[1])/density*i
        vy1 = p1[1] + (p2[1] - p1[1])/((totinterval*i))
        #vx2 = p3[0] + (p4[0] - p3[0])/density*i
        vx2 = p3[0] + intervalX*i
        #vy2 = p3[1] + (p4[1] - p3[1])/density*i
        vy2 = p3[1] + (p4[1] - p3[1])/((totinterval*i))
        f.append(shapes.line((vx1,vy1),(vx2,vy2)))
        if (i == 0):
            cubes[cubeID]["vector"] = ((vx1,vy1),(vx2,vy2))
    if "fillSquares" in cubes[cubeID]:
        cubes[cubeID]["fillSquares"].append( [(p1,p2), (p3,p4)] )
    else:
        cubes[cubeID]["fillSquares"] = [(p1,p2), (p3,p4)]
    maingroup.append(f)
    return (maingroup)
    #print(cubes[cubeID])
    #plotter.write(f)

def fillSquareSlanted (p1,p2,p3,p4,density,cubeID,intersectingcubeID, offset):
    cubes[cubeID]["fillType"] = "slanted"
    ##get p1X

    ##get interval (if just one intersectinplaneID, this works, else update code)
    interval = cubes[intersectingcubeID]["fillSquares"][0]
    print(interval)

    ##get intersectioncubefill
    pass

def getKeyY(item):
        return item[1]

def getKeyX(item):
        return item[0]

def fillSquarePerpendicular(p1,p2,p3,p4,density,cubeID):
    maingroup = shapes.group([])
    cubes[cubeID]["fillType"] = "perpendicular"

    f = shapes.group([])
    ### get pointssequence X min  X max, other two  minY, maxY
    l = [p1,p2,p3,p4]
    #print l
    sortedl = sorted(l,key=getKeyX)
    #print sortedl
    if (sortedl[1][0] == sortedl[0][0]):
        #do a parallel fill, we're done here
        print ("doinf parallel lines!!")
        return (fillSquare(sortedl[0], sortedl[2], sortedl[1],sortedl[3],density,cubeID))

    else:
        pass

    ## get interval
##    intervalX = ( sortedl[3][0] - sortedl[0][0] ) / density
    intervalX = density
    #get first series of Y coordinates at X interval
    normalvector01 = (sortedl[1][0] - sortedl[0][0], sortedl[1][1] - sortedl[0][1])
#    print normalvector01
    normalvector13 = (sortedl[3][0] - sortedl[1][0], sortedl[3][1] - sortedl[1][1])
    normalvector02 = (sortedl[2][0] - sortedl[0][0], sortedl[2][1] - sortedl[0][1])
    normalvector23 = (sortedl[3][0] - sortedl[2][0], sortedl[3][1] - sortedl[2][1])
    #print ("normalvectopr")
    #print (normalvector23)
    i = 0
    x1 = 0
    toplist = []
    while x1 < sortedl[1][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        if (normalvector01[0] == 0):
            y1 = sortedl[0][1]
        else:
            y1 = sortedl[0][1] + normalvector01[1] * (intervalX * i) / normalvector01[0]
        i = i + 1
        toplist.append((x1,y1))
        #print (x1,y1)
        #print("go down")
        #print toplist
    j = 0
    #print x1
    offsetcorrectionX = i*intervalX - normalvector01[0]

    #print offsetcorrectionX
    while x1 < sortedl[3][0] - intervalX:
        x1 = sortedl[0][0] + (i * intervalX)
        y1 = sortedl[1][1] + normalvector13[1] *   (intervalX * j + offsetcorrectionX) / normalvector13[0]
        i = i + 1
        j = j + 1
        toplist.append((x1,y1))
        #print (x1,y1)

    i = 0
    x1 = 0
    bottomlist = []
    while x1 < sortedl[2][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        y1 = sortedl[0][1] + normalvector02[1] *   (intervalX * i) / normalvector02[0]
        i = i + 1
        bottomlist.append((x1,y1))
        #print (x1,y1)
    #print x1
    j = 0
    offsetcorrectionX = i*intervalX - normalvector02[0]

    #print offsetcorrectionX
    while x1 < sortedl[3][0] - intervalX:
        x1 = sortedl[0][0] + i * intervalX
        y1 = sortedl[2][1] + normalvector23[1] * (intervalX * j + offsetcorrectionX) / normalvector23[0]
#        y1 = 980 -  999 * 950/10
        i = i + 1
        j = j + 1
        bottomlist.append((x1,y1))
        #print (x1,y1)

    for i in range(len(toplist)):
        x1 = toplist[i][0]
        y1 = toplist[i][1]
        x2 = bottomlist[i][0]
        y2 = bottomlist[i][1]
        f.append(shapes.line((x1,y1),(x2,y2)))
    maingroup.append(f)
    return (maingroup)



def oldfillsquares():

    if (p1[1] == p2[1]):
        #do a parallel fill, we're done here
        fillSquare(p1,p2,p3,p4,density,cubeID)
        return
    else:
        pass
#interval?
    #print ("points")
    #print(p1, p2, p3, p4 )
    normalvector12 = (p2[0] - p1[0], p2[1] - p1[1])
    normalvector14 = (p4[0] - p1[0], p4[1] - p1[1])
    interval = (p3[0] - p1[0]) / density
    #print("interval =" + str(interval))
    #print("normalvector12 " + str(normalvector12))
    #print("normalvector14" + str(normalvector14))
    if (p2[1] == p1[1]):
        interval12Y = 0
    else:
        interval12Y = (normalvector12[1]) / (normalvector12[0]/interval)
    if (p4[1] == p1[1]):
        interval14Y = 0
    else:
        interval14Y = (normalvector14[1]) / ((p4[0]-p1[0])/interval)
    #print("interval12Y" + str(interval12Y))
    for i in range(int(interval12Y)):
        x1 = p1[0] + i*interval
        y1 = p1[1] + (normalvector12[1]/normalvector12[0]) * i * interval12Y
        x2 = x1
        y2 = p1[1] + (normalvector14[1]/normalvector14[0]) * i * interval14Y
        f.append(shapes.line((x1,y1),(x2,y2)))
    maingroup.append(f)

def getXinterval (p1,p2,p3,p4):
    pass

def plotDynamicCube(cubeID, size, x, y, a1, a2, a3, f1,f2,f3,f4, density):

    """a1,a2,a3 - slantvectors f1-f4 --fillcorners


#
#                           (6)
#                       _.-+.
#              (2) _.-""     '.
#              +:""            '.
#              J \               '.
#               \ \             _.-+ (5)
#               |  '.       _.-"   L
#               J    \  _.-"      /
#                L (1)+"          J
#           (3)  +    |           |
#                 \   |          .+  (4)
#                  \  |       .-'
#                   \ |    .-'
#                    \| .-'
#                (0)  +'
#


    """
    maingroup = shapes.group([])
    cubes[cubeID] = {}
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

    print len(points)

    # for p in range(7):
    #     t = shapes.label("P"+str(p), 0.2, 0.2)
    #     transforms.offset(t, points[p])
    #     g.append(t)

    #fillSquare(points[f1],points[f2],points[f3],points[f4], density, cubeID)
    fill = fillSquarePerpendicular (points[f1],points[f2],points[f3],points[f4], density, cubeID)

    maingroup.append(g)
    maingroup.append(fill)
    return(maingroup)
    ###add cube to memory


#    plotter.write(g)



def cubeStudies():

    for i in range(7):
        # plotDynamicCube(500, i*500, 0, 0, math.radians(i*10), 10, i,i+1,i+2,i+3)
        # plotDynamicCube(500, i*500, 0, 0, math.radians(i*2), 10, 3,2,0,1)
        # plotDynamicCube(500, i*600, 0, random.randint(0,300),0, 100, 0,0,0,0)
        for t in range(5):
            v1 = random.randint(0,7)
            v2= random.randint(0,7)
            v3 = random.randint(0,7)
            v4 = random.randint(0,7)
            plotDynamicCube("cubeH"+str(i)+"V"+str(t),500, i*1000, t*1000, math.radians((t-2)*20), 0, math.radians((i-3)*30), v1,v2,v3,v4, 10)

# plotCube(300, 500, 600)


#plotDynamicCube(600, 100, 0, -20, 20, 10,0,1,3,2)
#plotDynamicCube(1000, 300, -500, 0,20, 10, 1,2,5,6)
#plotDynamicCube(1000, 300, -500, 0, 20, 10, 4,3,5,6)

def intersectStudy(scale, x, y):
    maingroup = shapes.group([])
    plotter.select_pen(1)
    maingroup.append(plotDynamicCube("cube1", 800, 100,0, 0.4, 0.9, 0.2, 0,1,2,3, 30))
    transforms.scale(maingroup, scale)
    transforms.offset(maingroup, (x+globaloffset[0],y+globaloffset[1]))
    plotter.write(maingroup)

    maingroup = shapes.group([])
    plotter.select_pen(2)
    maingroup.append(plotDynamicCube("cube2", 700, -615,-200, 0.3, 0.5, 0.2, 7,6,4,5,30))
    transforms.scale(maingroup, scale)
    transforms.offset(maingroup, (x+globaloffset[0],y+globaloffset[1]))
    plotter.write(maingroup)



    maingroup = shapes.group([])
    plotter.select_pen(3)
    maingroup.append(plotDynamicCube("cube3", 1200, -823,-400, 0.2,0,0.5, 2,6,1,5,30))
    transforms.scale(maingroup, scale)
    transforms.offset(maingroup, (x+globaloffset[0],y+globaloffset[1]))
    plotter.write(maingroup)



    maingroup = shapes.group([])
    plotter.select_pen(3)
    maingroup.append(plotDynamicCube("cube4", 900, 829,-200, 0.3,0.8,0.5, 2,6,7,3,30))
    transforms.scale(maingroup, scale)
    transforms.offset(maingroup, (x+globaloffset[0],y+globaloffset[1]))
    plotter.write(maingroup)



def randomintersectstudy():
    maingroup = shapes.group([])
    for f in xrange(6):
        if (f == 0):
            q,r,s,t = 2,6,5,1
        if (f == 1):
            q,r,s,t = 0,1,5,4
        if (f == 2):
            q,r,s,t = 3,2,6,7
        if (f == 3):
            q,r,s,t = 0,4,7,3
        if (f == 4):
            q,r,s,t = 4,5,6,7
        if (f == 5):
            q,r,s,t = 0,1,2,3
        subgroup = shapes.group([])
        subgroup.append(plotDynamicCube("cube",
                                        random.randrange(1000,1500,100),
                                        random.randrange(0,2200,30)+(f*3),
                                        random.randrange(0,1000,30),
                                        random.uniform(0.2,0.7)-0.4,
                                        random.uniform(0.01,0.4)-0.2,
                                        random.uniform(0.3,0.7)-0.5,
                                        q,r,s,t,
                                        filldensity))
        maingroup.append(subgroup)
    return maingroup



#    plotter.write(maingroup)





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
  #print "size is ", g.width
  #plotter.write(g)
  return g




  # print VERTS
def writeword(textstring, size, font, xpos, ypos):
        word = shapes.group([])
	print (textstring)
	tt = xpos
	for char in textstring:
                a = plotchar(char, size, font, tt, ypos)
		tt = tt + a.width
                word.append(a)
        return word




#intersectStudy(4,6000,1800)
#def randomCubes():
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
        zonesize = (zone[1][0] - zone[0][0], zone[1][1] - zone[0][1])
        rightx = zone[0][0] - g.minmax_coordinates[0].x + (zonesize[0] - g.width) / 2
        righty = zone[0][1] - g.minmax_coordinates[0].y + (zonesize[1] - g.height) / 2
        transforms.offset(g,(rightx,righty ))
	return g


def plotcover(start, end):
        #plot metadata
        t = shapes.label(str(start) + "/" + str(end), 0.5, 0.5)
        transforms.offset(t,(10/plotunit+globaloffset[0],10/plotunit+globaloffset[1]))
        plotter.write(t)
        plotter.select_pen(3)
        #plott some cubes
        G = randomintersectstudy()
        scaledG = plotgroup(G,1,squareszone,(0,0),1)
#        scaledG = plotgroup(G,1,frontflap,(0,0),1)
        #print scaledG.bounding_rectangle
        print scaledG.minmax_coordinates[0].x
        transforms.offset(scaledG,globaloffset)
        print scaledG.width
        print scaledG.height
        pen = 1
        pens = 8
        for g in scaledG:
                plotter.select_pen(pen%pens)
                plotter.write(g)
                pen = pen+1

        #plottext

        text = shapes.group([])
        text.append(writeword("A", 20, "rus.ttf", 500, 10500))
        text.append(writeword("little_white_box", 13, "USSR.ttf", 500,9000))
        text.append(writeword("railway_horizon", 13, "USSR.ttf", 500,8000))
        text.append(writeword("level_in_het_bos", 13, "USSR.ttf", 500,7000))
        text.append(writeword("Leeds", 13, "USSR.ttf", 500,6000))
        text.append(writeword("G_Spreads", 13, "USSR.ttf", 500,5000))

        text.append(writeword("B", 20, "rus.ttf", 500, 3500))
        text.append(writeword("Swing_Along", 13, "USSR.ttf", 500,2000))
        text.append(writeword("Sponge_Breeds", 13, "USSR.ttf", 500,1000))
        text.append(writeword("88", 13, "USSR.ttf", 500,0))
        text.append(writeword("Death_Threads", 13, "USSR.ttf", 500,-1000))
        text.append(writeword("Two_of_a_kind", 13, "USSR.ttf", 500,-2000))
        text.append(writeword("Forest_Code", 13, "USSR.ttf", 500,-3000))
        text.append(writeword("Disobedient_Operator", 13, "USSR.ttf", 500,-4000))
        text.append(writeword("N-Rave", 13, "USSR.ttf", 500,-5000))
        text.append(writeword("Short_Cuts", 13, "USSR.ttf", 500,-6000))
        text = plotgroup(text,1,tracklistzone,(0,0),1)
        transforms.offset(text,globaloffset)
        plotter.write(text)

        title = shapes.group([])
        title.append(writeword("SONDERVAN", 30, "USSR.ttf", 500, 5000))
        title.append(writeword("CUTS", 25, "rus.ttf", 500, 2000))
        title.append(writeword("of_the", 20, "USSR.ttf", 500, 500))
        title.append(writeword("HYPERCUBE", 25, "rus.ttf", 500, -1300))
        title = plotgroup(title,1,titlezone,(0,0),1)
        transforms.offset(title,globaloffset)
        plotter.write(title)

        backcube = plotDynamicCube("cube",
                                        random.randrange(1000,1500,100),
                                        random.randrange(0,2200,30),
                                        random.randrange(0,1000,30),
                                        random.uniform(0.2,0.7)-0.4,
                                        random.uniform(0.01,0.4)-0.2,
                                        random.uniform(0.3,0.7)-0.5,
                                        3,2,6,7,
                                        filldensity)
        backcubeplot = plotgroup(backcube,1,backcubezone,(0,0),3)
        transforms.offset(backcubeplot, globaloffset)
        plotter.write(backcubeplot)




#transforms.scale(maingroup, 0.8*11040/maingroup.height)
#transforms.offset(maingroup, (maingroup.width/10, maingroup.height/10))

#plotter.select_pen(2)
#plotter.write(shapes.line((0,0), (2500,0)))
#plotter.write(shapes.line((0,0), (0,2500)))

#print(cubes)




if plotbounds:
        ##disable to not plot bounds
        plotter.select_pen(2)
        plotzonebounds(fullzone)
        plotter.select_pen(2)
        plotzonebounds(backflap)
        plotter.select_pen(2)
        plotzonebounds(frontflap)
        #plotter.select_pen(3)
        #plotzonebounds(squareszone)





print('startnumber/stopnumber will be plotted')
startnumber = input('enter startnumber: ')
stopnumber = input('enter stopnumber (eg. 300): ')
#plotter.clear()
for x in xrange(startnumber,stopnumber):
        ready = input('is record ready? press 1 to continue, press 2 for boundingboxtest (needs 2 pens) :')
        print(ready)
        if(ready == 1):
                print x
                plotcover(x, stopnumber)
                io.view(plotter)


        if(ready == 2):
                plotter.select_pen(1)
                plotzonebounds(fullzone)
                plotter.select_pen(2)
                plotzonebounds(backflap)
                plotzonebounds(frontflap)
                io.view(plotter)

        else:
                print('press CTRL-C')
