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

from PySide.QtGui import (
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
    QPainter,
)
from PySide.QtWidgets import (
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
from PySide.QtCore import (
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
import Serialize_Ribbon
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

import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local.panel import RibbonPanel
from pyqtribbon_local.toolbutton import RibbonToolButton
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategoryLayoutButton

# import pyqtribbon_local as pyqtribbon
# from pyqtribbon.ribbonbar import RibbonMenu, RibbonBar
# from pyqtribbon.panel import RibbonPanel
# from pyqtribbon.toolbutton import RibbonToolButton
# from pyqtribbon.separator import RibbonSeparator
# from pyqtribbon.category import RibbonCategoryLayoutButton


class CustomRibbonToolButton(RibbonToolButton):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        # Create a QToolButton with icon
        button = QToolButton()
        button_icon = QStyle.SP_ArrowDown

        layout.addWidget(button)
        self.setLayout(layout)
        self.setIcon(button, button_icon)

    def setIcon(self, button, button_icon, padding=10):
        # Load the original icon as a QPixmap.
        original_icon = QPixmap(button.style().standardIcon(button_icon).pixmap(25, 22))

        # Create a new QPixmap with increased dimensions in preparation to offset the original icon's position. Fill with transparency.
        padded_icon = QPixmap(original_icon.width() + padding, original_icon.height() + 0)
        padded_icon.fill(Qt.transparent)

        # Paint the original icon onto the transparent QPixmap with an offset making the icon sit in the bottom-right.
        painter = QPainter(padded_icon)
        painter.drawPixmap(2, 0, original_icon)
        painter.end()

        # Convert the QPixmap to a QIcon and add it to the button.
        button.setIcon(QIcon(padded_icon))


#
