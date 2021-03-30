#used for debugging
import matplotlib.pyplot as plt






import os
import sys
import numpy as np
import cmath
import argparse
from loguru import logger

#Dependencies: loguru


class Arc:
    def __init__(self, xCenter, yCenter, xStart, yStart, angle, layer, width):
        self.xCenter = xCenter
        self.yCenter = yCenter
        self.xStart = xStart
        self.yStart = yStart
        self.angle = angle
        self.layer = layer
        self.width = width


    def toLineSegments(self,maxArcLength_mm):
        
        
        #center of the arc
        centerOffset = complex(self.xCenter,self.yCenter)
        #start of the arc when centered at 0,0
        start = complex(self.xStart,self.yStart) - centerOffset
        radius = abs(start)
        #radians that can be stepped to maintain the maxArcLength_mm
        maxArcAngle = maxArcLength_mm / (abs(start))

        if(self.angle < 0):
            maxArcAngle *= -1
        #abs because angle can be negative
        stepCount = int(np.ceil(abs(np.deg2rad(self.angle) / maxArcAngle)))

        logger.info("Need {} steps of {:.3} rads".format(stepCount,maxArcAngle))
        
        
        

        lines = []
        points = []
        startAngle = np.angle(start)
        for i in range(0,stepCount):
            nextPoint = cmath.rect(radius,startAngle + i*maxArcAngle)
            nextPoint += centerOffset
            logger.debug(nextPoint)
            points.append(nextPoint)

        finalStep = np.deg2rad(self.angle) % maxArcAngle
        nextPoint = cmath.rect(abs(start),startAngle + (stepCount-1)*maxArcAngle + finalStep)
        nextPoint += centerOffset
        logger.debug(nextPoint)
        points.append(nextPoint)

        startPoint = start + centerOffset
        #_PlotPoints(points)
        for point in points:
            lines.append(Line.fromComplex(startPoint,point,self.layer,self.width))
            startPoint = point
        return lines




    @classmethod
    def fromText(cls, text:str):
        splits = text.strip().split(' ')

        params = []
        for s in splits:
            s = s.replace("(","")
            s = s.replace(")","")
            params.append(s)


        #do some safety checks
        if params[1] != "start":
            raise Exception("Bad file format. Looks like the scripts is out of date :(")
        if params[4] != "end":
            raise Exception("Bad file format. Looks like the scripts is out of date :(")

        #convert the elements to their appropriate types
        xCenter = float(params[2])
        yCenter = float(params[3])
        
        xStart = float(params[5])
        yStart = float(params[6])
        
        angle = float(params[8])
        layer = params[10]
        width = float(params[12])
        arc = Arc(xCenter,yCenter,xStart,yStart,angle,layer,width)
        return arc

class Line:
    def __init__(self, x1, y1, x2, y2, layer, width):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.layer = layer
        self.width = width

    def __str__(self):
        #(fp_line (start 6.034 3.256) (end 8.998 1.154) (layer Cmts.User) (width 0.12))
        string = "(fp_line (start {:.6f} {:.6f}) (end {:.6f} {:.6f}) (layer {}) (width {:.3f}))".format(self.x1, self.y1, self.x2, self.y2, self.layer, self.width)
        return string
    @classmethod
    def fromComplex(cls, z1, z2, layer, width):
        line = Line(np.real(z1),np.imag(z1),np.real(z2),np.imag(z2),layer,width)
        return line

    @classmethod
    def fromText(cls, text:str):
        splits = text.strip().split(' ')

        params = []
        for s in splits:
            s = s.replace("(","")
            s = s.replace(")","")
            params.append(s)
        #   0        1    2       3      4    5      6       7        8        9     10
        #(fp_line (start 4.031 -7.300) (end 4.031 -7.300) (layer Cmts.User) (width 0.100))
        #do some safety checks
        if params[0] != "fp_line":
            raise Exception("Expected an fpline, got {} :(".format(params[0]))
        if params[1] != "start":
            raise Exception("Bad file format. Looks like the scripts is out of date :(")
        if params[4] != "end":
            raise Exception("Bad file format. Looks like the scripts is out of date :(")

        #convert the elements to their appropriate types
        x1 = float(params[2])
        y1 = float(params[3])
        
        x2 = float(params[5])
        y2 = float(params[6])
        
        layer = params[8]
        width = float(params[10])
        line = Line(x1,y1,x2,y2,layer,width)
        return line


