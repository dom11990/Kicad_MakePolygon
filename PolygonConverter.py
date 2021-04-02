import matplotlib.pyplot as plt

import os
import sys
import numpy as np
import cmath
import pcbnew

from LogWrapper import *


# Dependencies: numpy

def ArcAngle(arc) -> float:
    """Converts the angle returned by pcbnew arc.GetAngle() to degrees.
    for some reason the returned value from pcbnew is the angle * 10

    Args:
        arc (pcbnew.DRAWSEGMENT): the arc to operate on

    Returns:
        float: angle in degrees
    """
    return arc.GetAngle() / 10.0


def ArcLineCount(arc,maxArcLength_mm):
    # we want mm
    maxArcLength = pcbnew.FromMM(maxArcLength_mm) 
    
    # center of the arc
    centerOffset = complex(arc.GetCenter().x,arc.GetCenter().y)
    
    # start of the arc when centered at 0,0
    start = complex(arc.GetArcStart().x,arc.GetArcStart().y) - centerOffset
    radius = abs(start)
    
    # radians that can be stepped to maintain the maxArcLength
    maxArcAngle = maxArcLength / radius

    if(ArcAngle(arc) < 0):
        maxArcAngle *= -1
    
    # abs because angle can be negative,
    # round up so we don't come up one element short
    stepCount = int(np.ceil(abs(np.deg2rad(ArcAngle(arc)) / maxArcAngle)))
    return stepCount



def ArcToLines(arc,maxArcLength_mm):
    # we want mm
    maxArcLength = pcbnew.FromMM(maxArcLength_mm) 
    
    # center of the arc
    centerOffset = complex(arc.GetCenter().x,arc.GetCenter().y)
    
    # start of the arc when centered at 0,0
    start = complex(arc.GetArcStart().x,arc.GetArcStart().y) - centerOffset
    radius = abs(start)
    
    # radians that can be stepped to maintain the maxArcLength
    maxArcAngle = maxArcLength / radius

    if(ArcAngle(arc) < 0):
        maxArcAngle *= -1
    
    # abs because angle can be negative,
    # round up so we don't come up one element short
    stepCount = int(np.ceil(abs(np.deg2rad(ArcAngle(arc)) / maxArcAngle)))

    LogInfo("Need {} steps of {:.3} rads".format(stepCount,maxArcAngle))
    
    lines = []
    points = []
    startAngle = np.angle(start)

    # loop through the number of needed steps and generate the vertexes of the segments
    # use complex numbers here to represent x and y, x = real, y = imag
    for i in range(0,stepCount):
        nextPoint = cmath.rect(radius,startAngle + i*maxArcAngle)
        nextPoint += centerOffset
        # LogDebug(nextPoint)
        points.append(nextPoint)

    # get the remainder of the last step so that the final segment ends 
    # directly on the end point of the arc
    finalStep = np.deg2rad(ArcAngle(arc)) % maxArcAngle
    nextPoint = cmath.rect(abs(start),startAngle + (stepCount-1)*maxArcAngle + finalStep)
    nextPoint += centerOffset
    points.append(nextPoint)

    startPoint = start + centerOffset
    
    lines = []
    LogInfo("Discretizing arc...")
    for point in points:
        # create the new line
        # lines.append(Line.fromComplex(startPoint,point,self.layer,self.width))
        newDrawing = pcbnew.DRAWSEGMENT()
        newDrawing.SetStartX(int(startPoint.real))
        newDrawing.SetStartY(int(startPoint.imag))
        newDrawing.SetEndX(int(point.real))
        newDrawing.SetEndY(int(point.imag))
        lines.append(newDrawing)
        startPoint = point
    LogInfo("Done generating lines")
    return lines

