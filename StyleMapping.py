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
from PySide.QtGui import QIcon, QPixmap, QAction
from PySide.QtWidgets import (
    QListWidgetItem,
    QTableWidgetItem,
    QListWidget,
    QTableWidget,
    QToolBar,
    QToolButton,
    QComboBox,
    QPushButton,
    QMenu,
    QWidget,
)
from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread
import sys
import json
from datetime import datetime
import shutil
import Standard_Functions_RIbbon as StandardFunctions
import Parameters_Ribbon
import webbrowser
import time

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathBackup)


def ReturnStyleItem(ControlName):
    """
    Enter one of the names below:

    ControlName (string):
        "Background_Color" returns string,
        "Border_Color" returns string,
        "ApplicationButton_Background" returns string,
        "ScrollLeftButton_Tab returns QIcon",
        "ScrollRightButton_Tab" returns QIcon,
        "ScrollLeftButton_Category" returns QIcon,
        "ScrollRightButton_Category" returns QIcon,
        "OptionButton" returns QIcon,
        "PinButton_open" returns QIcon,
        "PinButton_closed" returns QIcon,
    """
    # define a result holder and a dict for the StyleMapping file
    result = None

    # Get the current stylesheet for FreeCAD
    FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
    currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")

    ListIcons = [
        "ScrollLeftButton_Tab",
        "ScrollRightButton_Tab",
        "ScrollLeftButton_Category",
        "ScrollRightButton_Category",
        "OptionButton",
        "PinButton_open",
        "PinButton_closed",
    ]

    isIcon = False
    for control in ListIcons:
        if control == ControlName:
            isIcon = True

    try:
        if isIcon is True:
            PixmapName = StyleMapping["Stylesheets"][currentStyleSheet][ControlName]
            if PixmapName == "":
                PixmapName = StyleMapping["Stylesheets"][""][ControlName]
            pixmap = QPixmap(os.path.join(pathIcons, PixmapName))
            result = QIcon()
            result.addPixmap(pixmap)
            return result
        if isIcon is False:
            result = StyleMapping["Stylesheets"][currentStyleSheet][ControlName]
            if result == "":
                result = StyleMapping["Stylesheets"][""][ControlName]
            return result
    except Exception:
        return None


def ReturnStyleSheet(control, radius="2px", padding_right="0px", width="15px"):
    """
    Enter one of the names below:

    control (string):
        "toolbutton,
        "applicationbutton,
    """
    StyleSheet = ""
    try:
        BorderColor = ReturnStyleItem("Border_Color")
        BackgroundColor = ReturnStyleItem("Background_Color")
        ApplicationButton = ReturnStyleItem("ApplicationButton_Background")
        HoverColor = ReturnStyleItem("Background_Color_Hover")

        # AppColor_1 = ApplicationButton
        # AppColor_2 = BackgroundColor
        # AppColor_3 = BackgroundColor
        # AppBorder_1 = "transparant"
        # AppBorder_2 = BorderColor
        AppColor_1 = ApplicationButton
        AppColor_2 = ApplicationButton
        AppColor_3 = ApplicationButton
        AppBorder_1 = BorderColor
        AppBorder_2 = BorderColor
        if BackgroundColor is not None and BorderColor is not None:
            if control.lower() == "toolbutton":
                StyleSheet = (
                    """QToolButton {
                            padding-right: """
                    + padding_right
                    + """;}"""
                    + """QToolButton::menu-arrow {
                        width: 10px;
                        height:24px;
                        subcontrol-origin: padding;
                        subcontrol-position: center right;
                    }"""
                    + """QToolButton::menu-button {
                        width: """
                    + width
                    + """;
                        border-radius: 2px;
                        padding: 1px;
                        border-radius: 2px;
                        subcontrol-origin: padding;
                        subcontrol-position: center right;
                    }"""
                    + """QToolButton:hover {
                            background: """
                    + HoverColor
                    + """;
                    border: 0.5px solid"""
                    + BorderColor
                    + """;}"""
                )
                return StyleSheet
            if control.lower() == "applicationbutton":
                StyleSheet = (
                    """QToolButton {
                            padding: 7px;
                            border-radius : """
                    + radius
                    + """;
                    border: 0.5px solid"""
                    + AppBorder_1
                    + """;
                    background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 """
                    + AppColor_1
                    + """, stop:0.9 """
                    + AppColor_2
                    + """, stop:1 """
                    + AppColor_3
                    + """)
                    ;}"""
                    + """QToolButton:hover {
                            border-radius : """
                    + radius
                    + """;
                    border: 3px solid"""
                    + AppBorder_2
                    + """;
                    }"""
                )

            return StyleSheet
    except Exception as e:
        print(e)
        return StyleSheet


