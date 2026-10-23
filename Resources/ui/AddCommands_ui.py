# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddCommandsVVWXut.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QToolButton, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(749, 739)
        Form.setAcceptDrops(True)
        self.gridLayout_13 = QGridLayout(Form)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.DockedButtonFrame = QFrame(Form)
        self.DockedButtonFrame.setObjectName(u"DockedButtonFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DockedButtonFrame.sizePolicy().hasHeightForWidth())
        self.DockedButtonFrame.setSizePolicy(sizePolicy)
        self.gridLayout_Docked = QGridLayout(self.DockedButtonFrame)
        self.gridLayout_Docked.setObjectName(u"gridLayout_Docked")
        self.okButton_2 = QPushButton(self.DockedButtonFrame)
        self.okButton_2.setObjectName(u"okButton_2")

        self.gridLayout_Docked.addWidget(self.okButton_2, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_Docked.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)

        self.cancelButton_2 = QPushButton(self.DockedButtonFrame)
        self.cancelButton_2.setObjectName(u"cancelButton_2")

        self.gridLayout_Docked.addWidget(self.cancelButton_2, 0, 3, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_Docked.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.verticalSpacer_dockedButtons = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_Docked.addItem(self.verticalSpacer_dockedButtons, 1, 1, 1, 1)

        self.applyButton_2 = QPushButton(self.DockedButtonFrame)
        self.applyButton_2.setObjectName(u"applyButton_2")

        self.gridLayout_Docked.addWidget(self.applyButton_2, 0, 2, 1, 1)


        self.gridLayout_13.addWidget(self.DockedButtonFrame, 0, 0, 1, 1)

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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy1)

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
        self.CommandsAvailable_NP.setSortingEnabled(True)
        self.CommandsAvailable_NP.setSupportedDragActions(Qt.DropAction.IgnoreAction)

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
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_6 = QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.CustomToolbarSelector_CP = QComboBox(self.tab_2)
        self.CustomToolbarSelector_CP.setObjectName(u"CustomToolbarSelector_CP")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.CustomToolbarSelector_CP.sizePolicy().hasHeightForWidth())
        self.CustomToolbarSelector_CP.setSizePolicy(sizePolicy2)
        self.CustomToolbarSelector_CP.setMinimumSize(QSize(150, 0))
        self.CustomToolbarSelector_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.CustomToolbarSelector_CP, 0, 1, 1, 2)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)

        self.RemovePanel_CP = QPushButton(self.tab_2)
        self.RemovePanel_CP.setObjectName(u"RemovePanel_CP")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.RemovePanel_CP.sizePolicy().hasHeightForWidth())
        self.RemovePanel_CP.setSizePolicy(sizePolicy3)
        self.RemovePanel_CP.setMinimumSize(QSize(100, 0))
        self.RemovePanel_CP.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.RemovePanel_CP, 0, 3, 1, 1)

        self.label_10 = QLabel(self.tab_2)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_10, 2, 0, 2, 1)

        self.WorkbenchList_CP = QComboBox(self.tab_2)
        self.WorkbenchList_CP.setObjectName(u"WorkbenchList_CP")
        sizePolicy2.setHeightForWidth(self.WorkbenchList_CP.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_CP.setSizePolicy(sizePolicy2)
        self.WorkbenchList_CP.setMinimumSize(QSize(0, 0))
        self.WorkbenchList_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.WorkbenchList_CP, 1, 1, 1, 3)

        self.PanelName_CP = QLineEdit(self.tab_2)
        self.PanelName_CP.setObjectName(u"PanelName_CP")
        sizePolicy2.setHeightForWidth(self.PanelName_CP.sizePolicy().hasHeightForWidth())
        self.PanelName_CP.setSizePolicy(sizePolicy2)
        self.PanelName_CP.setMinimumSize(QSize(120, 0))

        self.gridLayout_8.addWidget(self.PanelName_CP, 2, 1, 2, 3)


        self.gridLayout_6.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setSizeIncrement(QSize(0, 0))
        self.gridLayout_9 = QGridLayout(self.groupBox_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_9.addWidget(self.label_11, 0, 0, 1, 3)

        self.PanelAvailable_CP = QListWidget(self.groupBox_3)
        __qlistwidgetitem1 = QListWidgetItem(self.PanelAvailable_CP)
        __qlistwidgetitem1.setCheckState(Qt.Checked)
        self.PanelAvailable_CP.setObjectName(u"PanelAvailable_CP")
        self.PanelAvailable_CP.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.PanelAvailable_CP.setSortingEnabled(True)

        self.gridLayout_9.addWidget(self.PanelAvailable_CP, 1, 0, 1, 1)

        self.gridLayout_48 = QGridLayout()
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.PanelSelected_CP = QListWidget(self.groupBox_3)
        __qlistwidgetitem2 = QListWidgetItem(self.PanelSelected_CP)
        __qlistwidgetitem2.setCheckState(Qt.Checked)
        self.PanelSelected_CP.setObjectName(u"PanelSelected_CP")
        self.PanelSelected_CP.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.PanelSelected_CP.setMovement(QListView.Movement.Free)
        self.PanelSelected_CP.setViewMode(QListView.ViewMode.ListMode)
        self.PanelSelected_CP.setSortingEnabled(False)

        self.gridLayout_48.addWidget(self.PanelSelected_CP, 0, 0, 1, 1)

        self.AddCustomPanel_CP = QPushButton(self.groupBox_3)
        self.AddCustomPanel_CP.setObjectName(u"AddCustomPanel_CP")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.AddCustomPanel_CP.sizePolicy().hasHeightForWidth())
        self.AddCustomPanel_CP.setSizePolicy(sizePolicy4)
        self.AddCustomPanel_CP.setMinimumSize(QSize(10, 0))
        self.AddCustomPanel_CP.setBaseSize(QSize(15, 0))

        self.gridLayout_48.addWidget(self.AddCustomPanel_CP, 1, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_48, 1, 2, 1, 1)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_7, 4, 0, 1, 1)

        self.MoveUpPanelCommand_CP = QToolButton(self.groupBox_3)
        self.MoveUpPanelCommand_CP.setObjectName(u"MoveUpPanelCommand_CP")
        self.MoveUpPanelCommand_CP.setText(u"...")
        self.MoveUpPanelCommand_CP.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_12.addWidget(self.MoveUpPanelCommand_CP, 2, 0, 1, 1)

        self.MoveDownPanelCommand_CP = QToolButton(self.groupBox_3)
        self.MoveDownPanelCommand_CP.setObjectName(u"MoveDownPanelCommand_CP")
        self.MoveDownPanelCommand_CP.setText(u"...")
        self.MoveDownPanelCommand_CP.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_12.addWidget(self.MoveDownPanelCommand_CP, 3, 0, 1, 1)

        self.AddPanel_CP = QToolButton(self.groupBox_3)
        self.AddPanel_CP.setObjectName(u"AddPanel_CP")
        self.AddPanel_CP.setText(u"...")
        self.AddPanel_CP.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_12.addWidget(self.AddPanel_CP, 0, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_10, 1, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_12, 1, 1, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.gridLayout_5 = QGridLayout(self.widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_50 = QGridLayout(self.groupBox_5)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_50.addWidget(self.label_23, 0, 0, 1, 1)

        self.gridLayout_40 = QGridLayout()
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.CommandsAvailable_DDB = QListWidget(self.groupBox_5)
        __qlistwidgetitem3 = QListWidgetItem(self.CommandsAvailable_DDB)
        __qlistwidgetitem3.setCheckState(Qt.Checked)
        self.CommandsAvailable_DDB.setObjectName(u"CommandsAvailable_DDB")
        self.CommandsAvailable_DDB.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.CommandsAvailable_DDB.setSortingEnabled(True)

        self.gridLayout_40.addWidget(self.CommandsAvailable_DDB, 2, 0, 1, 1)

        self.SearchBar_DDB = QLineEdit(self.groupBox_5)
        self.SearchBar_DDB.setObjectName(u"SearchBar_DDB")

        self.gridLayout_40.addWidget(self.SearchBar_DDB, 0, 0, 1, 1)

        self.gridLayout_41 = QGridLayout()
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")
        sizePolicy1.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy1)

        self.gridLayout_41.addWidget(self.label_22, 0, 0, 1, 1)

        self.ListCategory_DDB = QComboBox(self.groupBox_5)
        self.ListCategory_DDB.setObjectName(u"ListCategory_DDB")
        self.ListCategory_DDB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_41.addWidget(self.ListCategory_DDB, 0, 1, 1, 1)


        self.gridLayout_40.addLayout(self.gridLayout_41, 1, 0, 1, 1)


        self.gridLayout_50.addLayout(self.gridLayout_40, 1, 0, 1, 1)

        self.gridLayout_42 = QGridLayout()
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.verticalSpacer_19 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_42.addItem(self.verticalSpacer_19, 5, 0, 1, 1)

        self.AddCommand_DDB = QToolButton(self.groupBox_5)
        self.AddCommand_DDB.setObjectName(u"AddCommand_DDB")
        self.AddCommand_DDB.setText(u"...")
        self.AddCommand_DDB.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_42.addWidget(self.AddCommand_DDB, 2, 0, 1, 1)

        self.MoveDownCommand_DDB = QToolButton(self.groupBox_5)
        self.MoveDownCommand_DDB.setObjectName(u"MoveDownCommand_DDB")
        self.MoveDownCommand_DDB.setText(u"...")
        self.MoveDownCommand_DDB.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_42.addWidget(self.MoveDownCommand_DDB, 7, 0, 1, 1)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_42.addItem(self.verticalSpacer_20, 1, 0, 1, 1)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_42.addItem(self.verticalSpacer_21, 8, 0, 1, 1)

        self.RemoveCommand_DDB = QToolButton(self.groupBox_5)
        self.RemoveCommand_DDB.setObjectName(u"RemoveCommand_DDB")
        self.RemoveCommand_DDB.setText(u"...")
        self.RemoveCommand_DDB.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_42.addWidget(self.RemoveCommand_DDB, 3, 0, 1, 1)

        self.MoveUpCommand_DDB = QToolButton(self.groupBox_5)
        self.MoveUpCommand_DDB.setObjectName(u"MoveUpCommand_DDB")
        self.MoveUpCommand_DDB.setText(u"...")
        self.MoveUpCommand_DDB.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_42.addWidget(self.MoveUpCommand_DDB, 6, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_42.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.gridLayout_50.addLayout(self.gridLayout_42, 1, 1, 1, 1)

        self.gridLayout_36 = QGridLayout()
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.RemoveControl_DDB = QPushButton(self.groupBox_5)
        self.RemoveControl_DDB.setObjectName(u"RemoveControl_DDB")
        sizePolicy3.setHeightForWidth(self.RemoveControl_DDB.sizePolicy().hasHeightForWidth())
        self.RemoveControl_DDB.setSizePolicy(sizePolicy3)
        self.RemoveControl_DDB.setMinimumSize(QSize(120, 0))

        self.gridLayout_36.addWidget(self.RemoveControl_DDB, 0, 1, 1, 1)

        self.NewControl_DDB = QListWidget(self.groupBox_5)
        __qlistwidgetitem4 = QListWidgetItem(self.NewControl_DDB)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        self.NewControl_DDB.setObjectName(u"NewControl_DDB")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.NewControl_DDB.sizePolicy().hasHeightForWidth())
        self.NewControl_DDB.setSizePolicy(sizePolicy5)
        self.NewControl_DDB.setMinimumSize(QSize(300, 0))
        self.NewControl_DDB.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.NewControl_DDB.setSortingEnabled(False)

        self.gridLayout_36.addWidget(self.NewControl_DDB, 2, 0, 1, 2)

        self.CommandList_DDB = QComboBox(self.groupBox_5)
        self.CommandList_DDB.setObjectName(u"CommandList_DDB")
        sizePolicy4.setHeightForWidth(self.CommandList_DDB.sizePolicy().hasHeightForWidth())
        self.CommandList_DDB.setSizePolicy(sizePolicy4)

        self.gridLayout_36.addWidget(self.CommandList_DDB, 0, 0, 1, 1)

        self.ControlName_DDB = QLineEdit(self.groupBox_5)
        self.ControlName_DDB.setObjectName(u"ControlName_DDB")

        self.gridLayout_36.addWidget(self.ControlName_DDB, 1, 0, 1, 2)

        self.CreateControl_DDB = QPushButton(self.groupBox_5)
        self.CreateControl_DDB.setObjectName(u"CreateControl_DDB")

        self.gridLayout_36.addWidget(self.CreateControl_DDB, 3, 0, 1, 2)


        self.gridLayout_50.addLayout(self.gridLayout_36, 1, 2, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.widget, "")
        self.CreateMacroButtons = QWidget()
        self.CreateMacroButtons.setObjectName(u"CreateMacroButtons")
        self.gridLayout_17 = QGridLayout(self.CreateMacroButtons)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(6, 6, 6, 6)
        self.groupBox_4 = QGroupBox(self.CreateMacroButtons)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_10 = QGridLayout(self.groupBox_4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(6, 6, 6, 6)
        self.MacroList = QListWidget(self.groupBox_4)
        self.MacroList.setObjectName(u"MacroList")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.MacroList.sizePolicy().hasHeightForWidth())
        self.MacroList.setSizePolicy(sizePolicy6)
        self.MacroList.setMaximumSize(QSize(16777215, 300))
        self.MacroList.setFrameShape(QFrame.Shape.Box)
        self.MacroList.setSupportedDragActions(Qt.DropAction.IgnoreAction)

        self.gridLayout_10.addWidget(self.MacroList, 0, 0, 1, 1)


        self.gridLayout_17.addWidget(self.groupBox_4, 0, 0, 2, 1)

        self.groupBox_2 = QGroupBox(self.CreateMacroButtons)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(0)
        self.gridLayout_7.setVerticalSpacing(10)
        self.SetShortcut = QLineEdit(self.groupBox_2)
        self.SetShortcut.setObjectName(u"SetShortcut")
        sizePolicy3.setHeightForWidth(self.SetShortcut.sizePolicy().hasHeightForWidth())
        self.SetShortcut.setSizePolicy(sizePolicy3)
        self.SetShortcut.setMinimumSize(QSize(200, 30))
        self.SetShortcut.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SetShortcut, 5, 1, 1, 1)

        self.SetStatusText = QLineEdit(self.groupBox_2)
        self.SetStatusText.setObjectName(u"SetStatusText")
        sizePolicy3.setHeightForWidth(self.SetStatusText.sizePolicy().hasHeightForWidth())
        self.SetStatusText.setSizePolicy(sizePolicy3)
        self.SetStatusText.setMinimumSize(QSize(200, 30))
        self.SetStatusText.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SetStatusText, 3, 1, 1, 1)

        self.SetMenuText = QLineEdit(self.groupBox_2)
        self.SetMenuText.setObjectName(u"SetMenuText")
        sizePolicy3.setHeightForWidth(self.SetMenuText.sizePolicy().hasHeightForWidth())
        self.SetMenuText.setSizePolicy(sizePolicy3)
        self.SetMenuText.setMinimumSize(QSize(200, 30))
        self.SetMenuText.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SetMenuText, 1, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        sizePolicy1.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy1)
        self.label_6.setMinimumSize(QSize(100, 0))
        self.label_6.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_6, 3, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setMinimumSize(QSize(100, 0))
        self.label_12.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_12, 5, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)
        self.label_8.setMinimumSize(QSize(100, 0))
        self.label_8.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_8, 4, 0, 1, 1)

        self.SelectMacro = QComboBox(self.groupBox_2)
        self.SelectMacro.setObjectName(u"SelectMacro")
        sizePolicy3.setHeightForWidth(self.SelectMacro.sizePolicy().hasHeightForWidth())
        self.SelectMacro.setSizePolicy(sizePolicy3)
        self.SelectMacro.setMinimumSize(QSize(200, 30))
        self.SelectMacro.setMaximumSize(QSize(16777215, 30))
        self.SelectMacro.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.SelectMacro, 0, 1, 1, 1)

        self.SetToolTip = QLineEdit(self.groupBox_2)
        self.SetToolTip.setObjectName(u"SetToolTip")
        sizePolicy3.setHeightForWidth(self.SetToolTip.sizePolicy().hasHeightForWidth())
        self.SetToolTip.setSizePolicy(sizePolicy3)
        self.SetToolTip.setMinimumSize(QSize(200, 30))
        self.SetToolTip.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SetToolTip, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_4, 1, 0, 1, 1)

        self.SetWhatIsThis = QLineEdit(self.groupBox_2)
        self.SetWhatIsThis.setObjectName(u"SetWhatIsThis")
        sizePolicy3.setHeightForWidth(self.SetWhatIsThis.sizePolicy().hasHeightForWidth())
        self.SetWhatIsThis.setSizePolicy(sizePolicy3)
        self.SetWhatIsThis.setMinimumSize(QSize(200, 30))
        self.SetWhatIsThis.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SetWhatIsThis, 4, 1, 1, 1)

        self.SelectIcon = QToolButton(self.groupBox_2)
        self.SelectIcon.setObjectName(u"SelectIcon")
        self.SelectIcon.setMaximumSize(QSize(32, 32))

        self.gridLayout_7.addWidget(self.SelectIcon, 6, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        sizePolicy1.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy1)
        self.label_13.setMinimumSize(QSize(100, 0))
        self.label_13.setBaseSize(QSize(0, 0))

        self.gridLayout_7.addWidget(self.label_13, 6, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.AddButton = QPushButton(self.groupBox_2)
        self.AddButton.setObjectName(u"AddButton")

        self.horizontalLayout.addWidget(self.AddButton)

        self.RemoveButton = QPushButton(self.groupBox_2)
        self.RemoveButton.setObjectName(u"RemoveButton")

        self.horizontalLayout.addWidget(self.RemoveButton)

        self.ReplaceButton = QPushButton(self.groupBox_2)
        self.ReplaceButton.setObjectName(u"ReplaceButton")

        self.horizontalLayout.addWidget(self.ReplaceButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 1)


        self.gridLayout_17.addWidget(self.groupBox_2, 0, 1, 2, 1)

        self.groupBox_6 = QGroupBox(self.CreateMacroButtons)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy7)
        self.gridLayout_11 = QGridLayout(self.groupBox_6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(6, 6, 6, 6)
        self.ListMacroButtons = QTableWidget(self.groupBox_6)
        if (self.ListMacroButtons.columnCount() < 6):
            self.ListMacroButtons.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.ListMacroButtons.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ListMacroButtons.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ListMacroButtons.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.ListMacroButtons.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.ListMacroButtons.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.ListMacroButtons.rowCount() < 6):
            self.ListMacroButtons.setRowCount(6)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(3, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(4, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.ListMacroButtons.setVerticalHeaderItem(5, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.ListMacroButtons.setItem(0, 0, __qtablewidgetitem11)
        self.ListMacroButtons.setObjectName(u"ListMacroButtons")
        sizePolicy5.setHeightForWidth(self.ListMacroButtons.sizePolicy().hasHeightForWidth())
        self.ListMacroButtons.setSizePolicy(sizePolicy5)
        self.ListMacroButtons.setFrameShape(QFrame.Shape.Box)
        self.ListMacroButtons.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.ListMacroButtons.setTabKeyNavigation(False)
        self.ListMacroButtons.setProperty(u"showDropIndicator", False)
        self.ListMacroButtons.setDragDropOverwriteMode(False)
        self.ListMacroButtons.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.ListMacroButtons.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.ListMacroButtons.setShowGrid(False)
        self.ListMacroButtons.setSupportedDragActions(Qt.DropAction.IgnoreAction)
        self.ListMacroButtons.horizontalHeader().setVisible(False)
        self.ListMacroButtons.horizontalHeader().setHighlightSections(False)
        self.ListMacroButtons.verticalHeader().setVisible(False)
        self.ListMacroButtons.verticalHeader().setHighlightSections(False)

        self.gridLayout_11.addWidget(self.ListMacroButtons, 0, 1, 1, 2)

        self.pushButton = QPushButton(self.groupBox_6)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_11.addWidget(self.pushButton, 1, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_4, 1, 2, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_2, 2, 2, 1, 1)


        self.gridLayout_17.addWidget(self.groupBox_6, 2, 0, 1, 2)

        self.tabWidget.addTab(self.CreateMacroButtons, "")

        self.gridLayout_13.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout.setVerticalSpacing(0)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.cancelButton = QPushButton(Form)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout.addWidget(self.cancelButton, 0, 5, 2, 1)

        self.HelpButton = QToolButton(Form)
        self.HelpButton.setObjectName(u"HelpButton")
        self.HelpButton.setText(u"...")

        self.gridLayout.addWidget(self.HelpButton, 0, 7, 2, 1)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_11, 0, 6, 2, 1)

        self.applyButton = QPushButton(Form)
        self.applyButton.setObjectName(u"applyButton")

        self.gridLayout.addWidget(self.applyButton, 0, 4, 2, 1)

        self.TimeStamp_Reloaded = QLabel(Form)
        self.TimeStamp_Reloaded.setObjectName(u"TimeStamp_Reloaded")
        font = QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.TimeStamp_Reloaded.setFont(font)

        self.gridLayout.addWidget(self.TimeStamp_Reloaded, 1, 1, 1, 1)

        self.LoadWB = QPushButton(Form)
        self.LoadWB.setObjectName(u"LoadWB")
        sizePolicy3.setHeightForWidth(self.LoadWB.sizePolicy().hasHeightForWidth())
        self.LoadWB.setSizePolicy(sizePolicy3)
        self.LoadWB.setMinimumSize(QSize(34, 34))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.LoadWB.setIcon(icon)

        self.gridLayout.addWidget(self.LoadWB, 0, 0, 2, 1)

        self.horizontalSpacer = QSpacerItem(651, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.okButton = QPushButton(Form)
        self.okButton.setObjectName(u"okButton")

        self.gridLayout.addWidget(self.okButton, 0, 3, 2, 1)


        self.gridLayout_13.addLayout(self.gridLayout, 2, 0, 1, 1)

        QWidget.setTabOrder(self.okButton_2, self.applyButton_2)
        QWidget.setTabOrder(self.applyButton_2, self.cancelButton_2)
        QWidget.setTabOrder(self.cancelButton_2, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.SearchBar_NP)
        QWidget.setTabOrder(self.SearchBar_NP, self.ListCategory_NP)
        QWidget.setTabOrder(self.ListCategory_NP, self.CommandsAvailable_NP)
        QWidget.setTabOrder(self.CommandsAvailable_NP, self.PanelTitle)
        QWidget.setTabOrder(self.PanelTitle, self.CreateNewPanel)
        QWidget.setTabOrder(self.CreateNewPanel, self.LoadWB)
        QWidget.setTabOrder(self.LoadWB, self.okButton)
        QWidget.setTabOrder(self.okButton, self.applyButton)
        QWidget.setTabOrder(self.applyButton, self.cancelButton)
        QWidget.setTabOrder(self.cancelButton, self.HelpButton)
        QWidget.setTabOrder(self.HelpButton, self.CustomToolbarSelector_CP)
        QWidget.setTabOrder(self.CustomToolbarSelector_CP, self.RemovePanel_CP)
        QWidget.setTabOrder(self.RemovePanel_CP, self.WorkbenchList_CP)
        QWidget.setTabOrder(self.WorkbenchList_CP, self.PanelName_CP)
        QWidget.setTabOrder(self.PanelName_CP, self.PanelAvailable_CP)
        QWidget.setTabOrder(self.PanelAvailable_CP, self.AddPanel_CP)
        QWidget.setTabOrder(self.AddPanel_CP, self.MoveUpPanelCommand_CP)
        QWidget.setTabOrder(self.MoveUpPanelCommand_CP, self.MoveDownPanelCommand_CP)
        QWidget.setTabOrder(self.MoveDownPanelCommand_CP, self.PanelSelected_CP)
        QWidget.setTabOrder(self.PanelSelected_CP, self.AddCustomPanel_CP)
        QWidget.setTabOrder(self.AddCustomPanel_CP, self.SearchBar_DDB)
        QWidget.setTabOrder(self.SearchBar_DDB, self.ListCategory_DDB)
        QWidget.setTabOrder(self.ListCategory_DDB, self.CommandsAvailable_DDB)
        QWidget.setTabOrder(self.CommandsAvailable_DDB, self.CommandList_DDB)
        QWidget.setTabOrder(self.CommandList_DDB, self.RemoveControl_DDB)
        QWidget.setTabOrder(self.RemoveControl_DDB, self.ControlName_DDB)
        QWidget.setTabOrder(self.ControlName_DDB, self.NewControl_DDB)
        QWidget.setTabOrder(self.NewControl_DDB, self.AddCommand_DDB)
        QWidget.setTabOrder(self.AddCommand_DDB, self.RemoveCommand_DDB)
        QWidget.setTabOrder(self.RemoveCommand_DDB, self.MoveUpCommand_DDB)
        QWidget.setTabOrder(self.MoveUpCommand_DDB, self.MoveDownCommand_DDB)
        QWidget.setTabOrder(self.MoveDownCommand_DDB, self.CreateControl_DDB)

        self.retranslateUi(Form)
        self.PanelTitle.returnPressed.connect(self.CreateNewPanel.animateClick)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.okButton_2.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.cancelButton_2.setText(QCoreApplication.translate("Form", u"Cancel", None))
#if QT_CONFIG(shortcut)
        self.cancelButton_2.setShortcut(QCoreApplication.translate("Form", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.applyButton_2.setText(QCoreApplication.translate("Form", u"Apply", None))
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
        self.label_7.setText(QCoreApplication.translate("Form", u"Select workbench:", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Select custom panel:", None))
        self.RemovePanel_CP.setText(QCoreApplication.translate("Form", u"Remove panel", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Panel name", None))
        self.PanelName_CP.setPlaceholderText(QCoreApplication.translate("Form", u"Enter the name of your custom panel...", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Select panels to add to the custom panel.</p></body></html>", None))

        __sortingEnabled1 = self.PanelAvailable_CP.isSortingEnabled()
        self.PanelAvailable_CP.setSortingEnabled(False)
        ___qlistwidgetitem1 = self.PanelAvailable_CP.item(0)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"New Item", None))
        self.PanelAvailable_CP.setSortingEnabled(__sortingEnabled1)


        __sortingEnabled2 = self.PanelSelected_CP.isSortingEnabled()
        self.PanelSelected_CP.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.PanelSelected_CP.item(0)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Form", u"New Item", None))
        self.PanelSelected_CP.setSortingEnabled(__sortingEnabled2)

        self.AddCustomPanel_CP.setText(QCoreApplication.translate("Form", u"Create/update panel", None))
#if QT_CONFIG(tooltip)
        self.MoveUpPanelCommand_CP.setToolTip(QCoreApplication.translate("Form", u"Move up", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.MoveDownPanelCommand_CP.setToolTip(QCoreApplication.translate("Form", u"Move down", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.AddPanel_CP.setToolTip(QCoreApplication.translate("Form", u"Add panel buttons", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Combine panels", None))
        self.groupBox_5.setTitle("")
        self.label_23.setText(QCoreApplication.translate("Form", u"Select commands to add to the new panel", None))

        __sortingEnabled3 = self.CommandsAvailable_DDB.isSortingEnabled()
        self.CommandsAvailable_DDB.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.CommandsAvailable_DDB.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Form", u"New Item", None))
        self.CommandsAvailable_DDB.setSortingEnabled(__sortingEnabled3)

        self.SearchBar_DDB.setInputMask("")
        self.SearchBar_DDB.setText("")
        self.SearchBar_DDB.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search...", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"Category:", None))
#if QT_CONFIG(tooltip)
        self.AddCommand_DDB.setToolTip(QCoreApplication.translate("Form", u"Add command", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.MoveDownCommand_DDB.setToolTip(QCoreApplication.translate("Form", u"Move down", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.RemoveCommand_DDB.setToolTip(QCoreApplication.translate("Form", u"Remove command", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.MoveUpCommand_DDB.setToolTip(QCoreApplication.translate("Form", u"Move up", None))
#endif // QT_CONFIG(tooltip)
        self.RemoveControl_DDB.setText(QCoreApplication.translate("Form", u"Remove control", None))

        __sortingEnabled4 = self.NewControl_DDB.isSortingEnabled()
        self.NewControl_DDB.setSortingEnabled(False)
        ___qlistwidgetitem4 = self.NewControl_DDB.item(0)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Form", u"New Item", None))
        self.NewControl_DDB.setSortingEnabled(__sortingEnabled4)

        self.ControlName_DDB.setInputMask("")
        self.ControlName_DDB.setText("")
        self.ControlName_DDB.setPlaceholderText(QCoreApplication.translate("Form", u"Enter command name...", None))
        self.CreateControl_DDB.setText(QCoreApplication.translate("Form", u"Create/update dropdown button", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), QCoreApplication.translate("Form", u"Create dropdown buttons", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Macro buttons:", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Create macro button", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Tooltip", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Macro", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Status text", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Accelerator", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"What's this", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Menu text", None))
        self.SelectIcon.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"Icon", None))
        self.AddButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.RemoveButton.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.ReplaceButton.setText(QCoreApplication.translate("Form", u"Replace", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Form", u"Available icons", None))
        ___qtablewidgetitem = self.ListMacroButtons.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"New Column", None))
        ___qtablewidgetitem1 = self.ListMacroButtons.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"1", None))
        ___qtablewidgetitem2 = self.ListMacroButtons.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"2", None))
        ___qtablewidgetitem3 = self.ListMacroButtons.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"3", None))
        ___qtablewidgetitem4 = self.ListMacroButtons.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"4", None))
        ___qtablewidgetitem5 = self.ListMacroButtons.verticalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"New Row", None))
        ___qtablewidgetitem6 = self.ListMacroButtons.verticalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"1", None))
        ___qtablewidgetitem7 = self.ListMacroButtons.verticalHeaderItem(2)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"2", None))
        ___qtablewidgetitem8 = self.ListMacroButtons.verticalHeaderItem(3)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"3", None))
        ___qtablewidgetitem9 = self.ListMacroButtons.verticalHeaderItem(4)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"4", None))
        ___qtablewidgetitem10 = self.ListMacroButtons.verticalHeaderItem(5)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Form", u"5", None))

        __sortingEnabled5 = self.ListMacroButtons.isSortingEnabled()
        self.ListMacroButtons.setSortingEnabled(False)
        self.ListMacroButtons.setSortingEnabled(__sortingEnabled5)

        self.pushButton.setText(QCoreApplication.translate("Form", u"Browse for icons...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CreateMacroButtons), QCoreApplication.translate("Form", u"Create macro buttons", None))
        self.label.setText(QCoreApplication.translate("Form", u"Refresh workbench data", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
#if QT_CONFIG(shortcut)
        self.cancelButton.setShortcut(QCoreApplication.translate("Form", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.applyButton.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.TimeStamp_Reloaded.setText(QCoreApplication.translate("Form", u"Last reloaded on: -", None))
        self.LoadWB.setText("")
        self.okButton.setText(QCoreApplication.translate("Form", u"Ok", None))
    # retranslateUi

