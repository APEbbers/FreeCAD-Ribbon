# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DesignOMElqt.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.setWindowModality(Qt.WindowModal)
        Form.resize(580, 724)
        Form.setAutoFillBackground(False)
        self.gridLayout_7 = QGridLayout(Form)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalSpacer = QSpacerItem(
            10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 3, 1, 1)

        self.GenerateJson = QPushButton(Form)
        self.GenerateJson.setObjectName("GenerateJson")

        self.gridLayout_6.addWidget(self.GenerateJson, 0, 4, 1, 1)

        self.ResetJson = QPushButton(Form)
        self.ResetJson.setObjectName("ResetJson")
        self.ResetJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.ResetJson, 0, 0, 1, 1)

        self.RestoreJson = QPushButton(Form)
        self.RestoreJson.setObjectName("RestoreJson")
        self.RestoreJson.setEnabled(True)

        self.gridLayout_6.addWidget(self.RestoreJson, 0, 2, 1, 1)

        self.GenerateJsonExit = QPushButton(Form)
        self.GenerateJsonExit.setObjectName("GenerateJsonExit")

        self.gridLayout_6.addWidget(self.GenerateJsonExit, 0, 5, 1, 1)

        self.gridLayout_7.addLayout(self.gridLayout_6, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.QAToolbars = QWidget()
        self.QAToolbars.setObjectName("QAToolbars")
        self.QAToolbars.setAutoFillBackground(True)
        self.layoutWidget = QWidget(self.QAToolbars)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 10, 551, 631))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.MoveUp_Command = QToolButton(self.layoutWidget)
        self.MoveUp_Command.setObjectName("MoveUp_Command")
        self.MoveUp_Command.setArrowType(Qt.UpArrow)

        self.gridLayout.addWidget(self.MoveUp_Command, 4, 0, 1, 1)

        self.MoveDown_Command = QToolButton(self.layoutWidget)
        self.MoveDown_Command.setObjectName("MoveDown_Command")
        self.MoveDown_Command.setArrowType(Qt.DownArrow)

        self.gridLayout.addWidget(self.MoveDown_Command, 5, 0, 1, 1)

        self.Remove_Command = QToolButton(self.layoutWidget)
        self.Remove_Command.setObjectName("Remove_Command")
        self.Remove_Command.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.Remove_Command, 2, 0, 1, 1)

        self.Add_Command = QToolButton(self.layoutWidget)
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
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.gridLayout_10.addWidget(self.label_3, 0, 0, 1, 1)

        self.ListCategory_1 = QComboBox(self.layoutWidget)
        self.ListCategory_1.setObjectName("ListCategory_1")

        self.gridLayout_10.addWidget(self.ListCategory_1, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_10, 2, 0, 1, 3)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 3)

        self.CommandsSelected = QListWidget(self.layoutWidget)
        __qlistwidgetitem = QListWidgetItem(self.CommandsSelected)
        __qlistwidgetitem.setCheckState(Qt.Checked)
        self.CommandsSelected.setObjectName("CommandsSelected")
        self.CommandsSelected.setDefaultDropAction(Qt.MoveAction)
        self.CommandsSelected.setMovement(QListView.Free)
        self.CommandsSelected.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.CommandsSelected, 4, 2, 1, 1)

        self.CommandsAvailable = QListWidget(self.layoutWidget)
        __qlistwidgetitem1 = QListWidgetItem(self.CommandsAvailable)
        __qlistwidgetitem1.setCheckState(Qt.Checked)
        self.CommandsAvailable.setObjectName("CommandsAvailable")
        self.CommandsAvailable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.CommandsAvailable.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.CommandsAvailable, 4, 0, 1, 1)

        self.SearchBar_1 = QLineEdit(self.layoutWidget)
        self.SearchBar_1.setObjectName("SearchBar_1")

        self.gridLayout_2.addWidget(self.SearchBar_1, 0, 0, 1, 3)

        self.tabWidget.addTab(self.QAToolbars, "")
        self.Toolbars = QWidget()
        self.Toolbars.setObjectName("Toolbars")
        self.Toolbars.setAutoFillBackground(True)
        self.layoutWidget_6 = QWidget(self.Toolbars)
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.layoutWidget_6.setGeometry(QRect(0, 10, 551, 631))
        self.gridLayout_17 = QGridLayout(self.layoutWidget_6)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_17.setContentsMargins(6, 6, 6, 6)
        self.ToolbarsToExclude = QListWidget(self.layoutWidget_6)
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

        self.Remove_Toolbar = QToolButton(self.layoutWidget_6)
        self.Remove_Toolbar.setObjectName("Remove_Toolbar")
        self.Remove_Toolbar.setArrowType(Qt.LeftArrow)

        self.gridLayout_18.addWidget(self.Remove_Toolbar, 2, 0, 1, 1)

        self.Add_Toolbar = QToolButton(self.layoutWidget_6)
        self.Add_Toolbar.setObjectName("Add_Toolbar")
        self.Add_Toolbar.setArrowType(Qt.RightArrow)

        self.gridLayout_18.addWidget(self.Add_Toolbar, 1, 0, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_18, 3, 1, 1, 1)

        self.label_13 = QLabel(self.layoutWidget_6)
        self.label_13.setObjectName("label_13")

        self.gridLayout_17.addWidget(self.label_13, 2, 0, 1, 3)

        self.ToolbarsExcluded = QListWidget(self.layoutWidget_6)
        __qlistwidgetitem3 = QListWidgetItem(self.ToolbarsExcluded)
        __qlistwidgetitem3.setCheckState(Qt.Checked)
        self.ToolbarsExcluded.setObjectName("ToolbarsExcluded")
        self.ToolbarsExcluded.setDefaultDropAction(Qt.MoveAction)
        self.ToolbarsExcluded.setMovement(QListView.Free)
        self.ToolbarsExcluded.setSortingEnabled(True)

        self.gridLayout_17.addWidget(self.ToolbarsExcluded, 3, 2, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_8 = QLabel(self.layoutWidget_6)
        self.label_8.setObjectName("label_8")
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)

        self.gridLayout_11.addWidget(self.label_8, 0, 0, 1, 1)

        self.ListCategory_2 = QComboBox(self.layoutWidget_6)
        self.ListCategory_2.setObjectName("ListCategory_2")

        self.gridLayout_11.addWidget(self.ListCategory_2, 0, 1, 1, 1)

        self.gridLayout_17.addLayout(self.gridLayout_11, 1, 0, 1, 3)

        self.SearchBar_2 = QLineEdit(self.layoutWidget_6)
        self.SearchBar_2.setObjectName("SearchBar_2")

        self.gridLayout_17.addWidget(self.SearchBar_2, 0, 0, 1, 3)

        self.tabWidget.addTab(self.Toolbars, "")
        self.Workbenches = QWidget()
        self.Workbenches.setObjectName("Workbenches")
        self.Workbenches.setAutoFillBackground(True)
        self.layoutWidget1 = QWidget(self.Workbenches)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 10, 551, 631))
        self.gridLayout_3 = QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.WorkbenchesAvailable = QListWidget(self.layoutWidget1)
        __qlistwidgetitem4 = QListWidgetItem(self.WorkbenchesAvailable)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        self.WorkbenchesAvailable.setObjectName("WorkbenchesAvailable")
        self.WorkbenchesAvailable.setSelectionMode(QAbstractItemView.MultiSelection)
        self.WorkbenchesAvailable.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesAvailable, 1, 0, 1, 1)

        self.WorkbenchesSelected = QListWidget(self.layoutWidget1)
        __qlistwidgetitem5 = QListWidgetItem(self.WorkbenchesSelected)
        __qlistwidgetitem5.setCheckState(Qt.Checked)
        self.WorkbenchesSelected.setObjectName("WorkbenchesSelected")
        self.WorkbenchesSelected.setDefaultDropAction(Qt.MoveAction)
        self.WorkbenchesSelected.setMovement(QListView.Free)
        self.WorkbenchesSelected.setSortingEnabled(True)

        self.gridLayout_3.addWidget(self.WorkbenchesSelected, 1, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.Remove_Workbench = QToolButton(self.layoutWidget1)
        self.Remove_Workbench.setObjectName("Remove_Workbench")
        self.Remove_Workbench.setArrowType(Qt.LeftArrow)

        self.gridLayout_4.addWidget(self.Remove_Workbench, 2, 0, 1, 1)

        self.Add_Workbench = QToolButton(self.layoutWidget1)
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

        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")

        self.gridLayout_3.addWidget(self.label_6, 0, 0, 1, 3)

        self.tabWidget.addTab(self.Workbenches, "")
        self.RibbonDesign = QWidget()
        self.RibbonDesign.setObjectName("RibbonDesign")
        self.RibbonDesign.setAutoFillBackground(True)
        self.layoutWidget2 = QWidget(self.RibbonDesign)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 10, 391, 58))
        self.gridLayout_5 = QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.layoutWidget2)
        self.label_2.setObjectName("label_2")

        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)

        self.WorkbenchList = QComboBox(self.layoutWidget2)
        self.WorkbenchList.setObjectName("WorkbenchList")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.WorkbenchList.sizePolicy().hasHeightForWidth()
        )
        self.WorkbenchList.setSizePolicy(sizePolicy1)

        self.gridLayout_5.addWidget(self.WorkbenchList, 0, 1, 1, 1)

        self.ToolbarList = QComboBox(self.layoutWidget2)
        self.ToolbarList.setObjectName("ToolbarList")

        self.gridLayout_5.addWidget(self.ToolbarList, 1, 1, 1, 1)

        self.label = QLabel(self.layoutWidget2)
        self.label.setObjectName("label")

        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)

        self.IconOnly = QCheckBox(self.layoutWidget2)
        self.IconOnly.setObjectName("IconOnly")

        self.gridLayout_5.addWidget(self.IconOnly, 1, 2, 1, 1)

        self.layoutWidget3 = QWidget(self.RibbonDesign)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 70, 541, 571))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.tableWidget = QTableWidget(self.layoutWidget3)
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

        self.horizontalLayout_3.addWidget(self.tableWidget)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalSpacer_9 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_9)

        self.MoveUp_RibbonCommand = QToolButton(self.layoutWidget3)
        self.MoveUp_RibbonCommand.setObjectName("MoveUp_RibbonCommand")
        self.MoveUp_RibbonCommand.setArrowType(Qt.UpArrow)

        self.verticalLayout.addWidget(self.MoveUp_RibbonCommand)

        self.MoveDown_RibbonCommand = QToolButton(self.layoutWidget3)
        self.MoveDown_RibbonCommand.setObjectName("MoveDown_RibbonCommand")
        self.MoveDown_RibbonCommand.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.MoveDown_RibbonCommand)

        self.verticalSpacer_8 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer_8)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.tabWidget.addTab(self.RibbonDesign, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(3)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Ribbon design", None))
        self.GenerateJson.setText(QCoreApplication.translate("Form", "Update", None))
        self.ResetJson.setText(QCoreApplication.translate("Form", "Reset", None))
        self.RestoreJson.setText(QCoreApplication.translate("Form", "Restore", None))
        self.GenerateJsonExit.setText(QCoreApplication.translate("Form", "Close", None))
        # if QT_CONFIG(shortcut)
        self.GenerateJsonExit.setShortcut(
            QCoreApplication.translate("Form", "Esc", None)
        )
        # endif // QT_CONFIG(shortcut)
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
                '<html><head/><body><p>Select toolbars to <span style=" font-weight:600;">exclude</span> from the ribbon.</p></body></html>',
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
            QCoreApplication.translate("Form", "Toolbars", None),
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
            QCoreApplication.translate("Form", "Workbenches", None),
        )
        self.label_2.setText(
            QCoreApplication.translate("Form", "Select toolbar:", None)
        )
        self.label.setText(
            QCoreApplication.translate("Form", "Select workbench:", None)
        )
        self.IconOnly.setText(QCoreApplication.translate("Form", "Icon only", None))
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

        __sortingEnabled6 = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        ___qtablewidgetitem5 = self.tableWidget.item(0, 0)
        ___qtablewidgetitem5.setText(
            QCoreApplication.translate("Form", "Command 1", None)
        )
        self.tableWidget.setSortingEnabled(__sortingEnabled6)

        self.MoveUp_RibbonCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        self.MoveDown_RibbonCommand.setText(
            QCoreApplication.translate("Form", "...", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.RibbonDesign),
            QCoreApplication.translate("Form", "Ribbon design", None),
        )

    # retranslateUi