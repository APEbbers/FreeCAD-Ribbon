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
from Parameters_Ribbon import Parameters
from Parameters_Ribbon import Settings
import Standard_Functions_Ribbon as StandardFunctions
import shutil
import sys
from datetime import datetime
import json

from PySide.QtCore import Qt, QTimer, QSize, QSettings
from PySide.QtGui import QGuiApplication
from PySide.QtWidgets import (
    QMainWindow,
    QLabel,
    QSizePolicy,
    QApplication,
    QToolButton,
    QStyle,
    QDockWidget,
)

# Set a value for the current needed version of the Ribbon structure. 
# Increasing this, results in a new created default structure file.
CurrentStructureVersion = 2

def QT_TRANSLATE_NOOP(context, text):
    return text


global pathIcons

# Get the resources
ConfigDirectory = Parameters.CONFIG_DIR
pathIcons = Parameters.ICON_LOCATION
pathStylSheets = Parameters.STYLESHEET_LOCATION
pathUI = Parameters.UI_LOCATION
pathScripts = os.path.join(ConfigDirectory, "Scripts")
pathPackages = os.path.join(os.path.dirname(FCBinding.__file__), "Resources", "packages")
pathBackup = Parameters.BACKUP_LOCATION
sys.path.append(ConfigDirectory)
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)
sys.path.append(pathBackup)

translate = App.Qt.translate
mw: QMainWindow = Gui.getMainWindow()

# Set the wait cursor
QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

# Move the data files to the new location for fixing issue with the new addon manager
# Function to move the data files out the addon folder to fix issue with the new addon manager
#
#Create the new folder for the data
if not os.path.exists(ConfigDirectory):
    os.makedirs(ConfigDirectory)
    
# Move the files if present
if Settings.GetStringSetting("RibbonStructure") == os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json"):
    try:
        # Update the paths for the ribbon structure and the backup folder
        Settings.SetStringSetting("RibbonStructure", os.path.join(ConfigDirectory, "RibbonStructure.json"))
        # Copy the data files if they exits
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json")): 
            shutil.copyfile(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonStructure.json"), os.path.join(ConfigDirectory, "RibbonStructure.json"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile.dat")):
            shutil.copyfile(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile.dat"), os.path.join(ConfigDirectory, "RibbonDataFile.dat"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile2.dat")):
            shutil.copyfile(os.path.join(os.path.dirname(FCBinding.__file__), "RibbonDataFile2.dat"), os.path.join(ConfigDirectory, "RibbonDataFile2.dat"))
    except Exception as e:
        print(e)
        pass

if Settings.GetStringSetting("BackupFolder") == os.path.join(os.path.dirname(FCBinding.__file__), "BackupFolder"):
    try:
        Settings.SetStringSetting("BackupFolder", os.path.join(ConfigDirectory, "Backups"))
        if os.path.exists(os.path.join(os.path.dirname(FCBinding.__file__), "Backups")):
            shutil.copytree(os.path.join(os.path.dirname(FCBinding.__file__), "Backups"), os.path.join(ConfigDirectory, "Backups"))
    except Exception:
        pass

# check if there is a "RibbonStructure.json". if not create one
file = os.path.join(ConfigDirectory, "RibbonStructure.json")
file_default = os.path.join(ConfigDirectory, "RibbonStructure_default.json")
source = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
source_default = os.path.join(
    os.path.dirname(FCBinding.__file__), "CreateStructure.txt"
)

NewDefaultNeeded = True
ribbonStructureVersion = Parameters_Ribbon.Settings.GetIntSetting("RibbonStructureVersion")
if ribbonStructureVersion >= CurrentStructureVersion:
    NewDefaultNeeded = False

# check if file exits
fileExists = os.path.exists(file)

# Check if the json file is not corrupted
if fileExists is True:  
    try:   
        with open(file, "r") as file_check:
            json.load(file_check)
    except Exception as e:
        # Store  the current corrupted file
        #
        # Create a suffix with the date
        Suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a backup name
        FileName = f"RibbonStructure_{Suffix}.json"
        Path = os.path.join(ConfigDirectory, "Error files")
        # If the backup folder doesn't exists, create it
        if os.path.exists(Path) is False:
            os.makedirs(Path)
        errorFile = os.path.join(Path, FileName)
        # Copy the file
        shutil.copy(file, errorFile)
        # If present, copy the logfile as well
        logFile = os.path.join(App.getUserAppDataDir(), "FreeCAD.log")
        logFileCopy = os.path.join(Path, f"FreeCAD_{Suffix}.log")
        if os.path.exists(logFile):
            shutil.copy(logFile, logFileCopy)
        
        # Create a new json file
        newFile = file
        source_default = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
        shutil.copy(source_default, newFile)
        
        # Print a message that the ribbon structure has ben reverted to default
        StandardFunctions.Print(translate("FreeCAD Ribbon", 
            f"""RibbonUI: RibbonStructure.json got corrupted. A new file is created\nYou can find the corruped file in {Path}"""), "Error")
        # Print the error message, so that it is on the log
        StandardFunctions.Print(translate("FreeCAD Ribbon", "Traceback: \n") + str(e.with_traceback(e.__traceback__)) + "\n in " + os.path.join(ConfigDirectory, "RibbonStructure.json"), "Error")

