# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Paul Ebbers                                   *
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
import os

from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread, QSize, QEvent
from PySide.QtWidgets import (
    QTabWidget,
    QSlider,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QLabel,
    QDialogButtonBox,
    QApplication,
    QPushButton,
    QDialog,
)
from PySide.QtGui import QIcon, QPixmap
import sys

import Standard_Functions_Ribbon as StandardFunctions
import Parameters_Ribbon

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathBackup)

# import graphical created Ui. (With QtDesigner or QtCreator)
import AddCommands_ui as AddCommands_ui

# Define the translation
translate = App.Qt.translate


class LoadDialog(AddCommands_ui.Ui_Form):
    def __init__(self):

        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # Get the main window from FreeCAD
        mw = Gui.getMainWindow()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(pathUI, "AddCommands.ui"))
        
        # Install an event filter to catch events from the main window and act on it.
        self.form.installEventFilter(EventInspector(self.form))

        # Get the address of the repository address
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.ReproAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "repository"
        )

        # Make sure that the dialog stays on top
        self.form.raise_()
        self.form.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        # self.form.setWindowFlags(Qt.WindowType.Tool)
        # self.form.setWindowModality(Qt.WindowModality.WindowModal)

        # Position the dialog in front of FreeCAD
        centerPoint = mw.geometry().center()
        Rectangle = self.form.frameGeometry()
        Rectangle.moveCenter(centerPoint)
        self.form.move(Rectangle.topLeft())

class EventInspector(QObject):
    form = None

    def __init__(self, parent):
        self.form = parent
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event):
        import FCBinding

        # Show the mainwindow after the application is activated
        if event.type() == QEvent.Type.Close:
            # self.closeSignal.emit()
            mw = Gui.getMainWindow()
            RibbonBar: FCBinding.ModernMenu = mw.findChild(
                FCBinding.ModernMenu, "Ribbon"
            )
            self.EnableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            return False

        if event.type() == QEvent.Type.WindowStateChange:
            # self.closeSignal.emit()
            mw = Gui.getMainWindow()
            if self.form.windowState() == Qt.WindowState.WindowMinimized:
                RibbonBar: FCBinding.ModernMenu = mw.findChild(
                    FCBinding.ModernMenu, "Ribbon"
                )
                self.EnableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            else:
                RibbonBar: FCBinding.ModernMenu = mw.findChild(
                    FCBinding.ModernMenu, "Ribbon"
                )
                self.DisableRibbonToolbarsAndMenus(RibbonBar=RibbonBar)
            return False

        return False

    def EnableRibbonToolbarsAndMenus(self, RibbonBar):
        RibbonBar.rightToolBar().setEnabled(True)
        RibbonBar.quickAccessToolBar().setEnabled(True)
        RibbonBar.applicationOptionButton().setEnabled(True)
        RibbonBar.DesignMenuLoaded = False
        Gui.updateGui()
        return

    def DisableRibbonToolbarsAndMenus(self, RibbonBar):
        RibbonBar.rightToolBar().setDisabled(True)
        RibbonBar.quickAccessToolBar().setDisabled(True)
        RibbonBar.applicationOptionButton().setDisabled(True)
        RibbonBar.DesignMenuLoaded = True
        Gui.updateGui()
        return

def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()
