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
import Standard_Functions_Ribbon as StandardFunctions

# Define the translation
translate = App.Qt.translate

preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/FreeCAD-Ribbon")

class Settings:

    # region -- Functions to read the settings from the FreeCAD Parameters
    # and make sure that a None type result is ""
    def GetStringSetting(settingName) -> str:
        result = preferences.GetString(settingName)

        if result.lower() == "none":
            result = ""
        return str(result)

    def GetIntSetting(settingName) -> int:
        result = preferences.GetInt(settingName)
        if result == "":
            result = None
        return int(result)

    def GetFloatSetting(settingName) -> float:
        result = preferences.GetFloat(settingName)
        if result == "":
            result = None
        return float(result)

    def GetBoolSetting(settingName) -> bool:
        result = None
        settings = preferences.GetContents()
        exists = False
        for setting in settings:
            if setting[0] == "Boolean" and setting[1] == settingName:
                exists = True
                break
        if exists is True:
            result = preferences.GetBool(settingName)
        return bool(result)

    def GetColorSetting(self, settingName: str) -> object:
        # Create a tuple from the int value of the color
        result = QColor.fromRgba(preferences.GetUnsigned(settingName)).toTuple()

        # correct the order of the tuple and divide them by 255
        result = (result[3] / 255, result[0] / 255, result[1] / 255, result[2] / 255)

        return tuple(result)

    # endregion

    # region - Functions to write settings to the FreeCAD Parameters
    #
    #
    def SetStringSetting(settingName, value: str):
        if value.lower() == "none":
            value = ""
        if value == "":
            value = Parameters.DefaultSettings[
                settingName
            ]  # pyright: ignore[reportAssignmentType]
        preferences.SetString(settingName, value)
        App.saveParameter()
        return

    def SetBoolSetting(settingName, value: bool):
        preferences.SetBool(settingName, value)
        App.saveParameter()
        return

    def SetIntSetting(settingName, value: int):
        if str(value).lower() == "":
            value = int(Parameters.DefaultSettings[settingName])
        if str(value).lower() != "":
            preferences.SetInt(settingName, value)
        App.saveParameter()
        return
    
    def SetFloatSetting(settingName, value: float):
        if str(value).lower() == "":
            value = float(Parameters.DefaultSettings[settingName])
        if str(value).lower() != "":
            preferences.SetFloat(settingName, value)
        App.saveParameter()
        return

    # endregion

    def WriteMissingSettings():
        # Get the current settings
        CurrentSettings: list = preferences.GetContents()
        
        for key, value in Parameters.DefaultSettings.items():
            IsPresent = False
            for item in CurrentSettings:
                if item[1] == key:
                    IsPresent = True

            if IsPresent is False:
                if type(value) is str:
                    Settings.SetStringSetting(key, value)
                if type(value) is bool:
                    Settings.SetBoolSetting(key, value)
                if type(value) is int:
                    Settings.SetIntSetting(key, value)
                if type(value) is float:
                    Settings.SetFloatSetting(key, value)
                    
                for name, value2 in vars(Parameters).items():
                    if value == value2:
                        Parameters.__dict__[name] = value
        return


