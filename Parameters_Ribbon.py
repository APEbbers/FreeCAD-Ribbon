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

    def WriteSettings():
        Settings.SetIntSetting("IconSize_Small", ICON_SIZE_SMALL)
        Settings.SetIntSetting("IconSize_Medium", ICON_SIZE_MEDIUM)
        Settings.SetIntSetting("IconSize_Large", ICON_SIZE_LARGE)
        Settings.SetIntSetting("ApplicationButtonSize", APP_ICON_SIZE)
        Settings.SetIntSetting("QuickAccessButtonSize", QUICK_ICON_SIZE)
        Settings.SetIntSetting("TabBarSize", TABBAR_SIZE)
        Settings.SetIntSetting("RightToolbarButtonSize", RIGHT_ICON_SIZE)
        Settings.SetBoolSetting("ShowOnHover", SHOW_ON_HOVER)
        Settings.SetIntSetting("TabBar_Scroll", TABBAR_SCROLLSPEED)
        Settings.SetIntSetting("Ribbon_Scroll", RIBBON_SCROLLSPEED)
        Settings.SetIntSetting("TabBar_Click", TABBAR_CLICKSPEED)
        Settings.SetIntSetting("Ribbon_Click", RIBBON_CLICKSPEED)


# region - Define the Ribbon structure location ------------------------------------------------------------------------
if Settings.GetStringSetting("RibbonStructure") != "":
    RIBBON_STRUCTURE_JSON = Settings.GetStringSetting("RibbonStructure")
else:
    RIBBON_STRUCTURE_JSON = os.path.join(os.path.dirname(__file__), "RibbonStructure.json")
    Settings.SetStringSetting("RibbonStructure", RIBBON_STRUCTURE_JSON)
# endregion ------------------------------------------------------------------------------------------------------------

# region - Define the resources
ICON_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "icons")
STYLESHEET_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "stylesheets")
UI_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "ui")
# endregion ------------------------------------------------------------------------------------------------------------

# region - Define the icon sizes ---------------------------------------------------------------------------------------
ICON_SIZE_SMALL = Settings.GetIntSetting("IconSize_Small")
if Settings.GetIntSetting("IconSize_Small") is None or Settings.GetIntSetting("IconSize_Small") == 0:
    ICON_SIZE_SMALL = int(30)
    Settings.SetIntSetting("IconSize_Small", 30)

ICON_SIZE_MEDIUM = Settings.GetIntSetting("IconSize_Medium")
if Settings.GetIntSetting("IconSize_Medium") is None or Settings.GetIntSetting("IconSize_Medium") == 0:
    ICON_SIZE_MEDIUM = int(40)
    Settings.SetIntSetting("IconSize_Medium", 40)

ICON_SIZE_LARGE = Settings.GetIntSetting("IconSize_Large")
if Settings.GetIntSetting("IconSize_Large") is None or Settings.GetIntSetting("IconSize_Large") == 0:
    ICON_SIZE_LARGE = int(200)
    Settings.SetIntSetting("IconSize_Large", 200)

APP_ICON_SIZE = Settings.GetIntSetting("ApplicationButtonSize")
if Settings.GetIntSetting("ApplicationButtonSize") is None or Settings.GetIntSetting("ApplicationButtonSize") == 0:
    APP_ICON_SIZE = int(60)
    Settings.SetIntSetting("ApplicationButtonSize", APP_ICON_SIZE)

QUICK_ICON_SIZE = Settings.GetIntSetting("QuickAccessButtonSize")
if Settings.GetIntSetting("QuickAccessButtonSize") is None or Settings.GetIntSetting("QuickAccessButtonSize") == 0:
    QUICK_ICON_SIZE = int(30)
    Settings.SetIntSetting("QuickAccessButtonSize", QUICK_ICON_SIZE)

TABBAR_SIZE = Settings.GetIntSetting("TabBarSize")
if Settings.GetIntSetting("TabBarSize") is None or Settings.GetIntSetting("TabBarSize") == 0:
    TABBAR_SIZE = int(30)
    Settings.SetIntSetting("TabBarSize", TABBAR_SIZE)

RIGHT_ICON_SIZE = Settings.GetIntSetting("RightToolbarButtonSize")
if Settings.GetIntSetting("RightToolbarButtonSize") is None or Settings.GetIntSetting("RightToolbarButtonSize") == 0:
    RIGHT_ICON_SIZE = int(30)
    Settings.SetIntSetting("RightToolbarButtonSize", RIGHT_ICON_SIZE)
# endregion ------------------------------------------------------------------------------------------------------------

# region - Backup parameters -------------------------------------------------------------------------------------------
ENABLE_BACKUP = Settings.GetBoolSetting("BackupEnabled")

BACKUP_LOCATION = Settings.GetStringSetting("BackupFolder")
if Settings.GetStringSetting("BackupFolder") == "":
    BACKUP_LOCATION = os.path.dirname(__file__) + "/Backups"
    Settings.SetStringSetting("BackupFolder", BACKUP_LOCATION)
# endregion ------------------------------------------------------------------------------------------------------------