StyleMapping = {
    "Stylesheets": {
        "": {
            "Background_Color": "#f0f0f0",
            "Background_Color_Hover": "#ced4da",
            "Border_Color": "#646464",
            "ApplicationButton_Background": "#e0e0e0",
            "ScrollLeftButton_Tab": "",
            "ScrollRightButton_Tab": "",
            "ScrollLeftButton_Category": "",
            "ScrollRightButton_Category": "",
            "OptionButton": "more_default.svg",
            "PinButton_open": "pin-icon-default.svg",
            "PinButton_closed": "pin-icon-default.svg",
            "collapseRibbonButton_up": "",
            "collapseRibbonButton_down": "",
        },
        "FreeCAD Dark.qss": {
            "Background_Color": "#333333",
            "Background_Color_Hover": "#444444",
            "Border_Color": "#ffffff",
            "ApplicationButton_Background": "#2a2a2a",
            "ScrollLeftButton_Tab": "backward_small_default_white.svg",
            "ScrollRightButton_Tab": "forward_small_default_white.svg",
            "ScrollLeftButton_Category": "backward_default_white.svg",
            "ScrollRightButton_Category": "forward_default_white.svg",
            "OptionButton": "more_default_white.svg",
            "PinButton_open": "pin-icon-default_white.svg",
            "PinButton_closed": "pin-icon-default_white.svg",
            "collapseRibbonButton_up": "",
            "collapseRibbonButton_down": "",
        },
        "FreeCAD Light.qss": {
            "Background_Color": "#f0f0f0",
            "Background_Color_Hover": "#ced4da",
            "Border_Color": "#646464",
            "ApplicationButton_Background": "#e0e0e0",
            "ScrollLeftButton_Tab": "backward_small_default.svg",
            "ScrollRightButton_Tab": "forward_small_default.svg",
            "ScrollLeftButton_Category": "backward_default.svg",
            "ScrollRightButton_Category": "forward_default.svg",
            "OptionButton": "more_default.svg",
            "PinButton_open": "pin-icon-default.svg",
            "PinButton_closed": "pin-icon-default.svg",
            "collapseRibbonButton_up": "",
            "collapseRibbonButton_down": "",
        },
        "OpenLight.qss": {
            "Background_Color": "#dee2e6",
            "Background_Color_Hover": "#a5d8ff",
            "Border_Color": "#1c7ed6",
            "ApplicationButton_Background": "#a5d8ff",
            "ScrollLeftButton_Tab": "backward_1.svg",
            "ScrollRightButton_Tab": "forward_1.svg",
            "ScrollLeftButton_Category": "backward_1.svg",
            "ScrollRightButton_Category": "forward_1.svg",
            "OptionButton": "more_1.svg",
            "PinButton_open": "pin-icon-open_1.svg",
            "PinButton_closed": "pin-icon-closed_1.svg",
            "collapseRibbonButton_up": "",
            "collapseRibbonButton_down": "",
        },
        "OpenDark.qss": {
            "Background_Color": "#212529",
            "Background_Color_Hover": "#1f364d",
            "Border_Color": "#264b69",
            "ApplicationButton_Background": "#1f364d",
            "ScrollLeftButton_Tab": "backward_small_default_white.svg",
            "ScrollRightButton_Tab": "forward_small_default_white.svg",
            "ScrollLeftButton_Category": "backward_default_white.svg",
            "ScrollRightButton_Category": "forward_default_white.svg",
            "OptionButton": "more_default_white.svg",
            "PinButton_open": "pin-icon-default_white.svg",
            "PinButton_closed": "pin-icon-default_white.svg",
            "collapseRibbonButton_up": "",
            "collapseRibbonButton_down": "",
        },
    }
}
