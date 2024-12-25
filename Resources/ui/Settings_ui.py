# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsfUQHnx.ui'
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
    QAbstractSpinBox,
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName("Settings")
        Settings.setWindowModality(Qt.WindowModality.WindowModal)
        Settings.resize(724, 722)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        Settings.setMinimumSize(QSize(600, 600))
        Settings.setAutoFillBackground(False)
        self.gridLayout_34 = QGridLayout(Settings)
        self.gridLayout_34.setObjectName("gridLayout_34")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.scrollArea = QScrollArea(Settings)
        self.scrollArea.setObjectName("scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(0, 550))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 690, 992))
        self.gridLayout_28 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.tabWidget = QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideRight)
        self.General = QWidget()
        self.General.setObjectName("General")
        self.General.setEnabled(True)
        self.General.setAutoFillBackground(True)
        self.gridLayout_9 = QGridLayout(self.General)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.groupBox = QGroupBox(self.General)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMinimumSize(QSize(0, 120))
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.gridLayout_8 = QGridLayout(self.groupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setContentsMargins(6, 6, 6, 6)
        self.EnableBackup = QCheckBox(self.groupBox)
        self.EnableBackup.setObjectName("EnableBackup")
        font1 = QFont()
        font1.setBold(False)
        self.EnableBackup.setFont(font1)

        self.gridLayout_8.addWidget(self.EnableBackup, 0, 0, 1, 1)

        self.groupBox_Backup = QGroupBox(self.groupBox)
        self.groupBox_Backup.setObjectName("groupBox_Backup")
        self.groupBox_Backup.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_Backup.sizePolicy().hasHeightForWidth())
        self.groupBox_Backup.setSizePolicy(sizePolicy2)
        self.groupBox_Backup.setMinimumSize(QSize(0, 50))
        self.groupBox_Backup.setFont(font1)
        self.gridLayout_13 = QGridLayout(self.groupBox_Backup)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_4 = QLabel(self.groupBox_Backup)
        self.label_4.setObjectName("label_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy3)
        self.label_4.setMinimumSize(QSize(400, 0))
        self.label_4.setFrameShape(QFrame.Shape.Box)
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_13.addWidget(self.label_4, 0, 0, 1, 1)

        self.BackUpLocation = QPushButton(self.groupBox_Backup)
        self.BackUpLocation.setObjectName("BackUpLocation")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(20)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.BackUpLocation.sizePolicy().hasHeightForWidth())
        self.BackUpLocation.setSizePolicy(sizePolicy4)
        self.BackUpLocation.setMinimumSize(QSize(20, 0))

        self.gridLayout_13.addWidget(self.BackUpLocation, 0, 1, 1, 1)

        self.gridLayout_8.addWidget(self.groupBox_Backup, 1, 0, 1, 1)

        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 2, 1)

        self.groupBox1 = QGroupBox(self.General)
        self.groupBox1.setObjectName("groupBox1")
        self.groupBox1.setMinimumSize(QSize(0, 300))
        self.groupBox1.setFont(font)
        self.gridLayout_4 = QGridLayout(self.groupBox1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_4 = QGroupBox(self.groupBox1)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_23 = QLabel(self.groupBox_4)
        self.label_23.setObjectName("label_23")

        self.gridLayout.addWidget(self.label_23, 5, 0, 1, 1)

        self.IconSize_Medium = QSpinBox(self.groupBox_4)
        self.IconSize_Medium.setObjectName("IconSize_Medium")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.IconSize_Medium.sizePolicy().hasHeightForWidth())
        self.IconSize_Medium.setSizePolicy(sizePolicy5)
        self.IconSize_Medium.setMinimumSize(QSize(50, 20))
        self.IconSize_Medium.setBaseSize(QSize(0, 0))
        self.IconSize_Medium.setFont(font1)
        self.IconSize_Medium.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.IconSize_Medium.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.IconSize_Medium.setValue(44)

        self.gridLayout.addWidget(self.IconSize_Medium, 1, 1, 1, 1)

        self.TabbarHeight = QSpinBox(self.groupBox_4)
        self.TabbarHeight.setObjectName("TabbarHeight")
        self.TabbarHeight.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.TabbarHeight, 5, 1, 1, 1)

        self.IconSize_Small = QSpinBox(self.groupBox_4)
        self.IconSize_Small.setObjectName("IconSize_Small")
        sizePolicy5.setHeightForWidth(self.IconSize_Small.sizePolicy().hasHeightForWidth())
        self.IconSize_Small.setSizePolicy(sizePolicy5)
        self.IconSize_Small.setMinimumSize(QSize(50, 20))
        self.IconSize_Small.setSizeIncrement(QSize(0, 0))
        self.IconSize_Small.setBaseSize(QSize(0, 0))
        self.IconSize_Small.setFont(font1)
        self.IconSize_Small.setFrame(True)
        self.IconSize_Small.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.IconSize_Small.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.IconSize_Small.setProperty("showGroupSeparator", False)
        self.IconSize_Small.setMinimum(0)
        self.IconSize_Small.setValue(24)

        self.gridLayout.addWidget(self.IconSize_Small, 0, 1, 1, 1)

        self.IconSize_ApplicationButton = QSpinBox(self.groupBox_4)
        self.IconSize_ApplicationButton.setObjectName("IconSize_ApplicationButton")
        self.IconSize_ApplicationButton.setMinimumSize(QSize(0, 20))
        self.IconSize_ApplicationButton.setMinimum(30)
        self.IconSize_ApplicationButton.setMaximum(200)
        self.IconSize_ApplicationButton.setValue(100)

        self.gridLayout.addWidget(self.IconSize_ApplicationButton, 3, 1, 1, 1)

        self.label_22 = QLabel(self.groupBox_4)
        self.label_22.setObjectName("label_22")

        self.gridLayout.addWidget(self.label_22, 6, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName("label_10")
        sizePolicy5.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy5)
        self.label_10.setMinimumSize(QSize(130, 0))
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName("label_21")

        self.gridLayout.addWidget(self.label_21, 4, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        sizePolicy5.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy5)
        self.label_11.setMinimumSize(QSize(130, 0))
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.IconSize_QuickAccessButton = QSpinBox(self.groupBox_4)
        self.IconSize_QuickAccessButton.setObjectName("IconSize_QuickAccessButton")
        self.IconSize_QuickAccessButton.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.IconSize_QuickAccessButton, 4, 1, 1, 1)

        self.IconSize_rightToolbarButton = QSpinBox(self.groupBox_4)
        self.IconSize_rightToolbarButton.setObjectName("IconSize_rightToolbarButton")
        self.IconSize_rightToolbarButton.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.IconSize_rightToolbarButton, 6, 1, 1, 1)

        self.label_25 = QLabel(self.groupBox_4)
        self.label_25.setObjectName("label_25")

        self.gridLayout.addWidget(self.label_25, 2, 0, 1, 1)

        self.IconSize_Large = QSpinBox(self.groupBox_4)
        self.IconSize_Large.setObjectName("IconSize_Large")
        self.IconSize_Large.setMaximum(200)

        self.gridLayout.addWidget(self.IconSize_Large, 2, 1, 1, 1)

        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.groupBox1)
        self.groupBox_5.setObjectName("groupBox_5")
        sizePolicy3.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy3)
        self.groupBox_5.setMinimumSize(QSize(0, 0))
        self.groupBox_5.setFont(font1)
        self.gridLayout_11 = QGridLayout(self.groupBox_5)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.MaxPanelColumn = QSpinBox(self.groupBox_5)
        self.MaxPanelColumn.setObjectName("MaxPanelColumn")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.MaxPanelColumn.sizePolicy().hasHeightForWidth())
        self.MaxPanelColumn.setSizePolicy(sizePolicy6)
        self.MaxPanelColumn.setMinimumSize(QSize(50, 20))
        self.MaxPanelColumn.setMinimum(0)
        self.MaxPanelColumn.setMaximum(99)
        self.MaxPanelColumn.setValue(6)

        self.gridLayout_10.addWidget(self.MaxPanelColumn, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName("label")

        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(0, 10))

        self.gridLayout_10.addWidget(self.label_2, 1, 0, 1, 3)

        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_5, 3, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.groupBox1)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_26 = QGridLayout()
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.ShowText_Medium = QCheckBox(self.groupBox_3)
        self.ShowText_Medium.setObjectName("ShowText_Medium")
        sizePolicy6.setHeightForWidth(self.ShowText_Medium.sizePolicy().hasHeightForWidth())
        self.ShowText_Medium.setSizePolicy(sizePolicy6)
        self.ShowText_Medium.setMinimumSize(QSize(100, 0))
        self.ShowText_Medium.setFont(font1)

        self.gridLayout_26.addWidget(self.ShowText_Medium, 1, 0, 1, 1)

        self.ShowText_Large = QCheckBox(self.groupBox_3)
        self.ShowText_Large.setObjectName("ShowText_Large")
        sizePolicy6.setHeightForWidth(self.ShowText_Large.sizePolicy().hasHeightForWidth())
        self.ShowText_Large.setSizePolicy(sizePolicy6)
        self.ShowText_Large.setMinimumSize(QSize(100, 0))
        self.ShowText_Large.setFont(font1)

        self.gridLayout_26.addWidget(self.ShowText_Large, 2, 0, 1, 1)

        self.ShowText_Small = QCheckBox(self.groupBox_3)
        self.ShowText_Small.setObjectName("ShowText_Small")
        sizePolicy6.setHeightForWidth(self.ShowText_Small.sizePolicy().hasHeightForWidth())
        self.ShowText_Small.setSizePolicy(sizePolicy6)
        self.ShowText_Small.setMinimumSize(QSize(100, 0))
        self.ShowText_Small.setFont(font1)

        self.gridLayout_26.addWidget(self.ShowText_Small, 0, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_26.addItem(self.horizontalSpacer_9, 0, 1, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout_26, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.groupBox1)
        self.groupBox_10.setObjectName("groupBox_10")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy7)
        self.groupBox_10.setMinimumSize(QSize(0, 0))
        self.gridLayout_25 = QGridLayout(self.groupBox_10)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.label_24 = QLabel(self.groupBox_10)
        self.label_24.setObjectName("label_24")

        self.gridLayout_24.addWidget(self.label_24, 0, 0, 1, 1)

        self.TabbarStyle = QComboBox(self.groupBox_10)
        self.TabbarStyle.addItem("")
        self.TabbarStyle.addItem("")
        self.TabbarStyle.setObjectName("TabbarStyle")
        self.TabbarStyle.setMinimumSize(QSize(100, 0))

        self.gridLayout_24.addWidget(self.TabbarStyle, 0, 1, 1, 1)

        self.gridLayout_25.addLayout(self.gridLayout_24, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_25.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox1)
        self.groupBox_2.setObjectName("groupBox_2")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy8)
        self.groupBox_2.setMinimumSize(QSize(0, 60))
        self.groupBox_2.setFont(font1)
        self.gridLayout_12 = QGridLayout(self.groupBox_2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 9, -1, -1)
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.label_7.setFrameShape(QFrame.Shape.Box)
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.gridLayout_12.addWidget(self.label_7, 0, 0, 1, 1)

        self.StyleSheetLocation = QPushButton(self.groupBox_2)
        self.StyleSheetLocation.setObjectName("StyleSheetLocation")
        sizePolicy4.setHeightForWidth(self.StyleSheetLocation.sizePolicy().hasHeightForWidth())
        self.StyleSheetLocation.setSizePolicy(sizePolicy4)
        self.StyleSheetLocation.setMinimumSize(QSize(20, 0))

        self.gridLayout_12.addWidget(self.StyleSheetLocation, 0, 1, 1, 1)

        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.gridLayout_9.addWidget(self.groupBox1, 2, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.DebugMode = QCheckBox(self.General)
        self.DebugMode.setObjectName("DebugMode")
        sizePolicy2.setHeightForWidth(self.DebugMode.sizePolicy().hasHeightForWidth())
        self.DebugMode.setSizePolicy(sizePolicy2)
        self.DebugMode.setMinimumSize(QSize(0, 0))
        self.DebugMode.setMaximumSize(QSize(150, 16777215))
        self.DebugMode.setBaseSize(QSize(20, 0))

        self.verticalLayout_2.addWidget(self.DebugMode)

        self.label_3 = QLabel(self.General)
        self.label_3.setObjectName("label_3")
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setMinimumSize(QSize(300, 0))
        self.label_3.setMaximumSize(QSize(16777215, 16777215))
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.gridLayout_9.addLayout(self.verticalLayout_2, 6, 0, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_7, 5, 0, 1, 1)

        self.tabWidget.addTab(self.General, "")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_14 = QGridLayout(self.tab)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.groupBox_7 = QGroupBox(self.tab)
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_18 = QGridLayout(self.groupBox_7)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.ScrollClicks_TabBar = QSpinBox(self.groupBox_7)
        self.ScrollClicks_TabBar.setObjectName("ScrollClicks_TabBar")
        sizePolicy5.setHeightForWidth(self.ScrollClicks_TabBar.sizePolicy().hasHeightForWidth())
        self.ScrollClicks_TabBar.setSizePolicy(sizePolicy5)
        self.ScrollClicks_TabBar.setMinimumSize(QSize(50, 0))
        self.ScrollClicks_TabBar.setSizeIncrement(QSize(0, 0))
        self.ScrollClicks_TabBar.setBaseSize(QSize(0, 0))
        self.ScrollClicks_TabBar.setFont(font1)
        self.ScrollClicks_TabBar.setFrame(True)
        self.ScrollClicks_TabBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ScrollClicks_TabBar.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.ScrollClicks_TabBar.setProperty("showGroupSeparator", False)
        self.ScrollClicks_TabBar.setMinimum(0)
        self.ScrollClicks_TabBar.setMaximum(10)
        self.ScrollClicks_TabBar.setValue(1)
        self.ScrollClicks_TabBar.setDisplayIntegerBase(10)

        self.gridLayout_17.addWidget(self.ScrollClicks_TabBar, 0, 1, 1, 1)

        self.label_14 = QLabel(self.groupBox_7)
        self.label_14.setObjectName("label_14")
        sizePolicy5.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy5)
        self.label_14.setMinimumSize(QSize(130, 0))
        self.label_14.setFont(font1)

        self.gridLayout_17.addWidget(self.label_14, 1, 0, 1, 1)

        self.ScrollClicks_Ribbon = QSpinBox(self.groupBox_7)
        self.ScrollClicks_Ribbon.setObjectName("ScrollClicks_Ribbon")
        sizePolicy5.setHeightForWidth(self.ScrollClicks_Ribbon.sizePolicy().hasHeightForWidth())
        self.ScrollClicks_Ribbon.setSizePolicy(sizePolicy5)
        self.ScrollClicks_Ribbon.setMinimumSize(QSize(50, 0))
        self.ScrollClicks_Ribbon.setBaseSize(QSize(0, 0))
        self.ScrollClicks_Ribbon.setFont(font1)
        self.ScrollClicks_Ribbon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ScrollClicks_Ribbon.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.ScrollClicks_Ribbon.setMaximum(10)
        self.ScrollClicks_Ribbon.setValue(1)
        self.ScrollClicks_Ribbon.setDisplayIntegerBase(10)

        self.gridLayout_17.addWidget(self.ScrollClicks_Ribbon, 1, 1, 1, 1)

        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setObjectName("label_15")
        sizePolicy5.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy5)
        self.label_15.setMinimumSize(QSize(130, 0))
        self.label_15.setFont(font1)

        self.gridLayout_17.addWidget(self.label_15, 0, 0, 1, 1)

        self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)

        self.gridLayout_14.addWidget(self.groupBox_7, 1, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.tab)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_16 = QGridLayout(self.groupBox_6)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.EnableEnterEvent = QCheckBox(self.groupBox_6)
        self.EnableEnterEvent.setObjectName("EnableEnterEvent")

        self.gridLayout_15.addWidget(self.EnableEnterEvent, 0, 0, 1, 1)

        self.ScrollSpeed_Ribbon = QSlider(self.groupBox_6)
        self.ScrollSpeed_Ribbon.setObjectName("ScrollSpeed_Ribbon")
        self.ScrollSpeed_Ribbon.setMaximum(10)
        self.ScrollSpeed_Ribbon.setPageStep(1)
        self.ScrollSpeed_Ribbon.setValue(5)
        self.ScrollSpeed_Ribbon.setOrientation(Qt.Orientation.Horizontal)
        self.ScrollSpeed_Ribbon.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ScrollSpeed_Ribbon.setTickInterval(1)

        self.gridLayout_15.addWidget(self.ScrollSpeed_Ribbon, 2, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_6)
        self.label_12.setObjectName("label_12")
        sizePolicy5.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy5)
        self.label_12.setMinimumSize(QSize(130, 0))
        self.label_12.setFont(font1)

        self.gridLayout_15.addWidget(self.label_12, 2, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_6)
        self.label_13.setObjectName("label_13")
        sizePolicy5.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy5)
        self.label_13.setMinimumSize(QSize(130, 0))
        self.label_13.setFont(font1)

        self.gridLayout_15.addWidget(self.label_13, 1, 0, 1, 1)

        self.ScrollSpeed_TabBar = QSlider(self.groupBox_6)
        self.ScrollSpeed_TabBar.setObjectName("ScrollSpeed_TabBar")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.ScrollSpeed_TabBar.sizePolicy().hasHeightForWidth())
        self.ScrollSpeed_TabBar.setSizePolicy(sizePolicy9)
        self.ScrollSpeed_TabBar.setMaximum(10)
        self.ScrollSpeed_TabBar.setSingleStep(1)
        self.ScrollSpeed_TabBar.setPageStep(1)
        self.ScrollSpeed_TabBar.setValue(5)
        self.ScrollSpeed_TabBar.setSliderPosition(5)
        self.ScrollSpeed_TabBar.setOrientation(Qt.Orientation.Horizontal)
        self.ScrollSpeed_TabBar.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ScrollSpeed_TabBar.setTickInterval(1)

        self.gridLayout_15.addWidget(self.ScrollSpeed_TabBar, 1, 1, 1, 1)

        self.gridLayout_16.addLayout(self.gridLayout_15, 0, 0, 1, 1)

        self.gridLayout_14.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_14.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_19 = QGridLayout(self.tab_2)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.groupBox_9 = QGroupBox(self.tab_2)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_23 = QGridLayout(self.groupBox_9)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.CustomIcons = QCheckBox(self.groupBox_9)
        self.CustomIcons.setObjectName("CustomIcons")

        self.gridLayout_23.addWidget(self.CustomIcons, 0, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_6, 1, 1, 1, 1)

        self.IconS = QGroupBox(self.groupBox_9)
        self.IconS.setObjectName("IconS")
        self.IconS.setEnabled(False)
        self.gridLayout_22 = QGridLayout(self.IconS)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.label_18 = QLabel(self.IconS)
        self.label_18.setObjectName("label_18")

        self.gridLayout_22.addWidget(self.label_18, 2, 0, 1, 1)

        self.label_16 = QLabel(self.IconS)
        self.label_16.setObjectName("label_16")

        self.gridLayout_22.addWidget(self.label_16, 0, 0, 1, 1)

        self.label_19 = QLabel(self.IconS)
        self.label_19.setObjectName("label_19")

        self.gridLayout_22.addWidget(self.label_19, 3, 0, 1, 1)

        self.Tab_Scroll_Left = QPushButton(self.IconS)
        self.Tab_Scroll_Left.setObjectName("Tab_Scroll_Left")
        sizePolicy6.setHeightForWidth(self.Tab_Scroll_Left.sizePolicy().hasHeightForWidth())
        self.Tab_Scroll_Left.setSizePolicy(sizePolicy6)
        self.Tab_Scroll_Left.setMinimumSize(QSize(10, 40))
        self.Tab_Scroll_Left.setMaximumSize(QSize(20, 40))
        self.Tab_Scroll_Left.setBaseSize(QSize(10, 40))

        self.gridLayout_22.addWidget(self.Tab_Scroll_Left, 0, 1, 1, 1)

        self.Ribbon_Scroll_Right = QPushButton(self.IconS)
        self.Ribbon_Scroll_Right.setObjectName("Ribbon_Scroll_Right")
        sizePolicy6.setHeightForWidth(self.Ribbon_Scroll_Right.sizePolicy().hasHeightForWidth())
        self.Ribbon_Scroll_Right.setSizePolicy(sizePolicy6)
        self.Ribbon_Scroll_Right.setMinimumSize(QSize(20, 60))
        self.Ribbon_Scroll_Right.setMaximumSize(QSize(20, 60))

        self.gridLayout_22.addWidget(self.Ribbon_Scroll_Right, 3, 1, 1, 1)

        self.label_17 = QLabel(self.IconS)
        self.label_17.setObjectName("label_17")

        self.gridLayout_22.addWidget(self.label_17, 1, 0, 1, 1)

        self.MoreCommands = QPushButton(self.IconS)
        self.MoreCommands.setObjectName("MoreCommands")
        sizePolicy6.setHeightForWidth(self.MoreCommands.sizePolicy().hasHeightForWidth())
        self.MoreCommands.setSizePolicy(sizePolicy6)
        self.MoreCommands.setMinimumSize(QSize(30, 30))
        self.MoreCommands.setMaximumSize(QSize(30, 30))
        self.MoreCommands.setBaseSize(QSize(30, 30))

        self.gridLayout_22.addWidget(self.MoreCommands, 4, 1, 1, 1)

        self.label_20 = QLabel(self.IconS)
        self.label_20.setObjectName("label_20")

        self.gridLayout_22.addWidget(self.label_20, 4, 0, 1, 1)

        self.Tab_Scroll_Right = QPushButton(self.IconS)
        self.Tab_Scroll_Right.setObjectName("Tab_Scroll_Right")
        sizePolicy6.setHeightForWidth(self.Tab_Scroll_Right.sizePolicy().hasHeightForWidth())
        self.Tab_Scroll_Right.setSizePolicy(sizePolicy6)
        self.Tab_Scroll_Right.setMinimumSize(QSize(10, 40))
        self.Tab_Scroll_Right.setMaximumSize(QSize(20, 40))
        self.Tab_Scroll_Right.setBaseSize(QSize(10, 40))

        self.gridLayout_22.addWidget(self.Tab_Scroll_Right, 1, 1, 1, 1)

        self.Ribbon_Scroll_Left = QPushButton(self.IconS)
        self.Ribbon_Scroll_Left.setObjectName("Ribbon_Scroll_Left")
        sizePolicy6.setHeightForWidth(self.Ribbon_Scroll_Left.sizePolicy().hasHeightForWidth())
        self.Ribbon_Scroll_Left.setSizePolicy(sizePolicy6)
        self.Ribbon_Scroll_Left.setMinimumSize(QSize(20, 60))
        self.Ribbon_Scroll_Left.setMaximumSize(QSize(20, 60))

        self.gridLayout_22.addWidget(self.Ribbon_Scroll_Left, 2, 1, 1, 1)

        self.pinButton = QPushButton(self.IconS)
        self.pinButton.setObjectName("pinButton")
        sizePolicy6.setHeightForWidth(self.pinButton.sizePolicy().hasHeightForWidth())
        self.pinButton.setSizePolicy(sizePolicy6)
        self.pinButton.setMinimumSize(QSize(30, 30))
        self.pinButton.setMaximumSize(QSize(30, 30))

        self.gridLayout_22.addWidget(self.pinButton, 5, 1, 1, 1)

        self.label_28 = QLabel(self.IconS)
        self.label_28.setObjectName("label_28")

        self.gridLayout_22.addWidget(self.label_28, 5, 0, 1, 1)

        self.gridLayout_23.addWidget(self.IconS, 1, 0, 1, 1)

        self.gridLayout_19.addWidget(self.groupBox_9, 1, 0, 1, 1)

        self.groupBox_8 = QGroupBox(self.tab_2)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_21 = QGridLayout(self.groupBox_8)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.CustomColors = QCheckBox(self.groupBox_8)
        self.CustomColors.setObjectName("CustomColors")

        self.gridLayout_21.addWidget(self.CustomColors, 0, 0, 1, 1)

        self.ColorS = QGroupBox(self.groupBox_8)
        self.ColorS.setObjectName("ColorS")
        self.ColorS.setEnabled(False)
        self.gridLayout_20 = QGridLayout(self.ColorS)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.label_9 = QLabel(self.ColorS)
        self.label_9.setObjectName("label_9")
        self.label_9.setWordWrap(True)

        self.gridLayout_20.addWidget(self.label_9, 2, 0, 1, 1)

        self.label_8 = QLabel(self.ColorS)
        self.label_8.setObjectName("label_8")
        self.label_8.setMinimumSize(QSize(200, 40))
        self.label_8.setWordWrap(True)

        self.gridLayout_20.addWidget(self.label_8, 1, 0, 1, 1)

        self.Color_Background = Gui_PrefColorButton(self.ColorS)
        self.Color_Background.setObjectName("Color_Background")
        sizePolicy6.setHeightForWidth(self.Color_Background.sizePolicy().hasHeightForWidth())
        self.Color_Background.setSizePolicy(sizePolicy6)

        self.gridLayout_20.addWidget(self.Color_Background, 1, 1, 1, 1)

        self.Color_Borders = Gui_PrefColorButton(self.ColorS)
        self.Color_Borders.setObjectName("Color_Borders")
        sizePolicy6.setHeightForWidth(self.Color_Borders.sizePolicy().hasHeightForWidth())
        self.Color_Borders.setSizePolicy(sizePolicy6)

        self.gridLayout_20.addWidget(self.Color_Borders, 0, 1, 1, 1)

        self.label_6 = QLabel(self.ColorS)
        self.label_6.setObjectName("label_6")

        self.gridLayout_20.addWidget(self.label_6, 0, 0, 1, 1)

        self.Color_Background_App = Gui_ColorButton(self.ColorS)
        self.Color_Background_App.setObjectName("Color_Background_App")
        sizePolicy6.setHeightForWidth(self.Color_Background_App.sizePolicy().hasHeightForWidth())
        self.Color_Background_App.setSizePolicy(sizePolicy6)

        self.gridLayout_20.addWidget(self.Color_Background_App, 2, 1, 1, 1)

        self.gridLayout_21.addWidget(self.ColorS, 1, 0, 1, 1)

        self.gridLayout_19.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_19.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_30 = QGridLayout(self.tab_3)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.verticalSpacer_3 = QSpacerItem(20, 708, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_30.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.groupBox_11 = QGroupBox(self.tab_3)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout_29 = QGridLayout(self.groupBox_11)
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_29.addItem(self.horizontalSpacer_8, 0, 1, 1, 1)

        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.label_27 = QLabel(self.groupBox_11)
        self.label_27.setObjectName("label_27")

        self.gridLayout_27.addWidget(self.label_27, 0, 0, 1, 1)

        self.PreferedViewPanel = QComboBox(self.groupBox_11)
        self.PreferedViewPanel.addItem("")
        self.PreferedViewPanel.addItem("")
        self.PreferedViewPanel.addItem("")
        self.PreferedViewPanel.addItem("")
        self.PreferedViewPanel.setObjectName("PreferedViewPanel")
        self.PreferedViewPanel.setMinimumSize(QSize(200, 0))

        self.gridLayout_27.addWidget(self.PreferedViewPanel, 0, 1, 1, 1)

        self.gridLayout_29.addLayout(self.gridLayout_27, 0, 0, 1, 1)

        self.gridLayout_31 = QGridLayout()
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.EnableToolsPanel = QCheckBox(self.groupBox_11)
        self.EnableToolsPanel.setObjectName("EnableToolsPanel")
        self.EnableToolsPanel.setChecked(True)

        self.gridLayout_31.addWidget(self.EnableToolsPanel, 0, 0, 1, 1)

        self.gridLayout_29.addLayout(self.gridLayout_31, 1, 0, 1, 1)

        self.gridLayout_30.addWidget(self.groupBox_11, 0, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.tab_3)
        self.groupBox_12.setObjectName("groupBox_12")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy10)
        self.gridLayout_32 = QGridLayout(self.groupBox_12)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.gridLayout_33 = QGridLayout()
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.FCOverlayEnabled = QCheckBox(self.groupBox_12)
        self.FCOverlayEnabled.setObjectName("FCOverlayEnabled")
        self.FCOverlayEnabled.setChecked(False)

        self.gridLayout_33.addWidget(self.FCOverlayEnabled, 0, 0, 1, 1)

        self.label_26 = QLabel(self.groupBox_12)
        self.label_26.setObjectName("label_26")
        sizePolicy10.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy10)
        self.label_26.setMinimumSize(QSize(300, 80))
        self.label_26.setSizeIncrement(QSize(0, 1))
        self.label_26.setTextFormat(Qt.TextFormat.AutoText)
        self.label_26.setWordWrap(True)

        self.gridLayout_33.addWidget(self.label_26, 0, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_33.addItem(self.horizontalSpacer_10, 0, 2, 1, 1)

        self.gridLayout_32.addLayout(self.gridLayout_33, 1, 1, 1, 1)

        self.gridLayout_30.addWidget(self.groupBox_12, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")

        self.gridLayout_28.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 0, 0, 1, 4)

        self.gridLayout_34.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.Reset = QPushButton(Settings)
        self.Reset.setObjectName("Reset")

        self.gridLayout_7.addWidget(self.Reset, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.GenerateJsonExit = QPushButton(Settings)
        self.GenerateJsonExit.setObjectName("GenerateJsonExit")

        self.gridLayout_7.addWidget(self.GenerateJsonExit, 0, 2, 1, 1)

        self.Cancel = QPushButton(Settings)
        self.Cancel.setObjectName("Cancel")

        self.gridLayout_7.addWidget(self.Cancel, 0, 3, 1, 1)

        self.gridLayout_34.addLayout(self.gridLayout_7, 1, 0, 1, 1)

        self.retranslateUi(Settings)
        self.EnableBackup.toggled.connect(self.groupBox_Backup.setEnabled)
        self.CustomColors.toggled.connect(self.ColorS.setEnabled)
        self.CustomIcons.toggled.connect(self.IconS.setEnabled)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Settings)

    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", "Preferences", None))
        self.groupBox.setTitle(QCoreApplication.translate("Settings", "Backup settings", None))
        self.EnableBackup.setText(QCoreApplication.translate("Settings", "Create backup", None))
        self.groupBox_Backup.setTitle(QCoreApplication.translate("Settings", "Backup location", None))
        self.label_4.setText(QCoreApplication.translate("Settings", "...\\", None))
        self.BackUpLocation.setText(QCoreApplication.translate("Settings", "Browse...", None))
        self.groupBox1.setTitle(QCoreApplication.translate("Settings", "Ribbon settings", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Settings", "Button size", None))
        self.label_23.setText(QCoreApplication.translate("Settings", "Size of Tabbar tabs:", None))
        self.label_22.setText(QCoreApplication.translate("Settings", "Size of right toolbar buttons:", None))
        self.label_5.setText(QCoreApplication.translate("Settings", "Size of application button:", None))
        self.label_10.setText(QCoreApplication.translate("Settings", "Size of small buttons:", None))
        self.label_21.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Size of quick access toolbar buttons:</p></body></html>", None
            )
        )
        self.label_11.setText(QCoreApplication.translate("Settings", "Size of medium buttons:", None))
        self.label_25.setText(QCoreApplication.translate("Settings", "Size of large buttons:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Settings", "Panels", None))
        self.label.setText(QCoreApplication.translate("Settings", "No. of columns per panel:", None))
        self.label_2.setText(
            QCoreApplication.translate(
                "Settings",
                "<html><head/><body><p><span style=\" font-style:italic;\">Set to '0'  to disable the maximum of columns</span></p></body></html>",
                None,
            )
        )
        self.groupBox_3.setTitle(QCoreApplication.translate("Settings", "Show text", None))
        self.ShowText_Medium.setText(QCoreApplication.translate("Settings", "Medium buttons", None))
        self.ShowText_Large.setText(QCoreApplication.translate("Settings", "Large buttons", None))
        self.ShowText_Small.setText(QCoreApplication.translate("Settings", "Small buttons", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Settings", "Tab style", None))
        self.label_24.setText(
            QCoreApplication.translate("Settings", "<html><head/><body><p>Set the tab style: </p></body></html>", None)
        )
        self.TabbarStyle.setItemText(0, QCoreApplication.translate("Settings", "Icon + text", None))
        self.TabbarStyle.setItemText(1, QCoreApplication.translate("Settings", "Text only", None))

        self.TabbarStyle.setCurrentText(QCoreApplication.translate("Settings", "Icon + text", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Settings", "Select stylesheet", None))
        self.label_7.setText(QCoreApplication.translate("Settings", "...\\", None))
        self.StyleSheetLocation.setText(QCoreApplication.translate("Settings", "Browse...", None))
        self.DebugMode.setText(QCoreApplication.translate("Settings", "Debug mode", None))
        self.label_3.setText(
            QCoreApplication.translate(
                "Settings",
                '<html><head/><body><p><span style=" font-style:italic;">Debug mode enables extra reports in the report view for debugging purposes.</span></p></body></html>',
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.General), QCoreApplication.translate("Settings", "General", None)
        )
        self.groupBox_7.setTitle(QCoreApplication.translate("Settings", "Scroll buttons", None))
        self.label_14.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Scroll steps per click for ribbon:</p></body></html>", None
            )
        )
        self.label_15.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Scroll steps per click for tab bar:</p></body></html>", None
            )
        )
        self.groupBox_6.setTitle(QCoreApplication.translate("Settings", "Mouse settings", None))
        self.EnableEnterEvent.setText(QCoreApplication.translate("Settings", "Show ribbon on hover. ", None))
        self.label_12.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Scroll speed for ribbon:</p></body></html>", None
            )
        )
        self.label_13.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Scroll speed for tab bar:</p></body></html>", None
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Settings", "Navigation", None)
        )
        self.groupBox_9.setTitle(QCoreApplication.translate("Settings", "Icons", None))
        self.CustomIcons.setText(QCoreApplication.translate("Settings", "Enable custom icons", None))
        self.label_18.setText(QCoreApplication.translate("Settings", "Ribbon bar scroll left:", None))
        self.label_16.setText(
            QCoreApplication.translate("Settings", "<html><head/><body><p>Tab bar scroll left:</p></body></html>", None)
        )
        self.label_19.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>Ribbon bar scroll right:</p></body></html>", None
            )
        )
        self.Tab_Scroll_Left.setText(QCoreApplication.translate("Settings", "...", None))
        self.Ribbon_Scroll_Right.setText(QCoreApplication.translate("Settings", "...", None))
        self.label_17.setText(QCoreApplication.translate("Settings", "Tab bar scroll right:", None))
        self.MoreCommands.setText(QCoreApplication.translate("Settings", "...", None))
        self.label_20.setText(
            QCoreApplication.translate(
                "Settings", "<html><head/><body><p>More commands button:</p></body></html>", None
            )
        )
        self.Tab_Scroll_Right.setText(QCoreApplication.translate("Settings", "...", None))
        self.Ribbon_Scroll_Left.setText(QCoreApplication.translate("Settings", "...", None))
        self.pinButton.setText(QCoreApplication.translate("Settings", "...", None))
        self.label_28.setText(QCoreApplication.translate("Settings", "Pin button:", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Settings", "Colors", None))
        self.CustomColors.setText(QCoreApplication.translate("Settings", "Enable custom colors", None))
        self.label_9.setText(
            QCoreApplication.translate("Settings", "Set the background color for the application button:", None)
        )
        self.label_8.setText(
            QCoreApplication.translate(
                "Settings",
                "<html><head/><body><p>Set the background color for the controls and toolbars:</p></body></html>",
                None,
            )
        )
        self.label_6.setText(QCoreApplication.translate("Settings", "Set the color for control borders:", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Settings", "Colors and icons", None)
        )
        self.groupBox_11.setTitle(QCoreApplication.translate("Settings", "Standard panels preference", None))
        self.label_27.setText(QCoreApplication.translate("Settings", "Select preferred standard view panel: ", None))
        self.PreferedViewPanel.setItemText(0, QCoreApplication.translate("Settings", "Individual views - Native", None))
        self.PreferedViewPanel.setItemText(1, QCoreApplication.translate("Settings", "Views - Native", None))
        self.PreferedViewPanel.setItemText(2, QCoreApplication.translate("Settings", "Views - Ribbon", None))
        self.PreferedViewPanel.setItemText(3, QCoreApplication.translate("Settings", "None", None))

        self.EnableToolsPanel.setText(QCoreApplication.translate("Settings", "Use standard Tools panel", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Settings", "Overlay preferences", None))
        # if QT_CONFIG(tooltip)
        self.FCOverlayEnabled.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "Use the overlay function from FreeCAD.\n"
                "Uncheck this when there are issues with the overlay function and the FreeCAD Ribbon.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.FCOverlayEnabled.setText(QCoreApplication.translate("Settings", "Use FreeCAD's overlay function.", None))
        self.label_26.setText(
            QCoreApplication.translate(
                "Settings",
                "<html><head/><body><p><span style=\" font-size:8pt; font-style:italic;\">The overlay function can give issues. Use at your own risk.</span></p><p><span style=\" font-size:8pt; font-style:italic;\">When there are issues, place a file </span><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:8pt; color:#ffffff;\">&quot;OVERLAY_DISABLED&quot; </span><span style=\" font-family:'Consolas','Courier New','monospace'; font-size:8pt; font-style:italic; color:#ffffff;\">in the folder of the add-on. (No extension) This will restore the ribbon and its own overlay function.</span></p></body></html>",
                None,
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("Settings", "Miscellaneous", None)
        )
        self.Reset.setText(QCoreApplication.translate("Settings", "Reset", None))
        self.GenerateJsonExit.setText(QCoreApplication.translate("Settings", "Close", None))
        # if QT_CONFIG(shortcut)
        self.GenerateJsonExit.setShortcut("")
        # endif // QT_CONFIG(shortcut)
        self.Cancel.setText(QCoreApplication.translate("Settings", "Cancel", None))
        # if QT_CONFIG(shortcut)
        self.Cancel.setShortcut(QCoreApplication.translate("Settings", "Esc", None))


# endif // QT_CONFIG(shortcut)
# retranslateUi