# region - Ribbon settings ---------------------------------------------------------------------------------------------
TAB_ORDER = Settings.GetStringSetting("TabOrder")
if Settings.GetStringSetting("TabOrder") == "":
    WorkbenchOrderParam = "User parameter:BaseApp/Preferences/Workbenches/"
    TAB_ORDER = App.ParamGet(WorkbenchOrderParam).GetString("Ordered")
    Settings.SetStringSetting("TabOrder", TAB_ORDER)

AUTOHIDE_RIBBON = Settings.GetBoolSetting("AutoHideRibbon")
if Settings.GetBoolSetting("AutoHideRibbon") is None:
    AUTOHIDE_RIBBON = bool(False)

STYLESHEET = Settings.GetStringSetting("Stylesheet")
if Settings.GetStringSetting("Stylesheet") == "":
    if int(App.Version()[0]) == 0 and int(App.Version()[1]) <= 21:
        STYLESHEET = os.path.join(STYLESHEET_LOCATION, "default_0.21.qss")
    else:
        STYLESHEET = os.path.join(STYLESHEET_LOCATION, "default.qss")
    Settings.SetStringSetting("Stylesheet", STYLESHEET)

SHOW_ICON_TEXT_SMALL = Settings.GetBoolSetting("ShowIconText_Small")
if Settings.GetBoolSetting("ShowIconText_Small") is None:
    SHOW_ICON_TEXT_SMALL = bool(False)
    Settings.SetBoolSetting("ShowIconText_Small", False)

SHOW_ICON_TEXT_MEDIUM = Settings.GetBoolSetting("ShowIconText_Medium")
if Settings.GetBoolSetting("ShowIconText_Medium") is None:
    SHOW_ICON_TEXT_MEDIUM = bool(False)
    Settings.SetBoolSetting("ShowIconText_Medium", False)

SHOW_ICON_TEXT_LARGE = Settings.GetBoolSetting("ShowIconText_Large")
if Settings.GetBoolSetting("ShowIconText_Large") is None:
    SHOW_ICON_TEXT_LARGE = bool(False)
    Settings.SetBoolSetting("ShowIconText_Large", False)

SHOW_ICON_TEXT_LARGE = Settings.GetBoolSetting("ShowIconText_Large")
if Settings.GetBoolSetting("ShowIconText_Large") is None:
    SHOW_ICON_TEXT_LARGE = bool(False)
    Settings.SetBoolSetting("ShowIconText_Large", False)

MAX_COLUMN_PANELS = Settings.GetIntSetting("MaxColumnsPerPanel")
if Settings.GetIntSetting("MaxColumnsPerPanel") is None:
    MAX_COLUMN_PANELS = int(6)
    Settings.SetIntSetting("MaxColumnsPerPanel", MAX_COLUMN_PANELS)
# endregion ------------------------------------------------------------------------------------------------------------

# region - Get the Debug Mode ------------------------------------------------------------------------------------------
DEBUG_MODE = Settings.GetBoolSetting("DebugMode")
if Settings.GetBoolSetting("DebugMode") is None:
    DEBUG_MODE = False
    Settings.SetBoolSetting("DebugMode", False)
# endregion ------------------------------------------------------------------------------------------------------------

# region - Navigation settings -----------------------------------------------------------------------------------------
SHOW_ON_HOVER = Settings.GetBoolSetting("ShowOnHover")
if Settings.GetBoolSetting("ShowOnHover") is None:
    SHOW_ON_HOVER = False
    Settings.SetBoolSetting("ShowOnHover", False)

TABBAR_SCROLLSPEED = Settings.GetIntSetting("TabBar_Scroll")
if Settings.GetIntSetting("TabBar_Scroll") is None or Settings.GetIntSetting("TabBar_Scroll") == 0:
    TABBAR_SCROLLSPEED = int(1)
    Settings.SetIntSetting("TabBar_Scroll", TABBAR_SCROLLSPEED)

RIBBON_SCROLLSPEED = Settings.GetIntSetting("Ribbon_Scroll")
if Settings.GetIntSetting("Ribbon_Scroll") is None or Settings.GetIntSetting("Ribbon_Scroll") == 0:
    RIBBON_SCROLLSPEED = int(1)
    Settings.SetIntSetting("Ribbon_Scroll", RIBBON_SCROLLSPEED)

TABBAR_CLICKSPEED = Settings.GetIntSetting("TabBar_Click")
if Settings.GetIntSetting("TabBar_Click") is None or Settings.GetIntSetting("TabBar_Click") == 0:
    TABBAR_CLICKSPEED = int(1)
    Settings.SetIntSetting("TabBar_Click", TABBAR_CLICKSPEED)

RIBBON_CLICKSPEED = Settings.GetIntSetting("Ribbon_Click")
if Settings.GetIntSetting("Ribbon_Click") is None or Settings.GetIntSetting("Ribbon_Click") == 0:
    RIBBON_CLICKSPEED = int(1)
    Settings.SetIntSetting("Ribbon_Click", RIBBON_CLICKSPEED)
# endregion ------------------------------------------------------------------------------------------------------------
