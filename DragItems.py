# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Paul Ebbers              *
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
    QDrag,
    # QKeySequence,
)
from PySide.QtWidgets import (
    QToolButton,
    QWidget,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QComboBox,
    QFontComboBox,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
    QProgressBar,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QDateTimeEdit,
    QDateEdit,
    QTimeEdit,
    QTableWidget,
    QTreeWidget,
    QCalendarWidget,
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
    QMimeData,
)

import json
import os
import sys
import Parameters_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
import platform
import subprocess
import xml.etree.ElementTree as ET

# Get the resources
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
sys.path.append(pathStylSheets)
sys.path.append(pathPackages)

translate = App.Qt.translate

import pyqtribbon_local_local_local as pyqtribbon_local_local_local
from pyqtribbon_local_local_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local_local_local.panel import RibbonPanel
from pyqtribbon_local_local_local.toolbutton import RibbonToolButton
from pyqtribbon_local_local_local.separator import RibbonSeparator


class DragTargetIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(25, 5, 25, 5)
        self.setStyleSheet(
            "QLabel { background-color: #ccc; border: 1px solid black; }"
        )


class DragRibbonToolButton(RibbonToolButton):
    """
    Generic list sorting handler.
    """

    orderChanged = Signal(list)

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        self.setLayout(self.blayout)

        # Add the drag target indicator. This is invisible by default,
        # we show it and move it around while the drag is active.
        self._drag_target_indicator = DragTargetIndicator()
        self.blayout.addWidget(self._drag_target_indicator)
        self._drag_target_indicator.hide()

        self.setLayout(self.blayout)

    # def dragEnterEvent(self, e):
    #     e.accept()

    # def dragLeaveEvent(self, e):
    #     self._drag_target_indicator.hide()
    #     e.accept()

    # def dragMoveEvent(self, e):
    #     # Find the correct location of the drop target, so we can move it there.
    #     index = self._find_drop_location(e)
    #     if index is not None:
    #         # Inserting moves the item if its alreaady in the layout.
    #         self.blayout.insertWidget(index, self._drag_target_indicator)
    #         # Hide the item being dragged.
    #         e.source().hide()
    #         # Show the target.
    #         self._drag_target_indicator.show()
    #     e.accept()

    # def dropEvent(self, e):
    #     widget = e.source()
    #     # Use drop target location for destination, then remove it.
    #     self._drag_target_indicator.hide()
    #     index = self.blayout.indexOf(self._drag_target_indicator)
    #     if index is not None:
    #         self.blayout.insertWidget(index, widget)
    #         self.orderChanged.emit(self.get_item_data())
    #         widget.show()
    #         self.blayout.activate()
    #     e.accept()

    # def _find_drop_location(self, e):
    #     pos = e.pos()
    #     spacing = self.blayout.spacing() / 2

    #     for n in range(self.blayout.count()):
    #         # Get the widget at each index in turn.
    #         w = self.blayout.itemAt(n).widget()

    #         if self.orientation == Qt.Orientation.Vertical:
    #             # Drag drop vertically.
    #             drop_here = pos.y() >= w.y() - spacing and pos.y() <= w.y() + w.size().height() + spacing
    #         else:
    #             # Drag drop horizontally.
    #             drop_here = pos.x() >= w.x() - spacing and pos.x() <= w.x() + w.size().width() + spacing

    #         if drop_here:
    #             # Drop over this target.
    #             break

    #     return n

    # def add_item(self, item):
    #     self.blayout.addWidget(item)

    # def get_item_data(self):
    #     data = []
    #     for n in range(self.blayout.count()):
    #         # Get the widget at each index in turn.
    #         w = self.blayout.itemAt(n).widget()
    #         data.append(w.data)
    #     return data

    # def mouseMoveEvent(self, e):
    #     if e.buttons() == Qt.MouseButton.LeftButton:
    #         drag = QDrag(self)
    #         mime = QMimeData()
    #         drag.setMimeData(mime)
    #         drag.exec(Qt.DropAction.MoveAction)


class DragSeparator(RibbonSeparator):
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.DropAction.MoveAction)


class DragPanel(RibbonPanel):
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec(Qt.DropAction.MoveAction)