class Polygon:

    def __init__(self, layer, width):
        self.lines = []
        self.layer = layer
        self.width = width

    def __str__(self):
        #(fp_poly (pts (xy 2.896 -8.33) (xy 2.406 -8.171) (xy 2.232 -8) (xy 2.174 -7.907)
        #(xy 2.781 -8.459) (xy 2.809 -8.462) (xy 2.828 -8.4635) (xy 2.852 -8.465)
        #(xy 2.896 -8.465)) (layer F.Cu) (width 0))
        string = "(fp_poly (pts "

        for idx,line in enumerate(self.lines):
            #mod 4 + 1 because the first entry gets an extra element
            if idx != 0 and (idx % 4) + 1 == 0:
                string += " " + "\n" 
            if idx == 0:
                "(xy {:.6f} {:.6f}) ".format(line.x1, line.y1)

            string += "(xy {:.6f} {:.6f}) ".format(line.x2, line.y2)


        string += "(layer {}) (width {:.3f}))".format(self.layer, self.width)
        return string



    @classmethod
    def fromLines(cls, sourceLines):

        #remove dupes
        srcLines = sourceLines
        sourceLines = []
        for line in srcLines:
            if not (_Equal(line.x1,line.x2) and _Equal(line.y1,line.y2)):
                sourceLines.append(line)



        matchedLines = []
        matchedLines.append(sourceLines[0])
        del sourceLines[0]
        
        while(len(sourceLines)):
            found = False
            for idx,line in enumerate(sourceLines):
                
                if idx == 141:
                    print("here")
                if (_Equal(line.x1, matchedLines[-1].x1) and _Equal(line.y1, matchedLines[-1].y1)):
                    # start matches start, flip the new line start stop positions
                    logger.error("wtf this should not happen")

                    
                if (_Equal(line.x1, matchedLines[-1].x2) and _Equal(line.y1, matchedLines[-1].y2)):
                    found = True
                    
                if (_Equal(line.x2, matchedLines[-1].x1) and _Equal(line.y2, matchedLines[-1].y1)):
                    if len(matchedLines) ==1:
                        #this can happen at the beginning, swap the first entry and proceed normally
                        x1 = matchedLines[-1].x1
                        y1 = matchedLines[-1].y1
                        matchedLines[-1].x1 = matchedLines[-1].x2
                        matchedLines[-1].y1 = matchedLines[-1].y2
                        matchedLines[-1].x2 = x1
                        matchedLines[-1].y2 = y1

                        x1 = line.x1
                        y1 = line.y1
                        line.x1 = line.x2
                        line.y1 = line.y2
                        line.x2 = x1
                        line.y2 = y1
                        logger.error("This should only happen once!")
                        found = True

                    
                    
                if (_Equal(line.x2, matchedLines[-1].x2) and _Equal(line.y2, matchedLines[-1].y2)):
                    x1 = line.x1
                    y1 = line.y1
                    line.x1 = line.x2
                    line.y1 = line.y2
                    line.x2 = x1
                    line.y2 = y1
                    logger.info("Swapping start- and end-points")
                    found = True

                if(found):
                    #we found a match!
                    matchedLines.append(line)
                    del sourceLines[idx]
                    break
            
            if(not found):
                raise Exception("Structure is not fully enclosed. Check to make sure every line or arc ends perfectly on another, ultimately forming a completely enclosed structure with no crossing / self-intersection")
        
        pol = Polygon(matchedLines[0].layer, matchedLines[0].width)
        pol.lines = matchedLines
        return pol




