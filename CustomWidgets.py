# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Hakan Seven, Geolta, Paul Ebbers              *
# *                                                                       *
# * This program is free software; you can redistribute it and/or modify  *
# * it under the terms of the GNU Lesser General Public License (LGPL)    *
# * as published by the Free Software Foundation; either version 3 of     *
# * the License, or (at your option) any later version.                   *
# * for detail see the LICENCE text file.                                 *
# *                                                                       *
# * This program is distributed in the hope that it will be useful,       *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# * GNU Library General Public License for more details.                  *
# *                                                                       *
# * You should have received a copy of the GNU Library General Public     *
# * License along with this program; if not, write to the Free Software   *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# * USA                                                                   *
# *                                                                       *
# *************************************************************************
import FreeCAD as App
import FreeCADGui as Gui
from pathlib import Path

from PySide6.QtGui import (
    QIcon,
    QAction,
    QPixmap,
    QScrollEvent,
    QKeyEvent,
    QActionGroup,
    QRegion,
    QFont,
    QColor,
    QStyleHints,
)
from PySide6.QtWidgets import (
    QToolButton,
    QToolBar,
    QSizePolicy,
    QDockWidget,
    QWidget,
    QMenuBar,
    QMenu,
    QMainWindow,
    QLayout,
    QSpacerItem,
    QLayoutItem,
    QGridLayout,
    QScrollArea,
    QTabBar,
    QWidgetAction,
    QStylePainter,
    QStyle,
    QStyleOptionButton,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    Signal,
    QObject,
    QMetaMethod,
    SIGNAL,
    QEvent,
    QMetaObject,
    QCoreApplication,
    QSize,
    Slot,
    QRect,
)

import json
import os
import sys
import webbrowser
import LoadDesign_Ribbon
import Parameters_Ribbon
import LoadSettings_Ribbon
import LoadLicenseForm_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
from Standard_Functions_RIbbon import CommandInfoCorrections
import Serialize
import StyleMapping
import platform

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate

# import pyqtribbon_local as pyqtribbon
# from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
# from pyqtribbon_local.panel import RibbonPanel
# from pyqtribbon_local.toolbutton import RibbonToolButton
# from pyqtribbon_local.separator import RibbonSeparator
# from pyqtribbon_local.category import RibbonCategoryLayoutButton

import pyqtribbon as pyqtribbon
from pyqtribbon.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon.panel import RibbonPanel
from pyqtribbon.toolbutton import RibbonToolButton
from pyqtribbon.separator import RibbonSeparator
from pyqtribbon.category import RibbonCategoryLayoutButton


class CustomRibbonToolButton(RibbonToolButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._icon = self.icon()
        if not self._icon.isNull():
            super().setIcon(QIcon())

    def sizeHint(self):
        hint = super().sizeHint()
        if not self.text() or self._icon.isNull():
            return hint
        style = self.style()
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        margin = style.pixelMetric(style.PM_ButtonMargin, opt, self)
        spacing = style.pixelMetric(style.PM_LayoutVerticalSpacing, opt, self)
        # get the possible rect required for the current label
        labelRect = self.fontMetrics().boundingRect(0, 0, 5000, 5000, Qt.TextShowMnemonic, self.text())
        iconHeight = self.iconSize().height()
        height = iconHeight + spacing + labelRect.height() + margin * 2
        if height > hint.height():
            hint.setHeight(height)
        return hint

    def setIcon(self, icon):
        # setting an icon might change the horizontal hint, so we need to use a
        # "local" reference for the actual icon and go on by letting Qt to *think*
        # that it doesn't have an icon;
        if icon == self._icon:
            return
        self._icon = icon
        self.updateGeometry()

    def paintEvent(self, event):
        if self._icon.isNull() or not self.text():
            super().paintEvent(event)
            return
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        opt.text = ""
        qp = QStylePainter(self)
        # draw the button without any text or icon
        qp.drawControl(QStyle.CE_PushButton, opt)

        rect = self.rect()
        style = self.style()
        margin = style.pixelMetric(style.PM_ButtonMargin, opt, self)
        iconSize = self.iconSize()
        iconRect = QRect((rect.width() - iconSize.width()) / 2, margin, iconSize.width(), iconSize.height())
        if self.underMouse():
            state = QIcon.Active
        elif self.isEnabled():
            state = QIcon.Normal
        else:
            state = QIcon.Disabled
        qp.drawPixmap(iconRect, self._icon.pixmap(iconSize, state))

        spacing = style.pixelMetric(style.PM_LayoutVerticalSpacing, opt, self)
        labelRect = QRect(rect)
        labelRect.setTop(iconRect.bottom() + spacing)
        qp.drawText(labelRect, Qt.TextShowMnemonic | Qt.AlignHCenter | Qt.AlignTop, self.text())