# if there is no ribbonStructure.json, copy and rename
if fileExists is False:
    shutil.copy(source, file)

# check if file exits
fileExists = os.path.isfile(file_default)
# if not, copy and rename
if fileExists is False or NewDefaultNeeded is True:
    shutil.copy(source_default, file_default)
    Parameters_Ribbon.Settings.SetIntSetting("RibbonStructureVersion", CurrentStructureVersion)
    
# Make sure that the parameter for the ribbon structure is correct
if os.path.exists(Settings.GetStringSetting("RibbonStructure")) is False:
    Settings.SetStringSetting("RibbonStructure", os.path.join(ConfigDirectory, "RibbonStructure.json"))
    
# Make sure that the parameter for the backup folder is correct
if os.path.exists(Settings.GetStringSetting("BackupFolder")) is False:
    Settings.SetStringSetting("BackupFolder", os.path.join(ConfigDirectory, "Backups"))

# remove the test workbench
try:    
    Gui.removeWorkbench("TestWorkbench")
except Exception:
    pass

# Get the overlay settings
preferences_DockWindows = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
if preferences_DockWindows.GetBool("ActivateOverlay") is True:
    Parameters.USE_OVERLAY = True
    if Parameters.OVERLAYSTATE == 2:
        state = Parameters_Ribbon.Settings.GetStringSetting("StoredOverlayState")
        if state != "":
            OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
            # Set the new string in parameters
            OverlayParam_Top.SetString("Widgets",state)
            
# If the searchBar is installed, disable the toolbar, since it is implemented in the ribbon
# This avoids seeing the searchBar toolbar during startup         
try:
    preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/SearchBar")
    preferences.SetBool("EnableToolbars", False)
    App.saveParameter()
except Exception:
    pass

# Check if there is a layout folder with default layouts
LayoutDir = os.path.join(ConfigDirectory, "Layouts", "Default")
if os.path.exists(LayoutDir) is False:
    # Create the directories
    os.makedirs(LayoutDir)
    # open "CreateStructure.txt" and create files for each workbench
    ribbonStructure = os.path.join(os.path.dirname(FCBinding.__file__), "CreateStructure.txt")
    structure = {}
    with open(ribbonStructure, "r") as file:
        structure.update(json.load(file))
    
    for workbench in structure["workbenches"]:
        # Define a file
        workbenchFile = os.path.join(LayoutDir, f"{workbench}.json")
        # Fill the dict
        workbenchDict = structure["workbenches"][workbench]        
        # Writing to file
        with open(workbenchFile, "w") as outfile:
            json.dump(workbenchDict, outfile, indent=4)

try:   
    print(translate("FreeCAD Ribbon", "Activating Ribbon UI..."))
    # # Set the wait cursor
    # QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

    if Parameters.HIDE_TITLEBAR_FC is False:
        mw.setWindowFlags(Qt.WindowType.WindowFullscreenButtonHint)
        mw.workbenchActivated.connect(FCBinding.run)
        # Set the mainwindow to the last state
        if Parameters_Ribbon.Settings.GetStringSetting("MainWindow") == "Maximized":
            mw.showMaximized()
        # Restore the cursor
        QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

    # Hide the Titlebar of FreeCAD
    if Parameters.HIDE_TITLEBAR_FC is True:
        # make a customized toolbar and hide all the buttons.
        # This works better than a frameless window
        mw.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        mw.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, False)
        mw.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        # Connect the ribbon when the workbench is activated
        mw.workbenchActivated.connect(FCBinding.run)
        # Set the mainwindow to the last state
        if Parameters_Ribbon.Settings.GetStringSetting("MainWindow") == "Maximized":
            mw.showMaximized()
        # Normally after setting the window frameless you show the window with mw.show()
        # This is now done in FCBinding with an eventfilter class
        print(translate("FreeCAD Ribbon", "Ribbon UI: FreeCAD loaded without titlebar"))
        # Restore the cursor
        QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
       
    Ribbon = mw.findChild(QDockWidget, "Ribbon")
    Ribbon.show()
            
except Exception as e:
    # raise e
    if Parameters.DEBUG_MODE is True:
        print(f"{e.with_traceback(e.__traceback__)}, 0")

Gui.addLanguagePath(os.path.join(os.path.dirname(FCBinding.__file__), "translations"))
Gui.updateLocale()