class PolygonConverter():
    @classmethod
    def CheckFiles(inputFilePath: str, outputFilePath: str):
        if inputFilePath == outputFilePath:
            raise Exception("Input an output file path must be different.")
        return
    
    @classmethod
    def ConvertArcs(self, inputFilePath: str, outputFilePath: str):
            
    
        intputFile = open(inputFilePath, 'r')
        lines = intputFile.readlines()
        intputFile.close()

        toWrite = []
        for line in lines:
            if line.find("fp_arc") >= 0:
                #we found an arc that needs to be converted
                logger.debug("Found an arc! -- Discretizing...")
                #    0      1    2     3     4       5         6       7        8     9       10         11    12
                #(fp_arc (start 1.02 0.017) (end 1.002001 -5.974999) (angle -269.8) (layer Cmts.User) (width 0.12))
                
                arc = Arc.fromText(line)
                lines = arc.toLineSegments(0.1)
                for lineSeg in lines:
                    
                    #get the current indent count
                    indentCount = _GetIndent(line)
                    indents = ""
                    for _ in range(0,indentCount):
                        indents += " "   
                
                    if not (_Equal(lineSeg.x1,lineSeg.x2) and _Equal(lineSeg.y1,lineSeg.y2)):
                        toWrite.append(indents + str(lineSeg)+"\n")
            else:
                toWrite.append(line)
        
        outputFile = open(outputFilePath, 'w')
        outputFile.writelines(toWrite)
        outputFile.close()
    
    @classmethod
    def ConvertPoly(self, inputFilePath : str, outputFilePath : str):
        intputFile = open(inputFilePath, 'r')
        lines = intputFile.readlines()
        intputFile.close()

        toWrite = []
        lineSegments = []
        
        for line in lines:
            if line.find("fp_line") >= 0:
                lineSegments.append(Line.fromText(line))
            else:
                toWrite.append(line)

        
        # _PlotLines(lineSegments)
        poly = Polygon.fromLines(lineSegments)
        toWrite += str(poly).split("\n")
        
        outputFile = open(outputFilePath, 'w')
        outputFile.writelines(toWrite)
        outputFile.close()

# Private Helper Functions

def _PlotPoints(points):
    x = []
    y = []
    radius = 0
    for p in points:
        x.append(np.real(p))
        y.append(-np.imag(p))
        plt.plot(x[-1],y[-1],'o')
        radius = max(radius, abs(p))
    plt.plot(x,y)
    ax = plt.gca()
    radius *= 1.5
    ax.set_xlim([-radius,radius])
    ax.set_ylim([-radius,radius])

    plt.show()

def _PlotLines(lines):
    x = []
    y = []
    radius = 0
    for line in lines:
        x.append(line.x1)
        x.append(line.x2)
        y.append(-line.y1)
        y.append(-line.y2)
        
        radius = max(radius, 15)
    plt.plot(x,y, 'o')
    ax = plt.gca()
    radius *= 1.5
    ax.set_xlim([-5,20])
    ax.set_ylim([-5,20])
    plt.show()


def _Equal(f1,f2, margin = 1e-5) -> bool:
    return abs(f1-f2) < margin


def _GetIndent(line: str) -> int:
    indentCount = 0
    for s in line.split(" "):
        if s != '':
            break
        indentCount += 1
    return indentCount


    
    # parser = argparse.ArgumentParser(description='Takes a kicad_mod file that contains an enclosed structure comprised of \nlines and/or arcs and converts it to a polygon with a fill. Note that \n the structure must be perfectly enclosed, \n that is, every segment starts where another ends (within 0.00001 mm')
    # parser.add_argument('inputFile', type=str, help='input file to be read and processed')
    # parser.add_argument('outputFile', type=str, help='Output file to write the new footprint file into. Must be different from input file!')

    # TODO: actually use the arguments, change the log levels based on arg
    # TODO: arguments: conserve/force layer, conserve/force width, delete replaced arcs

    # args = parser.parse_args()

     


    
    


