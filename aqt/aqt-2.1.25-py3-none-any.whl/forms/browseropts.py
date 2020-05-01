# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/browseropts.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(288, 195)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.fontCombo = QtWidgets.QFontComboBox(Dialog)
        self.fontCombo.setObjectName("fontCombo")
        self.horizontalLayout.addWidget(self.fontCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.fontSize = QtWidgets.QSpinBox(Dialog)
        self.fontSize.setMinimumSize(QtCore.QSize(75, 0))
        self.fontSize.setObjectName("fontSize")
        self.gridLayout.addWidget(self.fontSize, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineSize = QtWidgets.QSpinBox(Dialog)
        self.lineSize.setObjectName("lineSize")
        self.gridLayout.addWidget(self.lineSize, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.fullSearch = QtWidgets.QCheckBox(Dialog)
        self.fullSearch.setObjectName("fullSearch")
        self.verticalLayout.addWidget(self.fullSearch)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.fontCombo, self.fontSize)
        Dialog.setTabOrder(self.fontSize, self.lineSize)
        Dialog.setTabOrder(self.lineSize, self.fullSearch)
        Dialog.setTabOrder(self.fullSearch, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("Browser Options"))
        self.label.setText(_("<b>Font</b>:"))
        self.label_2.setText(_("<b>Font Size</b>:"))
        self.label_3.setText(_("<b>Line Size</b>:"))
        self.fullSearch.setText(_("Search within formatting (slow)"))
