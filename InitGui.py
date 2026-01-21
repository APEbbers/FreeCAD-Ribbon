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
from Parameters_Ribbon import Settings
import Standard_Functions_Ribbon as StandardFunctions
import shutil
import sys
import platform
from PySide.QtCore import Qt, QTimer, QSize, QSettings
from PySide.QtGui import QGuiApplication
from PySide.QtWidgets import (
    QMainWindow,
    QLabel,
    QSizePolicy,
    QApplication,
    QToolButton,
    QStyle,
)
import logging

# Set the logger levels to avoid extra output in the report panel
logging.getLogger("urllib3").setLevel(logging.INFO)

# Set a value for the current needed version of the Ribbon structure. 
# Increasing this, results in a new created default structure file.
CurrentStructureVersion = 2

def QT_TRANSLATE_NOOP(context, text):
    return text


global pathIcons

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(FCBinding.__file__), "Scripts")
pathPackages = os.path.join(
    os.path.dirname(FCBinding.__file__), "Resources", "packages"
)
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate

# Move the data files to the new location for fixing issue with the new addon manager
# Function to move the data files out the addon folder to fix issue with the new addon manager
#
#Create the new folder for the data
if not os.path.exists(os.path.join(App.getUserAppDataDir(), "RibbonUI")):
    os.makedirs(os.path.join(App.getUserAppDataDir(), "RibbonUI"))
# Move the files if present
if Settings.GetStringSetting("RibbonStructure") == os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json"):
    try:
        # Update the paths for the ribbon structure and the backup folder
        Settings.SetStringSetting("RibbonStructure", os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonStructure.json"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json")): 
            shutil.copy(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json"), os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonStructure.json"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile.dat")):
            shutil.copy(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile.dat"), os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonDataFile.dat"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile2.dat")):
            shutil.copy(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile2.dat"), os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonDataFile2.dat"))
    except Exception:
        pass

if Settings.GetStringSetting("BackupFolder") == os.path.join(os.path.dirname(FCBinding.__file__), "BackupFolder"):
    try:
        Settings.SetStringSetting("BackupFolder", os.path.join(App.getUserAppDataDir(), "RibbonUI", "Backups"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "Backups")):
            shutil.copy(os.path.join(os.path.dirname(FCBinding.__file__), "Backups"), os.path.join(App.getUserAppDataDir(), "RibbonUI", "Backups"))
    except Exception:
        pass

# check if there is a "RibbonStructure.json". if not create one
file = os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonStructure.json")
file_default = os.path.join(App.getUserAppDataDir(), "RibbonUI", "RibbonStructure_default.json")
source = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
source_default = os.path.join(
    os.path.dirname(FCBinding.__file__), "CreateStructure.txt"
)

NewDefaultNeeded = True
ribbonStructureVersion = Parameters_Ribbon.Settings.GetIntSetting("RibbonStructureVersion")
if ribbonStructureVersion >= CurrentStructureVersion:
    NewDefaultNeeded = False

# check if file exits
fileExists = os.path.isfile(file)

# if not, copy and rename
if fileExists is False:
    shutil.copy(source, file)

# check if file exits
fileExists = os.path.isfile(file_default)
# if not, copy and rename
if fileExists is False or NewDefaultNeeded is True:
    shutil.copy(source_default, file_default)
    Parameters_Ribbon.Settings.SetIntSetting("RibbonStructureVersion", CurrentStructureVersion)

# remove the test workbench
try:    
    Gui.removeWorkbench("TestWorkbench")
except Exception:
    pass

USECUSTOMOVERLAY = os.path.join(os.path.dirname(FCBinding.__file__), "OVERLAY_DISABLED")
if (
    Parameters_Ribbon.USE_FC_OVERLAY is False
    or os.path.exists(USECUSTOMOVERLAY) is True
):
    # Disable the overlay function
    preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
    preferences.SetBool("ActivateOverlay", False)

    # make sure that the ribbon will be shown on startup -> reset OverlayTop
    preferences = App.ParamGet(
        "User parameter:BaseApp/MainWindow/DockWindows/OverlayTop"
    )
    preferences.SetString("Widgets", "")
if Parameters_Ribbon.USE_FC_OVERLAY is True:
    # Disable the overlay function
    preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
    preferences.SetBool("ActivateOverlay", True)

try:
    print(translate("FreeCAD Ribbon", "Activating Ribbon UI..."))
    mw = Gui.getMainWindow()

    if Parameters_Ribbon.HIDE_TITLEBAR_FC is False:
        mw.setWindowFlags(Qt.WindowType.WindowFullscreenButtonHint)
        mw.workbenchActivated.connect(FCBinding.run)
        mw.showMaximized()

    # Hide the Titlebar of FreeCAD
    if Parameters_Ribbon.HIDE_TITLEBAR_FC is True:
        # make a customized toolbar and hide all the buttons.
        # This works better than a frameless window
        mw.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        mw.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, False)
        mw.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        # Connect the ribbon when the workbench is activated
        mw.workbenchActivated.connect(FCBinding.run)
        # Normally after setting the window frameless you show the window with mw.show()
        # This is now done in FCBinding with an eventfilter class
        print(translate("FreeCAD Ribbon", "Ribbon UI: FreeCAD loaded without titlebar"))

except Exception as e:
    # raise e
    if Parameters_Ribbon.DEBUG_MODE is True:
        print(f"{e.with_traceback(e.__traceback__)}, 0")

Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
Gui.updateLocale()


