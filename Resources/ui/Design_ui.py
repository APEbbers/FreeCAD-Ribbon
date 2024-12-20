# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DesignXfPaQY.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QGroupBox,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
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
        Form.setWindowModality(Qt.WindowModality.WindowModal)
        Form.resize(990, 787)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(730, 600))
        Form.setMaximumSize(QSize(100000, 10000))
        Form.setBaseSize(QSize(730, 0))
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        Form.setAutoFillBackground(False)
        self.gridLayout_46 = QGridLayout(Form)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.gridLayout_28 = QGridLayout()
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.LoadWB = QPushButton(Form)
        self.LoadWB.setObjectName("LoadWB")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LoadWB.sizePolicy().hasHeightForWidth())
        self.LoadWB.setSizePolicy(sizePolicy1)
        self.LoadWB.setMinimumSize(QSize(10, 10))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.LoadWB.setIcon(icon)

        self.gridLayout_28.addWidget(self.LoadWB, 0, 0, 1, 1)

        self.label_14 = QLabel(Form)
        self.label_14.setObjectName("label_14")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)

        self.gridLayout_28.addWidget(self.label_14, 0, 1, 1, 1)

        self.gridLayout_46.addLayout(self.gridLayout_28, 0, 0, 1, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.Cancel = QPushButton(Form)
        self.Cancel.setObjectName("Cancel")

        self.gridLayout_6.addWidget(self.Cancel, 2, 5, 1, 1)

        self.HelpButton = QToolButton(Form)
        self.HelpButton.setObjectName("HelpButton")

        self.gridLayout_6.addWidget(self.HelpButton, 2, 8, 1, 1)

        self.Close = QPushButton(Form)
        self.Close.setObjectName("Close")

        self.gridLayout_6.addWidget(self.Close, 2, 6, 1, 1)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 2, 7, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 2, 3, 1, 1)

        self.UpdateJson = QPushButton(Form)
        self.UpdateJson.setObjectName("UpdateJson")

        self.gridLayout_6.addWidget(self.UpdateJson, 2, 4, 1, 1)

        self.ResetJson = QPushButton(Form)
        self.ResetJson.setObjectName("ResetJson")
        self.ResetJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.ResetJson, 2, 0, 1, 1)

        self.RestoreJson = QPushButton(Form)
        self.RestoreJson.setObjectName("RestoreJson")
        self.RestoreJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.RestoreJson, 2, 2, 1, 1)

        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName("scrollArea")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy3)
        self.scrollArea.setMinimumSize(QSize(530, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 968, 703))
        self.gridLayout_26 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tabWidget.setMinimumSize(QSize(200, 0))
        font = QFont()
        font.setStyleStrategy(QFont.NoAntialias)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setInputMethodHints(Qt.InputMethodHint.ImhMultiLine)
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideNone)
        self.tabWidget.setDocumentMode(False)
        self.InItialSetup = QWidget()
        self.InItialSetup.setObjectName("InItialSetup")
        self.gridLayout_32 = QGridLayout(self.InItialSetup)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.gridLayout_30 = QGridLayout()
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.ExportBox = QGroupBox(self.InItialSetup)
        self.ExportBox.setObjectName("ExportBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.ExportBox.sizePolicy().hasHeightForWidth())
        self.ExportBox.setSizePolicy(sizePolicy4)
        self.ExportBox.setMinimumSize(QSize(200, 0))
        self.gridLayout_29 = QGridLayout(self.ExportBox)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.ImportDropDownButtons_IS = QPushButton(self.ExportBox)
        self.ImportDropDownButtons_IS.setObjectName("ImportDropDownButtons_IS")

        self.gridLayout_29.addWidget(self.ImportDropDownButtons_IS, 3, 0, 1, 1)

        self.ImportCustomPanels_IS = QPushButton(self.ExportBox)
        self.ImportCustomPanels_IS.setObjectName("ImportCustomPanels_IS")

        self.gridLayout_29.addWidget(self.ImportCustomPanels_IS, 2, 0, 1, 1)

        self.Importlayout_IS = QPushButton(self.ExportBox)
        self.Importlayout_IS.setObjectName("Importlayout_IS")

        self.gridLayout_29.addWidget(self.Importlayout_IS, 0, 0, 1, 1)

        self.ExportLayout_IS = QPushButton(self.ExportBox)
        self.ExportLayout_IS.setObjectName("ExportLayout_IS")

        self.gridLayout_29.addWidget(self.ExportLayout_IS, 1, 0, 1, 1)

        self.gridLayout_30.addWidget(self.ExportBox, 0, 0, 1, 1)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_30.addItem(self.verticalSpacer_13, 1, 0, 1, 1)

        self.SetupBox = QGroupBox(self.InItialSetup)
        self.SetupBox.setObjectName("SetupBox")
        self.gridLayout_27 = QGridLayout(self.SetupBox)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.gridLayout_31 = QGridLayout()
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.label_15 = QLabel(self.SetupBox)
        self.label_15.setObjectName("label_15")
        sizePolicy4.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy4)
        self.label_15.setMinimumSize(QSize(120, 0))

        self.gridLayout_31.addWidget(self.label_15, 0, 0, 1, 1)

        self.DefaultButtonSize_IS_Workbenches = QComboBox(self.SetupBox)
        self.DefaultButtonSize_IS_Workbenches.addItem("")
        self.DefaultButtonSize_IS_Workbenches.addItem("")
        self.DefaultButtonSize_IS_Workbenches.addItem("")
        self.DefaultButtonSize_IS_Workbenches.setObjectName("DefaultButtonSize_IS_Workbenches")

        self.gridLayout_31.addWidget(self.DefaultButtonSize_IS_Workbenches, 0, 1, 1, 1)

        self.label_16 = QLabel(self.SetupBox)
        self.label_16.setObjectName("label_16")

        self.gridLayout_31.addWidget(self.label_16, 0, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_31.addItem(self.horizontalSpacer_8, 0, 4, 1, 1)

        self.gridLayout_27.addLayout(self.gridLayout_31, 0, 0, 1, 3)

        self.WorkbenchList_IS = QListWidget(self.SetupBox)
        QListWidgetItem(self.WorkbenchList_IS)
        self.WorkbenchList_IS.setObjectName("WorkbenchList_IS")
        self.WorkbenchList_IS.setMinimumSize(QSize(300, 0))
        self.WorkbenchList_IS.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.WorkbenchList_IS.setSortingEnabled(True)

        self.gridLayout_27.addWidget(self.WorkbenchList_IS, 1, 0, 1, 3)

        self.GenerateSetup_IS_WorkBenches = QPushButton(self.SetupBox)
        self.GenerateSetup_IS_WorkBenches.setObjectName("GenerateSetup_IS_WorkBenches")

        self.gridLayout_27.addWidget(self.GenerateSetup_IS_WorkBenches, 2, 0, 1, 3)

        self.gridLayout_30.addWidget(self.SetupBox, 0, 1, 2, 1)

        self.groupBox_2 = QGroupBox(self.InItialSetup)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_45 = QGridLayout(self.groupBox_2)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.gridLayout_44 = QGridLayout()
        self.gridLayout_44.setObjectName("gridLayout_44")
        self.label_24 = QLabel(self.groupBox_2)
        self.label_24.setObjectName("label_24")
        sizePolicy4.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy4)
        self.label_24.setMinimumSize(QSize(120, 0))

        self.gridLayout_44.addWidget(self.label_24, 0, 0, 1, 1)

        self.DefaultButtonSize_IS_Panels = QComboBox(self.groupBox_2)
        self.DefaultButtonSize_IS_Panels.addItem("")
        self.DefaultButtonSize_IS_Panels.addItem("")
        self.DefaultButtonSize_IS_Panels.addItem("")
        self.DefaultButtonSize_IS_Panels.setObjectName("DefaultButtonSize_IS_Panels")

        self.gridLayout_44.addWidget(self.DefaultButtonSize_IS_Panels, 0, 1, 1, 1)

        self.label_25 = QLabel(self.groupBox_2)
        self.label_25.setObjectName("label_25")

        self.gridLayout_44.addWidget(self.label_25, 0, 3, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_44.addItem(self.horizontalSpacer_9, 0, 4, 1, 1)

        self.gridLayout_45.addLayout(self.gridLayout_44, 0, 0, 1, 1)

        self.Panels_IS = QListWidget(self.groupBox_2)
        self.Panels_IS.setObjectName("Panels_IS")
        self.Panels_IS.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.Panels_IS.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.Panels_IS.setSortingEnabled(True)

        self.gridLayout_45.addWidget(self.Panels_IS, 1, 0, 1, 1)

        self.GenerateSetup_IS_Panels = QPushButton(self.groupBox_2)
        self.GenerateSetup_IS_Panels.setObjectName("GenerateSetup_IS_Panels")

        self.gridLayout_45.addWidget(self.GenerateSetup_IS_Panels, 2, 0, 1, 1)

        self.gridLayout_30.addWidget(self.groupBox_2, 0, 2, 2, 1)

        self.gridLayout_32.addLayout(self.gridLayout_30, 0, 0, 1, 1)

        self.tabWidget.addTab(self.InItialSetup, "")
        self.QAToolbars = QWidget()
        self.QAToolbars.setObjectName("QAToolbars")
        sizePolicy2.setHeightForWidth(self.QAToolbars.sizePolicy().hasHeightForWidth())
        self.QAToolbars.setSizePolicy(sizePolicy2)
        self.QAToolbars.setMinimumSize(QSize(550, 0))
        self.QAToolbars.setAutoFillBackground(True)
        self.gridLayout_7 = QGridLayout(self.QAToolbars)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame = QFrame(self.QAToolbars)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.MoveUp_Command_QC = QToolButton(self.frame)
        self.MoveUp_Command_QC.setObjectName("MoveUp_Command_QC")
        self.MoveUp_Command_QC.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout.addWidget(self.MoveUp_Command_QC, 4, 0, 1, 1)

        self.MoveDown_Command_QC = QToolButton(self.frame)
        self.MoveDown_Command_QC.setObjectName("MoveDown_Command_QC")
        self.MoveDown_Command_QC.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout.addWidget(self.MoveDown_Command_QC, 5, 0, 1, 1)

        self.Remove_Command_QC = QToolButton(self.frame)
        self.Remove_Command_QC.setObjectName("Remove_Command_QC")
        self.Remove_Command_QC.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout.addWidget(self.Remove_Command_QC, 2, 0, 1, 1)

        self.Add_Command_QC = QToolButton(self.frame)
        self.Add_Command_QC.setObjectName("Add_Command_QC")
        self.Add_Command_QC.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout.addWidget(self.Add_Command_QC, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_3, 3, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 4, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        sizePolicy4.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy4)

        self.gridLayout_10.addWidget(self.label_3, 0, 0, 1, 1)

        self.ListCategory_QC = QComboBox(self.frame)
        self.ListCategory_QC.setObjectName("ListCategory_QC")
        self.ListCategory_QC.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_10.addWidget(self.ListCategory_QC, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_10, 2, 0, 1, 3)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName("label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 3)

        self.CommandsSelected_QC = QListWidget(self.frame)
        __qlistwidgetitem = QListWidgetItem(self.CommandsSelected_QC)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        self.CommandsSelected_QC.setObjectName("CommandsSelected_QC")
        self.CommandsSelected_QC.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.CommandsSelected_QC.setMovement(QListView.Movement.Free)
        self.CommandsSelected_QC.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.CommandsSelected_QC, 4, 2, 1, 1)

        self.CommandsAvailable_QC = QListWidget(self.frame)
        __qlistwidgetitem1 = QListWidgetItem(self.CommandsAvailable_QC)
        __qlistwidgetitem1.setCheckState(Qt.Checked)
        self.CommandsAvailable_QC.setObjectName("CommandsAvailable_QC")
        self.CommandsAvailable_QC.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.CommandsAvailable_QC.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.CommandsAvailable_QC, 4, 0, 1, 1)

        self.SearchBar_QC = QLineEdit(self.frame)
        self.SearchBar_QC.setObjectName("SearchBar_QC")

        self.gridLayout_2.addWidget(self.SearchBar_QC, 0, 0, 1, 3)

        self.gridLayout_7.addWidget(self.frame, 0, 0, 1, 1)

        self.tabWidget.addTab(self.QAToolbars, "")
        self.Toolbars = QWidget()
        self.Toolbars.setObjectName("Toolbars")
        self.Toolbars.setAutoFillBackground(True)
        self.gridLayout_22 = QGridLayout(self.Toolbars)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.frame_6 = QFrame(self.Toolbars)
        self.frame_6.setObjectName("frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_17 = QGridLayout(self.frame_6)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_17.setContentsMargins(6, 6, 6, 6)
        self.PanelsToExclude_EP = QListWidget(self.frame_6)
        __qlistwidgetitem2 = QListWidgetItem(self.PanelsToExclude_EP)
        __qlistwidgetitem2.setCheckState(Qt.Checked)
        self.PanelsToExclude_EP.setObjectName("PanelsToExclude_EP")
        self.PanelsToExclude_EP.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.PanelsToExclude_EP.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.PanelsToExclude_EP, 3, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_15, 0, 0, 1, 1)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_18.addItem(self.verticalSpacer_16, 3, 0, 1, 1)

        self.RemovePanel_EP = QToolButton(self.frame_6)
        self.RemovePanel_EP.setObjectName("RemovePanel_EP")
        self.RemovePanel_EP.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_18.addWidget(self.RemovePanel_EP, 2, 0, 1, 1)

        self.AddPanel_EP = QToolButton(self.frame_6)
        self.AddPanel_EP.setObjectName("AddPanel_EP")
        self.AddPanel_EP.setAutoRaise(False)
        self.AddPanel_EP.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_18.addWidget(self.AddPanel_EP, 1, 0, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_18, 3, 1, 1, 1)

        self.label_13 = QLabel(self.frame_6)
        self.label_13.setObjectName("label_13")

        self.gridLayout_17.addWidget(self.label_13, 2, 0, 1, 3)

        self.PanelsExcluded_EP = QListWidget(self.frame_6)
        __qlistwidgetitem3 = QListWidgetItem(self.PanelsExcluded_EP)
        __qlistwidgetitem3.setCheckState(Qt.Checked)
        self.PanelsExcluded_EP.setObjectName("PanelsExcluded_EP")
        self.PanelsExcluded_EP.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.PanelsExcluded_EP.setMovement(QListView.Movement.Free)
        self.PanelsExcluded_EP.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.PanelsExcluded_EP, 3, 2, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_8 = QLabel(self.frame_6)
        self.label_8.setObjectName("label_8")
        sizePolicy4.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy4)

        self.gridLayout_11.addWidget(self.label_8, 0, 0, 1, 1)

        self.ListCategory_EP = QComboBox(self.frame_6)
        self.ListCategory_EP.setObjectName("ListCategory_EP")
        self.ListCategory_EP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_11.addWidget(self.ListCategory_EP, 0, 1, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_11, 1, 0, 1, 3)

        self.SearchBar_EP = QLineEdit(self.frame_6)
        self.SearchBar_EP.setObjectName("SearchBar_EP")

        self.gridLayout_17.addWidget(self.SearchBar_EP, 0, 0, 1, 3)

        self.gridLayout_22.addWidget(self.frame_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.Toolbars, "")
        self.Workbenches = QWidget()
        self.Workbenches.setObjectName("Workbenches")
        self.Workbenches.setAutoFillBackground(True)
        self.gridLayout_23 = QGridLayout(self.Workbenches)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.frame1 = QFrame(self.Workbenches)
        self.frame1.setObjectName("frame1")
        self.frame1.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_3 = QGridLayout(self.frame1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.WorkbenchesAvailable_IW = QListWidget(self.frame1)
        __qlistwidgetitem4 = QListWidgetItem(self.WorkbenchesAvailable_IW)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        self.WorkbenchesAvailable_IW.setObjectName("WorkbenchesAvailable_IW")
        self.WorkbenchesAvailable_IW.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.WorkbenchesAvailable_IW.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesAvailable_IW, 1, 0, 1, 1)

        self.WorkbenchesSelected_IW = QListWidget(self.frame1)
        __qlistwidgetitem5 = QListWidgetItem(self.WorkbenchesSelected_IW)
        __qlistwidgetitem5.setCheckState(Qt.Checked)
        self.WorkbenchesSelected_IW.setObjectName("WorkbenchesSelected_IW")
        self.WorkbenchesSelected_IW.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.WorkbenchesSelected_IW.setMovement(QListView.Movement.Free)
        self.WorkbenchesSelected_IW.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesSelected_IW, 1, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.RemoveWorkbench_IW = QToolButton(self.frame1)
        self.RemoveWorkbench_IW.setObjectName("RemoveWorkbench_IW")
        self.RemoveWorkbench_IW.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_4.addWidget(self.RemoveWorkbench_IW, 2, 0, 1, 1)

        self.AddWorkbench_IW = QToolButton(self.frame1)
        self.AddWorkbench_IW.setObjectName("AddWorkbench_IW")
        self.AddWorkbench_IW.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_4.addWidget(self.AddWorkbench_IW, 1, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 0, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_5, 3, 0, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_4, 1, 1, 1, 1)

        self.label_6 = QLabel(self.frame1)
        self.label_6.setObjectName("label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 3)

        self.gridLayout_23.addWidget(self.frame1, 0, 0, 1, 1)

        self.tabWidget.addTab(self.Workbenches, "")
        self.CombineToolbars = QWidget()
        self.CombineToolbars.setObjectName("CombineToolbars")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.CombineToolbars.sizePolicy().hasHeightForWidth())
        self.CombineToolbars.setSizePolicy(sizePolicy5)
        self.CombineToolbars.setMinimumSize(QSize(550, 0))
        self.gridLayout_21 = QGridLayout(self.CombineToolbars)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.CustomToolbarSelector_CP = QComboBox(self.CombineToolbars)
        self.CustomToolbarSelector_CP.setObjectName("CustomToolbarSelector_CP")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.CustomToolbarSelector_CP.sizePolicy().hasHeightForWidth())
        self.CustomToolbarSelector_CP.setSizePolicy(sizePolicy6)
        self.CustomToolbarSelector_CP.setMinimumSize(QSize(150, 0))
        self.CustomToolbarSelector_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.CustomToolbarSelector_CP, 0, 1, 1, 2)

        self.PanelName_CP = QLineEdit(self.CombineToolbars)
        self.PanelName_CP.setObjectName("PanelName_CP")
        sizePolicy6.setHeightForWidth(self.PanelName_CP.sizePolicy().hasHeightForWidth())
        self.PanelName_CP.setSizePolicy(sizePolicy6)
        self.PanelName_CP.setMinimumSize(QSize(120, 0))

        self.gridLayout_8.addWidget(self.PanelName_CP, 2, 1, 2, 2)

        self.AddCustomPanel_CP = QPushButton(self.CombineToolbars)
        self.AddCustomPanel_CP.setObjectName("AddCustomPanel_CP")
        sizePolicy1.setHeightForWidth(self.AddCustomPanel_CP.sizePolicy().hasHeightForWidth())
        self.AddCustomPanel_CP.setSizePolicy(sizePolicy1)
        self.AddCustomPanel_CP.setMinimumSize(QSize(10, 0))
        self.AddCustomPanel_CP.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.AddCustomPanel_CP, 2, 3, 2, 1)

        self.label_7 = QLabel(self.CombineToolbars)
        self.label_7.setObjectName("label_7")
        sizePolicy4.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy4)

        self.gridLayout_8.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_9 = QLabel(self.CombineToolbars)
        self.label_9.setObjectName("label_9")
        sizePolicy4.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy4)

        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)

        self.WorkbenchList_CP = QComboBox(self.CombineToolbars)
        self.WorkbenchList_CP.setObjectName("WorkbenchList_CP")
        sizePolicy6.setHeightForWidth(self.WorkbenchList_CP.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_CP.setSizePolicy(sizePolicy6)
        self.WorkbenchList_CP.setMinimumSize(QSize(0, 0))
        self.WorkbenchList_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.WorkbenchList_CP, 1, 1, 1, 2)

        self.RemovePanel_CP = QPushButton(self.CombineToolbars)
        self.RemovePanel_CP.setObjectName("RemovePanel_CP")
        self.RemovePanel_CP.setMinimumSize(QSize(10, 0))
        self.RemovePanel_CP.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.RemovePanel_CP, 0, 3, 1, 1)

        self.label_10 = QLabel(self.CombineToolbars)
        self.label_10.setObjectName("label_10")
        sizePolicy4.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy4)

        self.gridLayout_8.addWidget(self.label_10, 2, 0, 2, 1)

        self.gridLayout_21.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.frame_3 = QFrame(self.CombineToolbars)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setSizeIncrement(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_9 = QGridLayout(self.frame_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_11 = QLabel(self.frame_3)
        self.label_11.setObjectName("label_11")

        self.gridLayout_9.addWidget(self.label_11, 0, 0, 1, 3)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.MoveDownPanelCommand_CP = QToolButton(self.frame_3)
        self.MoveDownPanelCommand_CP.setObjectName("MoveDownPanelCommand_CP")
        self.MoveDownPanelCommand_CP.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_12.addWidget(self.MoveDownPanelCommand_CP, 4, 0, 1, 1)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_12.addItem(self.verticalSpacer_10, 2, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_6, 0, 0, 1, 1)

        self.MoveUpPanelCommand_CP = QToolButton(self.frame_3)
        self.MoveUpPanelCommand_CP.setObjectName("MoveUpPanelCommand_CP")
        self.MoveUpPanelCommand_CP.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_12.addWidget(self.MoveUpPanelCommand_CP, 3, 0, 1, 1)

        self.AddPanel_CP = QToolButton(self.frame_3)
        self.AddPanel_CP.setObjectName("AddPanel_CP")
        self.AddPanel_CP.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_12.addWidget(self.AddPanel_CP, 1, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.verticalSpacer_7, 5, 0, 1, 1)

        self.gridLayout_9.addLayout(self.gridLayout_12, 1, 1, 1, 1)

        self.PanelAvailable_CP = QListWidget(self.frame_3)
        __qlistwidgetitem6 = QListWidgetItem(self.PanelAvailable_CP)
        __qlistwidgetitem6.setCheckState(Qt.Checked)
        self.PanelAvailable_CP.setObjectName("PanelAvailable_CP")
        self.PanelAvailable_CP.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.PanelAvailable_CP.setSortingEnabled(True)

        self.gridLayout_9.addWidget(self.PanelAvailable_CP, 1, 0, 1, 1)

        self.PanelSelected_CP = QListWidget(self.frame_3)
        __qlistwidgetitem7 = QListWidgetItem(self.PanelSelected_CP)
        __qlistwidgetitem7.setCheckState(Qt.Checked)
        self.PanelSelected_CP.setObjectName("PanelSelected_CP")
        self.PanelSelected_CP.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.PanelSelected_CP.setMovement(QListView.Movement.Free)
        self.PanelSelected_CP.setViewMode(QListView.ViewMode.ListMode)
        self.PanelSelected_CP.setSortingEnabled(False)

        self.gridLayout_9.addWidget(self.PanelSelected_CP, 1, 2, 1, 1)

        self.gridLayout_21.addWidget(self.frame_3, 1, 0, 1, 1)

        self.tabWidget.addTab(self.CombineToolbars, "")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_43 = QGridLayout(self.tab)
        self.gridLayout_43.setObjectName("gridLayout_43")
        self.label_23 = QLabel(self.tab)
        self.label_23.setObjectName("label_23")

        self.gridLayout_43.addWidget(self.label_23, 0, 0, 1, 1)

        self.gridLayout_40 = QGridLayout()
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.SearchBar_DDB = QLineEdit(self.tab)
        self.SearchBar_DDB.setObjectName("SearchBar_DDB")

        self.gridLayout_40.addWidget(self.SearchBar_DDB, 0, 0, 1, 1)

        self.CommandsAvailable_DDB = QListWidget(self.tab)
        __qlistwidgetitem8 = QListWidgetItem(self.CommandsAvailable_DDB)
        __qlistwidgetitem8.setCheckState(Qt.Checked)
        self.CommandsAvailable_DDB.setObjectName("CommandsAvailable_DDB")
        self.CommandsAvailable_DDB.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.CommandsAvailable_DDB.setSortingEnabled(True)

        self.gridLayout_40.addWidget(self.CommandsAvailable_DDB, 2, 0, 1, 1)

        self.gridLayout_41 = QGridLayout()
        self.gridLayout_41.setObjectName("gridLayout_41")
        self.label_22 = QLabel(self.tab)
        self.label_22.setObjectName("label_22")
        sizePolicy4.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy4)

        self.gridLayout_41.addWidget(self.label_22, 0, 0, 1, 1)

        self.ListCategory_DDB = QComboBox(self.tab)
        self.ListCategory_DDB.setObjectName("ListCategory_DDB")
        self.ListCategory_DDB.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_41.addWidget(self.ListCategory_DDB, 0, 1, 1, 1)

        self.gridLayout_40.addLayout(self.gridLayout_41, 1, 0, 1, 1)

        self.gridLayout_43.addLayout(self.gridLayout_40, 1, 0, 1, 1)

        self.gridLayout_42 = QGridLayout()
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_42.addItem(self.verticalSpacer_19, 4, 0, 1, 1)

        self.MoveUpCommand_DDB = QToolButton(self.tab)
        self.MoveUpCommand_DDB.setObjectName("MoveUpCommand_DDB")
        self.MoveUpCommand_DDB.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_42.addWidget(self.MoveUpCommand_DDB, 5, 0, 1, 1)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_42.addItem(self.verticalSpacer_21, 7, 0, 1, 1)

        self.RemoveCommand_DDB = QToolButton(self.tab)
        self.RemoveCommand_DDB.setObjectName("RemoveCommand_DDB")
        self.RemoveCommand_DDB.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_42.addWidget(self.RemoveCommand_DDB, 2, 0, 1, 1)

        self.MoveDownCommand_DDB = QToolButton(self.tab)
        self.MoveDownCommand_DDB.setObjectName("MoveDownCommand_DDB")
        self.MoveDownCommand_DDB.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_42.addWidget(self.MoveDownCommand_DDB, 6, 0, 1, 1)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_42.addItem(self.verticalSpacer_20, 0, 0, 1, 1)

        self.AddCommand_DDB = QToolButton(self.tab)
        self.AddCommand_DDB.setObjectName("AddCommand_DDB")
        self.AddCommand_DDB.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_42.addWidget(self.AddCommand_DDB, 1, 0, 1, 1)

        self.gridLayout_43.addLayout(self.gridLayout_42, 1, 1, 1, 1)

        self.gridLayout_36 = QGridLayout()
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.NewControl_DDB = QListWidget(self.tab)
        __qlistwidgetitem9 = QListWidgetItem(self.NewControl_DDB)
        __qlistwidgetitem9.setCheckState(Qt.Checked)
        self.NewControl_DDB.setObjectName("NewControl_DDB")
        sizePolicy3.setHeightForWidth(self.NewControl_DDB.sizePolicy().hasHeightForWidth())
        self.NewControl_DDB.setSizePolicy(sizePolicy3)
        self.NewControl_DDB.setMinimumSize(QSize(300, 0))
        self.NewControl_DDB.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.NewControl_DDB.setSortingEnabled(False)

        self.gridLayout_36.addWidget(self.NewControl_DDB, 2, 0, 1, 2)

        self.CreateControl_DDB = QPushButton(self.tab)
        self.CreateControl_DDB.setObjectName("CreateControl_DDB")

        self.gridLayout_36.addWidget(self.CreateControl_DDB, 3, 0, 1, 2)

        self.ControlName_DDB = QLineEdit(self.tab)
        self.ControlName_DDB.setObjectName("ControlName_DDB")

        self.gridLayout_36.addWidget(self.ControlName_DDB, 1, 0, 1, 2)

        self.RemoveControl_DDB = QPushButton(self.tab)
        self.RemoveControl_DDB.setObjectName("RemoveControl_DDB")
        sizePolicy1.setHeightForWidth(self.RemoveControl_DDB.sizePolicy().hasHeightForWidth())
        self.RemoveControl_DDB.setSizePolicy(sizePolicy1)
        self.RemoveControl_DDB.setMinimumSize(QSize(120, 0))

        self.gridLayout_36.addWidget(self.RemoveControl_DDB, 0, 1, 1, 1)

        self.CommandList_DDB = QComboBox(self.tab)
        self.CommandList_DDB.setObjectName("CommandList_DDB")

        self.gridLayout_36.addWidget(self.CommandList_DDB, 0, 0, 1, 1)

        self.gridLayout_43.addLayout(self.gridLayout_36, 1, 2, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.Createnewpanels = QWidget()
        self.Createnewpanels.setObjectName("Createnewpanels")
        self.gridLayout_35 = QGridLayout(self.Createnewpanels)
        self.gridLayout_35.setObjectName("gridLayout_35")
        self.gridLayout_33 = QGridLayout()
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.gridLayout_33.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_33.setContentsMargins(6, 6, 6, 6)
        self.CustomToolbarSelector_NP = QComboBox(self.Createnewpanels)
        self.CustomToolbarSelector_NP.setObjectName("CustomToolbarSelector_NP")
        sizePolicy6.setHeightForWidth(self.CustomToolbarSelector_NP.sizePolicy().hasHeightForWidth())
        self.CustomToolbarSelector_NP.setSizePolicy(sizePolicy6)
        self.CustomToolbarSelector_NP.setMinimumSize(QSize(150, 0))
        self.CustomToolbarSelector_NP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_33.addWidget(self.CustomToolbarSelector_NP, 0, 1, 1, 2)

        self.PanelName_NP = QLineEdit(self.Createnewpanels)
        self.PanelName_NP.setObjectName("PanelName_NP")
        sizePolicy6.setHeightForWidth(self.PanelName_NP.sizePolicy().hasHeightForWidth())
        self.PanelName_NP.setSizePolicy(sizePolicy6)
        self.PanelName_NP.setMinimumSize(QSize(120, 0))

        self.gridLayout_33.addWidget(self.PanelName_NP, 2, 1, 2, 2)

        self.AddCustomToolbar_NP = QPushButton(self.Createnewpanels)
        self.AddCustomToolbar_NP.setObjectName("AddCustomToolbar_NP")
        sizePolicy1.setHeightForWidth(self.AddCustomToolbar_NP.sizePolicy().hasHeightForWidth())
        self.AddCustomToolbar_NP.setSizePolicy(sizePolicy1)
        self.AddCustomToolbar_NP.setMinimumSize(QSize(10, 0))
        self.AddCustomToolbar_NP.setBaseSize(QSize(15, 0))

        self.gridLayout_33.addWidget(self.AddCustomToolbar_NP, 2, 3, 2, 1)

        self.label_17 = QLabel(self.Createnewpanels)
        self.label_17.setObjectName("label_17")
        sizePolicy4.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy4)

        self.gridLayout_33.addWidget(self.label_17, 1, 0, 1, 1)

        self.label_18 = QLabel(self.Createnewpanels)
        self.label_18.setObjectName("label_18")
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)

        self.gridLayout_33.addWidget(self.label_18, 0, 0, 1, 1)

        self.WorkbenchList_NP = QComboBox(self.Createnewpanels)
        self.WorkbenchList_NP.setObjectName("WorkbenchList_NP")
        sizePolicy6.setHeightForWidth(self.WorkbenchList_NP.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_NP.setSizePolicy(sizePolicy6)
        self.WorkbenchList_NP.setMinimumSize(QSize(0, 0))
        self.WorkbenchList_NP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_33.addWidget(self.WorkbenchList_NP, 1, 1, 1, 2)

        self.RemovePanel_NP = QPushButton(self.Createnewpanels)
        self.RemovePanel_NP.setObjectName("RemovePanel_NP")
        self.RemovePanel_NP.setMinimumSize(QSize(10, 0))
        self.RemovePanel_NP.setBaseSize(QSize(15, 0))

        self.gridLayout_33.addWidget(self.RemovePanel_NP, 0, 3, 1, 1)

        self.label_19 = QLabel(self.Createnewpanels)
        self.label_19.setObjectName("label_19")
        sizePolicy4.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy4)

        self.gridLayout_33.addWidget(self.label_19, 2, 0, 2, 1)

        self.gridLayout_35.addLayout(self.gridLayout_33, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.Createnewpanels)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_37 = QGridLayout(self.groupBox)
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.gridLayout_38 = QGridLayout()
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.SearchBar_NP = QLineEdit(self.groupBox)
        self.SearchBar_NP.setObjectName("SearchBar_NP")

        self.gridLayout_38.addWidget(self.SearchBar_NP, 0, 0, 1, 1)

        self.CommandsAvailable_NP = QListWidget(self.groupBox)
        __qlistwidgetitem10 = QListWidgetItem(self.CommandsAvailable_NP)
        __qlistwidgetitem10.setCheckState(Qt.Checked)
        self.CommandsAvailable_NP.setObjectName("CommandsAvailable_NP")
        self.CommandsAvailable_NP.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.CommandsAvailable_NP.setSortingEnabled(True)

        self.gridLayout_38.addWidget(self.CommandsAvailable_NP, 2, 0, 1, 1)

        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName("label_21")
        sizePolicy4.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy4)

        self.gridLayout_39.addWidget(self.label_21, 0, 0, 1, 1)

        self.ListCategory_NP = QComboBox(self.groupBox)
        self.ListCategory_NP.setObjectName("ListCategory_NP")
        self.ListCategory_NP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_39.addWidget(self.ListCategory_NP, 0, 1, 1, 1)

        self.gridLayout_38.addLayout(self.gridLayout_39, 1, 0, 1, 1)

        self.gridLayout_37.addLayout(self.gridLayout_38, 2, 0, 1, 1)

        self.NewPanel_NP = QListWidget(self.groupBox)
        __qlistwidgetitem11 = QListWidgetItem(self.NewPanel_NP)
        __qlistwidgetitem11.setCheckState(Qt.Checked)
        self.NewPanel_NP.setObjectName("NewPanel_NP")
        self.NewPanel_NP.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.NewPanel_NP.setSortingEnabled(False)

        self.gridLayout_37.addWidget(self.NewPanel_NP, 2, 2, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName("label_20")

        self.gridLayout_37.addWidget(self.label_20, 0, 0, 2, 1)

        self.gridLayout_34 = QGridLayout()
        self.gridLayout_34.setObjectName("gridLayout_34")
        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_34.addItem(self.verticalSpacer_14, 4, 0, 1, 1)

        self.MoveDownPanelCommand_NP = QToolButton(self.groupBox)
        self.MoveDownPanelCommand_NP.setObjectName("MoveDownPanelCommand_NP")
        self.MoveDownPanelCommand_NP.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_34.addWidget(self.MoveDownPanelCommand_NP, 6, 0, 1, 1)

        self.MoveUpPanelCommand_NP = QToolButton(self.groupBox)
        self.MoveUpPanelCommand_NP.setObjectName("MoveUpPanelCommand_NP")
        self.MoveUpPanelCommand_NP.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_34.addWidget(self.MoveUpPanelCommand_NP, 5, 0, 1, 1)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_34.addItem(self.verticalSpacer_18, 7, 0, 1, 1)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_34.addItem(self.verticalSpacer_17, 0, 0, 1, 1)

        self.RemovePanelCommand_NP = QToolButton(self.groupBox)
        self.RemovePanelCommand_NP.setObjectName("RemovePanelCommand_NP")
        self.RemovePanelCommand_NP.setArrowType(Qt.ArrowType.LeftArrow)

        self.gridLayout_34.addWidget(self.RemovePanelCommand_NP, 2, 0, 1, 1)

        self.AddPanelCommand_NP = QToolButton(self.groupBox)
        self.AddPanelCommand_NP.setObjectName("AddPanelCommand_NP")
        self.AddPanelCommand_NP.setArrowType(Qt.ArrowType.RightArrow)

        self.gridLayout_34.addWidget(self.AddPanelCommand_NP, 1, 0, 1, 1)

        self.gridLayout_37.addLayout(self.gridLayout_34, 2, 1, 1, 1)

        self.gridLayout_35.addWidget(self.groupBox, 1, 0, 1, 1)

        self.tabWidget.addTab(self.Createnewpanels, "")
        self.RibbonDesign = QWidget()
        self.RibbonDesign.setObjectName("RibbonDesign")
        sizePolicy2.setHeightForWidth(self.RibbonDesign.sizePolicy().hasHeightForWidth())
        self.RibbonDesign.setSizePolicy(sizePolicy2)
        self.RibbonDesign.setMinimumSize(QSize(900, 0))
        self.RibbonDesign.setSizeIncrement(QSize(10, 0))
        self.RibbonDesign.setBaseSize(QSize(900, 0))
        self.RibbonDesign.setAutoFillBackground(True)
        self.gridLayout_15 = QGridLayout(self.RibbonDesign)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_16.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.label_12 = QLabel(self.RibbonDesign)
        self.label_12.setObjectName("label_12")
        font1 = QFont()
        font1.setBold(True)
        font1.setStyleStrategy(QFont.NoAntialias)
        self.label_12.setFont(font1)

        self.gridLayout_16.addWidget(self.label_12, 0, 0, 1, 1)

        self.frame2 = QFrame(self.RibbonDesign)
        self.frame2.setObjectName("frame2")
        sizePolicy2.setHeightForWidth(self.frame2.sizePolicy().hasHeightForWidth())
        self.frame2.setSizePolicy(sizePolicy2)
        self.frame2.setMinimumSize(QSize(506, 0))
        self.frame2.setFrameShape(QFrame.Shape.StyledPanel)
        self.gridLayout_14 = QGridLayout(self.frame2)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_14.setContentsMargins(6, 6, 6, 10)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_9)

        self.MoveUp_RibbonCommand_RD = QToolButton(self.frame2)
        self.MoveUp_RibbonCommand_RD.setObjectName("MoveUp_RibbonCommand_RD")
        self.MoveUp_RibbonCommand_RD.setArrowType(Qt.ArrowType.UpArrow)

        self.verticalLayout.addWidget(self.MoveUp_RibbonCommand_RD)

        self.MoveDown_RibbonCommand_RD = QToolButton(self.frame2)
        self.MoveDown_RibbonCommand_RD.setObjectName("MoveDown_RibbonCommand_RD")
        self.MoveDown_RibbonCommand_RD.setArrowType(Qt.ArrowType.DownArrow)

        self.verticalLayout.addWidget(self.MoveDown_RibbonCommand_RD)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_8)

        self.gridLayout_14.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.CommandTable_RD = QTableWidget(self.frame2)
        if self.CommandTable_RD.columnCount() < 4:
            self.CommandTable_RD.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.CommandTable_RD.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.CommandTable_RD.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.CommandTable_RD.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.CommandTable_RD.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if self.CommandTable_RD.rowCount() < 1:
            self.CommandTable_RD.setRowCount(1)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.CommandTable_RD.setItem(0, 0, __qtablewidgetitem4)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setCheckState(Qt.Checked)
        __qtablewidgetitem5.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem5.setBackground(brush)
        __qtablewidgetitem5.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.CommandTable_RD.setItem(0, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setCheckState(Qt.Checked)
        __qtablewidgetitem6.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem6.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.CommandTable_RD.setItem(0, 2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setCheckState(Qt.Checked)
        __qtablewidgetitem7.setTextAlignment(Qt.AlignCenter)
        __qtablewidgetitem7.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.CommandTable_RD.setItem(0, 3, __qtablewidgetitem7)
        self.CommandTable_RD.setObjectName("CommandTable_RD")
        sizePolicy2.setHeightForWidth(self.CommandTable_RD.sizePolicy().hasHeightForWidth())
        self.CommandTable_RD.setSizePolicy(sizePolicy2)
        self.CommandTable_RD.setMinimumSize(QSize(470, 300))
        self.CommandTable_RD.setSizeIncrement(QSize(5, 5))
        self.CommandTable_RD.setBaseSize(QSize(300, 500))
        self.CommandTable_RD.setStyleSheet("border-color: rgb(167, 167rgb(217, 217, 217), 167);")
        self.CommandTable_RD.setFrameShape(QFrame.Shape.StyledPanel)
        self.CommandTable_RD.setFrameShadow(QFrame.Shadow.Plain)
        self.CommandTable_RD.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.CommandTable_RD.setAlternatingRowColors(True)
        self.CommandTable_RD.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.CommandTable_RD.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.CommandTable_RD.setIconSize(QSize(16, 16))
        self.CommandTable_RD.horizontalHeader().setVisible(False)
        self.CommandTable_RD.horizontalHeader().setCascadingSectionResizes(False)
        self.CommandTable_RD.horizontalHeader().setProperty("showSortIndicator", False)
        self.CommandTable_RD.verticalHeader().setVisible(False)

        self.gridLayout_14.addWidget(self.CommandTable_RD, 0, 0, 1, 1)

        self.gridLayout_16.addWidget(self.frame2, 1, 0, 1, 1)

        self.gridLayout_15.addLayout(self.gridLayout_16, 1, 0, 1, 1)

        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.AddSeparator_RD = QPushButton(self.RibbonDesign)
        self.AddSeparator_RD.setObjectName("AddSeparator_RD")
        self.AddSeparator_RD.setMinimumSize(QSize(100, 0))
        font2 = QFont()
        font2.setBold(False)
        font2.setStyleStrategy(QFont.NoAntialias)
        self.AddSeparator_RD.setFont(font2)

        self.gridLayout_25.addWidget(self.AddSeparator_RD, 0, 1, 1, 1)

        self.RemoveSeparator_RD = QPushButton(self.RibbonDesign)
        self.RemoveSeparator_RD.setObjectName("RemoveSeparator_RD")
        self.RemoveSeparator_RD.setMinimumSize(QSize(100, 0))
        self.RemoveSeparator_RD.setFont(font2)

        self.gridLayout_25.addWidget(self.RemoveSeparator_RD, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(30, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_5, 0, 3, 1, 1)

        self.gridLayout_15.addLayout(self.gridLayout_25, 2, 0, 1, 1)

        self.gridLayout_19 = QGridLayout()
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.gridLayout_19.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label_4 = QLabel(self.RibbonDesign)
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font1)

        self.gridLayout_19.addWidget(self.label_4, 0, 0, 1, 1)

        self.frame3 = QFrame(self.RibbonDesign)
        self.frame3.setObjectName("frame3")
        sizePolicy2.setHeightForWidth(self.frame3.sizePolicy().hasHeightForWidth())
        self.frame3.setSizePolicy(sizePolicy2)
        self.frame3.setMinimumSize(QSize(350, 0))
        self.frame3.setBaseSize(QSize(350, 0))
        self.frame3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame3.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_13 = QGridLayout(self.frame3)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_13.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_13.setContentsMargins(6, 6, 6, 6)
        self.PanelOrder_RD = QListWidget(self.frame3)
        __qlistwidgetitem12 = QListWidgetItem(self.PanelOrder_RD)
        __qlistwidgetitem12.setCheckState(Qt.Checked)
        self.PanelOrder_RD.setObjectName("PanelOrder_RD")
        sizePolicy3.setHeightForWidth(self.PanelOrder_RD.sizePolicy().hasHeightForWidth())
        self.PanelOrder_RD.setSizePolicy(sizePolicy3)
        self.PanelOrder_RD.setMinimumSize(QSize(300, 0))
        self.PanelOrder_RD.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.PanelOrder_RD.setMovement(QListView.Movement.Free)
        self.PanelOrder_RD.setSortingEnabled(False)

        self.gridLayout_13.addWidget(self.PanelOrder_RD, 1, 0, 1, 1)

        self.gridLayout_20 = QGridLayout()
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_12, 0, 0, 1, 1)

        self.MoveUpPanel_RD = QToolButton(self.frame3)
        self.MoveUpPanel_RD.setObjectName("MoveUpPanel_RD")
        self.MoveUpPanel_RD.setArrowType(Qt.ArrowType.UpArrow)

        self.gridLayout_20.addWidget(self.MoveUpPanel_RD, 1, 0, 1, 1)

        self.MoveDownPanel_RD = QToolButton(self.frame3)
        self.MoveDownPanel_RD.setObjectName("MoveDownPanel_RD")
        self.MoveDownPanel_RD.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_20.addWidget(self.MoveDownPanel_RD, 2, 0, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_11, 3, 0, 1, 1)

        self.gridLayout_13.addLayout(self.gridLayout_20, 1, 1, 1, 1)

        self.gridLayout_19.addWidget(self.frame3, 1, 0, 1, 1)

        self.gridLayout_15.addLayout(self.gridLayout_19, 1, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.RibbonDesign)
        self.label_2.setObjectName("label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.WorkbenchList_RD = QComboBox(self.RibbonDesign)
        self.WorkbenchList_RD.setObjectName("WorkbenchList_RD")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.WorkbenchList_RD.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_RD.setSizePolicy(sizePolicy7)
        self.WorkbenchList_RD.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_5.addWidget(self.WorkbenchList_RD, 0, 1, 1, 1)

        self.PanelList_RD = QComboBox(self.RibbonDesign)
        self.PanelList_RD.setObjectName("PanelList_RD")
        self.PanelList_RD.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_5.addWidget(self.PanelList_RD, 1, 1, 1, 1)

        self.label = QLabel(self.RibbonDesign)
        self.label.setObjectName("label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.IconOnly_RD = QCheckBox(self.RibbonDesign)
        self.IconOnly_RD.setObjectName("IconOnly_RD")

        self.gridLayout_5.addWidget(self.IconOnly_RD, 1, 2, 1, 1)

        self.gridLayout_15.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.tabWidget.addTab(self.RibbonDesign, "")

        self.gridLayout_26.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 1, 0, 1, 9)

        self.gridLayout_46.addLayout(self.gridLayout_6, 1, 0, 1, 1)

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(7)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Ribbon design", None))
        self.LoadWB.setText("")
        self.label_14.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p><span style=" font-style:italic;">Reload workbenches. This may take a while.</span></p></body></html>',
                None,
            )
        )
        self.Cancel.setText(QCoreApplication.translate("Form", "Cancel", None))
        # if QT_CONFIG(shortcut)
        self.Cancel.setShortcut(QCoreApplication.translate("Form", "Esc", None))
        # endif // QT_CONFIG(shortcut)
        self.HelpButton.setText(QCoreApplication.translate("Form", "...", None))
        self.Close.setText(QCoreApplication.translate("Form", "Close", None))
        self.UpdateJson.setText(QCoreApplication.translate("Form", "Update", None))
        self.ResetJson.setText(QCoreApplication.translate("Form", "Reset", None))
        self.RestoreJson.setText(QCoreApplication.translate("Form", "Restore", None))
        self.ExportBox.setTitle(QCoreApplication.translate("Form", "Import/Export", None))
        self.ImportDropDownButtons_IS.setText(QCoreApplication.translate("Form", "Import dropdown buttons", None))
        self.ImportCustomPanels_IS.setText(QCoreApplication.translate("Form", "Import custom panels", None))
        self.Importlayout_IS.setText(QCoreApplication.translate("Form", "Import layout", None))
        self.ExportLayout_IS.setText(QCoreApplication.translate("Form", "Export layout", None))
        self.SetupBox.setTitle(QCoreApplication.translate("Form", "Set inital button size - Workbenches", None))
        self.label_15.setText(QCoreApplication.translate("Form", "Set all buttons to: ", None))
        self.DefaultButtonSize_IS_Workbenches.setItemText(0, QCoreApplication.translate("Form", "Small", None))
        self.DefaultButtonSize_IS_Workbenches.setItemText(1, QCoreApplication.translate("Form", "Medium", None))
        self.DefaultButtonSize_IS_Workbenches.setItemText(2, QCoreApplication.translate("Form", "Large", None))

        self.label_16.setText(QCoreApplication.translate("Form", "for:", None))

        __sortingEnabled = self.WorkbenchList_IS.isSortingEnabled()
        self.WorkbenchList_IS.setSortingEnabled(False)
        ___qlistwidgetitem = self.WorkbenchList_IS.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", "All", None))
        self.WorkbenchList_IS.setSortingEnabled(__sortingEnabled)

        self.GenerateSetup_IS_WorkBenches.setText(QCoreApplication.translate("Form", "Generate", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", "Set inital button size - Panels", None))
        self.label_24.setText(QCoreApplication.translate("Form", "Set all buttons to: ", None))
        self.DefaultButtonSize_IS_Panels.setItemText(0, QCoreApplication.translate("Form", "Small", None))
        self.DefaultButtonSize_IS_Panels.setItemText(1, QCoreApplication.translate("Form", "Medium", None))
        self.DefaultButtonSize_IS_Panels.setItemText(2, QCoreApplication.translate("Form", "Large", None))

        self.label_25.setText(QCoreApplication.translate("Form", "for:", None))
        self.GenerateSetup_IS_Panels.setText(QCoreApplication.translate("Form", "Generate", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.InItialSetup), QCoreApplication.translate("Form", "Initial setup", None)
        )
        # if QT_CONFIG(tooltip)
        self.MoveUp_Command_QC.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUp_Command_QC.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveDown_Command_QC.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDown_Command_QC.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.Remove_Command_QC.setToolTip(QCoreApplication.translate("Form", "Remove command", None))
        # endif // QT_CONFIG(tooltip)
        self.Remove_Command_QC.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.Add_Command_QC.setToolTip(QCoreApplication.translate("Form", "Add command", None))
        # endif // QT_CONFIG(tooltip)
        self.Add_Command_QC.setText(QCoreApplication.translate("Form", "...", None))
        self.label_3.setText(QCoreApplication.translate("Form", "Category:", None))
        self.label_5.setText(
            QCoreApplication.translate("Form", "Select commands to add to the quick access toolbar", None)
        )

        __sortingEnabled1 = self.CommandsSelected_QC.isSortingEnabled()
        self.CommandsSelected_QC.setSortingEnabled(False)
        ___qlistwidgetitem1 = self.CommandsSelected_QC.item(0)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", "New Item", None))
        self.CommandsSelected_QC.setSortingEnabled(__sortingEnabled1)

        __sortingEnabled2 = self.CommandsAvailable_QC.isSortingEnabled()
        self.CommandsAvailable_QC.setSortingEnabled(False)
        ___qlistwidgetitem2 = self.CommandsAvailable_QC.item(0)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Form", "New Item", None))
        self.CommandsAvailable_QC.setSortingEnabled(__sortingEnabled2)

        self.SearchBar_QC.setInputMask("")
        self.SearchBar_QC.setText("")
        self.SearchBar_QC.setPlaceholderText(QCoreApplication.translate("Form", "Type to search...", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.QAToolbars), QCoreApplication.translate("Form", "Quick access toolbar", None)
        )

        __sortingEnabled3 = self.PanelsToExclude_EP.isSortingEnabled()
        self.PanelsToExclude_EP.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.PanelsToExclude_EP.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Form", "New Item", None))
        self.PanelsToExclude_EP.setSortingEnabled(__sortingEnabled3)

        # if QT_CONFIG(tooltip)
        self.RemovePanel_EP.setToolTip(QCoreApplication.translate("Form", "Include panel", None))
        # endif // QT_CONFIG(tooltip)
        self.RemovePanel_EP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.AddPanel_EP.setToolTip(QCoreApplication.translate("Form", "Exclude panel", None))
        # endif // QT_CONFIG(tooltip)
        self.AddPanel_EP.setText(QCoreApplication.translate("Form", "...", None))
        self.label_13.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p>Select panels to <span style=" font-weight:600;">exclude</span> from the ribbon.</p></body></html>',
                None,
            )
        )

        __sortingEnabled4 = self.PanelsExcluded_EP.isSortingEnabled()
        self.PanelsExcluded_EP.setSortingEnabled(False)
        ___qlistwidgetitem4 = self.PanelsExcluded_EP.item(0)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("Form", "New Item", None))
        self.PanelsExcluded_EP.setSortingEnabled(__sortingEnabled4)

        self.label_8.setText(QCoreApplication.translate("Form", "Category:", None))
        self.SearchBar_EP.setInputMask("")
        self.SearchBar_EP.setText("")
        self.SearchBar_EP.setPlaceholderText(QCoreApplication.translate("Form", "Type to search...", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Toolbars), QCoreApplication.translate("Form", "Exclude panels", None)
        )

        __sortingEnabled5 = self.WorkbenchesAvailable_IW.isSortingEnabled()
        self.WorkbenchesAvailable_IW.setSortingEnabled(False)
        ___qlistwidgetitem5 = self.WorkbenchesAvailable_IW.item(0)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("Form", "New Item", None))
        self.WorkbenchesAvailable_IW.setSortingEnabled(__sortingEnabled5)

        __sortingEnabled6 = self.WorkbenchesSelected_IW.isSortingEnabled()
        self.WorkbenchesSelected_IW.setSortingEnabled(False)
        ___qlistwidgetitem6 = self.WorkbenchesSelected_IW.item(0)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("Form", "New Item", None))
        self.WorkbenchesSelected_IW.setSortingEnabled(__sortingEnabled6)

        # if QT_CONFIG(tooltip)
        self.RemoveWorkbench_IW.setToolTip(QCoreApplication.translate("Form", "Exclude workbench", None))
        # endif // QT_CONFIG(tooltip)
        self.RemoveWorkbench_IW.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.AddWorkbench_IW.setToolTip(QCoreApplication.translate("Form", "Include workbench", None))
        # endif // QT_CONFIG(tooltip)
        self.AddWorkbench_IW.setText(QCoreApplication.translate("Form", "...", None))
        self.label_6.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p>Select workbenches to<span style=" font-weight:600;"> include</span> in the ribbon.</p></body></html>',
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Workbenches), QCoreApplication.translate("Form", "Include workbenches", None)
        )
        self.PanelName_CP.setPlaceholderText(
            QCoreApplication.translate("Form", "Enter the name of your custom panel...", None)
        )
        self.AddCustomPanel_CP.setText(QCoreApplication.translate("Form", "Add", None))
        self.label_7.setText(QCoreApplication.translate("Form", "Select workbench:", None))
        self.label_9.setText(QCoreApplication.translate("Form", "Select custom panel:", None))
        self.RemovePanel_CP.setText(QCoreApplication.translate("Form", "Remove", None))
        self.label_10.setText(QCoreApplication.translate("Form", "Panel name", None))
        self.label_11.setText(
            QCoreApplication.translate(
                "Form", "<html><head/><body><p>Select panels to add to the custom panel.</p></body></html>", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.MoveDownPanelCommand_CP.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDownPanelCommand_CP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveUpPanelCommand_CP.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUpPanelCommand_CP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.AddPanel_CP.setToolTip(QCoreApplication.translate("Form", "Add panel buttons", None))
        # endif // QT_CONFIG(tooltip)
        self.AddPanel_CP.setText(QCoreApplication.translate("Form", "...", None))

        __sortingEnabled7 = self.PanelAvailable_CP.isSortingEnabled()
        self.PanelAvailable_CP.setSortingEnabled(False)
        ___qlistwidgetitem7 = self.PanelAvailable_CP.item(0)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("Form", "New Item", None))
        self.PanelAvailable_CP.setSortingEnabled(__sortingEnabled7)

        __sortingEnabled8 = self.PanelSelected_CP.isSortingEnabled()
        self.PanelSelected_CP.setSortingEnabled(False)
        ___qlistwidgetitem8 = self.PanelSelected_CP.item(0)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("Form", "New Item", None))
        self.PanelSelected_CP.setSortingEnabled(__sortingEnabled8)

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.CombineToolbars), QCoreApplication.translate("Form", "Combine panels", None)
        )
        self.label_23.setText(QCoreApplication.translate("Form", "Select commands to add to the new panel", None))
        self.SearchBar_DDB.setInputMask("")
        self.SearchBar_DDB.setText("")
        self.SearchBar_DDB.setPlaceholderText(QCoreApplication.translate("Form", "Type to search...", None))

        __sortingEnabled9 = self.CommandsAvailable_DDB.isSortingEnabled()
        self.CommandsAvailable_DDB.setSortingEnabled(False)
        ___qlistwidgetitem9 = self.CommandsAvailable_DDB.item(0)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("Form", "New Item", None))
        self.CommandsAvailable_DDB.setSortingEnabled(__sortingEnabled9)

        self.label_22.setText(QCoreApplication.translate("Form", "Category:", None))
        # if QT_CONFIG(tooltip)
        self.MoveUpCommand_DDB.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUpCommand_DDB.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.RemoveCommand_DDB.setToolTip(QCoreApplication.translate("Form", "Remove command", None))
        # endif // QT_CONFIG(tooltip)
        self.RemoveCommand_DDB.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveDownCommand_DDB.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDownCommand_DDB.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.AddCommand_DDB.setToolTip(QCoreApplication.translate("Form", "Add command", None))
        # endif // QT_CONFIG(tooltip)
        self.AddCommand_DDB.setText(QCoreApplication.translate("Form", "...", None))

        __sortingEnabled10 = self.NewControl_DDB.isSortingEnabled()
        self.NewControl_DDB.setSortingEnabled(False)
        ___qlistwidgetitem10 = self.NewControl_DDB.item(0)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("Form", "New Item", None))
        self.NewControl_DDB.setSortingEnabled(__sortingEnabled10)

        self.CreateControl_DDB.setText(QCoreApplication.translate("Form", "Create/update dropdown button", None))
        self.ControlName_DDB.setInputMask("")
        self.ControlName_DDB.setText("")
        self.ControlName_DDB.setPlaceholderText(QCoreApplication.translate("Form", "Enter command name...", None))
        self.RemoveControl_DDB.setText(QCoreApplication.translate("Form", "Remove control", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", "Create dropdown buttons", None)
        )
        self.PanelName_NP.setPlaceholderText(
            QCoreApplication.translate("Form", "Enter the name of your custom panel...", None)
        )
        self.AddCustomToolbar_NP.setText(QCoreApplication.translate("Form", "Add", None))
        self.label_17.setText(QCoreApplication.translate("Form", "Select workbench:", None))
        self.label_18.setText(QCoreApplication.translate("Form", "Select custom panel:", None))
        self.RemovePanel_NP.setText(QCoreApplication.translate("Form", "Remove", None))
        self.label_19.setText(QCoreApplication.translate("Form", "Panel name", None))
        self.groupBox.setTitle("")
        self.SearchBar_NP.setInputMask("")
        self.SearchBar_NP.setText("")
        self.SearchBar_NP.setPlaceholderText(QCoreApplication.translate("Form", "Type to search...", None))

        __sortingEnabled11 = self.CommandsAvailable_NP.isSortingEnabled()
        self.CommandsAvailable_NP.setSortingEnabled(False)
        ___qlistwidgetitem11 = self.CommandsAvailable_NP.item(0)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("Form", "New Item", None))
        self.CommandsAvailable_NP.setSortingEnabled(__sortingEnabled11)

        self.label_21.setText(QCoreApplication.translate("Form", "Category:", None))

        __sortingEnabled12 = self.NewPanel_NP.isSortingEnabled()
        self.NewPanel_NP.setSortingEnabled(False)
        ___qlistwidgetitem12 = self.NewPanel_NP.item(0)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("Form", "New Item", None))
        self.NewPanel_NP.setSortingEnabled(__sortingEnabled12)

        self.label_20.setText(QCoreApplication.translate("Form", "Select commands to add to the new panel", None))
        # if QT_CONFIG(tooltip)
        self.MoveDownPanelCommand_NP.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDownPanelCommand_NP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveUpPanelCommand_NP.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUpPanelCommand_NP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.RemovePanelCommand_NP.setToolTip(QCoreApplication.translate("Form", "Remove command", None))
        # endif // QT_CONFIG(tooltip)
        self.RemovePanelCommand_NP.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.AddPanelCommand_NP.setToolTip(QCoreApplication.translate("Form", "Add command", None))
        # endif // QT_CONFIG(tooltip)
        self.AddPanelCommand_NP.setText(QCoreApplication.translate("Form", "...", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Createnewpanels), QCoreApplication.translate("Form", "Create new panels", None)
        )
        self.label_12.setText(QCoreApplication.translate("Form", "Set the icon size", None))
        # if QT_CONFIG(tooltip)
        self.MoveUp_RibbonCommand_RD.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUp_RibbonCommand_RD.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveDown_RibbonCommand_RD.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDown_RibbonCommand_RD.setText(QCoreApplication.translate("Form", "...", None))
        ___qtablewidgetitem = self.CommandTable_RD.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", "Command", None))
        ___qtablewidgetitem1 = self.CommandTable_RD.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", "Small", None))
        ___qtablewidgetitem2 = self.CommandTable_RD.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", "Medium", None))
        ___qtablewidgetitem3 = self.CommandTable_RD.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", "Large", None))

        __sortingEnabled13 = self.CommandTable_RD.isSortingEnabled()
        self.CommandTable_RD.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.CommandTable_RD.item(0, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", "All", None))
        self.CommandTable_RD.setSortingEnabled(__sortingEnabled13)

        self.AddSeparator_RD.setText(QCoreApplication.translate("Form", "Add separator", None))
        self.RemoveSeparator_RD.setText(QCoreApplication.translate("Form", "Remove separator", None))
        self.label_4.setText(QCoreApplication.translate("Form", "Set the panel order", None))

        __sortingEnabled14 = self.PanelOrder_RD.isSortingEnabled()
        self.PanelOrder_RD.setSortingEnabled(False)
        ___qlistwidgetitem13 = self.PanelOrder_RD.item(0)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("Form", "New Item", None))
        self.PanelOrder_RD.setSortingEnabled(__sortingEnabled14)

        # if QT_CONFIG(tooltip)
        self.MoveUpPanel_RD.setToolTip(QCoreApplication.translate("Form", "Move up", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveUpPanel_RD.setText(QCoreApplication.translate("Form", "...", None))
        # if QT_CONFIG(tooltip)
        self.MoveDownPanel_RD.setToolTip(QCoreApplication.translate("Form", "Move down", None))
        # endif // QT_CONFIG(tooltip)
        self.MoveDownPanel_RD.setText(QCoreApplication.translate("Form", "...", None))
        self.label_2.setText(QCoreApplication.translate("Form", "Select panel:", None))
        self.label.setText(QCoreApplication.translate("Form", "Select workbench:", None))
        self.IconOnly_RD.setText(QCoreApplication.translate("Form", "Icon only", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.RibbonDesign), QCoreApplication.translate("Form", "Ribbon design", None)
        )

    # retranslateUi
