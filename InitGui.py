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
import os
import FreeCAD as App
import FreeCADGui as Gui
import FCBinding
import Parameters_Ribbon
import shutil
import sys
import platform
from PySide.QtCore import Qt, QTimer, QSize, QSettings
from PySide.QtGui import QGuiApplication
from PySide.QtWidgets import QMainWindow, QLabel, QSizePolicy, QApplication


def QT_TRANSLATE_NOOP(context, text):
    return text


global pathIcons

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(FCBinding.__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(FCBinding.__file__), "Resources", "packages")
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate

# check if there is a "RibbonStructure.json". if not create one
file = os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json")
file_default = os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure_default.json")
source = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
source_default = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")

# check if file exits
fileExists = os.path.isfile(file)
# if not, copy and rename
if fileExists is False:
    shutil.copy(source, file)

# check if file exits
fileExists = os.path.isfile(file_default)
# if not, copy and rename
if fileExists is False:
    shutil.copy(source_default, file_default)

# remove the test workbench
Gui.removeWorkbench("TestWorkbench")

USECUSTOMOVERLAY = os.path.join(os.path.dirname(FCBinding.__file__), "OVERLAY_DISABLED")
if Parameters_Ribbon.USE_FC_OVERLAY is False or os.path.exists(USECUSTOMOVERLAY) is True:
    # Disable the overlay function
    preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
    preferences.SetBool("ActivateOverlay", False)

    # make sure that the ribbon will be shown on startup -> reset OverlayTop
    preferences = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
    preferences.SetString("Widgets", "")
if Parameters_Ribbon.USE_FC_OVERLAY is True:
    # Disable the overlay function
    preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
    preferences.SetBool("ActivateOverlay", True)

try:
    print(translate("FreeCAD Ribbon", "Activating Ribbon Bar..."))
    mw = Gui.getMainWindow()

    if Parameters_Ribbon.HIDE_TITLEBAR_FC is False:
        mw.workbenchActivated.connect(FCBinding.run)

    # Hide the Titlebar of FreeCAD
    if Parameters_Ribbon.HIDE_TITLEBAR_FC is True:
        mw.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)

        # Define a timer
        timer = QTimer()
        # Use singleshot to show the mainwindow after the UI is loaded comppletly
        timer.singleShot(0, mw.workbenchActivated.connect(FCBinding.run))
        mw.showMaximized()
        print(translate("FreeCAD Ribbon", "FreeCAD loaded without titlebar"))

except Exception as e:
    # raise e
    if Parameters_Ribbon.DEBUG_MODE is True:
        print(f"{e.with_traceback(e.__traceback__)}, 0")

Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
Gui.updateLocale()
