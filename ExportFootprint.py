from PyQt5 import QtWidgets
from PyQt5.QtCore import *

from ExportFootprintDialog import Ui_mw_ExportFootprint
from LogWrapper import *

class ExportFootprint(QtWidgets.QDialog):



    def __init__(self):
        super().__init__()
        self.ui = Ui_mw_ExportFootprint()
        self.ui.setupUi(self)
        # in case the user clicks the x button, this way the dialog will exit as rejected
        self.setResult(QtWidgets.QDialog.Rejected)

        # slots
        self.ui.b_Save.clicked.connect(self.SaveClicked)
        self.ui.b_Cancel.clicked.connect(self.CancelClicked)
        

    def SaveClicked(self):
        self.done(QtWidgets.QDialog.Accepted)
        self.close()

    def CancelClicked(self):
        self.done(QtWidgets.QDialog.Rejected)
        self.close()


        # TODO Connect close of the gui with show of the main