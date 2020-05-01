# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object,unused-import
from anki.lang import _
# Form implementation generated from reading ui file 'designer/exporting.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        ExportDialog.setObjectName("ExportDialog")
        ExportDialog.resize(295, 223)
        self.vboxlayout = QtWidgets.QVBoxLayout(ExportDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtWidgets.QLabel(ExportDialog)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.format = QtWidgets.QComboBox(ExportDialog)
        self.format.setObjectName("format")
        self.gridlayout.addWidget(self.format, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(ExportDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.deck = QtWidgets.QComboBox(ExportDialog)
        self.deck.setObjectName("deck")
        self.gridlayout.addWidget(self.deck, 1, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.vboxlayout1 = QtWidgets.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.includeSched = QtWidgets.QCheckBox(ExportDialog)
        self.includeSched.setChecked(True)
        self.includeSched.setObjectName("includeSched")
        self.vboxlayout1.addWidget(self.includeSched)
        self.includeMedia = QtWidgets.QCheckBox(ExportDialog)
        self.includeMedia.setChecked(True)
        self.includeMedia.setObjectName("includeMedia")
        self.vboxlayout1.addWidget(self.includeMedia)
        self.includeTags = QtWidgets.QCheckBox(ExportDialog)
        self.includeTags.setChecked(True)
        self.includeTags.setObjectName("includeTags")
        self.vboxlayout1.addWidget(self.includeTags)
        self.includeHTML = QtWidgets.QCheckBox(ExportDialog)
        self.includeHTML.setObjectName("includeHTML")
        self.vboxlayout1.addWidget(self.includeHTML)
        self.vboxlayout.addLayout(self.vboxlayout1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(ExportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ExportDialog)
        self.buttonBox.accepted.connect(ExportDialog.accept)
        self.buttonBox.rejected.connect(ExportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportDialog)
        ExportDialog.setTabOrder(self.format, self.deck)
        ExportDialog.setTabOrder(self.deck, self.includeSched)
        ExportDialog.setTabOrder(self.includeSched, self.includeMedia)
        ExportDialog.setTabOrder(self.includeMedia, self.includeTags)
        ExportDialog.setTabOrder(self.includeTags, self.buttonBox)

    def retranslateUi(self, ExportDialog):
        _translate = QtCore.QCoreApplication.translate
        ExportDialog.setWindowTitle(_("Export"))
        self.label.setText(_("<b>Export format</b>:"))
        self.label_2.setText(_("<b>Include</b>:"))
        self.includeSched.setText(_("Include scheduling information"))
        self.includeMedia.setText(_("Include media"))
        self.includeTags.setText(_("Include tags"))
        self.includeHTML.setText(_("Include HTML and media references"))
