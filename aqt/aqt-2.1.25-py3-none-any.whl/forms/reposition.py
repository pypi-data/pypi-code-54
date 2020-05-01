# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/reposition.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(272, 229)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.start = QtWidgets.QSpinBox(Dialog)
        self.start.setMinimum(-20000000)
        self.start.setMaximum(200000000)
        self.start.setProperty("value", 0)
        self.start.setObjectName("start")
        self.gridLayout.addWidget(self.start, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.step = QtWidgets.QSpinBox(Dialog)
        self.step.setMinimum(1)
        self.step.setMaximum(10000)
        self.step.setObjectName("step")
        self.gridLayout.addWidget(self.step, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.randomize = QtWidgets.QCheckBox(Dialog)
        self.randomize.setObjectName("randomize")
        self.verticalLayout.addWidget(self.randomize)
        self.shift = QtWidgets.QCheckBox(Dialog)
        self.shift.setChecked(True)
        self.shift.setObjectName("shift")
        self.verticalLayout.addWidget(self.shift)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.start, self.step)
        Dialog.setTabOrder(self.step, self.randomize)
        Dialog.setTabOrder(self.randomize, self.shift)
        Dialog.setTabOrder(self.shift, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("Reposition New Cards"))
        self.label_2.setText(_("Start position:"))
        self.label_3.setText(_("Step:"))
        self.randomize.setText(_("Randomize order"))
        self.shift.setText(_("Shift position of existing cards"))
