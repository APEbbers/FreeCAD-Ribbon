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
from PySide.QtGui import QColor
import os
import sys

# Define the translation
translate = App.Qt.translate

preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/FreeCAD-Ribbon")


class Settings:

    # region -- Functions to read the settings from the FreeCAD Parameters
    # and make sure that a None type result is ""
    def GetStringSetting(settingName: str) -> str:
        result = preferences.GetString(settingName)

        if result.lower() == "none":
            result = ""
        return result

    def GetIntSetting(settingName: str) -> int:
        result = preferences.GetInt(settingName)
        if result == "":
            result = None
        return result

    def GetFloatSetting(settingName: str) -> int:
        result = preferences.GetFloat(settingName)
        if result == "":
            result = None
        return result

    def GetBoolSetting(settingName: str) -> bool:
        result = preferences.GetBool(settingName)
        if str(result).lower() == "none":
            result = False
        return result

    def GetColorSetting(settingName: str) -> object:
        # Create a tuple from the int value of the color
        result = QColor.fromRgba(preferences.GetUnsigned(settingName)).toTuple()

        # correct the order of the tuple and divide them by 255
        result = (result[3] / 255, result[0] / 255, result[1] / 255, result[2] / 255)

        return result

    # endregion

    # region - Functions to write settings to the FreeCAD Parameters
    #
    #
    def SetStringSetting(settingName: str, value: str):
        if value.lower() == "none":
            value = ""
        preferences.SetString(settingName, value)
        return

    def SetBoolSetting(settingName: str, value):
        if str(value).lower() == "true":
            Bool = True
        if str(value).lower() == "none" or str(value).lower() != "true":
            Bool = False
        preferences.SetBool(settingName, Bool)
        return

    def SetIntSetting(settingName: str, value: int):
        if str(value).lower() != "":
            preferences.SetInt(settingName, value)
        return

    # endregion


# Define the Ribbon structure location
if Settings.GetStringSetting("RibbonStructureJson") != "":
    RIBBON_STRUCTURE_JSON = Settings.GetStringSetting("RibbonStructureJson")
else:
    RIBBON_STRUCTURE_JSON = os.path.join(os.path.dirname(__file__), "RibbonStructure.json")
    Settings.SetStringSetting("RibbonStructure.json", RIBBON_STRUCTURE_JSON)

# Define the resources
ICON_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "icons")
STYLESHEET_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "stylesheets")
UI_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "ui")

# Define the icon sizes
if Settings.GetIntSetting("IconSize_Small") is not None or Settings.GetIntSetting("IconSize_Small") > 0:
    ICON_SIZE_SMALL = Settings.GetIntSetting("IconSize_Small")
else:
    ICON_SIZE_SMALL = int(30)
    Settings.SetIntSetting("IconSize_Small", 30)

if Settings.GetIntSetting("IconSize_Medium") is not None or Settings.GetIntSetting("IconSize_Medium") > 0:
    ICON_SIZE_MEDIUM = Settings.GetIntSetting("IconSize_Medium")
else:
    ICON_SIZE_MEDIUM = int(40)
    Settings.SetIntSetting("IconSize_Medium", 40)

if Settings.GetIntSetting("IconSize_Large") is not None or Settings.GetIntSetting("IconSize_Large") > 0:
    ICON_SIZE_LARGE = Settings.GetIntSetting("IconSize_Large")
else:
    ICON_SIZE_LARGE = int(50)
    Settings.SetIntSetting("IconSize_Large", 50)

# Backup parameters
ENABLE_BACKUP = Settings.GetBoolSetting("BackupEnabled")

if Settings.GetStringSetting("BackupFolder") != "":
    BACKUP_LOCATION = Settings.GetStringSetting("BackupFolder")
else:
    BACKUP_LOCATION = os.path.dirname(__file__) + "/Backups"
    Settings.SetStringSetting("BackupFolder", BACKUP_LOCATION)

# Ribbon settings
if Settings.GetStringSetting("TabOrder") != "":
    TAB_ORDER = Settings.GetStringSetting("TabOrder")
else:
    WorkbenchOrderParam = "User parameter:BaseApp/Preferences/Workbenches/"
    TAB_ORDER = App.ParamGet(WorkbenchOrderParam).GetString("Ordered")
    Settings.SetStringSetting("TabOrder", TAB_ORDER)

if Settings.GetBoolSetting("AutoHideRibbon") is True:
    AUTOHIDE_RIBBON = Settings.GetBoolSetting("AutoHideRibbon")
else:
    AUTOHIDE_RIBBON = bool(False)
if Settings.GetStringSetting("Stylesheet") != "":
    STYLESHEET = Settings.GetStringSetting("Stylesheet")
else:
    if int(App.Version()[0]) == 0 and int(App.Version()[1]) <= 21:
        STYLESHEET = os.path.join(STYLESHEET_LOCATION, "default_0.21.qss")
    else:
        STYLESHEET = os.path.join(STYLESHEET_LOCATION, "default.qss")
    Settings.SetStringSetting("Stylesheet", STYLESHEET)

if Settings.GetBoolSetting("ShowIconText_Small") is True:
    SHOW_ICON_TEXT_SMALL = Settings.GetBoolSetting("ShowIconText_Small")
else:
    SHOW_ICON_TEXT_SMALL = bool(False)
    Settings.SetBoolSetting("ShowIconText_Small", False)

if Settings.GetBoolSetting("ShowIconText_Medium") is True:
    SHOW_ICON_TEXT_MEDIUM = Settings.GetBoolSetting("ShowIconText_Medium")
else:
    SHOW_ICON_TEXT_MEDIUM = bool(False)
    Settings.SetBoolSetting("ShowIconText_Medium", False)

if Settings.GetBoolSetting("ShowIconText_Large") is True:
    SHOW_ICON_TEXT_LARGE = Settings.GetBoolSetting("ShowIconText_Large")
else:
    SHOW_ICON_TEXT_LARGE = bool(False)
    Settings.SetBoolSetting("ShowIconText_Large", False)

if Settings.GetIntSetting("MaxColumnsPerPanel") is not None or Settings.GetIntSetting("MaxColumnsPerPanel") > 0:
    MAX_COLUMN_PANELS = Settings.GetIntSetting("MaxColumnsPerPanel")
else:
    MAX_COLUMN_PANELS = int(6)
    Settings.SetIntSetting("MaxColumnsPerPanel", MAX_COLUMN_PANELS)

# Get the Debug Mode
if Settings.GetBoolSetting("DebugMode") is True:
    DEBUG_MODE = Settings.GetBoolSetting("DebugMode")
else:
    DEBUG_MODE = False
    Settings.SetBoolSetting("DebugMode", False)
