import sys

#dependencies 
# pip install loguru PyQt5, matplotlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets



# from PolygonConverter import PolygonConverter

# sys.path.append("/home/dom/Documents/Source/KiCAD/action_scripts/MakePolygon/") 
# sys.path.append("./") 

import pcbnew

from MakePolygonDialog import Ui_MainWindow


from PolygonConverter import *
from LogWrapper import *

class Polygonize(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Polygonize"
        self.category = ""
        self.description = "Takes the selected arcs and lines (that form an enclosed shape) and creates a polygon that can be filled"
        

    def Run(self):
        # The entry function of the plugin that is executed on user action

        app = QtWidgets.QApplication([])
        
        application = MakePolygonDialog()
        application.show()
        retval = app.exec()
        # sys.exit(app.exec())


class MakePolygonDialog(QtWidgets.QMainWindow):

    def __init__(self):

        super(MakePolygonDialog, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.b_Polygonize.clicked.connect(self.PolygonizeClicked)

        pcb = pcbnew.GetBoard()
        layerCount = pcbnew.PCB_LAYER_ID_COUNT
        copperLayerCount = pcb.GetCopperLayerCount()
        
        #this layer stuff is so gross. there must be a better way...
        # todo: extract only the layers that the user selected in their
        # board config
        layers = []
        # layers are organized with copper at the start, FCu , InnerN.. BCu
        # so if fewer than all copper layers are used the index has to be changed
        # to skip the unused inner layers
        for i in range(0,copperLayerCount-1) : layers.append(pcbnew.BOARD_GetStandardLayerName(i))
        
        for i in range(31,layerCount-1):
            layers.append(pcbnew.BOARD_GetStandardLayerName(i))
        
        # add the valid layers to the combo box
        for s in layers:
            self.ui.cb_Layer.addItem(s)
            
        

    def UpdateStatus(self, text: str) -> None:
        self.ui.l_Status.setText(text)


    def PolygonizeClicked(self):

        pcb = pcbnew.GetBoard()

        self.UpdateStatus("Getting drawings...")
        drawings = pcb.GetDrawings()
        self.UpdateStatus("Got drawing count: {}".format(drawings.GetCount()))
        valid = True
        for idx,drawing in enumerate(drawings):
            if drawing.IsSelected():
                shapeStr = drawing.GetShapeStr()
                self.UpdateStatus("Selected type: "+shapeStr)
                
                if shapeStr == "Arc":
                    # ArcToLines(drawing, self.ui.dsb_ArcLength.value())
                    newLines = ArcToLines(drawing, 0.05)
                    self.UpdateStatus("Parsing object {} of {}".format(idx,drawings.GetCount()))
                    # get the selected layer IDs
                    logInfo("Getting layerID: {}".format(self.ui.cb_Layer.currentText()))
                    layerID = pcb.GetLayerID(self.ui.cb_Layer.currentText())
                    logInfo("Got layerID {}".format(layerID))
                    # add the new lines to the board
                    for line in newLines: 
                        line.SetLayer(layerID)
                        pcb.Add(line) 

                    pcbnew.Refresh()

                    pass
                elif shapeStr == "Line":
                    pass
                elif shapeStr == "Polygon":
                    self.ui.l_Status.setText("Invalid! Selection contains a polygon, only arcs and lines are allowed.")
                    valid= False
                    break

                elif shapeStr == "Circle":
                    self.ui.l_Status.setText("Invalid! Selection contains a circle, only arcs and lines are allowed.")
                    valid = False
                    break
                
                self.close()
        
        


        
        # PolygonConverter.ConvertPoly(inputFilePath, outputFilePath)

        

Polygonize().register() # Instantiate and register to Pcbnew
# Polygonize().Run()