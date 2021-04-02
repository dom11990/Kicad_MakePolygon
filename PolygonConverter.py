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



def ArcToLines(arc,maxArcLength_mm):
        
        maxArcLength = maxArcLength_mm * 1e6 #kicad return in nanometers
        logInfo("Max arc length in Kicad units: {:.9f}".format(maxArcLength))
        #center of the arc
        # pcbnew.DRAWSEGMENT.getang
        centerOffset = complex(arc.GetCenter().x,arc.GetCenter().y)
        #start of the arc when centered at 0,0

        start = complex(arc.GetArcStart().x,arc.GetArcStart().y) - centerOffset
        radius = abs(start)
        #radians that can be stepped to maintain the maxArcLength
        maxArcAngle = maxArcLength / radius

        logInfo("Angle: {}".format(ArcAngle(arc)))

        if(ArcAngle(arc) < 0):
            maxArcAngle *= -1
        #abs because angle can be negative
        stepCount = int(np.ceil(abs(np.deg2rad(ArcAngle(arc)) / maxArcAngle)))

        logInfo("Need {} steps of {:.3} rads".format(stepCount,maxArcAngle))
        
        lines = []
        points = []
        startAngle = np.angle(start)

        # loop through the number of needed steps and generate the vertexes of the segments
        # use complex numbers here to represent x and y, x = real, y = imag
        for i in range(0,stepCount):
            nextPoint = cmath.rect(radius,startAngle + i*maxArcAngle)
            nextPoint += centerOffset
            # logDebug(nextPoint)
            points.append(nextPoint)

        # get the remainder of the last step so that the final segment ends 
        # directly on the end point of the arc
        finalStep = np.deg2rad(ArcAngle(arc)) % maxArcAngle
        nextPoint = cmath.rect(abs(start),startAngle + (stepCount-1)*maxArcAngle + finalStep)
        nextPoint += centerOffset
        points.append(nextPoint)

        startPoint = start + centerOffset



        
        lines = []
        pcb = pcbnew.GetBoard()
        logInfo("Discretizing arc...")
        for point in points:
            # create the new line
            # lines.append(Line.fromComplex(startPoint,point,self.layer,self.width))
            newDrawing = pcbnew.DRAWSEGMENT(pcb)
            newDrawing.SetStartX(int(startPoint.real))
            newDrawing.SetStartY(int(startPoint.imag))
            newDrawing.SetEndX(int(point.real))
            newDrawing.SetEndY(int(point.imag))
            lines.append(newDrawing)
            startPoint = point
        logInfo("Done generating lines")
        return lines