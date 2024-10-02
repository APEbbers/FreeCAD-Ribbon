# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Design.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setWindowModality(Qt.WindowModal)
        Form.resize(940, 724)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(580, 724))
        Form.setMaximumSize(QSize(940, 724))
        Form.setBaseSize(QSize(0, 0))
        Form.setContextMenuPolicy(Qt.NoContextMenu)
        Form.setAutoFillBackground(False)
        self.gridLayout_7 = QGridLayout(Form)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalSpacer = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.GenerateJsonExit = QPushButton(Form)
        self.GenerateJsonExit.setObjectName("GenerateJsonExit")

        self.gridLayout_6.addWidget(self.GenerateJsonExit, 0, 6, 1, 1)

        self.HelpButton = QToolButton(Form)
        self.HelpButton.setObjectName("HelpButton")

        self.gridLayout_6.addWidget(self.HelpButton, 0, 8, 1, 1)

        self.RestoreJson = QPushButton(Form)
        self.RestoreJson.setObjectName("RestoreJson")
        self.RestoreJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.RestoreJson, 0, 2, 1, 1)

        self.GenerateJson = QPushButton(Form)
        self.GenerateJson.setObjectName("GenerateJson")

        self.gridLayout_6.addWidget(self.GenerateJson, 0, 4, 1, 1)

        self.Cancel = QPushButton(Form)
        self.Cancel.setObjectName("Cancel")

        self.gridLayout_6.addWidget(self.Cancel, 0, 5, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.ResetJson = QPushButton(Form)
        self.ResetJson.setObjectName("ResetJson")
        self.ResetJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.ResetJson, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 0, 7, 1, 1)

        self.gridLayout_7.addLayout(self.gridLayout_6, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.QAToolbars = QWidget()
        self.QAToolbars.setObjectName("QAToolbars")
        self.QAToolbars.setAutoFillBackground(True)
        self.frame = QFrame(self.QAToolbars)
        self.frame.setObjectName("frame")
        self.frame.setGeometry(QRect(0, 10, 551, 631))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.MoveUp_Command = QToolButton(self.frame)
        self.MoveUp_Command.setObjectName("MoveUp_Command")
        self.MoveUp_Command.setArrowType(Qt.UpArrow)

        self.gridLayout.addWidget(self.MoveUp_Command, 4, 0, 1, 1)

        self.MoveDown_Command = QToolButton(self.frame)
        self.MoveDown_Command.setObjectName("MoveDown_Command")
        self.MoveDown_Command.setArrowType(Qt.DownArrow)

        self.gridLayout.addWidget(self.MoveDown_Command, 5, 0, 1, 1)

        self.Remove_Command = QToolButton(self.frame)
        self.Remove_Command.setObjectName("Remove_Command")
        self.Remove_Command.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.Remove_Command, 2, 0, 1, 1)

        self.Add_Command = QToolButton(self.frame)
        self.Add_Command.setObjectName("Add_Command")
        self.Add_Command.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.Add_Command, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 4, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.gridLayout_10.addWidget(self.label_3, 0, 0, 1, 1)

        self.ListCategory_1 = QComboBox(self.frame)
        self.ListCategory_1.setObjectName("ListCategory_1")

        self.gridLayout_10.addWidget(self.ListCategory_1, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_10, 2, 0, 1, 3)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName("label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 3)

        self.CommandsSelected = QListWidget(self.frame)
        __qlistwidgetitem = QListWidgetItem(self.CommandsSelected)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        self.CommandsSelected.setObjectName("CommandsSelected")
        self.CommandsSelected.setDefaultDropAction(Qt.MoveAction)
        self.CommandsSelected.setMovement(QListView.Free)
        self.CommandsSelected.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.CommandsSelected, 4, 2, 1, 1)

        self.CommandsAvailable = QListWidget(self.frame)
        __qlistwidgetitem1 = QListWidgetItem(self.CommandsAvailable)
        __qlistwidgetitem1.setCheckState(Qt.Checked)
        self.CommandsAvailable.setObjectName("CommandsAvailable")
        self.CommandsAvailable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.CommandsAvailable.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.CommandsAvailable, 4, 0, 1, 1)

        self.SearchBar_1 = QLineEdit(self.frame)
        self.SearchBar_1.setObjectName("SearchBar_1")

        self.gridLayout_2.addWidget(self.SearchBar_1, 0, 0, 1, 3)

        self.tabWidget.addTab(self.QAToolbars, "")
        self.Toolbars = QWidget()
        self.Toolbars.setObjectName("Toolbars")
        self.Toolbars.setAutoFillBackground(True)
        self.frame_6 = QFrame(self.Toolbars)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setGeometry(QRect(0, 10, 551, 631))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_17 = QGridLayout(self.frame_6)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_17.setContentsMargins(6, 6, 6, 6)
        self.ToolbarsToExclude = QListWidget(self.frame_6)
        __qlistwidgetitem2 = QListWidgetItem(self.ToolbarsToExclude)
        __qlistwidgetitem2.setCheckState(Qt.Checked)
        self.ToolbarsToExclude.setObjectName("ToolbarsToExclude")
        self.ToolbarsToExclude.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ToolbarsToExclude.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.ToolbarsToExclude, 3, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.verticalSpacer_15 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_18.addItem(self.verticalSpacer_15, 0, 0, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_18.addItem(self.verticalSpacer_16, 3, 0, 1, 1)

        self.Remove_Toolbar = QToolButton(self.frame_6)
        self.Remove_Toolbar.setObjectName("Remove_Toolbar")
        self.Remove_Toolbar.setArrowType(Qt.LeftArrow)

        self.gridLayout_18.addWidget(self.Remove_Toolbar, 2, 0, 1, 1)

        self.Add_Toolbar = QToolButton(self.frame_6)
        self.Add_Toolbar.setObjectName("Add_Toolbar")
        self.Add_Toolbar.setAutoRaise(False)
        self.Add_Toolbar.setArrowType(Qt.RightArrow)

        self.gridLayout_18.addWidget(self.Add_Toolbar, 1, 0, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_18, 3, 1, 1, 1)

        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName("label_13")

        self.gridLayout_17.addWidget(self.label_13, 2, 0, 1, 3)

        self.ToolbarsExcluded = QListWidget(self.frame_6)
        __qlistwidgetitem3 = QListWidgetItem(self.ToolbarsExcluded)
        __qlistwidgetitem3.setCheckState(Qt.Checked)
        self.ToolbarsExcluded.setObjectName("ToolbarsExcluded")
        self.ToolbarsExcluded.setDefaultDropAction(Qt.MoveAction)
        self.ToolbarsExcluded.setMovement(QListView.Free)
        self.ToolbarsExcluded.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.ToolbarsExcluded, 3, 2, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName("label_8")
        sizePolicy1.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy1)

        self.gridLayout_11.addWidget(self.label_8, 0, 0, 1, 1)

        self.ListCategory_2 = QComboBox(self.frame_6)
        self.ListCategory_2.setObjectName("ListCategory_2")

        self.gridLayout_11.addWidget(self.ListCategory_2, 0, 1, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_11, 1, 0, 1, 3)

        self.SearchBar_2 = QLineEdit(self.frame_6)
        self.SearchBar_2.setObjectName("SearchBar_2")

        self.gridLayout_17.addWidget(self.SearchBar_2, 0, 0, 1, 3)

        self.tabWidget.addTab(self.Toolbars, "")
        self.Workbenches = QWidget()
        self.Workbenches.setObjectName("Workbenches")
        self.Workbenches.setAutoFillBackground(True)
        self.frame1 = QFrame(self.Workbenches)
        self.frame1.setObjectName("frame1")
        self.frame1.setGeometry(QRect(0, 10, 551, 631))
        self.frame1.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.frame1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.WorkbenchesAvailable = QListWidget(self.frame1)
        __qlistwidgetitem4 = QListWidgetItem(self.WorkbenchesAvailable)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        self.WorkbenchesAvailable.setObjectName("WorkbenchesAvailable")
        self.WorkbenchesAvailable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.WorkbenchesAvailable.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesAvailable, 1, 0, 1, 1)

        self.WorkbenchesSelected = QListWidget(self.frame1)
        __qlistwidgetitem5 = QListWidgetItem(self.WorkbenchesSelected)
        __qlistwidgetitem5.setCheckState(Qt.Checked)
        self.WorkbenchesSelected.setObjectName("WorkbenchesSelected")
        self.WorkbenchesSelected.setDefaultDropAction(Qt.MoveAction)
        self.WorkbenchesSelected.setMovement(QListView.Free)
        self.WorkbenchesSelected.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesSelected, 1, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Remove_Workbench = QToolButton(self.frame1)
        self.Remove_Workbench.setObjectName("Remove_Workbench")
        self.Remove_Workbench.setArrowType(Qt.LeftArrow)

        self.gridLayout_4.addWidget(self.Remove_Workbench, 2, 0, 1, 1)

        self.Add_Workbench = QToolButton(self.frame1)
        self.Add_Workbench.setObjectName("Add_Workbench")
        self.Add_Workbench.setArrowType(Qt.RightArrow)

        self.gridLayout_4.addWidget(self.Add_Workbench, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_4.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_4.addItem(self.verticalSpacer_5, 3, 0, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame1)
        self.label_6.setObjectName("label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 3)

        self.tabWidget.addTab(self.Workbenches, "")
        self.CombineToolbars = QWidget()
        self.CombineToolbars.setObjectName("CombineToolbars")
        self.layoutWidget_2 = QWidget(self.CombineToolbars)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 10, 541, 101))
        self.gridLayout_8 = QGridLayout(self.layoutWidget_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.ToolbarName = QLineEdit(self.layoutWidget_2)
        self.ToolbarName.setObjectName("ToolbarName")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ToolbarName.sizePolicy().hasHeightForWidth())
        self.ToolbarName.setSizePolicy(sizePolicy2)
        self.ToolbarName.setMinimumSize(QSize(120, 0))

        self.gridLayout_8.addWidget(self.ToolbarName, 3, 1, 2, 2)

        self.label_10 = QLabel(self.layoutWidget_2)
        self.label_10.setObjectName("label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_10, 3, 0, 2, 1)

        self.label_7 = QLabel(self.layoutWidget_2)
        self.label_7.setObjectName("label_7")
        sizePolicy1.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_7, 2, 0, 1, 1)

        self.AddCustomToolbar = QPushButton(self.layoutWidget_2)
        self.AddCustomToolbar.setObjectName("AddCustomToolbar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.AddCustomToolbar.sizePolicy().hasHeightForWidth()
        )
        self.AddCustomToolbar.setSizePolicy(sizePolicy3)
        self.AddCustomToolbar.setMinimumSize(QSize(10, 0))
        self.AddCustomToolbar.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.AddCustomToolbar, 3, 3, 2, 1)

        self.CustomToolbarSelector = QComboBox(self.layoutWidget_2)
        self.CustomToolbarSelector.setObjectName("CustomToolbarSelector")
        sizePolicy2.setHeightForWidth(
            self.CustomToolbarSelector.sizePolicy().hasHeightForWidth()
        )
        self.CustomToolbarSelector.setSizePolicy(sizePolicy2)
        self.CustomToolbarSelector.setMinimumSize(QSize(150, 0))

        self.gridLayout_8.addWidget(self.CustomToolbarSelector, 0, 1, 1, 2)

        self.WorkbenchList_2 = QComboBox(self.layoutWidget_2)
        self.WorkbenchList_2.setObjectName("WorkbenchList_2")
        sizePolicy2.setHeightForWidth(
            self.WorkbenchList_2.sizePolicy().hasHeightForWidth()
        )
        self.WorkbenchList_2.setSizePolicy(sizePolicy2)
        self.WorkbenchList_2.setMinimumSize(QSize(0, 0))

        self.gridLayout_8.addWidget(self.WorkbenchList_2, 2, 1, 1, 2)

        self.label_9 = QLabel(self.layoutWidget_2)
        self.label_9.setObjectName("label_9")
        sizePolicy1.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)

        self.RemovePanel = QPushButton(self.layoutWidget_2)
        self.RemovePanel.setObjectName("RemovePanel")
        self.RemovePanel.setMinimumSize(QSize(10, 0))
        self.RemovePanel.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.RemovePanel, 0, 3, 1, 1)

        self.line = QFrame(self.layoutWidget_2)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_8.addWidget(self.line, 1, 0, 1, 4)

        self.frame_3 = QFrame(self.CombineToolbars)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setGeometry(QRect(10, 120, 541, 521))
        self.frame_3.setSizeIncrement(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName("label_11")

        self.gridLayout_9.addWidget(self.label_11, 0, 0, 1, 3)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.MoveDown_PanelCommand = QToolButton(self.frame_3)
        self.MoveDown_PanelCommand.setObjectName("MoveDown_PanelCommand")
        self.MoveDown_PanelCommand.setArrowType(Qt.DownArrow)

        self.gridLayout_12.addWidget(self.MoveDown_PanelCommand, 4, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed
        )

        self.gridLayout_12.addItem(self.verticalSpacer_10, 2, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_12.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.MoveUp_PanelCommand = QToolButton(self.frame_3)
        self.MoveUp_PanelCommand.setObjectName("MoveUp_PanelCommand")
        self.MoveUp_PanelCommand.setArrowType(Qt.UpArrow)

        self.gridLayout_12.addWidget(self.MoveUp_PanelCommand, 3, 0, 1, 1)

        self.Add_Panel = QToolButton(self.frame_3)
        self.Add_Panel.setObjectName("Add_Panel")
        self.Add_Panel.setArrowType(Qt.RightArrow)

        self.gridLayout_12.addWidget(self.Add_Panel, 1, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_12.addItem(self.verticalSpacer_7, 5, 0, 1, 1)

        self.gridLayout_9.addLayout(self.gridLayout_12, 1, 1, 1, 1)

        self.ToolbarsAvailable = QListWidget(self.frame_3)
        __qlistwidgetitem6 = QListWidgetItem(self.ToolbarsAvailable)
        __qlistwidgetitem6.setCheckState(Qt.Checked)
        self.ToolbarsAvailable.setObjectName("ToolbarsAvailable")
        self.ToolbarsAvailable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.ToolbarsAvailable.setSortingEnabled(True)

        self.gridLayout_9.addWidget(self.ToolbarsAvailable, 1, 0, 1, 1)

        self.ToolbarsSelected = QListWidget(self.frame_3)
        __qlistwidgetitem7 = QListWidgetItem(self.ToolbarsSelected)
        __qlistwidgetitem7.setCheckState(Qt.Checked)
        self.ToolbarsSelected.setObjectName("ToolbarsSelected")
        self.ToolbarsSelected.setDefaultDropAction(Qt.CopyAction)
        self.ToolbarsSelected.setMovement(QListView.Free)
        self.ToolbarsSelected.setViewMode(QListView.ListMode)
        self.ToolbarsSelected.setSortingEnabled(False)

        self.gridLayout_9.addWidget(self.ToolbarsSelected, 1, 2, 1, 1)

        self.tabWidget.addTab(self.CombineToolbars, "")
        self.RibbonDesign = QWidget()
        self.RibbonDesign.setObjectName("RibbonDesign")
        self.RibbonDesign.setAutoFillBackground(True)
        self.layoutWidget = QWidget(self.RibbonDesign)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 10, 391, 58))
        self.gridLayout_5 = QGridLayout(self.layoutWidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.WorkbenchList = QComboBox(self.layoutWidget)
        self.WorkbenchList.setObjectName("WorkbenchList")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.WorkbenchList.sizePolicy().hasHeightForWidth()
        )
        self.WorkbenchList.setSizePolicy(sizePolicy4)

        self.gridLayout_5.addWidget(self.WorkbenchList, 0, 1, 1, 1)

        self.ToolbarList = QComboBox(self.layoutWidget)
        self.ToolbarList.setObjectName("ToolbarList")

        self.gridLayout_5.addWidget(self.ToolbarList, 1, 1, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.IconOnly = QCheckBox(self.layoutWidget)
        self.IconOnly.setObjectName("IconOnly")

        self.gridLayout_5.addWidget(self.IconOnly, 1, 2, 1, 1)

        self.layoutWidget1 = QWidget(self.RibbonDesign)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 70, 551, 571))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.layoutWidget1)
        self.label_12.setObjectName("label_12")
        font = QFont()
        font.setBold(True)
        self.label_12.setFont(font)

        self.verticalLayout_3.addWidget(self.label_12)

        self.frame2 = QFrame(self.layoutWidget1)
        self.frame2.setObjectName("frame2")
        self.frame2.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_14 = QGridLayout(self.frame2)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, 6, 6, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_9 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_9)

        self.MoveUp_RibbonCommand = QToolButton(self.frame2)
        self.MoveUp_RibbonCommand.setObjectName("MoveUp_RibbonCommand")
        self.MoveUp_RibbonCommand.setArrowType(Qt.UpArrow)

        self.verticalLayout.addWidget(self.MoveUp_RibbonCommand)

        self.MoveDown_RibbonCommand = QToolButton(self.frame2)
        self.MoveDown_RibbonCommand.setObjectName("MoveDown_RibbonCommand")
        self.MoveDown_RibbonCommand.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.MoveDown_RibbonCommand)

        self.verticalSpacer_8 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_8)

        self.gridLayout_14.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.tableWidget = QTableWidget(self.frame2)
        if self.tableWidget.columnCount() < 4:
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if self.tableWidget.rowCount() < 1:
            self.tableWidget.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidget.setItem(0, 0, __qtablewidgetitem5)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setCheckState(Qt.Checked)
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem6.setBackground(brush)
        __qtablewidgetitem6.setFlags(
            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        )
        self.tableWidget.setItem(0, 1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setCheckState(Qt.Checked)
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem7.setFlags(
            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        )
        self.tableWidget.setItem(0, 2, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setCheckState(Qt.Checked)
        __qtablewidgetitem8.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem8.setFlags(
            Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        )
        self.tableWidget.setItem(0, 3, __qtablewidgetitem8)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setStyleSheet(
            "border-color: rgb(167, 167rgb(217, 217, 217), 167);"
        )
        self.tableWidget.setFrameShape(QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QFrame.Plain)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setIconSize(QSize(16, 16))
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.gridLayout_14.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.AddSeparator = QPushButton(self.frame2)
        self.AddSeparator.setObjectName("AddSeparator")
        self.AddSeparator.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        font1.setBold(False)
        self.AddSeparator.setFont(font1)

        self.horizontalLayout.addWidget(self.AddSeparator)

        self.RemoveSeparator = QPushButton(self.frame2)
        self.RemoveSeparator.setObjectName("RemoveSeparator")
        self.RemoveSeparator.setMinimumSize(QSize(100, 0))
        self.RemoveSeparator.setFont(font1)

        self.horizontalLayout.addWidget(self.RemoveSeparator)

        self.horizontalSpacer_5 = QSpacerItem(
            30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.gridLayout_14.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.verticalLayout_3.addWidget(self.frame2)

        self.layoutWidget2 = QWidget(self.RibbonDesign)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(560, 70, 352, 571))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget2)
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font)

        self.verticalLayout_4.addWidget(self.label_4)

        self.frame3 = QFrame(self.layoutWidget2)
        self.frame3.setObjectName("frame3")
        sizePolicy1.setHeightForWidth(self.frame3.sizePolicy().hasHeightForWidth())
        self.frame3.setSizePolicy(sizePolicy1)
        self.frame3.setMinimumSize(QSize(350, 0))
        self.frame3.setFrameShape(QFrame.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Plain)
        self.gridLayout_13 = QGridLayout(self.frame3)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_13.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_13.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalSpacer_12 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_12)

        self.MoveUp_Toolbar = QToolButton(self.frame3)
        self.MoveUp_Toolbar.setObjectName("MoveUp_Toolbar")
        self.MoveUp_Toolbar.setArrowType(Qt.UpArrow)

        self.verticalLayout_2.addWidget(self.MoveUp_Toolbar)

        self.MoveDown_Toolbar = QToolButton(self.frame3)
        self.MoveDown_Toolbar.setObjectName("MoveDown_Toolbar")
        self.MoveDown_Toolbar.setArrowType(Qt.DownArrow)

        self.verticalLayout_2.addWidget(self.MoveDown_Toolbar)

        self.verticalSpacer_11 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_11)

        self.gridLayout_13.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.ToolbarsOrder = QListWidget(self.frame3)
        __qlistwidgetitem8 = QListWidgetItem(self.ToolbarsOrder)
        __qlistwidgetitem8.setCheckState(Qt.Checked)
        self.ToolbarsOrder.setObjectName("ToolbarsOrder")
        self.ToolbarsOrder.setDefaultDropAction(Qt.MoveAction)
        self.ToolbarsOrder.setMovement(QListView.Free)
        self.ToolbarsOrder.setSortingEnabled(False)

        self.gridLayout_13.addWidget(self.ToolbarsOrder, 1, 0, 1, 1)

        self.verticalLayout_4.addWidget(self.frame3)

        self.tabWidget.addTab(self.RibbonDesign, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(4)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Ribbon design", None))
        self.GenerateJsonExit.setText(QCoreApplication.translate("Form", "Close", None))
        self.HelpButton.setText(QCoreApplication.translate("Form", "...", None))
        self.RestoreJson.setText(QCoreApplication.translate("Form", "Restore", None))
        self.GenerateJson.setText(QCoreApplication.translate("Form", "Update", None))
        self.Cancel.setText(QCoreApplication.translate("Form", "Cancel", None))
        # if QT_CONFIG(shortcut)
        self.Cancel.setShortcut(QCoreApplication.translate("Form", "Esc", None))
        # endif // QT_CONFIG(shortcut)
        self.ResetJson.setText(QCoreApplication.translate("Form", "Reset", None))
        self.MoveUp_Command.setText(QCoreApplication.translate("Form", "...", None))
        self.MoveDown_Command.setText(QCoreApplication.translate("Form", "...", None))
        self.Remove_Command.setText(QCoreApplication.translate("Form", "...", None))
        self.Add_Command.setText(QCoreApplication.translate("Form", "...", None))
        self.label_3.setText(QCoreApplication.translate("Form", "Category:", None))
        self.label_5.setText(
            QCoreApplication.translate(
                "Form", "Select commands to add to the quick access toolbar", None
            )
        )

        __sortingEnabled = self.CommandsSelected.isSortingEnabled()
        self.CommandsSelected.setSortingEnabled(False)
        ___qlistwidgetitem = self.CommandsSelected.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", "New Item", None))
        self.CommandsSelected.setSortingEnabled(__sortingEnabled)

        __sortingEnabled1 = self.CommandsAvailable.isSortingEnabled()
        self.CommandsAvailable.setSortingEnabled(False)
        ___qlistwidgetitem1 = self.CommandsAvailable.item(0)
        ___qlistwidgetitem1.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.CommandsAvailable.setSortingEnabled(__sortingEnabled1)

        self.SearchBar_1.setInputMask("")
        self.SearchBar_1.setText("")
        self.SearchBar_1.setPlaceholderText(
            QCoreApplication.translate("Form", "Type to search..", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.QAToolbars),
            QCoreApplication.translate("Form", "Quick access toolbar", None),
        )

        __sortingEnabled2 = self.ToolbarsToExclude.isSortingEnabled()
        self.ToolbarsToExclude.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.ToolbarsToExclude.item(0)
        ___qlistwidgetitem2.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.ToolbarsToExclude.setSortingEnabled(__sortingEnabled2)

        self.Remove_Toolbar.setText(QCoreApplication.translate("Form", "...", None))
        self.Add_Toolbar.setText(QCoreApplication.translate("Form", "...", None))
        self.label_13.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p>Select panels to <span style=" font-weight:600;">exclude</span> from the ribbon.</p></body></html>',
                None,
            )
        )

        __sortingEnabled3 = self.ToolbarsExcluded.isSortingEnabled()
        self.ToolbarsExcluded.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.ToolbarsExcluded.item(0)
        ___qlistwidgetitem3.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.ToolbarsExcluded.setSortingEnabled(__sortingEnabled3)

        self.label_8.setText(QCoreApplication.translate("Form", "Category:", None))
        self.SearchBar_2.setInputMask("")
        self.SearchBar_2.setText("")
        self.SearchBar_2.setPlaceholderText(
            QCoreApplication.translate("Form", "Type to search..", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Toolbars),
            QCoreApplication.translate("Form", "Exclude panels", None),
        )

        __sortingEnabled4 = self.WorkbenchesAvailable.isSortingEnabled()
        self.WorkbenchesAvailable.setSortingEnabled(False)
        ___qlistwidgetitem4 = self.WorkbenchesAvailable.item(0)
        ___qlistwidgetitem4.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.WorkbenchesAvailable.setSortingEnabled(__sortingEnabled4)

        __sortingEnabled5 = self.WorkbenchesSelected.isSortingEnabled()
        self.WorkbenchesSelected.setSortingEnabled(False)
        ___qlistwidgetitem5 = self.WorkbenchesSelected.item(0)
        ___qlistwidgetitem5.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.WorkbenchesSelected.setSortingEnabled(__sortingEnabled5)

        self.Remove_Workbench.setText(QCoreApplication.translate("Form", "...", None))
        self.Add_Workbench.setText(QCoreApplication.translate("Form", "...", None))
        self.label_6.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p>Select workbenches to<span style=" font-weight:600;"> include</span> in the ribbon.</p></body></html>',
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Workbenches),
            QCoreApplication.translate("Form", "Include workbenches", None),
        )
        self.ToolbarName.setPlaceholderText(
            QCoreApplication.translate(
                "Form", "Enter the name of your custom panel...", None
            )
        )
        self.label_10.setText(QCoreApplication.translate("Form", "Panel name", None))
        self.label_7.setText(
            QCoreApplication.translate("Form", "Select workbench:", None)
        )
        self.AddCustomToolbar.setText(QCoreApplication.translate("Form", "Add", None))
        self.label_9.setText(
            QCoreApplication.translate("Form", "select custom panel: ", None)
        )
        self.RemovePanel.setText(QCoreApplication.translate("Form", "Remove", None))
        self.label_11.setText(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p>Select panels to add to the custom panell.</p></body></html>",
                None,
            )
        )
        self.MoveDown_PanelCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        self.MoveUp_PanelCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        self.Add_Panel.setText(QCoreApplication.translate("Form", "...", None))

        __sortingEnabled6 = self.ToolbarsAvailable.isSortingEnabled()
        self.ToolbarsAvailable.setSortingEnabled(False)
        ___qlistwidgetitem6 = self.ToolbarsAvailable.item(0)
        ___qlistwidgetitem6.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.ToolbarsAvailable.setSortingEnabled(__sortingEnabled6)

        __sortingEnabled7 = self.ToolbarsSelected.isSortingEnabled()
        self.ToolbarsSelected.setSortingEnabled(False)
        ___qlistwidgetitem7 = self.ToolbarsSelected.item(0)
        ___qlistwidgetitem7.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.ToolbarsSelected.setSortingEnabled(__sortingEnabled7)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.CombineToolbars),
            QCoreApplication.translate("Form", "Create custom panels", None),
        )
        self.label_2.setText(QCoreApplication.translate("Form", "Select panel:", None))
        self.label.setText(
            QCoreApplication.translate("Form", "Select workbench:", None)
        )
        self.IconOnly.setText(QCoreApplication.translate("Form", "Icon only", None))
        self.label_12.setText(
            QCoreApplication.translate("Form", " Set the icon size", None)
        )
        self.MoveUp_RibbonCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        self.MoveDown_RibbonCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", "Command", None))
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", "Small", None))
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", "Medium", None))
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", "Large", None))
        ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", "1", None))

        __sortingEnabled8 = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("Form", "Command 1", None)
        )
        self.tableWidget.setSortingEnabled(__sortingEnabled8)

        self.AddSeparator.setText(
            QCoreApplication.translate("Form", "Add separator", None)
        )
        self.RemoveSeparator.setText(
            QCoreApplication.translate("Form", "Remove separator", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("Form", " Set the panel order", None)
        )
        self.MoveUp_Toolbar.setText(QCoreApplication.translate("Form", "...", None))
        self.MoveDown_Toolbar.setText(QCoreApplication.translate("Form", "...", None))

        __sortingEnabled9 = self.ToolbarsOrder.isSortingEnabled()
        self.ToolbarsOrder.setSortingEnabled(False)
        ___qlistwidgetitem8 = self.ToolbarsOrder.item(0)
        ___qlistwidgetitem8.setText(
            QCoreApplication.translate("Form", "New Item", None)
        )
        self.ToolbarsOrder.setSortingEnabled(__sortingEnabled9)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.RibbonDesign),
            QCoreApplication.translate("Form", "Ribbon design", None),
        )

    # retranslateUi
