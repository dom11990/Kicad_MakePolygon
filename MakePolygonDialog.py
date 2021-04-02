# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MakePolygonDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(422, 269)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.chb_DeleteAfter = QtWidgets.QCheckBox(self.centralwidget)
        self.chb_DeleteAfter.setEnabled(True)
        self.chb_DeleteAfter.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chb_DeleteAfter.setText("")
        self.chb_DeleteAfter.setChecked(True)
        self.chb_DeleteAfter.setObjectName("chb_DeleteAfter")
        self.horizontalLayout_2.addWidget(self.chb_DeleteAfter)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 3, 1, 1)
        self.cb_Layer = QtWidgets.QComboBox(self.centralwidget)
        self.cb_Layer.setDuplicatesEnabled(True)
        self.cb_Layer.setObjectName("cb_Layer")
        self.gridLayout.addWidget(self.cb_Layer, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dsb_Width = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dsb_Width.sizePolicy().hasHeightForWidth())
        self.dsb_Width.setSizePolicy(sizePolicy)
        self.dsb_Width.setObjectName("dsb_Width")
        self.gridLayout.addWidget(self.dsb_Width, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.dsb_ArcLength = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.dsb_ArcLength.setProperty("value", 0.1)
        self.dsb_ArcLength.setObjectName("dsb_ArcLength")
        self.gridLayout.addWidget(self.dsb_ArcLength, 2, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.l_Status = QtWidgets.QLabel(self.centralwidget)
        self.l_Status.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_Status.sizePolicy().hasHeightForWidth())
        self.l_Status.setSizePolicy(sizePolicy)
        self.l_Status.setTextFormat(QtCore.Qt.PlainText)
        self.l_Status.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.l_Status.setWordWrap(True)
        self.l_Status.setObjectName("l_Status")
        self.verticalLayout.addWidget(self.l_Status)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.b_Polygonize = QtWidgets.QPushButton(self.centralwidget)
        self.b_Polygonize.setObjectName("b_Polygonize")
        self.horizontalLayout.addWidget(self.b_Polygonize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 422, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Make Polygon"))
        self.label_3.setToolTip(_translate("MainWindow", "Deletes the elements used to create the polygon. Make this false when you are checking if the polygon looks correct."))
        self.label_3.setText(_translate("MainWindow", "Delete elements?"))
        self.label_2.setToolTip(_translate("MainWindow", "The layer assigned to the fill of the polygon"))
        self.label_2.setText(_translate("MainWindow", "Layer"))
        self.label.setToolTip(_translate("MainWindow", "Width of the polygon lines. Recommended 0"))
        self.label.setText(_translate("MainWindow", "Line Width"))
        self.label_4.setText(_translate("MainWindow", "Max arc length [mm]"))
        self.dsb_ArcLength.setToolTip(_translate("MainWindow", "Specifies the maximum length an arc is allowed to have when discretizing. A smaller number means finer steps and therefore more line segments to approximate the arc."))
        self.l_Status.setText(_translate("MainWindow", "Status"))
        self.b_Polygonize.setText(_translate("MainWindow", "Polygonize!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
