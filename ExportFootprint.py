from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir, QFileInfo, QSettings
import pcbnew

from .ExportFootprintDialog import Ui_mw_ExportFootprint
from .LogWrapper import LogInfo, LogDebug
from .PolygonConverter import WriteToFootprint, GetSelectedDrawings


class ExportFP(QtWidgets.QDialog):

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
        self.accepted.connect(self.SaveSettings)

        self.LoadSettings()

    def ValidateSave(self) -> bool:
            """Checks if a valid footprint name and folder are selected

            Returns:
                bool: true if the selected folder exists
            """
            name = self.ui.le_Name.text()
            folder = QDir(self.ui.le_Path.text())


            folderInfo  = QFileInfo(folder.absolutePath())

            if(folderInfo.isDir() and folderInfo.isWritable()):
                return folder.exists() and name != ""
            else:
                return False
            
    # Slots


    def SaveClicked(self):
        LogInfo("Temp path: {} {}".format(QDir.temp(),QDir.tempPath()))
        if(self.ValidateSave()):
            self.done(QtWidgets.QDialog.Accepted)
            self.close()
        else:
            msgBox = QtWidgets.QMessageBox()
            if self.ui.le_Name == "":
                msgBox.setText("Name must not be empty")    
            else:
                msgBox.setText("Selected folder does not exist or is write-protected")
            msgBox.exec()
        
        polygons = GetSelectedDrawings()
        WriteToFootprint(self.ui.le_Name.text(),self.ui.le_Path.text(),polygons, True)


    def CancelClicked(self):
        self.done(QtWidgets.QDialog.Rejected)
        self.close()


    def FolderClicked(self):
        dialog = QtWidgets.QFileDialog(self)
     
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        _OutputFolder = dialog.getExistingDirectory(self, "Select Destination Folder", QDir.homePath())
        self.ui.le_Path.setText(_OutputFolder)

    def SaveSettings(self):
        settingsPath = QDir.temp().absoluteFilePath("polygonize.ini")
        settings = QSettings(settingsPath, QSettings.IniFormat)
        settings.beginGroup("export")
        settings.setValue("path",self.ui.le_Path.text())
        settings.setValue("name",self.ui.le_Name.text())
        settings.endGroup()
        settings.sync()
        

    def LoadSettings(self):
        settingsPath = QDir.temp().absoluteFilePath("polygonize.ini")
        settings = QSettings(settingsPath, QSettings.IniFormat)
        
        settings.beginGroup("export")
        if settings.contains("path"):
            self.ui.le_Path.setText(settings.value("path"))
        if settings.contains("name"):
            self.ui.le_Name.setText(settings.value("name"))
        settings.endGroup()


        
        # if settings.contains("ui_values/path"):
            # self.ui.le_Path.setText(settings.value("ui_values/path"))
        
        # if settings.contains("ui_values/name"):
        #     self.ui.le_Name.setText(settings.value("ui_values/name"))
    
        
    