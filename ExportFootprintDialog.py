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
        mw_ExportFootprint.setWindowModality(QtCore.Qt.ApplicationModal)
        mw_ExportFootprint.resize(600, 220)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mw_ExportFootprint.sizePolicy().hasHeightForWidth())
        mw_ExportFootprint.setSizePolicy(sizePolicy)
        mw_ExportFootprint.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(mw_ExportFootprint)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_FootprintName = QtWidgets.QLineEdit(self.centralwidget)
        self.le_FootprintName.setObjectName("le_FootprintName")
        self.horizontalLayout_2.addWidget(self.le_FootprintName)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 2)
        self.le_FootprintPath = QtWidgets.QLineEdit(self.centralwidget)
        self.le_FootprintPath.setObjectName("le_FootprintPath")
        self.gridLayout.addWidget(self.le_FootprintPath, 0, 4, 1, 1)
        self.b_SelectPath = QtWidgets.QPushButton(self.centralwidget)
        self.b_SelectPath.setObjectName("b_SelectPath")
        self.gridLayout.addWidget(self.b_SelectPath, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.b_Cancel = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_Cancel.sizePolicy().hasHeightForWidth())
        self.b_Cancel.setSizePolicy(sizePolicy)
        self.b_Cancel.setToolTip("")
        self.b_Cancel.setObjectName("b_Cancel")
        self.horizontalLayout.addWidget(self.b_Cancel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.b_Save = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_Save.sizePolicy().hasHeightForWidth())
        self.b_Save.setSizePolicy(sizePolicy)
        self.b_Save.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.b_Save.setObjectName("b_Save")
        self.horizontalLayout.addWidget(self.b_Save)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mw_ExportFootprint.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mw_ExportFootprint)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 30))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        mw_ExportFootprint.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mw_ExportFootprint)
        self.statusbar.setObjectName("statusbar")
        mw_ExportFootprint.setStatusBar(self.statusbar)
        self.actionHow_to_use = QtWidgets.QAction(mw_ExportFootprint)
        self.actionHow_to_use.setObjectName("actionHow_to_use")
        self.actionAbout = QtWidgets.QAction(mw_ExportFootprint)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionHow_to_use)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mw_ExportFootprint)
        QtCore.QMetaObject.connectSlotsByName(mw_ExportFootprint)

    def retranslateUi(self, mw_ExportFootprint):
        _translate = QtCore.QCoreApplication.translate
        mw_ExportFootprint.setWindowTitle(_translate("mw_ExportFootprint", "Export Footprint"))
        self.label.setText(_translate("mw_ExportFootprint", "Footprint path:"))
        self.b_SelectPath.setText(_translate("mw_ExportFootprint", "Select Path"))
        self.label_2.setText(_translate("mw_ExportFootprint", "Footprint name"))
        self.b_Cancel.setText(_translate("mw_ExportFootprint", "Cancel"))
        self.b_Save.setText(_translate("mw_ExportFootprint", "Save As"))
        self.menuHelp.setTitle(_translate("mw_ExportFootprint", "Help"))
        self.actionHow_to_use.setText(_translate("mw_ExportFootprint", "How to use?"))
        self.actionAbout.setText(_translate("mw_ExportFootprint", "About"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mw_ExportFootprint = QtWidgets.QMainWindow()
    ui = Ui_mw_ExportFootprint()
    ui.setupUi(mw_ExportFootprint)
    mw_ExportFootprint.show()
    sys.exit(app.exec_())