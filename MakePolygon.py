import sys

#dependencies 
# pip install loguru PyQt5

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from loguru import logger

from PolygonConverter import PolygonConverter

sys.path.append("/home/dom/Documents/Source/KiCAD/action_scripts/MakePolygon/") 

import pcbnew

from MakePolygonDialog import Ui_MainWindow


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
        logger.info("Exiting with code: ",retval)
        # sys.exit(app.exec())


class MakePolygonDialog(QtWidgets.QMainWindow):

    def __init__(self):

        super(MakePolygonDialog, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.b_Polygonize.clicked.connect(self.PolygonizeClicked)
        

    def PolygonizeClicked(self):
        logger.info("Clicked")    
        

        inputFilePath = "D:\\SVN\\kt_kicad\\Footprints\\KT_Microstrip_Structures.pretty\\Output.kicad_mod"
        outputFilePath = "D:\\SVN\\kt_kicad\\Footprints\\KT_Microstrip_Structures.pretty\\Output2.kicad_mod"
        
        # toWrite = ConvertArcs(inputFilePath)
        PolygonConverter.ConvertPoly(inputFilePath, outputFilePath)

        

Polygonize().register() # Instantiate and register to Pcbnew
Polygonize().Run()