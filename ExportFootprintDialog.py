# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportFootprintDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mw_ExportFootprint(object):
    def setupUi(self, mw_ExportFootprint):
        mw_ExportFootprint.setObjectName("mw_ExportFootprint")
        mw_ExportFootprint.resize(506, 165)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mw_ExportFootprint.sizePolicy().hasHeightForWidth())
        mw_ExportFootprint.setSizePolicy(sizePolicy)
        mw_ExportFootprint.setMinimumSize(QtCore.QSize(0, 165))
        mw_ExportFootprint.setMaximumSize(QtCore.QSize(16777215, 165))
        self.gridLayout = QtWidgets.QGridLayout(mw_ExportFootprint)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.b_Cancel = QtWidgets.QPushButton(mw_ExportFootprint)
        self.b_Cancel.setObjectName("b_Cancel")
        self.horizontalLayout.addWidget(self.b_Cancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.b_Save = QtWidgets.QPushButton(mw_ExportFootprint)
        self.b_Save.setObjectName("b_Save")
        self.horizontalLayout.addWidget(self.b_Save)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(mw_ExportFootprint)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.b_SelectPath = QtWidgets.QPushButton(mw_ExportFootprint)
        self.b_SelectPath.setObjectName("b_SelectPath")
        self.gridLayout_2.addWidget(self.b_SelectPath, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(mw_ExportFootprint)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.le_Path = QtWidgets.QLineEdit(mw_ExportFootprint)
        self.le_Path.setObjectName("le_Path")
        self.gridLayout_2.addWidget(self.le_Path, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.le_Name = QtWidgets.QLineEdit(mw_ExportFootprint)
        self.le_Name.setObjectName("le_Name")
        self.horizontalLayout_2.addWidget(self.le_Name)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)

        self.retranslateUi(mw_ExportFootprint)
        QtCore.QMetaObject.connectSlotsByName(mw_ExportFootprint)

    def retranslateUi(self, mw_ExportFootprint):
        _translate = QtCore.QCoreApplication.translate
        mw_ExportFootprint.setWindowTitle(_translate("mw_ExportFootprint", "Export Footpring"))
        self.b_Cancel.setText(_translate("mw_ExportFootprint", "Cancel"))
        self.b_Save.setText(_translate("mw_ExportFootprint", "Save"))
        self.label.setText(_translate("mw_ExportFootprint", "Save Folder"))
        self.b_SelectPath.setText(_translate("mw_ExportFootprint", "Select Folder"))
        self.label_2.setText(_translate("mw_ExportFootprint", "Footprint Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw_ExportFootprint = QtWidgets.QDialog()
    ui = Ui_mw_ExportFootprint()
    ui.setupUi(mw_ExportFootprint)
    mw_ExportFootprint.show()
    sys.exit(app.exec_())
