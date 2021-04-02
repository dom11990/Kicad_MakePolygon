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

        # slots
        self.ui.b_Polygonize.clicked.connect(self.PolygonizeClicked)
        self.ui.b_Discretize.clicked.connect(self.DiscretizeClicked)

        # class members
        self.pcb = pcbnew.GetBoard()

        
        layerCount = pcbnew.PCB_LAYER_ID_COUNT
        copperLayerCount = self.pcb.GetCopperLayerCount()
        
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


    def ValidateSelectionPolygon(self, drawings):
        for drawing in drawings:
            if drawing.GetShapeStr() != "Line":
                return False
        return True

    def ValidateSelectionDiscretize(self, drawings):
        """Checks if there are any invalid selections such as circles or polygons

        Args:
            drawings (DrawingsList):

        Returns:
            bool: True if the selection is good
        """
        valid = True
        for idx,drawing in enumerate(drawings):
            if drawing.IsSelected():
                shapeStr = drawing.GetShapeStr()
                if shapeStr == "Polygon":
                    self.ui.l_Status.setText("Invalid! Selection contains a polygon, only arcs and lines are allowed.")
                    valid= False
                    break

                elif shapeStr == "Circle":
                    self.ui.l_Status.setText("Invalid! Selection contains a circle, only arcs and lines are allowed.")
                    valid = False
                    break
        return valid
        

    
    def GetSelectedDrawings(self):
        """Retrieves only the selected drawings

        Returns:
            List of drawings:
        """

        selected = []
        drawings = self.pcb.GetDrawings()
        for idx,drawing in enumerate(drawings):
            if drawing.IsSelected():
                selected.append(drawing)
        return selected


    def DiscretizeClicked(self):
        self.UpdateStatus("Getting drawings...")
        drawings = self.pcb.GetDrawings()
        self.UpdateStatus("Got drawing count: {}".format(drawings.GetCount()))
        
        drawings = self.GetSelectedDrawings()
        
        if not self.ValidateSelectionDiscretize(drawings):
            return


        for idx,drawing in enumerate(drawings):
            shapeStr = drawing.GetShapeStr()
            self.UpdateStatus("Selected type: "+shapeStr)
            
            if shapeStr == "Arc":
                # ArcToLines(drawing, self.ui.dsb_ArcLength.value())
                newLines = ArcToLines(drawing, 0.05)
                self.UpdateStatus("Parsing object {} of {}".format(idx,len(drawings)))
                # get the selected layer IDs
                layerID = self.pcb.GetLayerID(self.ui.cb_Layer.currentText())
                # add the new lines to the board
                for line in newLines: 
                    line.SetParent(self.pcb)
                    line.SetLayer(layerID)
                    line.SetWidth(pcbnew.FromMM(int(self.ui.dsb_Width.value())))
                    self.pcb.Add(line) 
                if(self.ui.chb_DeleteAfter.checkState()):
                    self.pcb.Remove(drawing)

                
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
            
            
        pcbnew.Refresh()
        self.close()



    def PolygonizeClicked(self):
        drawings = self.GetSelectedDrawings()
        if not self.ValidateSelectionPolygon(drawings):
            self.ui.l_Status.setText("Polygons can only be made from lines. If you have arcs, discretize them first.")
            return
        poly = LinesToPolygon(drawings)
        
        # apply user selected properties, add it to the board, and close
        poly.SetParent(self.pcb)
        layerID = self.pcb.GetLayerID(self.ui.cb_Layer.currentText())
        poly.SetLayer(layerID)
        poly.SetShape(pcbnew.S_POLYGON)
        poly.SetWidth(pcbnew.FromMM(int(self.ui.dsb_Width.value())))
        self.pcb.Add(poly) 

        if(self.ui.chb_DeleteAfter.checkState()):
            for line in drawings: self.pcb.Remove(line)

        pcbnew.Refresh()
        self.ui.l_Status.setText("Added polygon")
        
        self.close()

#TODO: if during poligonization i find a duplicate, give the option to delete both! this allows two structures that touch to be treated as one large structure

        

Polygonize().register() # Instantiate and register to Pcbnew
# Polygonize().Run()