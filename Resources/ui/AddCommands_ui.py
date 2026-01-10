# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddCommandshDkFJG.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(471, 418)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_37 = QGridLayout(self.groupBox)
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.gridLayout_38 = QGridLayout()
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.SearchBar_NP = QLineEdit(self.groupBox)
        self.SearchBar_NP.setObjectName(u"SearchBar_NP")

        self.gridLayout_38.addWidget(self.SearchBar_NP, 0, 0, 1, 1)

        self.CommandsAvailable_NP = QListWidget(self.groupBox)
        __qlistwidgetitem = QListWidgetItem(self.CommandsAvailable_NP)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        self.CommandsAvailable_NP.setObjectName(u"CommandsAvailable_NP")
        self.CommandsAvailable_NP.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.CommandsAvailable_NP.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.CommandsAvailable_NP.setItemAlignment(Qt.AlignmentFlag.AlignLeading)
        self.CommandsAvailable_NP.setSortingEnabled(True)
        self.CommandsAvailable_NP.setSupportedDragActions(Qt.DropAction.CopyAction)

        self.gridLayout_38.addWidget(self.CommandsAvailable_NP, 2, 0, 1, 1)

        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)

        self.gridLayout_39.addWidget(self.label_21, 0, 0, 1, 1)

        self.ListCategory_NP = QComboBox(self.groupBox)
        self.ListCategory_NP.setObjectName(u"ListCategory_NP")
        self.ListCategory_NP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_39.addWidget(self.ListCategory_NP, 0, 1, 1, 1)


        self.gridLayout_38.addLayout(self.gridLayout_39, 1, 0, 1, 1)


        self.gridLayout_37.addLayout(self.gridLayout_38, 2, 0, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_37.addWidget(self.label_20, 0, 0, 2, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.SearchBar_NP.setInputMask("")
        self.SearchBar_NP.setText("")
        self.SearchBar_NP.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search...", None))

        __sortingEnabled = self.CommandsAvailable_NP.isSortingEnabled()
        self.CommandsAvailable_NP.setSortingEnabled(False)
        ___qlistwidgetitem = self.CommandsAvailable_NP.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.CommandsAvailable_NP.setSortingEnabled(__sortingEnabled)

        self.label_21.setText(QCoreApplication.translate("Form", u"Category:", None))
        self.label_20.setText(QCoreApplication.translate("Form", u"Select commands to add to the new panel", None))
    # retranslateUi