#TODO: make this function fail-safe
def LinesToPolygon(lines):
        
        sourceLines = []
        dupeLines = []
        #remove dupes
        for line in lines:
            if not (_Equal(line.GetStart().x,line.GetEnd().x) and _Equal(line.GetStart().y,line.GetEnd().y)):
                sourceLines.append(line)
            else:
                dupeLines.append(line)

        matchedLines = []
        matchedLines.append(sourceLines[0])
        del sourceLines[0]
        
        # search through the list of lines, finding another that ends or starts where the previous one ends
        while(len(sourceLines)):
            found = False
            for idx,line in enumerate(sourceLines):
                if (_Equal(line.GetStart().x, matchedLines[-1].GetStart().x) and _Equal(line.GetStart().y, matchedLines[-1].GetStart().y)):
                    # start matches start, flip the new line start stop positions
                    LogError("wtf this should not happen")
                    raise Exception("There are duplicate lines that have the same start and stop coordinates.")

                    
                if (_Equal(line.GetStart().x, matchedLines[-1].GetEnd().x) and _Equal(line.GetStart().y, matchedLines[-1].GetEnd().y)):
                    found = True
                    
                if (_Equal(line.GetEnd().x, matchedLines[-1].GetStart().x) and _Equal(line.GetEnd().y, matchedLines[-1].GetStart().y)):
                    if len(matchedLines) == 1:
                        #this can happen at the very first match. if that is the case
                        # it is likely the structure was drawn 'the other way' so it will be easier to 
                        # swap the first entry and proceed normally than to swap all subsequent entries
                        x1 = matchedLines[-1].GetStart().x
                        y1 = matchedLines[-1].GetStart().y
                        matchedLines[-1].SetStartX(matchedLines[-1].GetEnd().x)
                        matchedLines[-1].SetStartY(matchedLines[-1].GetEnd().y)
                        matchedLines[-1].SetEndX(x1)
                        matchedLines[-1].SetEndY(y1)

                        x1 = line.GetStart().x
                        y1 = line.GetStart().y
                        line.SetStartX(line.GetEnd().x)
                        line.SetStartY(line.GetEnd().y)
                        line.SetEndX(x1)
                        line.SetEndY(y1)
                        found = True

                    
                if (_Equal(line.GetEnd().x, matchedLines[-1].GetEnd().x) and _Equal(line.GetEnd().y, matchedLines[-1].GetEnd().y)):
                    x1 = line.GetStart().x
                    y1 = line.GetStart().y
                    line.SetStartX(line.GetEnd().x)
                    line.SetStartY(line.GetEnd().y)
                    line.SetEndX(x1)
                    line.SetEndY(y1)
                    LogInfo("Swapping start- and end-points")
                    found = True

                if(found):
                    #we found a match!
                    matchedLines.append(line)
                    del sourceLines[idx]
                    break
            
            if(not found):
                raise Exception("Structure is not fully enclosed. Check to make sure every line or arc ends perfectly on another, ultimately forming a completely enclosed structure with no crossing / self-intersection")
        
        # now check the last lines closes with the first line
        #TODO: actual do this check...
        
        
        #we made it through the whole structure and it appears to be enclose
        
        # create the polygon
        polygon = pcbnew.DRAWSEGMENT()
        points = pcbnew.wxPoint_Vector()
        
        
        # do the first one outside the loop since we also need the start point, not just the end point
        points.append(pcbnew.wxPoint(matchedLines[0].GetStart().x, matchedLines[0].GetStart().y))
        points.append(pcbnew.wxPoint(matchedLines[0].GetEnd().x, matchedLines[0].GetEnd().y))
        del matchedLines[0]

        # now just add the end points of each line
        for line in matchedLines:
            points.append(pcbnew.wxPoint(line.GetEnd().x, line.GetEnd().y))
        
        polygon.SetPolyPoints(points)


        xx = [p.x for p in points]
        yy = [p.y for p in points]

        LogInfo("Polyshape valid: {}".format(polygon.IsPolyShapeValid()))
        LogInfo("Polygon Position: {} {}".format(pcbnew.ToMM(polygon.GetPosition().x),pcbnew.ToMM(polygon.GetPosition().y)))

        # plt.plot(xx,yy)
        # plt.show()
        



        return polygon


def _Equal(f1,f2, margin = pcbnew.FromMM(0.0001)) -> bool:
    return abs(f1-f2) < margin