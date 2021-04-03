import sys

#dependencies 
# pip install loguru PyQt5, matplotlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
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
        self.ui.actionAbout.triggered.connect(self.AboutClicked)
        self.ui.actionHow_to_use.triggered.connect(self.HowToUseClicked)
        # make escape close the window
        shortcut = QtWidgets.QShortcut(QKeySequence("Escape"), self)
        shortcut.activated.connect(self.close)

        # class members
        self._pcb = pcbnew.GetBoard()
        self._version = 0.1
        self._github = "https://github.com/dom11990/Kicad_MakePolygon"

        # center the main window
        desktopRect = QtWidgets.QApplication.desktop().availableGeometry()
        center = desktopRect.center()
        self.move(center.x() - self.width() * 0.5, center.y() - self.height() * 0.5)
        


        layerCount = pcbnew.PCB_LAYER_ID_COUNT
        copperLayerCount = self._pcb.GetCopperLayerCount()
        
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
        drawings = self._pcb.GetDrawings()
        for idx,drawing in enumerate(drawings):
            if drawing.IsSelected():
                selected.append(drawing)
        return selected


    def DiscretizeClicked(self):
        self.UpdateStatus("Getting drawings...")
        drawings = self._pcb.GetDrawings()
        self.UpdateStatus("Got drawing count: {}".format(drawings.GetCount()))
        
        drawings = self.GetSelectedDrawings()
        
        if not self.ValidateSelectionDiscretize(drawings):
            return

        arcsDiscretized = 0
        linesCreated = 0
        for idx,drawing in enumerate(drawings):
            shapeStr = drawing.GetShapeStr()
            self.UpdateStatus("Selected type: "+shapeStr)
            
            if shapeStr == "Arc":
                try:
                    newLines = ArcToLines(drawing, 0.05)
                except Exception as ex:
                    self.ui.l_Status.setText(str(ex))
                    return
                
                self.UpdateStatus("Parsing object {} of {}".format(idx,len(drawings)))
                # get the selected layer IDs
                layerID = self._pcb.GetLayerID(self.ui.cb_Layer.currentText())
                # add the new lines to the board
                for line in newLines: 
                    line.SetParent(self._pcb)
                    line.SetLayer(layerID)
                    line.SetWidth(pcbnew.FromMM(int(self.ui.dsb_Width.value())))
                    self._pcb.Add(line) 
                if(self.ui.chb_DeleteAfter.checkState()):
                    self._pcb.Remove(drawing)

                arcsDiscretized += 1
                linesCreated += len(newLines)
            elif shapeStr == "Line":
                pass
            elif shapeStr == "Polygon":
                self.ui.l_Status.setText("Invalid! Selection contains a polygon, only arcs and lines are allowed. Ignoring invalid items and proceeding.")
                break

            elif shapeStr == "Circle":
                self.ui.l_Status.setText("Invalid! Selection contains a circle, only arcs and lines are allowed. Ignoring invalid items and proceeding.")
                break
            
            
        pcbnew.Refresh()
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Successfully discretized {} arcs, creating {} new lines".format(arcsDiscretized,linesCreated))
        msgBox.exec()
        self.close()



    def PolygonizeClicked(self):
        drawings = self.GetSelectedDrawings()
        if not self.ValidateSelectionPolygon(drawings):
            self.ui.l_Status.setText("Polygons can only be made from lines. If you have arcs, discretize them first.")
            return
        try:
            self.SetButtonsEnabled(False)
            poly = LinesToPolygon(drawings)
        except Exception as ex:
            self.ui.l_Status.setText(str(ex))
            return
        finally:
            self.SetButtonsEnabled(True)
            
        
        # apply user selected properties, add it to the board, and close
        poly.SetParent(self._pcb)
        layerID = self._pcb.GetLayerID(self.ui.cb_Layer.currentText())
        poly.SetLayer(layerID)
        poly.SetShape(pcbnew.S_POLYGON)
        poly.SetWidth(pcbnew.FromMM(int(self.ui.dsb_Width.value())))
        self._pcb.Add(poly) 

        if(self.ui.chb_DeleteAfter.checkState()):
            for line in drawings: self._pcb.Remove(line)

        pcbnew.Refresh()
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Successfully generated polygon!")
        msgBox.exec()
        
        self.close()


    def AboutClicked(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Version {}, 2021\nDominik Eyerly\nGithub: {}".format(self._version,self._github))
        msgBox.exec()

    def HowToUseClicked(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("See Readme or Github: {} for full, up-to-date description.".format(self._github))
        msgBox.exec()

    def SetButtonsEnabled(self, enabled: bool):
        self.ui.b_Discretize.setEnabled(enabled)
        self.ui.b_Polygonize.setEnabled(enabled)
        

Polygonize().register() # Instantiate and register to Pcbnew
# Polygonize().Run()