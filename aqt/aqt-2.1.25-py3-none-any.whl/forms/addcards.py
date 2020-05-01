# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/addcards.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 366)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/anki.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(12, 6, 12, 12)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.modelArea = QtWidgets.QWidget(Dialog)
        self.modelArea.setMinimumSize(QtCore.QSize(0, 10))
        self.modelArea.setObjectName("modelArea")
        self.horizontalLayout.addWidget(self.modelArea)
        self.deckArea = QtWidgets.QWidget(Dialog)
        self.deckArea.setObjectName("deckArea")
        self.horizontalLayout.addWidget(self.deckArea)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.fieldsArea = QtWidgets.QWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.fieldsArea.sizePolicy().hasHeightForWidth())
        self.fieldsArea.setSizePolicy(sizePolicy)
        self.fieldsArea.setAutoFillBackground(True)
        self.fieldsArea.setObjectName("fieldsArea")
        self.verticalLayout.addWidget(self.fieldsArea)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.NoButton)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_("Add"))
from . import icons_rc
