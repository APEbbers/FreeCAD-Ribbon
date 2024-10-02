# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
    QAbstractSpinBox,
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


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
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)

        self.Cancel = QPushButton(Form)
        self.Cancel.setObjectName("Cancel")

        self.gridLayout_6.addWidget(self.Cancel, 0, 1, 1, 1)

        self.GenerateJsonExit = QPushButton(Form)
        self.GenerateJsonExit.setObjectName("GenerateJsonExit")

        self.gridLayout_6.addWidget(self.GenerateJsonExit, 0, 2, 1, 1)

        self.gridLayout_7.addLayout(self.gridLayout_6, 1, 0, 1, 1)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setElideMode(Qt.ElideRight)
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
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBox_Backup.sizePolicy().hasHeightForWidth()
        )
        self.groupBox_Backup.setSizePolicy(sizePolicy)
        self.groupBox_Backup.setMinimumSize(QSize(0, 50))
        self.groupBox_Backup.setFont(font1)
        self.gridLayout_13 = QGridLayout(self.groupBox_Backup)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_4 = QLabel(self.groupBox_Backup)
        self.label_4.setObjectName("label_4")
        self.label_4.setFrameShape(QFrame.Box)
        self.label_4.setScaledContents(True)
        self.label_4.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_13.addWidget(self.label_4, 0, 0, 1, 1)

        self.BackUpLocation = QPushButton(self.groupBox_Backup)
        self.BackUpLocation.setObjectName("BackUpLocation")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(20)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.BackUpLocation.sizePolicy().hasHeightForWidth()
        )
        self.BackUpLocation.setSizePolicy(sizePolicy1)
        self.BackUpLocation.setMinimumSize(QSize(20, 0))

        self.gridLayout_13.addWidget(self.BackUpLocation, 0, 1, 1, 1)

        self.gridLayout_8.addWidget(self.groupBox_Backup, 1, 0, 1, 1)

        self.gridLayout_9.addWidget(self.groupBox, 0, 0, 2, 1)

        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_9.addItem(self.verticalSpacer_7, 3, 0, 1, 1)

        self.groupBox1 = QGroupBox(self.General)
        self.groupBox1.setObjectName("groupBox1")
        self.groupBox1.setMinimumSize(QSize(0, 300))
        self.groupBox1.setFont(font)
        self.gridLayout_4 = QGridLayout(self.groupBox1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_3 = QGroupBox(self.groupBox1)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setFont(font1)
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ShowText_Small = QCheckBox(self.groupBox_3)
        self.ShowText_Small.setObjectName("ShowText_Small")
        self.ShowText_Small.setFont(font1)

        self.verticalLayout.addWidget(self.ShowText_Small)

        self.ShowText_Medium = QCheckBox(self.groupBox_3)
        self.ShowText_Medium.setObjectName("ShowText_Medium")
        self.ShowText_Medium.setFont(font1)

        self.verticalLayout.addWidget(self.ShowText_Medium)

        self.ShowText_Large = QCheckBox(self.groupBox_3)
        self.ShowText_Large.setObjectName("ShowText_Large")
        self.ShowText_Large.setFont(font1)

        self.verticalLayout.addWidget(self.ShowText_Large)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox1)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setFont(font1)
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName("label_11")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy2)
        self.label_11.setMinimumSize(QSize(130, 0))
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName("label_10")
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)
        self.label_10.setMinimumSize(QSize(130, 0))
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.IconSize_Small = QSpinBox(self.groupBox_4)
        self.IconSize_Small.setObjectName("IconSize_Small")
        sizePolicy2.setHeightForWidth(
            self.IconSize_Small.sizePolicy().hasHeightForWidth()
        )
        self.IconSize_Small.setSizePolicy(sizePolicy2)
        self.IconSize_Small.setMinimumSize(QSize(50, 0))
        self.IconSize_Small.setSizeIncrement(QSize(0, 0))
        self.IconSize_Small.setBaseSize(QSize(0, 0))
        self.IconSize_Small.setFont(font1)
        self.IconSize_Small.setFrame(True)
        self.IconSize_Small.setAlignment(Qt.AlignCenter)
        self.IconSize_Small.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.IconSize_Small.setProperty("showGroupSeparator", False)
        self.IconSize_Small.setMinimum(0)
        self.IconSize_Small.setValue(24)

        self.gridLayout.addWidget(self.IconSize_Small, 0, 1, 1, 1)

        self.IconSize_Medium = QSpinBox(self.groupBox_4)
        self.IconSize_Medium.setObjectName("IconSize_Medium")
        sizePolicy2.setHeightForWidth(
            self.IconSize_Medium.sizePolicy().hasHeightForWidth()
        )
        self.IconSize_Medium.setSizePolicy(sizePolicy2)
        self.IconSize_Medium.setMinimumSize(QSize(50, 0))
        self.IconSize_Medium.setBaseSize(QSize(0, 0))
        self.IconSize_Medium.setFont(font1)
        self.IconSize_Medium.setAlignment(Qt.AlignCenter)
        self.IconSize_Medium.setCorrectionMode(QAbstractSpinBox.CorrectToNearestValue)
        self.IconSize_Medium.setValue(44)

        self.gridLayout.addWidget(self.IconSize_Medium, 1, 1, 1, 1)

        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_5.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.groupBox1)
        self.groupBox_5.setObjectName("groupBox_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
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
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(
            self.MaxPanelColumn.sizePolicy().hasHeightForWidth()
        )
        self.MaxPanelColumn.setSizePolicy(sizePolicy4)
        self.MaxPanelColumn.setMinimumSize(QSize(50, 0))
        self.MaxPanelColumn.setMinimum(0)
        self.MaxPanelColumn.setMaximum(99)
        self.MaxPanelColumn.setValue(6)

        self.gridLayout_10.addWidget(self.MaxPanelColumn, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName("label")

        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_10.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumSize(QSize(0, 10))

        self.gridLayout_10.addWidget(self.label_2, 1, 0, 1, 3)

        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.gridLayout_3.addWidget(self.groupBox_5, 2, 0, 1, 1)

        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox1)
        self.groupBox_2.setObjectName("groupBox_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy5)
        self.groupBox_2.setMinimumSize(QSize(0, 60))
        self.groupBox_2.setFont(font1)
        self.gridLayout_12 = QGridLayout(self.groupBox_2)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.gridLayout_12.setContentsMargins(-1, 9, -1, -1)
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.label_7.setFrameShape(QFrame.Box)
        self.label_7.setScaledContents(True)
        self.label_7.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_12.addWidget(self.label_7, 0, 0, 1, 1)

        self.StyleSheetLocation = QPushButton(self.groupBox_2)
        self.StyleSheetLocation.setObjectName("StyleSheetLocation")
        sizePolicy1.setHeightForWidth(
            self.StyleSheetLocation.sizePolicy().hasHeightForWidth()
        )
        self.StyleSheetLocation.setSizePolicy(sizePolicy1)
        self.StyleSheetLocation.setMinimumSize(QSize(20, 0))

        self.gridLayout_12.addWidget(self.StyleSheetLocation, 0, 1, 1, 1)

        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.gridLayout_9.addWidget(self.groupBox1, 2, 0, 1, 1)

        self.tabWidget.addTab(self.General, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.EnableBackup.toggled.connect(self.groupBox_Backup.setEnabled)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.Cancel.setText(QCoreApplication.translate("Form", "Cancel", None))
        # if QT_CONFIG(shortcut)
        self.Cancel.setShortcut(QCoreApplication.translate("Form", "Esc", None))
        # endif // QT_CONFIG(shortcut)
        self.GenerateJsonExit.setText(QCoreApplication.translate("Form", "Close", None))
        # if QT_CONFIG(shortcut)
        self.GenerateJsonExit.setShortcut("")
        # endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(
            QCoreApplication.translate("Form", "Backup settings", None)
        )
        self.EnableBackup.setText(
            QCoreApplication.translate("Form", "Create backup", None)
        )
        self.groupBox_Backup.setTitle(
            QCoreApplication.translate("Form", "Backup location", None)
        )
        self.label_4.setText(QCoreApplication.translate("Form", "...\\", None))
        self.BackUpLocation.setText(
            QCoreApplication.translate("Form", "Browse..", None)
        )
        self.groupBox1.setTitle(
            QCoreApplication.translate("Form", "Ribbon settings", None)
        )
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", "Show text", None))
        self.ShowText_Small.setText(
            QCoreApplication.translate("Form", "Small buttons", None)
        )
        self.ShowText_Medium.setText(
            QCoreApplication.translate("Form", "Medium buttons", None)
        )
        self.ShowText_Large.setText(
            QCoreApplication.translate("Form", "Large buttons", None)
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate("Form", "Button size", None)
        )
        self.label_11.setText(
            QCoreApplication.translate("Form", "Size of medium buttons:", None)
        )
        self.label_10.setText(
            QCoreApplication.translate("Form", "Size of small buttons:", None)
        )
        self.groupBox_5.setTitle(QCoreApplication.translate("Form", "Panels", None))
        self.label.setText(
            QCoreApplication.translate("Form", "No. of columns per panel", None)
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "Form",
                "<html><head/><body><p><span style=\" font-style:italic;\">Set to '0'  to disable the maximum of columns</span></p></body></html>",
                None,
            )
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate("Form", "Select stylesheet", None)
        )
        self.label_7.setText(QCoreApplication.translate("Form", "...\\", None))
        self.StyleSheetLocation.setText(
            QCoreApplication.translate("Form", "Browse..", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.General),
            QCoreApplication.translate("Form", "General", None),
        )

    # retranslateUi