class Parameters:
    # region - The FreeCAD version to check
    FreeCAD_Version = {
        "mainVersion": 1,
        "subVersion": 1,
        "patchVersion": 0,
        "gitVersion": 14555,
    }
    # endregion



    # region - Define the resources ----------------------------------------------------------------------------------------
    ICON_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "icons")
    STYLESHEET_LOCATION = os.path.join(
        os.path.dirname(__file__), "Resources", "stylesheets"
    )
    UI_LOCATION = os.path.join(os.path.dirname(__file__), "Resources", "ui")
    # endregion ------------------------------------------------------------------------------------------------------------

    DefaultSettings = {
        "ConfigDir":os.path.join(App.getUserAppDataDir(), "RibbonUI_Data"),
        "ImportLocation": os.path.join(App.getUserAppDataDir(), "RibbonUI_Data", ""),
        "ExportLocation": os.path.join(App.getUserAppDataDir(), "RibbonUI_Data", ""),
        "RibbonStructure": os.path.join(App.getUserAppDataDir(), "RibbonUI_Data", "RibbonStructure.json"),
        "TabBar_Style": int(0),
        "Link_IconSizes": bool(True),
        "IconSize_Small": int(24),
        "IconSize_Medium": int(36),
        "IconSize_Large": int(72),
        "ApplicationButtonSize": int(40),
        "QuickAccessButtonSize": int(24),
        "TabBarSize": int(24),
        "RightToolbarButtonSize": int(24),
        "BackupEnabled": bool(True),
        "BackupFolder": os.path.join(App.getUserAppDataDir(), "RibbonUI_Data", "Backups"),
        "TabOrder": App.ParamGet(
            "User parameter:BaseApp/Preferences/Workbenches/"
        ).GetString("Ordered"),
        "AutoHideRibbon": bool(False),
        "Stylesheet": os.path.join(os.path.join(STYLESHEET_LOCATION, "default.qss")),
        "ShowIconText_Small": bool(False),
        "ShowIconText_Medium": bool(False),
        "ShowIconText_Large": bool(True),
        "MaxColumnsPerPanel": int(6),
        "DebugMode": bool(False),
        "ShowOnHover": bool(False),
        "TabBar_Scroll": int(1),
        "Ribbon_Scroll": int(1),
        "TabBar_Click": int(1),
        "Ribbon_Click": int(1),
        "Preferred_view": int(2),
        "UseToolsPanel": bool(True),
        "WrapText_Medium": bool(True),
        "WrapText_Large": bool(True),
        "UseOverlay": bool(True),
        "UseFCOverlay": bool(False),
        "UseButtonBackGround": bool(False),
        "CustomColors": bool(False),
        "BorderTransparant": bool(True),
        "Color_Borders": "",
        # "Color_Background": "",
        "Color_Background_Hover": "",
        "Color_Background_App": "",
        "CustomIcons": bool(False),
        "ScrollLeftButton_Tab": "",
        "ScrollRightButton_Tab": "",
        "ScrollLeftButton_Category": "",
        "ScrollRightButton_Category": "",
        "OptionButton": "",
        "PinButton_open": "",
        "PinButton_closed": "",
        "Shortcut_Application": "Alt+A",
        "CustomPanelPosition": "Right",
        "FontSize_Menus": int(11),
        "FontSize_Buttons": int(11),
        "FontSize_Tabs": int(14),
        "FontSize_Panels": int(11),
        "Toolbar_Position": int(0),
        "Hide_Titlebar_FC": bool(True),
        "BetaFunctions": bool(False),
        "SizeFactor": float(1.3),
        "PanelHeightOffset": int(26),
        "RibbonHeightOffset": int(20),
        "RibbonMinimumHeight": int(16),
        "ButtonSpacing": int(6),
    }

    # Get the install location of FreeCAD
    AppDir = os.path.join(App.getUserAppDataDir().split('FreeCAD')[0], "FreeCAD")
    OldModDir = os.path.join(AppDir, "Mod")
    CurrentModDir = os.path.join(App.getUserAppDataDir(), "Mod")

    # region - Define the import location ----------------------------------------------------------------------------------
    CONFIG_DIR = Settings.GetStringSetting("ConfigDir")
    if CONFIG_DIR == ""  or os.path.isfile(CONFIG_DIR) is False:
        CONFIG_DIR = str(DefaultSettings["ConfigDir"])
        Settings.SetStringSetting("ConfigDir", CONFIG_DIR)
        
    # endregion ------------------------------------------------------------------------------------------------------------


    # region - Define the import location ----------------------------------------------------------------------------------
    IMPORT_LOCATION = Settings.GetStringSetting("ImportLocation")
    if IMPORT_LOCATION == ""  or os.path.isfile(IMPORT_LOCATION) is False:
        IMPORT_LOCATION = str(DefaultSettings["ImportLocation"])
        Settings.SetStringSetting("ImportLocation", IMPORT_LOCATION)
        Settings.SetStringSetting("AddonDir", os.path.dirname(__file__))
        
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Define the export location ----------------------------------------------------------------------------------
    EXPORT_LOCATION = Settings.GetStringSetting("ExportLocation")
    if EXPORT_LOCATION == "" or os.path.isfile(EXPORT_LOCATION) is False:
        EXPORT_LOCATION = str(DefaultSettings["ExportLocation"])
        Settings.SetStringSetting("exportLocation", EXPORT_LOCATION)
        Settings.SetStringSetting("AddonDir", os.path.dirname(__file__))
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Define the Ribbon structure location ------------------------------------------------------------------------
    # The location for the ribbon structure is retrieved from parameters as standard.
    RIBBON_STRUCTURE_JSON = Settings.GetStringSetting("RibbonStructure")
    if RIBBON_STRUCTURE_JSON == "":
        RIBBON_STRUCTURE_JSON = str(DefaultSettings["RibbonStructure"])
        Settings.SetStringSetting("RibbonStructure", RIBBON_STRUCTURE_JSON)
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Define the default position for global panels ---------------------------------------------------------------
    DEFAULT_PANEL_POSITION_CUSTOM = Settings.GetStringSetting("CustomPanelPosition")
    if DEFAULT_PANEL_POSITION_CUSTOM == "":
        DEFAULT_PANEL_POSITION_CUSTOM = str(DefaultSettings["CustomPanelPosition"])
        Settings.SetStringSetting("CustomPanelPosition", DEFAULT_PANEL_POSITION_CUSTOM)
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Define the tabbar style -------------------------------------------------------------------------------------
    if (
        Settings.GetIntSetting("TabBar_Style") is None
        or Settings.GetIntSetting("TabBar_Style") > 2
    ):
        TABBAR_STYLE = int(DefaultSettings["TabBar_Style"])
        Settings.SetIntSetting("TabBar_Style", TABBAR_STYLE)
    TABBAR_STYLE = Settings.GetIntSetting("TabBar_Style")

    if (
        Settings.GetIntSetting("Toolbar_Position") is None
        or Settings.GetIntSetting("Toolbar_Position") > 1
    ):
        TOOLBAR_POSITION = int(DefaultSettings["Toolbar_Position"])
        Settings.SetIntSetting("Toolbar_Position", TOOLBAR_POSITION)
    TOOLBAR_POSITION = Settings.GetIntSetting("Toolbar_Position")

    if Settings.GetBoolSetting("Hide_Titlebar_FC") is None:
        HIDE_TITLEBAR_FC = bool(DefaultSettings["Hide_Titlebar_FC"])
        Settings.SetBoolSetting("Hide_Titlebar_FC", HIDE_TITLEBAR_FC)
    HIDE_TITLEBAR_FC = Settings.GetBoolSetting("Hide_Titlebar_FC")
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Define the icon sizes ---------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("Link_IconSizes") is None:
        LINK_ICON_SIZES = bool(DefaultSettings["Link_IconSizes"])
        Settings.SetBoolSetting("Link_IconSizes", LINK_ICON_SIZES)
    LINK_ICON_SIZES = Settings.GetBoolSetting("Link_IconSizes")

    if (
        Settings.GetIntSetting("IconSize_Small") is None
        or Settings.GetIntSetting("IconSize_Small") == 0
    ):
        ICON_SIZE_SMALL = int(DefaultSettings["IconSize_Small"])
        Settings.SetIntSetting("IconSize_Small", ICON_SIZE_SMALL)
    ICON_SIZE_SMALL = Settings.GetIntSetting("IconSize_Small")

    if (
        Settings.GetIntSetting("IconSize_Medium") is None
        or Settings.GetIntSetting("IconSize_Medium") == 0
    ):
        ICON_SIZE_MEDIUM = int(DefaultSettings["IconSize_Medium"])
        Settings.SetIntSetting("IconSize_Medium", ICON_SIZE_MEDIUM)
    ICON_SIZE_MEDIUM = Settings.GetIntSetting("IconSize_Medium")

    if (
        Settings.GetIntSetting("IconSize_Large") is None
        or Settings.GetIntSetting("IconSize_Large") == 0
    ):
        ICON_SIZE_LARGE = int(DefaultSettings["IconSize_Large"])
        Settings.SetIntSetting("IconSize_Large", ICON_SIZE_SMALL)
    ICON_SIZE_LARGE = Settings.GetIntSetting("IconSize_Large")

    if (
        Settings.GetIntSetting("ApplicationButtonSize") is None
        or Settings.GetIntSetting("ApplicationButtonSize") == 0
    ):
        APP_ICON_SIZE = int(DefaultSettings["ApplicationButtonSize"])
        Settings.SetIntSetting("ApplicationButtonSize", APP_ICON_SIZE)
    APP_ICON_SIZE = Settings.GetIntSetting("ApplicationButtonSize")

    if (
        Settings.GetIntSetting("QuickAccessButtonSize") is None
        or Settings.GetIntSetting("QuickAccessButtonSize") == 0
    ):
        QUICK_ICON_SIZE = int(DefaultSettings["QuickAccessButtonSize"])
        Settings.SetIntSetting("QuickAccessButtonSize", QUICK_ICON_SIZE)
    QUICK_ICON_SIZE = Settings.GetIntSetting("QuickAccessButtonSize")

    if (
        Settings.GetIntSetting("TabBarSize") is None
        or Settings.GetIntSetting("TabBarSize") == 0
    ):
        TABBAR_SIZE = int(DefaultSettings["TabBarSize"])
        Settings.SetIntSetting("TabBarSize", TABBAR_SIZE)
    TABBAR_SIZE = Settings.GetIntSetting("TabBarSize")

    if (
        Settings.GetIntSetting("RightToolbarButtonSize") is None
        or Settings.GetIntSetting("RightToolbarButtonSize") == 0
    ):
        RIGHT_ICON_SIZE = int(DefaultSettings["RightToolbarButtonSize"])
        Settings.SetIntSetting("RightToolbarButtonSize", RIGHT_ICON_SIZE)
    RIGHT_ICON_SIZE = Settings.GetIntSetting("RightToolbarButtonSize")
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Backup parameters -------------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("BackupEnabled") is None:
        ENABLE_BACKUP = bool(DefaultSettings["BackupEnabled"])
        Settings.SetBoolSetting("BackupEnabled", ENABLE_BACKUP)
    ENABLE_BACKUP = Settings.GetBoolSetting("BackupEnabled")

    if Settings.GetStringSetting("BackupFolder") == "":
        BACKUP_LOCATION = str(DefaultSettings["BackupFolder"])
        Settings.SetStringSetting("BackupFolder", BACKUP_LOCATION)
    BACKUP_LOCATION = Settings.GetStringSetting("BackupFolder")
    if os.path.isfile(BACKUP_LOCATION) is False:
        BACKUP_LOCATION = str(DefaultSettings["BackupFolder"])
        Settings.SetStringSetting("BackupFolder", BACKUP_LOCATION)
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Ribbon settings ---------------------------------------------------------------------------------------------
    WorkbenchOrderParam = "User parameter:BaseApp/Preferences/Workbenches/"
    TAB_ORDER = str(App.ParamGet(WorkbenchOrderParam).GetString("Ordered"))
    Settings.SetStringSetting("TabOrder", TAB_ORDER)

    if Settings.GetBoolSetting("AutoHideRibbon") is None:
        AUTOHIDE_RIBBON = bool(False)
    AUTOHIDE_RIBBON: bool = Settings.GetBoolSetting("AutoHideRibbon")

    if Settings.GetStringSetting("Stylesheet") == "":
        STYLESHEET = str(DefaultSettings["Stylesheet"])
        Settings.SetStringSetting("Stylesheet", STYLESHEET)
    STYLESHEET = Settings.GetStringSetting("Stylesheet")
    if os.path.isfile(STYLESHEET) is False:
        STYLESHEET = str(DefaultSettings["Stylesheet"])
        Settings.SetStringSetting("Stylesheet", STYLESHEET)

    if Settings.GetBoolSetting("ShowIconText_Small") is FileExistsError:
        SHOW_ICON_TEXT_SMALL = bool(DefaultSettings["ShowIconText_Small"])
        Settings.SetBoolSetting("ShowIconText_Small", SHOW_ICON_TEXT_SMALL)
    SHOW_ICON_TEXT_SMALL = Settings.GetBoolSetting("ShowIconText_Small")

    if Settings.GetBoolSetting("ShowIconText_Medium") is None:
        SHOW_ICON_TEXT_MEDIUM = bool(DefaultSettings["ShowIconText_Medium"])
        Settings.SetBoolSetting("ShowIconText_Medium", SHOW_ICON_TEXT_MEDIUM)
    SHOW_ICON_TEXT_MEDIUM = Settings.GetBoolSetting("ShowIconText_Medium")

    if Settings.GetBoolSetting("ShowIconText_Large") is None:
        SHOW_ICON_TEXT_LARGE = bool(DefaultSettings["ShowIconText_Large"])
        Settings.SetBoolSetting("ShowIconText_Large", SHOW_ICON_TEXT_LARGE)
    SHOW_ICON_TEXT_LARGE = Settings.GetBoolSetting("ShowIconText_Large")

    if Settings.GetIntSetting("MaxColumnsPerPanel") is None:
        MAX_COLUMN_PANELS = int(DefaultSettings["MaxColumnsPerPanel"])
        Settings.SetIntSetting("MaxColumnsPerPanel", MAX_COLUMN_PANELS)
    MAX_COLUMN_PANELS = Settings.GetIntSetting("MaxColumnsPerPanel")

    if Settings.GetBoolSetting("WrapText_Medium") == "":
        WRAPTEXT_MEDIUM = bool(DefaultSettings["WrapText_Medium"])
        Settings.SetBoolSetting("WrapText_Medium", WRAPTEXT_MEDIUM)
    WRAPTEXT_MEDIUM = Settings.GetBoolSetting("WrapText_Medium")

    if Settings.GetBoolSetting("WrapText_Large") == "":
        WRAPTEXT_LARGE = bool(DefaultSettings["WrapText_Large"])
        Settings.SetBoolSetting("WrapText_Large", WRAPTEXT_LARGE)
    WRAPTEXT_LARGE = Settings.GetBoolSetting("WrapText_Large")

    if (
        Settings.GetIntSetting("FontSize_Menus") is None
        or Settings.GetIntSetting("FontSize_Menus") == 0
    ):
        FONTSIZE_MENUS = int(DefaultSettings["FontSize_Menus"])
        Settings.SetIntSetting("FontSize_Menus", FONTSIZE_MENUS)
    FONTSIZE_MENUS = Settings.GetIntSetting("FontSize_Menus")

    if (
        Settings.GetIntSetting("FontSize_Buttons") is None
        or Settings.GetIntSetting("FontSize_Buttons") == 0
    ):
        FONTSIZE_BUTTONS = int(DefaultSettings["FontSize_Buttons"])
        Settings.SetIntSetting("FontSize_Buttons", FONTSIZE_BUTTONS)
    FONTSIZE_BUTTONS = Settings.GetIntSetting("FontSize_Buttons")

    if (
        Settings.GetIntSetting("FontSize_Tabs") is None
        or Settings.GetIntSetting("FontSize_Tabs") == 0
    ):
        FONTSIZE_TABS = int(DefaultSettings["FontSize_Tabs"])
        Settings.SetIntSetting("FontSize_Tabs", FONTSIZE_TABS)
    FONTSIZE_TABS = Settings.GetIntSetting("FontSize_Tabs")

    if (
        Settings.GetIntSetting("FontSize_Panels") is None
        or Settings.GetIntSetting("FontSize_Panels") == 0
    ):
        FONTSIZE_PANELS = int(DefaultSettings["FontSize_Panels"])
        Settings.SetIntSetting("FontSize_Panels", FONTSIZE_PANELS)
    FONTSIZE_PANELS = Settings.GetIntSetting("FontSize_Panels")
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Get the Debug Mode ------------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("DebugMode") is None:
        DEBUG_MODE = bool(DefaultSettings["DebugMode"])
        Settings.SetBoolSetting("DebugMode", DEBUG_MODE)
    DEBUG_MODE = Settings.GetBoolSetting("DebugMode")
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Navigation settings -----------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("ShowOnHover") is None:
        SHOW_ON_HOVER = bool(DefaultSettings["ShowOnHover"])
        Settings.SetBoolSetting("ShowOnHover", False)
    SHOW_ON_HOVER = Settings.GetBoolSetting("ShowOnHover")

    if (
        Settings.GetIntSetting("TabBar_Scroll") is None
        or Settings.GetIntSetting("TabBar_Scroll") == 0
    ):
        TABBAR_SCROLLSPEED = int(DefaultSettings["TabBar_Scroll"])
        Settings.SetIntSetting("TabBar_Scroll", TABBAR_SCROLLSPEED)
    TABBAR_SCROLLSPEED = Settings.GetIntSetting("TabBar_Scroll")

    if (
        Settings.GetIntSetting("Ribbon_Scroll") is None
        or Settings.GetIntSetting("Ribbon_Scroll") == 0
    ):
        RIBBON_SCROLLSPEED = int(DefaultSettings["Ribbon_Scroll"])
        Settings.SetIntSetting("Ribbon_Scroll", RIBBON_SCROLLSPEED)
    RIBBON_SCROLLSPEED = Settings.GetIntSetting("Ribbon_Scroll")

    if (
        Settings.GetIntSetting("TabBar_Click") is None
        or Settings.GetIntSetting("TabBar_Click") == 0
    ):
        TABBAR_CLICKSPEED = int(DefaultSettings["TabBar_Click"])
        Settings.SetIntSetting("TabBar_Click", TABBAR_CLICKSPEED)
    TABBAR_CLICKSPEED = Settings.GetIntSetting("TabBar_Click")

    if (
        Settings.GetIntSetting("Ribbon_Click") is None
        or Settings.GetIntSetting("Ribbon_Click") == 0
    ):
        RIBBON_CLICKSPEED = int(DefaultSettings["Ribbon_Click"])
        Settings.SetIntSetting("Ribbon_Click", RIBBON_CLICKSPEED)
    RIBBON_CLICKSPEED = Settings.GetIntSetting("Ribbon_Click")

    if Settings.GetStringSetting("Shortcut_Application") == "":
        SHORTCUT_APPLICATION = str(DefaultSettings["Shortcut_Application"])
        Settings.SetStringSetting("Shortcut_Application", SHORTCUT_APPLICATION)
    SHORTCUT_APPLICATION = Settings.GetStringSetting("Shortcut_Application")

    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Miscellaneous settings --------------------------------------------------------------------------------------
    if (
        Settings.GetIntSetting("Preferred_view") is None
        or Settings.GetIntSetting("Preferred_view") == 0
    ):
        PREFERRED_VIEW = int(DefaultSettings["Preferred_view"])
        Settings.SetIntSetting("Preferred_view", PREFERRED_VIEW)
    PREFERRED_VIEW = Settings.GetIntSetting("Preferred_view")

    if Settings.GetBoolSetting("UseToolsPanel") is None:
        USE_TOOLSPANEL = bool(DefaultSettings["UseToolsPanel"])
        Settings.SetBoolSetting("UseToolsPanel", USE_TOOLSPANEL)
    USE_TOOLSPANEL = Settings.GetBoolSetting("UseToolsPanel")

    if Settings.GetBoolSetting("UseOverlay") is None:
        USE_OVERLAY = bool(DefaultSettings["UseOverlay"])
        Settings.SetBoolSetting("UseOverlay", USE_OVERLAY)
    USE_OVERLAY = Settings.GetBoolSetting("UseOverlay")

    if Settings.GetBoolSetting("UseFCOverlay") is None:
        USE_FC_OVERLAY = bool(DefaultSettings["UseFCOverlay"])
        Settings.SetBoolSetting("UseFCOverlay", USE_FC_OVERLAY)
    USE_FC_OVERLAY = Settings.GetBoolSetting("UseFCOverlay")

    if Settings.GetBoolSetting("UseButtonBackGround") is None:
        BUTTON_BACKGROUND_ENABLED = bool(DefaultSettings["UseButtonBackGround"])
        Settings.SetBoolSetting("UseButtonBackGround", BUTTON_BACKGROUND_ENABLED)
    BUTTON_BACKGROUND_ENABLED = Settings.GetBoolSetting("UseButtonBackGround")
    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Color and icon settings -------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("CustomIcons") is None:
        BETA_FUNCTIONS_ENABLED = bool(DefaultSettings["CustomIcons"])
        Settings.SetBoolSetting("CustomIcons", BETA_FUNCTIONS_ENABLED)
    BETA_FUNCTIONS_ENABLED = Settings.GetBoolSetting("CustomIcons")

    if Settings.GetStringSetting("ScrollLeftButton_Tab") == "":
        SCROLL_LEFT_BUTTON_TAB = str(DefaultSettings["ScrollLeftButton_Tab"])
        Settings.SetStringSetting("ScrollLeftButton_Tab", SCROLL_LEFT_BUTTON_TAB)
    SCROLL_LEFT_BUTTON_TAB = Settings.GetStringSetting("ScrollLeftButton_Tab")

    if Settings.GetStringSetting("ScrollRightButton_Tab") == "":
        SCROLL_RIGHT_BUTTON_TAB = str(DefaultSettings["ScrollRightButton_Tab"])
        Settings.SetStringSetting("ScrollRightButton_Tab", SCROLL_RIGHT_BUTTON_TAB)
    SCROLL_RIGHT_BUTTON_TAB = Settings.GetStringSetting("ScrollRightButton_Tab")

    if Settings.GetStringSetting("ScrollLeftButton_Category") == "":
        SCROLL_LEFT_BUTTON_CATEGORY = str(DefaultSettings["ScrollLeftButton_Category"])
        Settings.SetStringSetting("ScrollLeftButton_Category", SCROLL_LEFT_BUTTON_CATEGORY)
    SCROLL_LEFT_BUTTON_CATEGORY = Settings.GetStringSetting("ScrollLeftButton_Category")

    if Settings.GetStringSetting("ScrollRightButton_Category") == "":
        SCROLL_RIGHT_BUTTON_CATEGORY = str(DefaultSettings["ScrollRightButton_Category"])
        Settings.SetStringSetting(
            "ScrollRightButton_Category", SCROLL_RIGHT_BUTTON_CATEGORY
        )
    SCROLL_RIGHT_BUTTON_CATEGORY = Settings.GetStringSetting("ScrollRightButton_Category")

    if Settings.GetStringSetting("OptionButton") == "":
        OPTION_BUTTON = str(DefaultSettings["OptionButton"])
        Settings.SetStringSetting("OptionButton", OPTION_BUTTON)
    OPTION_BUTTON = Settings.GetStringSetting("OptionButton")

    if Settings.GetStringSetting("PinButton_open") == "":
        PIN_BUTTON_OPEN = str(DefaultSettings["PinButton_open"])
        Settings.SetStringSetting("PinButton_open", PIN_BUTTON_OPEN)
    PIN_BUTTON_OPEN = Settings.GetStringSetting("PinButton_open")

    if Settings.GetStringSetting("PinButton_closed") == "":
        PIN_BUTTON_CLOSED = str(DefaultSettings["PinButton_closed"])
        Settings.SetStringSetting("PinButton_closed", PIN_BUTTON_CLOSED)
    PIN_BUTTON_CLOSED = Settings.GetStringSetting("PinButton_closed")

    if Settings.GetBoolSetting("CustomColors") is None:
        CUSTOM_COLORS_ENABLED = bool(DefaultSettings["CustomColors"])
        Settings.SetBoolSetting("CustomColors", CUSTOM_COLORS_ENABLED)
    CUSTOM_COLORS_ENABLED = Settings.GetBoolSetting("CustomColors")

    if Settings.GetBoolSetting("BorderTransparant") is None:
        BORDER_TRANSPARANT = bool(DefaultSettings["BorderTransparant"])
        Settings.SetBoolSetting("BorderTransparant", BORDER_TRANSPARANT)
    BORDER_TRANSPARANT = Settings.GetBoolSetting("BorderTransparant")

    if Settings.GetStringSetting("Color_Borders") == "":
        COLOR_BORDERS = str(DefaultSettings["Color_Borders"])
        Settings.SetStringSetting("Color_Borders", COLOR_BORDERS)
    COLOR_BORDERS = Settings.GetStringSetting("Color_Borders")

    # if Settings.GetStringSetting("Color_Background") == "":
    #     COLOR_BACKGROUND = str(DefaultSettings["Color_Background"])
    #     Settings.SetStringSetting("Color_Background", COLOR_BACKGROUND)
    # COLOR_BACKGROUND = Settings.GetStringSetting("Color_Background")

    if Settings.GetStringSetting("Color_Background_Hover") == "":
        COLOR_BACKGROUND_HOVER = str(DefaultSettings["Color_Background_Hover"])
        Settings.SetStringSetting("Color_Background_Hover", COLOR_BACKGROUND_HOVER)
    COLOR_BACKGROUND_HOVER = Settings.GetStringSetting("Color_Background_Hover")

    if Settings.GetStringSetting("Color_Background_App") == "":
        COLOR_APPLICATION_BUTTON_BACKGROUND = str(DefaultSettings["Color_Background_App"])
        Settings.SetStringSetting(
            "Color_Background_App", COLOR_APPLICATION_BUTTON_BACKGROUND
        )
    COLOR_APPLICATION_BUTTON_BACKGROUND = Settings.GetStringSetting("Color_Background_App")

    # endregion ------------------------------------------------------------------------------------------------------------

    # region - Context menu ------------------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("BetaFunctions") is None:
        BETA_FUNCTIONS_ENABLED = bool(DefaultSettings["BetaFunctions"])
        Settings.SetBoolSetting("BetaFunctions", BETA_FUNCTIONS_ENABLED)
    BETA_FUNCTIONS_ENABLED = Settings.GetBoolSetting("BetaFunctions")
    # endregion

    # region - Advanced size settings ------------------------------------------------------------------------------------------------
    if Settings.GetBoolSetting("BetaFunctions") is None:
        SIZE_FACTOR = bool(DefaultSettings["SizeFactor"])
        Settings.SetBoolSetting("SizeFactor", SIZE_FACTOR)
    SIZE_FACTOR = Settings.GetBoolSetting("SizeFactor")
        
    if Settings.GetIntSetting("PanelHeightOffset") is None:
        PANEL_HEIGHT_OFFSET = bool(DefaultSettings["PanelHeightOffset"])
        Settings.SetIntSetting("PanelHeightOffset", PANEL_HEIGHT_OFFSET)
    PANEL_HEIGHT_OFFSET = Settings.GetIntSetting("PanelHeightOffset")
        
    if Settings.GetIntSetting("RibbonHeightOffset") is None:
        RIBBON_HEIGHT_OFFSET = bool(DefaultSettings["RibbonHeightOffset"])
        Settings.SetIntSetting("RibbonHeightOffset", RIBBON_HEIGHT_OFFSET)
    RIBBON_HEIGHT_OFFSET = Settings.GetIntSetting("RibbonHeightOffset")
        
    if Settings.GetIntSetting("RibbonMinimumHeight") is None:
        RIBBON_MINIMUM_HEIGHT = bool(DefaultSettings["RibbonMinimumHeight"])
        Settings.SetIntSetting("RibbonMinimumHeight", RIBBON_MINIMUM_HEIGHT)
    RIBBON_MINIMUM_HEIGHT = Settings.GetIntSetting("RibbonMinimumHeight")
        
    if Settings.GetIntSetting("ButtonSpacing") is None:
        BUTTON_SPACING = bool(DefaultSettings["ButtonSpacing"])
        Settings.SetIntSetting("ButtonSpacing", BUTTON_SPACING)
    BUTTON_SPACING = Settings.GetIntSetting("ButtonSpacing")
    # endregion

