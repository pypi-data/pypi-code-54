# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/preview.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(335, 282)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.frontPrevBox = QtWidgets.QVBoxLayout(self.groupBox)
        self.frontPrevBox.setContentsMargins(0, 0, 0, 0)
        self.frontPrevBox.setObjectName("frontPrevBox")
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.backPrevBox = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.backPrevBox.setContentsMargins(0, 0, 0, 0)
        self.backPrevBox.setObjectName("backPrevBox")
        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_("Form"))
        self.groupBox.setTitle(_("Front Preview"))
        self.groupBox_2.setTitle(_("Back Preview"))
