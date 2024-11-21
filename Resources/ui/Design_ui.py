# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DesignPjQWPA.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QFrame, QGridLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(929, 773)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(580, 600))
        Form.setMaximumSize(QSize(100000, 10000))
        Form.setBaseSize(QSize(730, 0))
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        Form.setAutoFillBackground(False)
        self.gridLayout_24 = QGridLayout(Form)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.HelpButton = QToolButton(Form)
        self.HelpButton.setObjectName(u"HelpButton")

        self.gridLayout_6.addWidget(self.HelpButton, 1, 8, 1, 1)

        self.ResetJson = QPushButton(Form)
        self.ResetJson.setObjectName(u"ResetJson")
        self.ResetJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.ResetJson, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.GenerateJson = QPushButton(Form)
        self.GenerateJson.setObjectName(u"GenerateJson")

        self.gridLayout_6.addWidget(self.GenerateJson, 1, 4, 1, 1)

        self.RestoreJson = QPushButton(Form)
        self.RestoreJson.setObjectName(u"RestoreJson")
        self.RestoreJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.RestoreJson, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 1, 7, 1, 1)

        self.GenerateJsonExit = QPushButton(Form)
        self.GenerateJsonExit.setObjectName(u"GenerateJsonExit")

        self.gridLayout_6.addWidget(self.GenerateJsonExit, 1, 6, 1, 1)

        self.Cancel = QPushButton(Form)
        self.Cancel.setObjectName(u"Cancel")

        self.gridLayout_6.addWidget(self.Cancel, 1, 5, 1, 1)

        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 924, 709))
        self.gridLayout_26 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"")
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideRight)
        self.QAToolbars = QWidget()
        self.QAToolbars.setObjectName(u"QAToolbars")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.QAToolbars.sizePolicy().hasHeightForWidth())
        self.QAToolbars.setSizePolicy(sizePolicy1)
        self.QAToolbars.setMinimumSize(QSize(550, 0))
        self.QAToolbars.setAutoFillBackground(True)
        self.gridLayout_7 = QGridLayout(self.QAToolbars)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame = QFrame(self.QAToolbars)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.MoveUp_Command = QToolButton(self.frame)
        self.MoveUp_Command.setObjectName(u"MoveUp_Command")
        self.MoveUp_Command.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout.addWidget(self.MoveUp_Command, 4, 0, 1, 1)

        self.MoveDown_Command = QToolButton(self.frame)
        self.MoveDown_Command.setObjectName(u"MoveDown_Command")
        self.MoveDown_Command.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout.addWidget(self.MoveDown_Command, 5, 0, 1, 1)

        self.Remove_Command = QToolButton(self.frame)
        self.Remove_Command.setObjectName(u"Remove_Command")
        self.Remove_Command.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout.addWidget(self.Remove_Command, 2, 0, 1, 1)

        self.Add_Command = QToolButton(self.frame)
        self.Add_Command.setObjectName(u"Add_Command")
        self.Add_Command.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout.addWidget(self.Add_Command, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 4, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

        self.gridLayout_10.addWidget(self.label_3, 0, 0, 1, 1)

        self.ListCategory_1 = QComboBox(self.frame)
        self.ListCategory_1.setObjectName(u"ListCategory_1")

        self.gridLayout_10.addWidget(self.ListCategory_1, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_10, 2, 0, 1, 3)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 3)

        self.CommandsSelected = QListWidget(self.frame)
        __qlistwidgetitem = QListWidgetItem(self.CommandsSelected)
        __qlistwidgetitem.setCheckState(Qt.Checked);
        self.CommandsSelected.setObjectName(u"CommandsSelected")
        self.CommandsSelected.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.CommandsSelected.setMovement(QListView.Movement.Free)
        self.CommandsSelected.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.CommandsSelected, 4, 2, 1, 1)

        self.CommandsAvailable = QListWidget(self.frame)
        __qlistwidgetitem1 = QListWidgetItem(self.CommandsAvailable)
        __qlistwidgetitem1.setCheckState(Qt.Checked);
        self.CommandsAvailable.setObjectName(u"CommandsAvailable")
        self.CommandsAvailable.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.CommandsAvailable.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.CommandsAvailable, 4, 0, 1, 1)

        self.SearchBar_1 = QLineEdit(self.frame)
        self.SearchBar_1.setObjectName(u"SearchBar_1")

        self.gridLayout_2.addWidget(self.SearchBar_1, 0, 0, 1, 3)


        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget.addTab(self.QAToolbars, "")
        self.Toolbars = QWidget()
        self.Toolbars.setObjectName(u"Toolbars")
        self.Toolbars.setAutoFillBackground(True)
        self.gridLayout_22 = QGridLayout(self.Toolbars)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.frame_6 = QFrame(self.Toolbars)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_17 = QGridLayout(self.frame_6)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(6, 6, 6, 6)
        self.ToolbarsToExclude = QListWidget(self.frame_6)
        __qlistwidgetitem2 = QListWidgetItem(self.ToolbarsToExclude)
        __qlistwidgetitem2.setCheckState(Qt.Checked);
        self.ToolbarsToExclude.setObjectName(u"ToolbarsToExclude")
        self.ToolbarsToExclude.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ToolbarsToExclude.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.ToolbarsToExclude, 3, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_15, 0, 0, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_16, 3, 0, 1, 1)

        self.Remove_Toolbar = QToolButton(self.frame_6)
        self.Remove_Toolbar.setObjectName(u"Remove_Toolbar")
        self.Remove_Toolbar.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_18.addWidget(self.Remove_Toolbar, 2, 0, 1, 1)

        self.Add_Toolbar = QToolButton(self.frame_6)
        self.Add_Toolbar.setObjectName(u"Add_Toolbar")
        self.Add_Toolbar.setAutoRaise(False)
        self.Add_Toolbar.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_18.addWidget(self.Add_Toolbar, 1, 0, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_18, 3, 1, 1, 1)

        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_17.addWidget(self.label_13, 2, 0, 1, 3)

        self.ToolbarsExcluded = QListWidget(self.frame_6)
        __qlistwidgetitem3 = QListWidgetItem(self.ToolbarsExcluded)
        __qlistwidgetitem3.setCheckState(Qt.Checked);
        self.ToolbarsExcluded.setObjectName(u"ToolbarsExcluded")
        self.ToolbarsExcluded.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.ToolbarsExcluded.setMovement(QListView.Movement.Free)
        self.ToolbarsExcluded.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.ToolbarsExcluded, 3, 2, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)

        self.gridLayout_11.addWidget(self.label_8, 0, 0, 1, 1)

        self.ListCategory_2 = QComboBox(self.frame_6)
        self.ListCategory_2.setObjectName(u"ListCategory_2")

        self.gridLayout_11.addWidget(self.ListCategory_2, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_11, 1, 0, 1, 3)

        self.SearchBar_2 = QLineEdit(self.frame_6)
        self.SearchBar_2.setObjectName(u"SearchBar_2")

        self.gridLayout_17.addWidget(self.SearchBar_2, 0, 0, 1, 3)


        self.gridLayout_22.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.Toolbars, "")
        self.Workbenches = QWidget()
        self.Workbenches.setObjectName(u"Workbenches")
        self.Workbenches.setAutoFillBackground(True)
        self.gridLayout_23 = QGridLayout(self.Workbenches)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.frame1 = QFrame(self.Workbenches)
        self.frame1.setObjectName(u"frame1")
        self.frame1.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.frame1)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.WorkbenchesAvailable = QListWidget(self.frame1)
        __qlistwidgetitem4 = QListWidgetItem(self.WorkbenchesAvailable)
        __qlistwidgetitem4.setCheckState(Qt.Checked);
        self.WorkbenchesAvailable.setObjectName(u"WorkbenchesAvailable")
        self.WorkbenchesAvailable.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.WorkbenchesAvailable.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesAvailable, 1, 0, 1, 1)

        self.WorkbenchesSelected = QListWidget(self.frame1)
        __qlistwidgetitem5 = QListWidgetItem(self.WorkbenchesSelected)
        __qlistwidgetitem5.setCheckState(Qt.Checked);
        self.WorkbenchesSelected.setObjectName(u"WorkbenchesSelected")
        self.WorkbenchesSelected.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.WorkbenchesSelected.setMovement(QListView.Movement.Free)
        self.WorkbenchesSelected.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesSelected, 1, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.Remove_Workbench = QToolButton(self.frame1)
        self.Remove_Workbench.setObjectName(u"Remove_Workbench")
        self.Remove_Workbench.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_4.addWidget(self.Remove_Workbench, 2, 0, 1, 1)

        self.Add_Workbench = QToolButton(self.frame1)
        self.Add_Workbench.setObjectName(u"Add_Workbench")
        self.Add_Workbench.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_4.addWidget(self.Add_Workbench, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_5, 3, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame1)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 3)


        self.gridLayout_23.addWidget(self.frame1, 0, 0, 1, 1)

        self.tabWidget.addTab(self.Workbenches, "")
        self.CombineToolbars = QWidget()
        self.CombineToolbars.setObjectName(u"CombineToolbars")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.CombineToolbars.sizePolicy().hasHeightForWidth())
        self.CombineToolbars.setSizePolicy(sizePolicy3)
        self.CombineToolbars.setMinimumSize(QSize(550, 0))
        self.gridLayout_21 = QGridLayout(self.CombineToolbars)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.label_9 = QLabel(self.CombineToolbars)
        self.label_9.setObjectName(u"label_9")
        sizePolicy2.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy2)

        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)

        self.AddCustomToolbar = QPushButton(self.CombineToolbars)
        self.AddCustomToolbar.setObjectName(u"AddCustomToolbar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.AddCustomToolbar.sizePolicy().hasHeightForWidth())
        self.AddCustomToolbar.setSizePolicy(sizePolicy4)
        self.AddCustomToolbar.setMinimumSize(QSize(10, 0))
        self.AddCustomToolbar.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.AddCustomToolbar, 3, 3, 2, 1)

        self.label_7 = QLabel(self.CombineToolbars)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)

        self.gridLayout_8.addWidget(self.label_7, 2, 0, 1, 1)

        self.WorkbenchList_2 = QComboBox(self.CombineToolbars)
        self.WorkbenchList_2.setObjectName(u"WorkbenchList_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.WorkbenchList_2.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_2.setSizePolicy(sizePolicy5)
        self.WorkbenchList_2.setMinimumSize(QSize(0, 0))

        self.gridLayout_8.addWidget(self.WorkbenchList_2, 2, 1, 1, 2)

        self.CustomToolbarSelector = QComboBox(self.CombineToolbars)
        self.CustomToolbarSelector.setObjectName(u"CustomToolbarSelector")
        sizePolicy5.setHeightForWidth(self.CustomToolbarSelector.sizePolicy().hasHeightForWidth())
        self.CustomToolbarSelector.setSizePolicy(sizePolicy5)
        self.CustomToolbarSelector.setMinimumSize(QSize(150, 0))

        self.gridLayout_8.addWidget(self.CustomToolbarSelector, 0, 1, 1, 2)

        self.line = QFrame(self.CombineToolbars)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_8.addWidget(self.line, 1, 0, 1, 4)

        self.ToolbarName = QLineEdit(self.CombineToolbars)
        self.ToolbarName.setObjectName(u"ToolbarName")
        sizePolicy5.setHeightForWidth(self.ToolbarName.sizePolicy().hasHeightForWidth())
        self.ToolbarName.setSizePolicy(sizePolicy5)
        self.ToolbarName.setMinimumSize(QSize(120, 0))

        self.gridLayout_8.addWidget(self.ToolbarName, 3, 1, 2, 2)

        self.RemovePanel = QPushButton(self.CombineToolbars)
        self.RemovePanel.setObjectName(u"RemovePanel")
        self.RemovePanel.setMinimumSize(QSize(10, 0))
        self.RemovePanel.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.RemovePanel, 0, 3, 1, 1)

        self.label_10 = QLabel(self.CombineToolbars)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)

        self.gridLayout_8.addWidget(self.label_10, 3, 0, 2, 1)


        self.gridLayout_21.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.CombineToolbars)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setSizeIncrement(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_9.addWidget(self.label_11, 0, 0, 1, 3)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.MoveDown_PanelCommand = QToolButton(self.frame_3)
        self.MoveDown_PanelCommand.setObjectName(u"MoveDown_PanelCommand")
        self.MoveDown_PanelCommand.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_12.addWidget(self.MoveDown_PanelCommand, 4, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_10, 2, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.MoveUp_PanelCommand = QToolButton(self.frame_3)
        self.MoveUp_PanelCommand.setObjectName(u"MoveUp_PanelCommand")
        self.MoveUp_PanelCommand.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_12.addWidget(self.MoveUp_PanelCommand, 3, 0, 1, 1)

        self.Add_Panel = QToolButton(self.frame_3)
        self.Add_Panel.setObjectName(u"Add_Panel")
        self.Add_Panel.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_12.addWidget(self.Add_Panel, 1, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_7, 5, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_12, 1, 1, 1, 1)

        self.ToolbarsAvailable = QListWidget(self.frame_3)
        __qlistwidgetitem6 = QListWidgetItem(self.ToolbarsAvailable)
        __qlistwidgetitem6.setCheckState(Qt.Checked);
        self.ToolbarsAvailable.setObjectName(u"ToolbarsAvailable")
        self.ToolbarsAvailable.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ToolbarsAvailable.setSortingEnabled(True)

        self.gridLayout_9.addWidget(self.ToolbarsAvailable, 1, 0, 1, 1)

        self.ToolbarsSelected = QListWidget(self.frame_3)
        __qlistwidgetitem7 = QListWidgetItem(self.ToolbarsSelected)
        __qlistwidgetitem7.setCheckState(Qt.Checked);
        self.ToolbarsSelected.setObjectName(u"ToolbarsSelected")
        self.ToolbarsSelected.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.ToolbarsSelected.setMovement(QListView.Movement.Free)
        self.ToolbarsSelected.setViewMode(QListView.ViewMode.ListMode)
        self.ToolbarsSelected.setSortingEnabled(False)

        self.gridLayout_9.addWidget(self.ToolbarsSelected, 1, 2, 1, 1)


        self.gridLayout_21.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget.addTab(self.CombineToolbars, "")
        self.RibbonDesign = QWidget()
        self.RibbonDesign.setObjectName(u"RibbonDesign")
        sizePolicy1.setHeightForWidth(self.RibbonDesign.sizePolicy().hasHeightForWidth())
        self.RibbonDesign.setSizePolicy(sizePolicy1)
        self.RibbonDesign.setMinimumSize(QSize(900, 0))
        self.RibbonDesign.setSizeIncrement(QSize(10, 0))
        self.RibbonDesign.setBaseSize(QSize(900, 0))
        self.RibbonDesign.setAutoFillBackground(True)
        self.gridLayout_15 = QGridLayout(self.RibbonDesign)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.RibbonDesign)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.WorkbenchList = QComboBox(self.RibbonDesign)
        self.WorkbenchList.setObjectName(u"WorkbenchList")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.WorkbenchList.sizePolicy().hasHeightForWidth())
        self.WorkbenchList.setSizePolicy(sizePolicy6)

        self.gridLayout_5.addWidget(self.WorkbenchList, 0, 1, 1, 1)

        self.ToolbarList = QComboBox(self.RibbonDesign)
        self.ToolbarList.setObjectName(u"ToolbarList")

        self.gridLayout_5.addWidget(self.ToolbarList, 1, 1, 1, 1)

        self.label = QLabel(self.RibbonDesign)
        self.label.setObjectName(u"label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.IconOnly = QCheckBox(self.RibbonDesign)
        self.IconOnly.setObjectName(u"IconOnly")

        self.gridLayout_5.addWidget(self.IconOnly, 1, 2, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_4 = QLabel(self.RibbonDesign)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)

        self.gridLayout_19.addWidget(self.label_4, 0, 0, 1, 1)

        self.frame2 = QFrame(self.RibbonDesign)
        self.frame2.setObjectName(u"frame2")
        sizePolicy1.setHeightForWidth(self.frame2.sizePolicy().hasHeightForWidth())
        self.frame2.setSizePolicy(sizePolicy1)
        self.frame2.setMinimumSize(QSize(350, 0))
        self.frame2.setBaseSize(QSize(350, 0))
        self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame2.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_13 = QGridLayout(self.frame2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_13.setContentsMargins(6, 6, 6, 6)
        self.ToolbarsOrder = QListWidget(self.frame2)
        __qlistwidgetitem8 = QListWidgetItem(self.ToolbarsOrder)
        __qlistwidgetitem8.setCheckState(Qt.Checked);
        self.ToolbarsOrder.setObjectName(u"ToolbarsOrder")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.ToolbarsOrder.sizePolicy().hasHeightForWidth())
        self.ToolbarsOrder.setSizePolicy(sizePolicy7)
        self.ToolbarsOrder.setMinimumSize(QSize(300, 0))
        self.ToolbarsOrder.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.ToolbarsOrder.setMovement(QListView.Movement.Free)
        self.ToolbarsOrder.setSortingEnabled(False)

        self.gridLayout_13.addWidget(self.ToolbarsOrder, 1, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_12, 0, 0, 1, 1)

        self.MoveUp_Toolbar = QToolButton(self.frame2)
        self.MoveUp_Toolbar.setObjectName(u"MoveUp_Toolbar")
        self.MoveUp_Toolbar.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_20.addWidget(self.MoveUp_Toolbar, 1, 0, 1, 1)

        self.MoveDown_Toolbar = QToolButton(self.frame2)
        self.MoveDown_Toolbar.setObjectName(u"MoveDown_Toolbar")
        self.MoveDown_Toolbar.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_20.addWidget(self.MoveDown_Toolbar, 2, 0, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_11, 3, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_20, 1, 1, 1, 1)


        self.gridLayout_19.addWidget(self.frame2, 1, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_19, 1, 1, 1, 1)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.label_12 = QLabel(self.RibbonDesign)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout_16.addWidget(self.label_12, 0, 0, 1, 1)

        self.frame3 = QFrame(self.RibbonDesign)
        self.frame3.setObjectName(u"frame3")
        sizePolicy1.setHeightForWidth(self.frame3.sizePolicy().hasHeightForWidth())
        self.frame3.setSizePolicy(sizePolicy1)
        self.frame3.setMinimumSize(QSize(506, 0))
        self.frame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_14 = QGridLayout(self.frame3)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, 6, 6, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_9)

        self.MoveUp_RibbonCommand = QToolButton(self.frame3)
        self.MoveUp_RibbonCommand.setObjectName(u"MoveUp_RibbonCommand")
        self.MoveUp_RibbonCommand.setArrowType(Qt.ArrowType.UpArrow)

        self.verticalLayout.addWidget(self.MoveUp_RibbonCommand)

        self.MoveDown_RibbonCommand = QToolButton(self.frame3)
        self.MoveDown_RibbonCommand.setObjectName(u"MoveDown_RibbonCommand")
        self.MoveDown_RibbonCommand.setArrowType(Qt.ArrowType.DownArrow)

        self.verticalLayout.addWidget(self.MoveDown_RibbonCommand)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_8)


        self.gridLayout_14.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.tableWidget = QTableWidget(self.frame3)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.tableWidget.rowCount() < 1):
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 0, __qtablewidgetitem5)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setCheckState(Qt.Checked);
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem6.setBackground(brush);
        __qtablewidgetitem6.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setCheckState(Qt.Checked);
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem7.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setCheckState(Qt.Checked);
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter);
        __qtablewidgetitem8.setFlags(Qt.ItemIsSelectable|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled);
        self.tableWidget.setItem(0, 3, __qtablewidgetitem8)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMinimumSize(QSize(470, 500))
        self.tableWidget.setSizeIncrement(QSize(5, 5))
        self.tableWidget.setBaseSize(QSize(300, 500))
        self.tableWidget.setStyleSheet(u"border-color: rgb(167, 167rgb(217, 217, 217), 167);")
        self.tableWidget.setFrameShape(QFrame.Shape.StyledPanel)
        self.tableWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setIconSize(QSize(16, 16))
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.gridLayout_14.addWidget(self.tableWidget, 0, 0, 1, 1)


        self.gridLayout_16.addWidget(self.frame3, 1, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_16, 1, 0, 1, 1)

        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.AddSeparator = QPushButton(self.RibbonDesign)
        self.AddSeparator.setObjectName(u"AddSeparator")
        self.AddSeparator.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        font1.setBold(False)
        self.AddSeparator.setFont(font1)

        self.gridLayout_25.addWidget(self.AddSeparator, 0, 1, 1, 1)

        self.RemoveSeparator = QPushButton(self.RibbonDesign)
        self.RemoveSeparator.setObjectName(u"RemoveSeparator")
        self.RemoveSeparator.setMinimumSize(QSize(100, 0))
        self.RemoveSeparator.setFont(font1)

        self.gridLayout_25.addWidget(self.RemoveSeparator, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_25, 2, 0, 1, 1)

        self.tabWidget.addTab(self.RibbonDesign, "")

        self.gridLayout_26.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 0, 0, 1, 9)


        self.gridLayout_24.addLayout(self.gridLayout_6, 1, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Ribbon design", None))
        self.HelpButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.ResetJson.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.GenerateJson.setText(QCoreApplication.translate("Form", u"Update", None))
        self.RestoreJson.setText(QCoreApplication.translate("Form", u"Restore", None))
        self.GenerateJsonExit.setText(QCoreApplication.translate("Form", u"Close", None))
        self.Cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
#if QT_CONFIG(shortcut)
        self.Cancel.setShortcut(QCoreApplication.translate("Form", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.MoveUp_Command.setText(QCoreApplication.translate("Form", u"...", None))
        self.MoveDown_Command.setText(QCoreApplication.translate("Form", u"...", None))
        self.Remove_Command.setText(QCoreApplication.translate("Form", u"...", None))
        self.Add_Command.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Category:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Select commands to add to the quick access toolbar", None))

        __sortingEnabled = self.CommandsSelected.isSortingEnabled()
        self.CommandsSelected.setSortingEnabled(False)
        ___qlistwidgetitem = self.CommandsSelected.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.CommandsSelected.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.CommandsAvailable.isSortingEnabled()
        self.CommandsAvailable.setSortingEnabled(False)
        ___qlistwidgetitem1 = self.CommandsAvailable.item(0)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.CommandsAvailable.setSortingEnabled(__sortingEnabled1)

        self.SearchBar_1.setInputMask("")
        self.SearchBar_1.setText("")
        self.SearchBar_1.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.QAToolbars), QCoreApplication.translate("Form", u"Quick access toolbar", None))

        __sortingEnabled2 = self.ToolbarsToExclude.isSortingEnabled()
        self.ToolbarsToExclude.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.ToolbarsToExclude.item(0)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.ToolbarsToExclude.setSortingEnabled(__sortingEnabled2)

        self.Remove_Toolbar.setText(QCoreApplication.translate("Form", u"...", None))
        self.Add_Toolbar.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Select panels to <span style=\" font-weight:600;\">exclude</span> from the ribbon.</p></body></html>", None))

        __sortingEnabled3 = self.ToolbarsExcluded.isSortingEnabled()
        self.ToolbarsExcluded.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.ToolbarsExcluded.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.ToolbarsExcluded.setSortingEnabled(__sortingEnabled3)

        self.label_8.setText(QCoreApplication.translate("Form", u"Category:", None))
        self.SearchBar_2.setInputMask("")
        self.SearchBar_2.setText("")
        self.SearchBar_2.setPlaceholderText(QCoreApplication.translate("Form", u"Type to search...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Toolbars), QCoreApplication.translate("Form", u"Exclude panels", None))

        __sortingEnabled4 = self.WorkbenchesAvailable.isSortingEnabled()
        self.WorkbenchesAvailable.setSortingEnabled(False)
        ___qlistwidgetitem4 = self.WorkbenchesAvailable.item(0)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.WorkbenchesAvailable.setSortingEnabled(__sortingEnabled4)


        __sortingEnabled5 = self.WorkbenchesSelected.isSortingEnabled()
        self.WorkbenchesSelected.setSortingEnabled(False)
        ___qlistwidgetitem5 = self.WorkbenchesSelected.item(0)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.WorkbenchesSelected.setSortingEnabled(__sortingEnabled5)

        self.Remove_Workbench.setText(QCoreApplication.translate("Form", u"...", None))
        self.Add_Workbench.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Select workbenches to<span style=\" font-weight:600;\"> include</span> in the ribbon.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Workbenches), QCoreApplication.translate("Form", u"Include workbenches", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Select custom panel:", None))
        self.AddCustomToolbar.setText(QCoreApplication.translate("Form", u"Add", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Select workbench:", None))
        self.ToolbarName.setPlaceholderText(QCoreApplication.translate("Form", u"Enter the name of your custom panel...", None))
        self.RemovePanel.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Panel name", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Select panels to add to the custom panel.</p></body></html>", None))
        self.MoveDown_PanelCommand.setText(QCoreApplication.translate("Form", u"...", None))
        self.MoveUp_PanelCommand.setText(QCoreApplication.translate("Form", u"...", None))
        self.Add_Panel.setText(QCoreApplication.translate("Form", u"...", None))

        __sortingEnabled6 = self.ToolbarsAvailable.isSortingEnabled()
        self.ToolbarsAvailable.setSortingEnabled(False)
        ___qlistwidgetitem6 = self.ToolbarsAvailable.item(0)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.ToolbarsAvailable.setSortingEnabled(__sortingEnabled6)


        __sortingEnabled7 = self.ToolbarsSelected.isSortingEnabled()
        self.ToolbarsSelected.setSortingEnabled(False)
        ___qlistwidgetitem7 = self.ToolbarsSelected.item(0)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.ToolbarsSelected.setSortingEnabled(__sortingEnabled7)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CombineToolbars), QCoreApplication.translate("Form", u"Create custom panels", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Select panel:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Select workbench:", None))
        self.IconOnly.setText(QCoreApplication.translate("Form", u"Icon only", None))
        self.label_4.setText(QCoreApplication.translate("Form", u" Set the panel order", None))

        __sortingEnabled8 = self.ToolbarsOrder.isSortingEnabled()
        self.ToolbarsOrder.setSortingEnabled(False)
        ___qlistwidgetitem8 = self.ToolbarsOrder.item(0)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("Form", u"New Item", None));
        self.ToolbarsOrder.setSortingEnabled(__sortingEnabled8)

        self.MoveUp_Toolbar.setText(QCoreApplication.translate("Form", u"...", None))
        self.MoveDown_Toolbar.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Set the icon size", None))
        self.MoveUp_RibbonCommand.setText(QCoreApplication.translate("Form", u"...", None))
        self.MoveDown_RibbonCommand.setText(QCoreApplication.translate("Form", u"...", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Command", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Small", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Medium", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Large", None));
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"1", None));

        __sortingEnabled9 = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Command 1", None));
        self.tableWidget.setSortingEnabled(__sortingEnabled9)

        self.AddSeparator.setText(QCoreApplication.translate("Form", u"Add separator", None))
        self.RemoveSeparator.setText(QCoreApplication.translate("Form", u"Remove separator", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RibbonDesign), QCoreApplication.translate("Form", u"Ribbon design", None))
    # retranslateUi

