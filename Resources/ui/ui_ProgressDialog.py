# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProgressDialogCCResE.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QProgressBar, QSizePolicy, QWidget


class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName("dialog")
        dialog.resize(685, 42)
        self.gridLayout = QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar = QProgressBar(dialog)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QProgressBar.Direction.TopToBottom)

        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)

        self.label = QLabel(dialog)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.retranslateUi(dialog)

        QMetaObject.connectSlotsByName(dialog)

    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle("")
        self.progressBar.setFormat("")
        self.label.setText(QCoreApplication.translate("dialog", "Loading workbench 01 of 20", None))

    # retranslateUi
