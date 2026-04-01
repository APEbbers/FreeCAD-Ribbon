# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddCommandsgJdlMc.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QComboBox,
    QDialogButtonBox, QFrame, QGridLayout, QGroupBox,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(854, 556)
        Form.setAcceptDrops(True)
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalSpacer = QSpacerItem(93, 19, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout.setVerticalSpacing(0)
        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(651, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 2, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.pushButton)

        self.TrashArea = QLabel(Form)
        self.TrashArea.setObjectName(u"TrashArea")
        self.TrashArea.setMinimumSize(QSize(0, 300))
        self.TrashArea.setAcceptDrops(True)
        self.TrashArea.setStyleSheet(u"QLabel {border-color: rgb(85, 85, 255);}")
        self.TrashArea.setFrameShape(QFrame.Shape.NoFrame)
        self.TrashArea.setFrameShadow(QFrame.Shadow.Plain)

        self.verticalLayout.addWidget(self.TrashArea)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_4.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_38 = QGridLayout()
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.ListCategory_NP = QComboBox(self.tab)
        self.ListCategory_NP.setObjectName(u"ListCategory_NP")
        self.ListCategory_NP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_39.addWidget(self.ListCategory_NP, 0, 1, 1, 1)

        self.label_21 = QLabel(self.tab)
        self.label_21.setObjectName(u"label_21")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)

        self.gridLayout_39.addWidget(self.label_21, 0, 0, 1, 1)


        self.gridLayout_38.addLayout(self.gridLayout_39, 1, 0, 1, 1)

        self.SearchBar_NP = QLineEdit(self.tab)
        self.SearchBar_NP.setObjectName(u"SearchBar_NP")

        self.gridLayout_38.addWidget(self.SearchBar_NP, 0, 0, 1, 1)

        self.CommandsAvailable_NP = QListWidget(self.tab)
        __qlistwidgetitem = QListWidgetItem(self.CommandsAvailable_NP)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        self.CommandsAvailable_NP.setObjectName(u"CommandsAvailable_NP")
        self.CommandsAvailable_NP.setAcceptDrops(True)
        self.CommandsAvailable_NP.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.CommandsAvailable_NP.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.CommandsAvailable_NP.setItemAlignment(Qt.AlignmentFlag.AlignLeading)
        self.CommandsAvailable_NP.setSortingEnabled(True)
        self.CommandsAvailable_NP.setSupportedDragActions(Qt.DropAction.CopyAction)

        self.gridLayout_38.addWidget(self.CommandsAvailable_NP, 2, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_38, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.CreateNewPanel = QPushButton(self.groupBox)
        self.CreateNewPanel.setObjectName(u"CreateNewPanel")

        self.gridLayout_2.addWidget(self.CreateNewPanel, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.PanelTitle = QLineEdit(self.groupBox)
        self.PanelTitle.setObjectName(u"PanelTitle")

        self.gridLayout_2.addWidget(self.PanelTitle, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 2, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Reload", None))
        self.TrashArea.setText(QCoreApplication.translate("Form", u"Remove widget", None))
        self.label_21.setText(QCoreApplication.translate("Form", u"Category:", None))
        self.SearchBar_NP.setInputMask("")
        self.SearchBar_NP.setText("")
        self.SearchBar_NP.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search...", None))

        __sortingEnabled = self.CommandsAvailable_NP.isSortingEnabled()
        self.CommandsAvailable_NP.setSortingEnabled(False)
        ___qlistwidgetitem = self.CommandsAvailable_NP.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"New Item", None))
        self.CommandsAvailable_NP.setSortingEnabled(__sortingEnabled)

        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Create a new empty panel", None))
        self.CreateNewPanel.setText(QCoreApplication.translate("Form", u"Add panel", None))
        self.label_2.setText("")
        self.PanelTitle.setInputMask("")
        self.PanelTitle.setText("")
        self.PanelTitle.setPlaceholderText(QCoreApplication.translate("Form", u"Enter a title for the panel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"Add commands", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QCoreApplication.translate("Form", u"Create dropdown buttons", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Combine panels", None))
    # retranslateUi

