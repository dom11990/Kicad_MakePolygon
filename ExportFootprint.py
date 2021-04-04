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
        self.ui.b_SelectPath.clicked.connect(self.FolderClicked)



    def ValidateSave(self) -> bool:
            """Checks if a valid footprint name and folder are selected

            Returns:
                bool: true if the selected folder exists
            """
            name = self.ui.le_Name.text()
            folder = QDir(self.ui.le_Path.text())


            folderInfo  = QFileInfo(folder.absolutePath())

            if(folderInfo.isDir() and folderInfo.isWritable()):
                return folder.exists()
            else:
                return False
            


            


    


    # Slots

    def SaveClicked(self):
        if(self.ValidateSave()):
            self.done(QtWidgets.QDialog.Accepted)
            self.close()
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Selected folder does not exist or is write-protected")
            msgBox.exec()

    def CancelClicked(self):
        self.done(QtWidgets.QDialog.Rejected)
        self.close()

    def FolderClicked(self):
        dialog = QtWidgets.QFileDialog(self)
     
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        _OutputFolder = dialog.getExistingDirectory(self, "Select Destination Folder", QDir.homePath())
        self.ui.le_Path.setText(_OutputFolder)
        
    