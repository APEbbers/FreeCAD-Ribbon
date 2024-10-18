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
from PySide6.QtGui import (
    QIcon,
    QAction,
    QPixmap,
    QScrollEvent,
    QKeyEvent,
    QActionGroup,
    QDrag,
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
    QHBoxLayout,
    QVBoxLayout,
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
    QMimeData,
)

import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local.panel import RibbonPanel
from pyqtribbon_local.toolbutton import RibbonToolButton
from pyqtribbon_local.separator import RibbonSeparator

from pyqtribbon.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon.panel import RibbonPanel
from pyqtribbon.toolbutton import RibbonToolButton
from pyqtribbon.separator import RibbonSeparator


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

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = pos.y() < w.y() + w.size().height() // 2
            else:
                # Drag drop horizontally.
                drop_here = pos.x() < w.x() + w.size().width() // 2

            if drop_here:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n - 1, widget)
                self.orderChanged.emit(self.get_item_data())
                break

        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            data.append(w.data)
        return data

    # def mouseMoveEvent(self, e):
    #     if e.buttons() == Qt.MouseButton.LeftButton:
    #         drag = QDrag(self)
    #         mime = QMimeData()
    #         drag.setMimeData(mime)
    #         drag.exec(Qt.DropAction.MoveAction)

    # def dragEnterEvent(self, e):
    #     e.accept()


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
