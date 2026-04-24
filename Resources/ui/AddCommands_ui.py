# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddCommandsbFBSkI.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
    QGroupBox, QLabel, QLayout, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(854, 463)
        Form.setAcceptDrops(True)
        self.gridLayout_4 = QGridLayout(Form)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.CustomToolbarSelector_CP.sizePolicy().hasHeightForWidth())
        self.CustomToolbarSelector_CP.setSizePolicy(sizePolicy1)
        self.CustomToolbarSelector_CP.setMinimumSize(QSize(150, 0))
        self.CustomToolbarSelector_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.CustomToolbarSelector_CP, 0, 1, 1, 2)

        self.label_7 = QLabel(self.tab_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)

        self.gridLayout_8.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)

        self.RemovePanel_CP = QPushButton(self.tab_2)
        self.RemovePanel_CP.setObjectName(u"RemovePanel_CP")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.RemovePanel_CP.sizePolicy().hasHeightForWidth())
        self.RemovePanel_CP.setSizePolicy(sizePolicy2)
        self.RemovePanel_CP.setMinimumSize(QSize(100, 0))
        self.RemovePanel_CP.setBaseSize(QSize(15, 0))

        self.gridLayout_8.addWidget(self.RemovePanel_CP, 0, 3, 1, 1)

        self.label_10 = QLabel(self.tab_2)
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)

        self.gridLayout_8.addWidget(self.label_10, 2, 0, 2, 1)

        self.WorkbenchList_CP = QComboBox(self.tab_2)
        self.WorkbenchList_CP.setObjectName(u"WorkbenchList_CP")
        sizePolicy1.setHeightForWidth(self.WorkbenchList_CP.sizePolicy().hasHeightForWidth())
        self.WorkbenchList_CP.setSizePolicy(sizePolicy1)
        self.WorkbenchList_CP.setMinimumSize(QSize(0, 0))
        self.WorkbenchList_CP.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        self.gridLayout_8.addWidget(self.WorkbenchList_CP, 1, 1, 1, 3)

        self.PanelName_CP = QLineEdit(self.tab_2)
        self.PanelName_CP.setObjectName(u"PanelName_CP")
        sizePolicy1.setHeightForWidth(self.PanelName_CP.sizePolicy().hasHeightForWidth())
        self.PanelName_CP.setSizePolicy(sizePolicy1)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.AddCustomPanel_CP.sizePolicy().hasHeightForWidth())
        self.AddCustomPanel_CP.setSizePolicy(sizePolicy3)
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
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)

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
        sizePolicy2.setHeightForWidth(self.RemoveControl_DDB.sizePolicy().hasHeightForWidth())
        self.RemoveControl_DDB.setSizePolicy(sizePolicy2)
        self.RemoveControl_DDB.setMinimumSize(QSize(120, 0))

        self.gridLayout_36.addWidget(self.RemoveControl_DDB, 0, 1, 1, 1)

        self.NewControl_DDB = QListWidget(self.groupBox_5)
        __qlistwidgetitem4 = QListWidgetItem(self.NewControl_DDB)
        __qlistwidgetitem4.setCheckState(Qt.Checked)
        self.NewControl_DDB.setObjectName(u"NewControl_DDB")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.NewControl_DDB.sizePolicy().hasHeightForWidth())
        self.NewControl_DDB.setSizePolicy(sizePolicy4)
        self.NewControl_DDB.setMinimumSize(QSize(300, 0))
        self.NewControl_DDB.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.NewControl_DDB.setSortingEnabled(False)

        self.gridLayout_36.addWidget(self.NewControl_DDB, 2, 0, 1, 2)

        self.CommandList_DDB = QComboBox(self.groupBox_5)
        self.CommandList_DDB.setObjectName(u"CommandList_DDB")
        sizePolicy3.setHeightForWidth(self.CommandList_DDB.sizePolicy().hasHeightForWidth())
        self.CommandList_DDB.setSizePolicy(sizePolicy3)

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

        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 2, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout.setVerticalSpacing(0)
        self.TimeStamp_Reloaded = QLabel(Form)
        self.TimeStamp_Reloaded.setObjectName(u"TimeStamp_Reloaded")
        font = QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.TimeStamp_Reloaded.setFont(font)

        self.gridLayout.addWidget(self.TimeStamp_Reloaded, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(651, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.LoadWB = QPushButton(Form)
        self.LoadWB.setObjectName(u"LoadWB")
        sizePolicy2.setHeightForWidth(self.LoadWB.sizePolicy().hasHeightForWidth())
        self.LoadWB.setSizePolicy(sizePolicy2)
        self.LoadWB.setMinimumSize(QSize(34, 34))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.LoadWB.setIcon(icon)

        self.gridLayout.addWidget(self.LoadWB, 0, 0, 2, 1)

        self.okButton = QPushButton(Form)
        self.okButton.setObjectName(u"okButton")

        self.gridLayout.addWidget(self.okButton, 0, 3, 2, 1)

        self.cancelButton = QPushButton(Form)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout.addWidget(self.cancelButton, 0, 4, 2, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 2, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 3, 0, 1, 1)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
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
        self.TimeStamp_Reloaded.setText(QCoreApplication.translate("Form", u"Last reloaded on: -", None))
        self.label.setText(QCoreApplication.translate("Form", u"Refresh workbench data", None))
        self.LoadWB.setText("")
        self.okButton.setText(QCoreApplication.translate("Form", u"Ok", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"Cancel", None))
#if QT_CONFIG(shortcut)
        self.cancelButton.setShortcut(QCoreApplication.translate("Form", u"Esc", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

