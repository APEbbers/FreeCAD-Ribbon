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
from pydoc import text
from turtle import isvisible
from typing import Any

from numpy import delete

from PySide import QtWidgets
import CustomWidgets
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
    QRegion,
    QFont,
    QColor,
    QStyleHints,
    QFontMetrics,
    QTextOption,
    QTextItem,
    QPainter,
    QKeySequence,
    QShortcut,
    QCursor,
    QGuiApplication,
)
from PySide.QtWidgets import (
    QCheckBox,
    QFrame,
    QSpinBox,
    QTextEdit,
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
    QGridLayout,
    QScrollArea,
    QTabBar,
    QWidgetAction,
    QStylePainter,
    QStyle,
    QStyleOptionButton,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QToolTip,
    QWidgetItem,
    QTreeWidget,
    QApplication,
    QStatusBar,
    QStyleOption,
    QDialog,
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
    QSize,
    Slot,
    QRect,
    QPoint,
    QSettings,
)
from CustomWidgets import CustomControls, DragTargetIndicator, Toggle, CheckBoxAction, SpinBoxAction, ComboBoxAction

import json
import os
import sys
import webbrowser
import LoadDesign_Ribbon
import Parameters_Ribbon
import LoadSettings_Ribbon
import LoadLicenseForm_Ribbon
import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Serialize_Ribbon
import StyleMapping_Ribbon
import platform
import math
from datetime import datetime
import shutil
import re

# import Ribbon. This contains the ribbon commands for FreeCAD
import Ribbon

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)
sys.path.append(pathBackup)

translate = App.Qt.translate

import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local.panel import RibbonPanel, RibbonPanelItemWidget
from pyqtribbon_local.toolbutton import RibbonToolButton
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategoryLayoutButton, RibbonNormalCategory, RibbonContextCategory

# import pyqtribbon as pyqtribbon
# from pyqtribbon.ribbonbar import RibbonMenu, RibbonBar
# from pyqtribbon.panel import RibbonPanel, RibbonPanelItemWidget
# from pyqtribbon.toolbutton import RibbonToolButton
# from pyqtribbon.separator import RibbonSeparator
# from pyqtribbon.category import RibbonCategoryLayoutButton


# Get the main window of FreeCAD
mw = Gui.getMainWindow()

# Define a timer
timer = QTimer()

# Write all settings, if they are not present yet
Parameters_Ribbon.Settings.WriteSettings()


class ModernMenu(RibbonBar):
    """
    Create ModernMenu QWidget.
    """

    # region - class parameters
    # Add workbenches that need to be loaded first or early here
    WBtoLoadFirst = ["BillOfMaterialsWB"]

    # The datafile version is set in LoadDesign.py
    DataFileVersion = LoadDesign_Ribbon.LoadDialog.DataFileVersion

    # Define a placeholder for the repro adress
    ReproAdress: str = ""
    # Placeholders for building the ribbonbar
    ribbonStructure = {}
    wbNameMapping = {}
    isWbLoaded = {}
    MainWindowLoaded = False
    LeaveEventEnabled = True

    # use icon size from FreeCAD preferences
    iconSize = Parameters_Ribbon.ICON_SIZE_SMALL
    ApplicationButtonSize = Parameters_Ribbon.APP_ICON_SIZE
    QuickAccessButtonSize = Parameters_Ribbon.QUICK_ICON_SIZE
    # RightToolBarButtonSize = Parameters_Ribbon.RIGHT_ICON_SIZE  # Is overruled
    # TabBar_Size = Parameters_Ribbon.TABBAR_SIZE  # Is overruled
    LargeButtonSize = Parameters_Ribbon.ICON_SIZE_LARGE

    # Define a placeholder for the ribbon height
    RibbonHeight = 0

    # Set a size factor for the buttons
    sizeFactor = 1.3
    # Create an offset for the panelheight
    PanelHeightOffset = 36
    # Create an offset for the whole ribbon height
    RibbonOffset = (
        50 + QuickAccessButtonSize * 2
    )  # Set to zero to hide the panel titles

    # Set the minimum height for the ribbon
    RibbonMinimalHeight = QuickAccessButtonSize * 2 + 16
    # From v1.6.x, the size of tab bar and right toolbar are controlled by the size of the quickaccess toolbar
    TabBar_Size = QuickAccessButtonSize
    RightToolBarButtonSize = QuickAccessButtonSize

    # Declare the right padding for dropdown menus
    PaddingRight = 10

    # Create the list for the commands
    List_Commands = []

    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []

    # Declare the custom overlay function states
    OverlayToggled = False
    OverlayToggled_Left = False
    OverlayToggled_Right = False
    OverlayToggled_Bottom = False
    TransparancyToggled = False

    # Define the menus
    RibbonMenu = QMenu()
    HelpMenu = QMenu()
    OverlayMenu = None
    AccessoriesMenu = None

    # Define the versions for update and developments
    UpdateVersion = ""
    DeveloperVersion = ""

    # Define a boolan to detect if an menu is entered.
    # used to keep the ribbon unfolded, when clicking on a dropdown menu
    MenuEntered = False

    # Store a value when the ribbon is loaded
    # used to hide the ribbon on startup
    isLoaded = False

    # Used for a message when a datafile update is needed.
    LayoutMenuShortCut = ""

    # Define a indictor for wether the design menu is loaded or not.
    DesignMenuLoaded = False

    # Define a indictor for wether beta functions are enabled
    BetaFunctionsEnabled = False

    # Define a indictor for wether the customize enviroment is enabled
    CustomizeEnabled = False
    # endregion

    def __init__(self):
        """
        Constructor
        """
        super().__init__(title="")
        self.setObjectName("Ribbon")

        # Enable dragdrop
        self.setAcceptDrops(True)

        # connect the signals
        self.connectSignals()

        # read ribbon structure from JSON file
        with open(Parameters_Ribbon.RIBBON_STRUCTURE_JSON, "r") as file:
            self.ribbonStructure.update(json.load(file))
        file.close()

        DataFile2 = os.path.join(os.path.dirname(__file__), "RibbonDataFile2.dat")
        if os.path.exists(DataFile2) is True:
            Data = {}
            # read ribbon structure from JSON file
            with open(DataFile2, "r") as file:
                Data.update(json.load(file))
            file.close()
            try:
                # Load the list of commands
                self.List_Commands = Data["List_Commands"]
            except Exception:
                pass

        if (
            StandardFunctions.checkFreeCADVersion(
                Parameters_Ribbon.FreeCAD_Version["mainVersion"],
                Parameters_Ribbon.FreeCAD_Version["subVersion"],
                Parameters_Ribbon.FreeCAD_Version["patchVersion"],
                Parameters_Ribbon.FreeCAD_Version["gitVersion"],
            )
            is True
        ):
            self.ConvertRibbonStructure()

        # check the language and remove texts from the ribbonstructure if the language does not match
        self.CheckLanguage()

        # if FreeCAD is version 0.21 create a custom toolbar "Individual Views"
        if int(App.Version()[0]) == 0 and int(App.Version()[1]) <= 21:
            StandardFunctions.CreateToolbar(
                Name="Individual views",
                WorkBenchName="Global",
                ButtonList=[
                    "Std_ViewIsometric",
                    "Std_ViewRight",
                    "Std_ViewLeft",
                    "Std_ViewFront",
                    "Std_ViewRear",
                    "Std_ViewTop",
                    "Std_ViewBottom",
                ],
            )
        if int(App.Version()[0]) == 1 and int(App.Version()[1]) >= 0:
            StandardFunctions.RemoveWorkBenchToolbars(
                Name="Individual views",
                WorkBenchName="Global",
            )

        # Check there is a custom toolbar "views - ribbon". If so, remove it
        if Parameters_Ribbon.Settings.GetBoolSetting("RibbonViewRemoved") is False:
            StandardFunctions.RemoveWorkBenchToolbars(
                Name="Views - Ribbon",
                WorkBenchName="Global",
            )
        Parameters_Ribbon.Settings.SetBoolSetting("RibbonViewRemoved", True)
        # Check there is a custom toolbar "Tools". If so, remove it
        if Parameters_Ribbon.Settings.GetBoolSetting("ToolsRemoved") is False:
            StandardFunctions.RemoveWorkBenchToolbars(
                Name="Tools",
                WorkBenchName="Global",
            )
        Parameters_Ribbon.Settings.SetBoolSetting("ToolsRemoved", True)

        # Add a toolbar "Views - Ribbon"
        #
        PreferredToolbar = Parameters_Ribbon.Settings.GetIntSetting("Preferred_view")
        # Create a key if not present
        if PreferredToolbar == 2:
            StandardFunctions.add_keys_nested_dict(
                self.ribbonStructure,
                ["newPanels", "Global", "Views - Ribbon_newPanel"],
            )
            self.ribbonStructure["newPanels"]["Global"]["Views - Ribbon_newPanel"] = [
                ["Std_ViewGroup", "Standard"],
                ["Std_ViewFitAll", "Standard"],
                ["Std_ViewFitSelection", "Standard"],
                ["Std_ViewZoomOut", "Standard"],
                ["Std_ViewZoomIn", "Standard"],
                ["Std_ViewBoxZoom", "Standard"],
                ["Std_AlignToSelection", "Standard"],
                ["Part_SelectFilter", "Standard"],
            ]
        else:
            try:
                if (
                    "Views - Ribbon_newPanel"
                    in self.ribbonStructure["newPanels"]["Global"]
                ):
                    del self.ribbonStructure["newPanels"]["Global"][
                        "Views - Ribbon_newPanel"
                    ]
            except Exception:
                pass
        # # Add a toolbar "tools"
        #
        UseToolsPanel = Parameters_Ribbon.Settings.GetBoolSetting("UseToolsPanel")
        # Create a key if not present
        try:
            NeedsUpdating = False
            if "Tools_newPanel" in self.ribbonStructure["newPanels"]["Global"]:
                for item in self.ribbonStructure["newPanels"]["Global"][
                    "Tools_newPanel"
                ]:
                    if item[1] != "Standard":
                        NeedsUpdating = True
            if (
                "Tools_newPanel" not in self.ribbonStructure["newPanels"]["Global"]
                and UseToolsPanel is True
            ) or NeedsUpdating is True:
                StandardFunctions.add_keys_nested_dict(
                    self.ribbonStructure,
                    ["newPanels", "Global", "Tools_newPanel"],
                )
                self.ribbonStructure["newPanels"]["Global"]["Tools_newPanel"] = [
                    ["Std_Measure", "Standard"],
                    ["Std_UnitsCalculator", "Standard"],
                    ["Std_Properties", "Standard"],
                    ["Std_BoxElementSelection", "Standard"],
                    ["Std_BoxSelection", "Standard"],
                    ["Std_WhatsThis", "Standard"],
                ]
        except Exception:
            pass

        # Set the preferred toolbars
        PreferredToolbar = Parameters_Ribbon.Settings.GetIntSetting("Preferred_view")
        ListIgnoredToolbars: list = self.ribbonStructure["ignoredToolbars"]
        # check if the toolbar is already ignored
        View_Inlist = False
        ViewsRibbon_Inlist = False
        IndividualViews_Inlist = False
        for ToolBar in ListIgnoredToolbars:
            if ToolBar == "View":
                View_Inlist = True
            if ToolBar == "Views - Ribbon":
                ViewsRibbon_Inlist = True
            if ToolBar == "Individual views":
                IndividualViews_Inlist = True

        if PreferredToolbar == 0:
            if View_Inlist is False:
                ListIgnoredToolbars.append("View")
            if ViewsRibbon_Inlist is False:
                ListIgnoredToolbars.append("Views - Ribbon")
            if "Individual views" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("Individual views")
        if PreferredToolbar == 1:
            if IndividualViews_Inlist is False:
                ListIgnoredToolbars.append("Individual views")
            if ViewsRibbon_Inlist is False:
                ListIgnoredToolbars.append("Views - Ribbon")
            if "View" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("View")
        if PreferredToolbar == 2:
            if IndividualViews_Inlist is False:
                ListIgnoredToolbars.append("Individual views")
            if View_Inlist is False:
                ListIgnoredToolbars.append("View")
            if "Views - Ribbon" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("Views - Ribbon")
        if PreferredToolbar == 3:
            if IndividualViews_Inlist is False:
                ListIgnoredToolbars.append("Individual views")
            if View_Inlist is False:
                ListIgnoredToolbars.append("View")
            if ViewsRibbon_Inlist is False:
                ListIgnoredToolbars.append("Views - Ribbon")
        self.ribbonStructure["ignoredToolbars"] = ListIgnoredToolbars
        # write the change to the json file
        # Writing to sample.json
        with open(Parameters_Ribbon.RIBBON_STRUCTURE_JSON, "w") as outfile:
            json.dump(self.ribbonStructure, outfile, indent=4)
        outfile.close()

        # Get the address of the repository address
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.ReproAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "repository"
        )
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(translate("FreeCAD Ribbon", "FreeCAD Ribbon: ") + self.ReproAdress)

        # Activate the workbenches used in the new panels otherwise the panel stays empty
        try:
            if "newPanels" in self.ribbonStructure:
                for WorkBenchName in self.ribbonStructure["newPanels"]:
                    for NewPanel in self.ribbonStructure["newPanels"][WorkBenchName]:
                        # Get the commands from the custom panel
                        Commands = self.ribbonStructure["newPanels"][WorkBenchName][
                            NewPanel
                        ]

                        # Get the command and its original toolbar
                        for CommandItem in Commands:
                            if (
                                CommandItem[1] != "General"
                                and CommandItem[1] != "Global"
                                and CommandItem[1] != "Standard"
                            ):
                                # Activate the workbench if not loaded
                                Gui.activateWorkbench(CommandItem[1])
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"new panels have wrong format. Please create them again!\n{e}",
                    "Error",
                )
            pass

        # Activate the workbenches used in the dropdown buttons otherwise the button stays empty
        try:
            if "dropdownButtons" in self.ribbonStructure:
                for DropDownCommand, Commands in self.ribbonStructure[
                    "dropdownButtons"
                ].items():
                    for CommandItem in Commands:
                        if (
                            CommandItem[1] != "General"
                            and CommandItem[1] != "Global"
                            and CommandItem[1] != "Standard"
                        ):
                            # Activate the workbench if not loaded
                            Gui.activateWorkbench(CommandItem[1])
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"dropdownbuttons have wrong format. Please create them again!\n{e}",
                    "Warning",
                )
            pass

        # Check if there is a new version
        # Get the latest version
        try:
            User = "APEbbers"
            Repo = "FreeCAD-Ribbon"
            Branch = "main"
            File = "package.xml"
            ElementName = "version"
            LatestVersion = StandardFunctions.ReturnXML_Value_Git(
                User, Repo, Branch, File, ElementName
            )
            if LatestVersion is not None:
                # Get the current version
                PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
                CurrentVersion = StandardFunctions.ReturnXML_Value(
                    PackageXML, "version"
                )
                # Check if you are on a developer version. If so set developer version
                if CurrentVersion.lower().endswith("x"):
                    self.DeveloperVersion = CurrentVersion
                    self.UpdateVersion = ""
                # If you are not on a developer version, check if you have the latest version
                if CurrentVersion.lower().endswith("x") is False:
                    # Create arrays from the versions
                    LatestVersionArray = LatestVersion.split(".")
                    CurrentVersionArray = CurrentVersion.split(".")

                    # Set the length to the shortest lenght
                    ArrayLenght = len(LatestVersionArray)
                    if len(CurrentVersionArray) < ArrayLenght:
                        ArrayLenght = len(CurrentVersionArray)

                    # Check per level if the latest version has the highest number
                    # if so set update version
                    for i in range(ArrayLenght):
                        if LatestVersionArray[i] > CurrentVersionArray[i]:
                            # print(f"{LatestVersionArray[i]}, {CurrentVersionArray[i]}")
                            self.UpdateVersion = LatestVersion
        except Exception:
            pass

        # Create the ribbon
        self.CreateMenus()  # Create the menus
        self.createModernMenu()  # Create the ribbon

        # Set the custom stylesheet
        StyleSheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
        # modify the stylesheet to set the border and background for a toolbar and menu
        hexColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        hexColorTab = StyleMapping_Ribbon.ReturnStyleItem(
            "Background_Color", True, True
        )
        if (
            hexColor is not None
            and hexColor != ""
            and Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED is True
        ):
            # Set the quickaccess toolbar background color. This fixes a transparant toolbar.
            self.quickAccessToolBar().setStyleSheet(
                "QToolBar {background: " + hexColor + ";}"
            )
            self.tabBar().setStyleSheet("background: " + hexColorTab + ";")
            # Set the background color. This fixes transparant backgrounds when FreeCAD has no stylesheet
            StyleSheet_Addition = (
                "\n\nQToolButton {background: solid " + hexColor + ";}"
            )
            StyleSheet_Addition_2 = (
                "\n\nRibbonBar {border: none;background: solid "
                + hexColor
                + ";color: "
                + hexColor
                + ";}"
            )
            StyleSheet = StyleSheet_Addition_2 + StyleSheet + StyleSheet_Addition
        self.setStyleSheet(StyleSheet)

        # If the text for the tabs is set to be disabled, update the stylesheet
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            StyleSheet_Addition_3 = (
                """QTabBar::tab {
                    background: """
                + StyleMapping_Ribbon.ReturnStyleItem(
                    "Background_Color_Hover", True, True
                )
                + """;color: """
                + StyleMapping_Ribbon.ReturnStyleItem(
                    "Background_Color_Hover", True, True
                )
                + """;min-width: """
                + str(self.TabBar_Size-3)
                + """px;
                            max-width: """
                + str(self.TabBar_Size-3)
                + """px;
                            padding-left: 6px;
                            padding-right: 3px;
                            margin: 3px
                        }"""
            )
            StyleSheet = StyleSheet_Addition_3 + StyleSheet
            self.setStyleSheet(StyleSheet)
            StyleSheet = StyleSheet_Addition_3 + StyleSheet
            self.setStyleSheet(StyleSheet)

        # Add an addition for selected tabs
        StyleSheet_Addition_4 = (
            """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
            + """;}"""
        )
        # If the tabs are set to icon only, set the text to the hover background color also
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            StyleSheet_Addition_4 = (
                """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + """;color: """
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + """;}"""
            )
        StyleSheet = StyleSheet_Addition_4 + StyleSheet
        self.setStyleSheet(StyleSheet)

        # add a stylesheet entry for the fontsize for menus
        StyleSheet_Addition_5 = (
            "QMenu::item, QMenu::menuAction, QMenuBar::item, RibbonMenu, RibbonToolButton, RibbonMenu::item, QMenu>QLabel {font-size: "
            + str(Parameters_Ribbon.FONTSIZE_MENUS)
            + "px;}"
        )
        StyleSheet = StyleSheet + StyleSheet_Addition_5
        self.setStyleSheet(StyleSheet)

        # get the state of the mainwindow
        self.MainWindowLoaded = True

        # Set these settings and connections at init
        # Set the autohide behavior of the ribbon
        preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
        if preferences.GetBool("ActivateOverlay") is True:
            Parameters_Ribbon.AUTOHIDE_RIBBON = False
        self.setAutoHideRibbon(Parameters_Ribbon.AUTOHIDE_RIBBON)

        # Remove the collapseble button
        RightToolbar = self.rightToolBar()
        RightToolbar.removeAction(RightToolbar.actions()[0])

        # make sure that the ribbon cannot "disappear"
        self.setMinimumHeight(self.RibbonMinimalHeight)

        self.setSizeIncrement(1, 1)

        # Set the menuBar hidden as standard
        mw.menuBar().hide()
        if self.isEnabled() is False:
            mw.menuBar().show()

        # connect a tabbar click event to the tarbar click funtion
        # this used to replaced the native functions
        self.tabBar().tabBarClicked.connect(self.onTabBarClicked)

        # override the default scroll behavior with a custom function
        self.tabBar().wheelEvent = lambda event_tabBar: self.wheelEvent_TabBar(
            event_tabBar
        )
        self.wheelEvent = lambda event_CC: self.wheelEvent_CC(event_CC)
        self.tabBar().setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.currentCategory().setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Customize the tabBar. Has only to be done once
        # The scrollbuttons for the ribbon are set per ribbon tab
        # So they are set in self.BuildPanels()
        #
        # Set the scroll buttons on the tabbar
        ScrollLeftButton_Tab: QToolButton = self.tabBar().findChildren(QToolButton)[0]
        ScrollRightButton_Tab: QToolButton = self.tabBar().findChildren(QToolButton)[1]
        # get the icons
        ScrollLeftButton_Tab_Icon = StyleMapping_Ribbon.ReturnStyleItem(
            "ScrollLeftButton_Tab"
        )
        ScrollRightButton_Tab_Icon = StyleMapping_Ribbon.ReturnStyleItem(
            "ScrollRightButton_Tab"
        )
        # Set the icons
        StyleSheet = "QToolButton {image: none;margin-top:6px;margin-bottom:6px;};QToolButton::arrow {image: none};"
        BackgroundColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        if (
            int(App.Version()[0]) == 0
            and int(App.Version()[1]) <= 21
            and BackgroundColor is not None
        ):
            StyleSheet = (
                """QToolButton {image: none;background: """
                + BackgroundColor
                + """};QToolButton::arrow {image: none;margin-top:6px;margin-bottom:6px;};"""
            )
        if ScrollLeftButton_Tab_Icon is not None:
            ScrollLeftButton_Tab.setStyleSheet(StyleSheet)
            ScrollLeftButton_Tab.setIcon(ScrollLeftButton_Tab_Icon)
        else:
            ScrollRightButton_Tab.setToolButtonStyle(
                Qt.ToolButtonStyle.ToolButtonTextOnly
            )
        if ScrollRightButton_Tab_Icon is not None:
            ScrollRightButton_Tab.setStyleSheet(StyleSheet)
            ScrollRightButton_Tab.setIcon(ScrollRightButton_Tab_Icon)
        else:
            ScrollRightButton_Tab.setArrowType(Qt.ArrowType.RightArrow)

        # Remove persistant toolbars
        PersistentToolbars = App.ParamGet(
            "User parameter:Tux/PersistentToolbars/User"
        ).GetGroups()
        for Group in PersistentToolbars:
            Parameter = App.ParamGet(
                "User parameter:Tux/PersistentToolbars/User/" + Group
            )
            Parameter.SetString("Top", "")
            Parameter.SetString("Left", "")
            Parameter.SetString("Right", "")
            Parameter.SetString("Bottom", "")

        # Connect shortcuts
        #
        # Application menu
        ShortcutKey = "Alt+A"
        try:
            CustomShortCuts = App.ParamGet(
                "User parameter:BaseApp/Preferences/Shortcut"
            )
            if "Ribbon_Menu" in CustomShortCuts.GetStrings():
                ShortcutKey = CustomShortCuts.GetString("Ribbon_Menu")
        except Exception:
            pass
        self.applicationOptionButton().setShortcut(ShortcutKey)
        ToolTip = f"{ShortcutKey}"
        self.applicationOptionButton().setToolTip(ToolTip)

        # Add a custom close event to show the original menubar again
        self.closeEvent = lambda close: self.closeEvent(close)
        # Add a custom enter event to the tabbar
        self.tabBar().enterEvent = lambda enter: self.enterEvent_Custom(enter)
        # When hovering over the menu button, hide the ribbon
        self.applicationOptionButton().enterEvent = lambda enter: self.leaveEvent(enter)

        # Rearrange the tabbar and toolbars
        if (
            Parameters_Ribbon.TOOLBAR_POSITION == 0
            or Parameters_Ribbon.TOOLBAR_POSITION == 1
        ):
            # Get the widgets
            _quickAccessToolBarWidget = self.quickAccessToolBar()
            _titleLabel = self._titleWidget._titleLabel
            _rightToolBar = self.rightToolBar()
            _tabBar = self.tabBar()
            # Remove the widgets
            self._titleWidget._tabBarLayout.removeWidget(_quickAccessToolBarWidget)
            self._titleWidget._tabBarLayout.removeWidget(_titleLabel)
            self._titleWidget._tabBarLayout.removeWidget(_rightToolBar)
            self._titleWidget._tabBarLayout.removeWidget(_tabBar)
            if Parameters_Ribbon.TOOLBAR_POSITION == 0:  # Toolbars above tabbar
                # Set the font size for the label
                font: QFont = _titleLabel.font()
                font.setPixelSize(Parameters_Ribbon.FONTSIZE_MENUS + 1)
                _titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                _titleLabel.setFont(font)
                # Set the label text to FreeCAD's version
                text = (
                    f"FreeCAD {App.Version()[0]}.{App.Version()[1]}.{App.Version()[2]}"
                )
                _titleLabel.setText(text)
                # Create a spacer to set the tab
                spacer = QWidget()
                spacer.setSizePolicy(
                    QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
                )
                spacer.setFixedWidth(3)
                self._titleWidget._tabBarLayout.setContentsMargins(3, 3, 3, 0)
                self._titleWidget._tabBarLayout.addWidget(
                    _quickAccessToolBarWidget, 0, 0, 1, 2, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _titleLabel, 0, 2, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _rightToolBar, 0, 3, 1, 2, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    spacer, 1, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _tabBar, 1, 1, 1, 4, Qt.AlignmentFlag.AlignVCenter
                )
                # Change the offsets
                self.RibbonMinimalHeight = self.QuickAccessButtonSize * 2 + 20
                self.RibbonOffset = 54 + self.QuickAccessButtonSize * 2
                self._titleWidget._tabBarLayout.setRowMinimumHeight(
                    0, self.QuickAccessButtonSize
                )
                self._titleWidget._tabBarLayout.setRowMinimumHeight(1, self.TabBar_Size)
                # self.setTitle("FreeCAD")
            if Parameters_Ribbon.TOOLBAR_POSITION == 1:  # Toolbars inline with tabbar
                # Add the widgets again in a different position
                self._titleWidget._tabBarLayout.addWidget(
                    _quickAccessToolBarWidget, 0, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _tabBar, 0, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _titleLabel, 0, 2, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _rightToolBar, 0, 3, 1, 2, Qt.AlignmentFlag.AlignVCenter
                )
                # Change the offsets
                self.RibbonMinimalHeight = self.QuickAccessButtonSize + 10
                self.RibbonOffset = 46 + self.QuickAccessButtonSize
                self._titleWidget._tabBarLayout.setRowMinimumHeight(
                    0, self.QuickAccessButtonSize
                )

        # Get the main window, its style, the ribbon and the restore button
        try:
            RestoreButton: QToolButton = self.rightToolBar().findChildren(
                QToolButton, "RestoreButton"
            )[0]
            # If the mainwindow is maximized, set the window state to maximize and set the correct icon
            if mw.isMaximized():
                try:
                    RestoreButton.setIcon(
                        StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[2]
                    )
                except Exception:
                    pass
            # If the mainwindow is not maximized, set the window state to no state and set the correct icon
            if mw.isMaximized() is False:
                try:
                    RestoreButton.setIcon(
                        StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[1]
                    )
                except Exception:
                    pass
        except Exception:
            pass

        # Install an event filter to catch events from the main window and act on it.
        mw.installEventFilter(EventInspector(mw))

        # Set isLoaded to True, to show that the loading is finished
        self.isLoaded = True
        # Fold the ribbon if unpinned
        self.FoldRibbon()
        # Check if an reload of the datafile is needed an show an message
        self.CheckDataFile()

        # Activate some WB's first to ensure proper loading of the panels
        for Wb in self.WBtoLoadFirst:
            try:
                Gui.activateWorkbench(Wb)
            except Exception:
                pass

        # Set the state of the Béta function switch
        switch: Toggle = self.rightToolBar().findChild(Toggle, "bétaSwitch")
        switch.setChecked(Parameters_Ribbon.BETA_FUNCTIONS_ENABLED)
        return

    # region - event functions
    def closeEvent(self, event):
        mw.menuBar().show()
        return True

    def eventFilter(self, obj, event):
        # Disable the standard hover behavior
        if event.type() == QEvent.Type.HoverMove:
            event.ignore()
            return False
        return False

    def enterEvent_Custom(self, QEvent):
        # # Hide any possible toolbar
        # self.hideClassicToolbars()
        TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        TB.show()
        # In FreeCAD 1.0, Overlays are introduced. These have also an enterEvent which results in strange behavior
        # Therefore this function is only activated when FreeCAD's overlay function is disabled.
        if (
            Parameters_Ribbon.SHOW_ON_HOVER is True
            and Parameters_Ribbon.USE_FC_OVERLAY is False
        ):
            self.UnfoldRibbon()
            return

    def leaveEvent(self, QEvent):
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True and self.MenuEntered is False:
            self.FoldRibbon()
            # print("LeaveEvent")

    # used to scroll a ribbon horizontally, when it's wider than the screen
    def wheelEvent_CC(self, event):
        if self.currentCategory().underMouse():
            x = 0
            # Get the scroll value (1 or -1)
            delta = event.angleDelta().y()
            x += delta and delta // abs(delta)

            NoClicks = Parameters_Ribbon.Settings.GetIntSetting("Ribbon_Scroll")
            if NoClicks == 0 or NoClicks is None:
                NoClicks = 1

            # go back or forward based on x.
            if x == 1:
                for i in range(NoClicks):
                    self.currentCategory().scrollPrevious()
            if x == -1:
                for i in range(NoClicks):
                    self.currentCategory().scrollNext()
        return

    # used to scroll the tabbar horizontally, when it's wider than the screen
    def wheelEvent_TabBar(self, event):
        if self.tabBar().underMouse():
            x = 0
            # Get the scroll value (1 or -1)
            delta = event.angleDelta().y()
            x += delta and delta // abs(delta)

            ScrollButtons_Tab = self.tabBar().children()
            ScrollLeftButton_Tab: QToolButton = ScrollButtons_Tab[0]
            ScrollRightButton_Tab: QToolButton = ScrollButtons_Tab[1]

            NoClicks = Parameters_Ribbon.Settings.GetIntSetting("TabBar_Scroll")
            if NoClicks == 0 or NoClicks is None:
                NoClicks = 1

            # go back or forward based on x.
            if x == 1:
                for i in range(NoClicks):
                    ScrollLeftButton_Tab.click()
            if x == -1:
                for i in range(NoClicks):
                    ScrollRightButton_Tab.click()
        return

    def contextMenuEvent(self, event):
        widget = None
        panel = None
        # If betaFunctions is enabled, coninue
        if self.BetaFunctionsEnabled is True:
            # Get the widget and the panel
            widget = self.childAt(event.pos()).parent()
            panel = widget.parent().parent()
            # Check if the panel is not none and of type RibbonPanel
            if panel is not None and type(panel) is RibbonPanel:
                if (
                    (type(widget) is RibbonToolButton or type(widget) is RibbonPanelItemWidget)
                    and self.CustomizeEnabled is True
                ):                        
                    # Define the context menu for buttons
                    contextMenu = QMenu(self)
                    
                    # set the checkbox for enabling text
                    RibbonButonAction_Text = CheckBoxAction(self, "Enable text")
                    # Check if the widget has text enabled
                    textVisible = False
                    for child in widget.children():
                        if type(child) == QLabel:
                            textVisible = child.isVisible()
                    # Set the checkbox action checked or unchecked
                    RibbonButonAction_Text.setChecked(textVisible)
                    RibbonButonAction_Text.checkStateChanged.connect(lambda: self.on_TextState_Changed(contextMenu, panel, widget, RibbonButonAction_Text))
                    # Add the checkbox action to the contextmenu
                    contextMenu.addAction(RibbonButonAction_Text)
                    
                    # Set the spinbox for the button size
                    RibbonButtonAction_Size = SpinBoxAction(self, "Set size")
                    RibbonButtonAction_Size.setMinimum(16)
                    RibbonButtonAction_Size.setMaximum(120)                        
                    RibbonButtonAction_Size.setValue(widget.height())
                    RibbonButtonAction_Size.valueChanged.connect(lambda: self.on_ButtonSize_Changed(contextMenu, panel, widget, RibbonButtonAction_Size))
                    contextMenu.addAction(RibbonButtonAction_Size)
                    
                    # Set the dropdown for the button style
                    RibbonButtonAction_Style = ComboBoxAction(self, "set button type")
                    RibbonButtonAction_Style.addItem("Small")
                    RibbonButtonAction_Style.addItem("Medium")
                    RibbonButtonAction_Style.addItem("Large")
                    RibbonButtonAction_Style.addItem("")
                    RibbonButtonAction_Style.setCurrentText("")
                    RibbonButtonAction_Style.currentTextChanged.connect(lambda: self.on_ButtonStyle_Clicked(panel, widget, RibbonButtonAction_Style, RibbonButtonAction_Size))                      
                    contextMenu.addAction(RibbonButtonAction_Style)
                                                     
                    # create the context menu action
                    contextMenu.exec_(self.mapToGlobal(event.pos()))

                    # Disconnect the widgetActions
                    RibbonButtonAction_Style.currentTextChanged.disconnect()
                    RibbonButonAction_Text.checkStateChanged.disconnect()
                    RibbonButtonAction_Size.valueChanged.disconnect()
                    return

            if panel is not None and type(panel) is not RibbonPanel:
                contextMenu = QMenu(self)
                title = "Customize..."
                if self.CustomizeEnabled is True:
                    title = "Exit customize..."
                CustomizeStartAct = contextMenu.addAction(title)
                action = contextMenu.exec_(self.mapToGlobal(event.pos()))

                Stylesheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
                if action == CustomizeStartAct:
                    if self.CustomizeEnabled is False:
                        Addition = """RibbonCategory {
                            border-top: 1px solid red;
                            border-bottom: 1px solid red;
                        }"""
                        Stylesheet = Addition + Stylesheet
                        self.setStyleSheet(Stylesheet)
                        self.CustomizeEnabled = True
                        self.setRibbonHeight(self.RibbonHeight + 6)                        
                        return
                    if self.CustomizeEnabled is True:
                        self.setStyleSheet(Stylesheet)
                        self.CustomizeEnabled = False
                        self.setRibbonHeight(self.RibbonHeight)
                        return

        return
        
    def on_ButtonStyle_Clicked(self, panel: RibbonPanel, ButtonWidget, ButtonStyleWidget: ComboBoxAction, ButtonSizeWidget: SpinBoxAction):                         
        # layout: QGridLayout = panel._actionsLayout
        layout = QGridLayout()
        newControl = RibbonToolButton()
                      
        WidgetTypeToSet = "SmallWidget"
        Size = "small"
        if ButtonStyleWidget.currentText() == "Medium":
            WidgetTypeToSet = "MediumWidget"
            Size = "medium"
        if ButtonStyleWidget.currentText() == "Large":
            WidgetTypeToSet = "LargeWidget"
            Size = "large"
        
        textVisible = False
        defaultAction = None
        for child in ButtonWidget.children():
            if type(child) == QLabel:
                textVisible = child.isVisible()
            if child.objectName() == "CommandButton":
                defaultAction = child.defaultAction()
            
        orderList = []    
        for widget in panel.widgets():
            action = None
            WidgetType = widget.objectName()
            for child in widget.children():                
                if child.objectName() == "CommandButton":
                    action = child.defaultAction()
                    if action.data() == defaultAction.data():
                        WidgetType = WidgetTypeToSet
                    orderList.append([action.data(), WidgetType, child])
            
        panel.widgets().clear()

        for item in orderList:
            currentWidget = item[2]
            WidgetType = item[1]
            
            if WidgetType == "SmallWidget":
                alignment = Qt.AlignmentFlag.AlignTop
                height = Parameters_Ribbon.ICON_SIZE_SMALL
                CommandWidget = currentWidget
                newControl = self.returnDropWidgets(CommandWidget, panel, showText=False,)
                # newControl.setFixedHeight(height)
                panel.removeWidget(currentWidget)
                panel.removeWidget(currentWidget.parent())
                panel.removeWidget(currentWidget.parent().parent())
                currentWidget.close()
                panel.addSmallWidget(widget=newControl, alignment=alignment, fixedHeight=False).setObjectName("SmallWidget")
            if WidgetType == "MediumWidget":
                alignment = Qt.AlignmentFlag.AlignTop
                height = Parameters_Ribbon.ICON_SIZE_MEDIUM
                CommandWidget = currentWidget
                newControl = self.returnDropWidgets(CommandWidget, panel, "Medium", showText=False,)           
                # newControl.setFixedHeight(height)
                panel.removeWidget(currentWidget)
                panel.removeWidget(currentWidget.parent())
                panel.removeWidget(currentWidget.parent().parent())
                currentWidget.close()
                panel.addMediumWidget(widget=newControl, alignment=alignment, fixedHeight=False).setObjectName("MediumWidget")
            if WidgetType == "LargeWidget":
                alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
                height = Parameters_Ribbon.ICON_SIZE_LARGE
                CommandWidget = currentWidget
                newControl = self.returnDropWidgets(CommandWidget, panel, "Large", showText=False,)
                newControl.setFixedSize(QSize(height, height))
                panel.removeWidget(currentWidget)
                panel.removeWidget(currentWidget.parent())
                panel.removeWidget(currentWidget.parent().parent())
                currentWidget.close()
                panel.addLargeWidget(widget=newControl, alignment=alignment, fixedHeight=False).setObjectName("LargeWidget")
                
                for child in ButtonWidget.children():
                    if type(child) == QLabel:
                        # show the text
                        if textVisible is True:
                            child.show()
                        else:
                            child.hide()
                            child.setMinimumWidth(0)
                          
        panel.removeWidget(ButtonWidget)
        panel.removeWidget(ButtonWidget.parent())
        ButtonWidget.close()

        layout.update()
        
        # write the changes to the ribbonstruture file 
        property = {"size": Size}
        self.WriteButtonSettings(ButtonWidget, panel, property)
        return
    
    def on_ButtonSize_Changed(self, contextMenu: QMenu, panel: RibbonPanel, ButtonWidget, ButtonSizeWidget: SpinBoxAction):
        # Get the menubutton height for large buttons
        menuButtonWidth = 0
        if ButtonWidget.objectName() != "LargeWidget":
            try:
                menuButtonWidth = ButtonWidget.findChild(QToolButton, "MenuButton").width()
            except Exception:
                pass
        
        # Get the label height for small and medium buttons
        labelWidth = 0
        for child in ButtonWidget.children():
            if type(child) == QLabel:
                if child.isVisible() is True:
                    labelWidth = child.maximumWidth()
 
        # Adjust the icon to the new heights
        delta = ButtonSizeWidget.value() - ButtonWidget.height()
        for child in ButtonWidget.children():
            if type(child) == QToolButton and child.objectName() == "CommandButton":
                height = child.height() + delta
                width = height
                if ButtonWidget.objectName() == "LargeWidget":
                    width = ButtonSizeWidget.value() + 6
                    if labelWidth > width:
                        width = labelWidth
                        labelWidth = 0
                child.setFixedSize(QSize(width, height))
                child.setIconSize(QSize(width, height))                
        ButtonWidget.setFixedHeight(ButtonSizeWidget.value())
        if ButtonWidget.objectName() != "LargeWidget":
            ButtonWidget.setFixedWidth(ButtonSizeWidget.value() + labelWidth + menuButtonWidth)
        if ButtonWidget.objectName() == "LargeWidget":
            ButtonWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)

        # write the changes to the ribbonstruture file 
        property = {"ButtonSize_small": ButtonSizeWidget.value()}
        if ButtonWidget.objectName() == "MediumWidget":
            property = {"ButtonSize_medium": ButtonSizeWidget.value()}
        if ButtonWidget.objectName() == "LargeWidget":
            property = {"ButtonSize_large": ButtonSizeWidget.value()}
        self.WriteButtonSettings(ButtonWidget, panel, property)
        return
    
    def on_TextState_Changed(self, contextMenu: QMenu, panel: RibbonPanel, ButtonWidget, TextStateWidget: CheckBoxAction):
        # Get the menubutton height for large buttons
        menuButtonWidth = 0
        if ButtonWidget.objectName() != "LargeWidget":
            try:
                menuButtonWidth = ButtonWidget.findChild(QToolButton, "MenuButton").width()
            except Exception:
                pass
        
        # Check if the widget has text enabled
        textVisible = False
        for child in ButtonWidget.children():
            if type(child) == QLabel:
                textVisible = child.isVisible()
                
        # Determine the button size
        baseWidth: int = Parameters_Ribbon.ICON_SIZE_SMALL
        for child in ButtonWidget.children():
            if type(child) == QToolButton and child.objectName() == "CommandButton":
                baseWidth = child.width()
        
        # Get the label height for small and medium buttons
        labelWidth = 0
        for child in ButtonWidget.children():
            if type(child) == QLabel:
                # if child.isVisible() is True:
                #     labelWidth = child.maximumWidth()
                if ButtonWidget.objectName() == "SmallWidget":
                    labelWidth = self.ReturnTextWidth(Label_Text=child, Width=baseWidth, Menu=ButtonWidget.menu(), setWordWrap=False)
                if ButtonWidget.objectName() == "MediumWidget":
                    labelWidth = self.ReturnTextWidth(Label_Text=child, Width=baseWidth, Menu=ButtonWidget.menu(), setWordWrap=Parameters_Ribbon.WRAPTEXT_MEDIUM)
                if ButtonWidget.objectName() == "LargeWidget":
                    labelWidth = self.ReturnTextWidth(Label_Text=child, Width=baseWidth, Menu=ButtonWidget.menu(), setWordWrap=Parameters_Ribbon.WRAPTEXT_LARGE, TextAlignment=Qt.AlignmentFlag.AlignCenter)
                
        # If the widget has not text, show it with the correct width
        if textVisible is False and TextStateWidget.isChecked() is True:            
            # Go through the children of the button.   
            for child in ButtonWidget.children():
                # If you find the QLabel, show it and update the baseWidth             
                if type(child) == QLabel:
                    # show the text
                    child.show()                                        
                    print(labelWidth)
                    # Because medium and small widgets have text on the right side,
                    # change the widht of the button
                    if ButtonWidget.objectName() != "LargeWidget":
                        ButtonWidget.setFixedWidth(
                            baseWidth + labelWidth + menuButtonWidth
                        )
                    if ButtonWidget.objectName() == "LargeWidget":
                        if labelWidth > baseWidth:
                            ButtonWidget.setFixedWidth(labelWidth)
                        else:
                            ButtonWidget.setFixedWidth(baseWidth)
                        # ButtonWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)   
                        
                # If the child is a QToolButton, set the width of the child and the button to the basewidth
                if type(child) == QToolButton and child.objectName() == "CommandButton":
                    child.setFixedWidth(baseWidth)
                    if ButtonWidget.objectName() == "LargeWidget":
                        if labelWidth > baseWidth:
                            child.setFixedWidth(labelWidth)
                        else:
                            child.setFixedWidth(baseWidth)
                    child.setIconSize(QSize(baseWidth, baseWidth))
                #     ButtonWidget.setFixedWidth(baseWidth)
            self.WriteButtonSettings(ButtonWidget, panel, {"textEnabled": TextStateWidget.isChecked()})
            contextMenu.close()
            return
        # if the widget has text, find its QTextEdit and hide it. Update the width
        if textVisible is True  and TextStateWidget.isChecked() is False:
            # Go through the children of the button.  
            for child in ButtonWidget.children():
                # If you find the QLabel, hide it and change its widht.
                if type(child) == QLabel:
                    # Set the width to zero to ensure that the button is not too wide
                    child.setFixedWidth(0)
                    # hide the text
                    child.hide()
                # If the child is a QToolButton, set the width of the child and the button to its height 
                if type(child) == QToolButton and child.objectName() == "CommandButton":
                    child.setFixedWidth(child.height())
                    ButtonWidget.setFixedWidth(child.height())                 
            self.WriteButtonSettings(ButtonWidget, panel, {"textEnabled": TextStateWidget.isChecked()})
            contextMenu.close()   
            return
    # endregion

    # region - drag drop event functions
    dragIndicator = DragTargetIndicator()
    position = None

    def dragEnterEvent(self, e):
        if self.CustomizeEnabled is True:    
            e.accept()

    def dragLeaveEvent(self, e):
        if self.CustomizeEnabled is True:
            # Hide the drag indicator when you leave the drag area
            self.dragIndicator.close()
            e.accept()

    def dragMoveEvent(self, e):
        if self.CustomizeEnabled is True:
            widget = e.source()
            parent = widget.parent().parent()

            # Find the correct location of the drop target, so we can move it there.
            position = self.find_drop_location(e)
            if position is None:
                # print("position is none")
                backup_size = QSize(
                    Parameters_Ribbon.ICON_SIZE_SMALL, Parameters_Ribbon.ICON_SIZE_SMALL
                )
                position = [0, 0, backup_size, backup_size]

            self.position = position
            # Inserting moves the item if its alreaady in the layout.
            rowSpan = 2
            self.dragIndicator.setFixedSize(QSize(
                    Parameters_Ribbon.ICON_SIZE_SMALL, Parameters_Ribbon.ICON_SIZE_SMALL
                ))
            if position[2].height() == Parameters_Ribbon.ICON_SIZE_MEDIUM:
                rowSpan = 3
                self.dragIndicator.setFixedSize(QSize(
                    Parameters_Ribbon.ICON_SIZE_MEDIUM, Parameters_Ribbon.ICON_SIZE_MEDIUM
                ))
            if position[2].height() == Parameters_Ribbon.ICON_SIZE_LARGE:
                rowSpan = 6
                self.dragIndicator.setFixedSize(QSize(
                    Parameters_Ribbon.ICON_SIZE_LARGE, Parameters_Ribbon.ICON_SIZE_LARGE
                ))
            parent._actionsLayout.addWidget(
                self.dragIndicator, position[0], position[1], rowSpan, 1
            )
            # # Hide the item being dragged.
            # e.source().hide()
            # Show the target.
            self.dragIndicator.show()
            e.accept()
        return

    def dropEvent(self, e):
        try:
            if self.CustomizeEnabled is True:
                # Get the widget
                widget = e.source()
                # Get the panel
                panel = widget.parent().parent()
                # Get tabBar
                parent = widget.parent()
                count = 0
                while (count < 10):
                    if type(parent) == RibbonNormalCategory or type(parent) == RibbonContextCategory:
                        break
                    else:
                        parent = parent.parent()
                # Get the workbench name                    
                WorkBenchName = parent.objectName()

                # if the grid layout is a Ribbon panel continue
                if isinstance(panel, RibbonPanel):
                    # Get the drop position
                    position = self.find_drop_location(e)
                    xPos = position[0]
                    yPos = position[1]

                    # Hide the drag indicator
                    self.dragIndicator.hide()
                    # Get the grid layout
                    gridLayout: QGridLayout = panel._actionsLayout

                    # Get the widget that has to be replaced
                    W_origin = gridLayout.itemAtPosition(xPos, yPos).widget()
                    W_drop_origin: QToolButton = W_origin.findChildren(QToolButton)[0]
                    T_origin: QToolButton = W_drop_origin.findChildren(QToolButton)[0]
                    original_size = position[3]

                    # Get the old position of the dragged widget
                    n = 0
                    OldPos = []
                    for n in range(gridLayout.count()):
                        if gridLayout.itemAt(n).widget().children()[1] == widget:
                            OldPos = gridLayout.getItemPosition(n)
                            break
                    # counter and old position is not empty, Swap the widgets
                    if n > -1 and len(OldPos) > 0 :
                        # Take the dragged widget
                        W_dropWidget = gridLayout.itemAt(n).widget()
                        W_drop_customControl: QToolButton = W_dropWidget.findChildren(
                            QToolButton
                        )[0]
                        T_dropWidget: QToolButton = W_drop_customControl.findChildren(
                            QToolButton
                        )[0]

                        # Get the new size
                        new_size = position[2]

                        # Set the rowspan for the dragged widget
                        buttonSize_dropWidget = "small"
                        if new_size.height() == Parameters_Ribbon.ICON_SIZE_MEDIUM:
                            buttonSize_dropWidget = "medium"
                        if new_size.height() == Parameters_Ribbon.ICON_SIZE_LARGE:
                            buttonSize_dropWidget = "large"
                        W_dropWidget.setFixedHeight(original_size.height())

                        # Set the rowspan for the original widget
                        buttonSize_origin = "small"
                        if original_size.height() == Parameters_Ribbon.ICON_SIZE_MEDIUM:
                            buttonSize_origin = "medium"
                        if original_size.height() == Parameters_Ribbon.ICON_SIZE_LARGE:
                            buttonSize_origin = "large"
                        W_origin.setFixedHeight(new_size.height())

                        # Create a new dragged widget, to add in the new place
                        draggedWidget = self.returnDropWidgets(                    
                            widget=T_dropWidget,
                            panel=panel,
                            ButtonType=buttonSize_dropWidget,
                            showText=False,
                        )
                        # Create a ribbonpanel item widget from the new dragged widget
                        draggedItem = RibbonPanelItemWidget(panel)
                        draggedItem.addWidget(draggedWidget)
                        gridLayout.replaceWidget(W_origin, draggedItem)
                        
                        # Create a new origina widget, to add in the old place          
                        originalWidget = self.returnDropWidgets(
                            widget=T_origin,
                            panel=panel,                    
                            ButtonType=buttonSize_origin,
                            showText=False,
                        )                    
                        # Create a ribbonpanel item widget from the new orignal widget
                        originalItem = RibbonPanelItemWidget(panel)
                        originalItem.addWidget(originalWidget)
                        gridLayout.replaceWidget(W_dropWidget, originalItem)
                        
                        def Delete(widget):
                            for i in range(20):
                                parent = widget.parent()
                                if type(parent) is RibbonPanel:
                                    break
                                else:
                                    parent.close()
                            return
                        Delete(W_origin)
                        Delete(W_dropWidget)
                        Delete(T_origin)
                        Delete(T_dropWidget)
                        
                        W_origin.close()
                        W_dropWidget.close()
                        T_origin.close()
                        T_dropWidget.close()

                    e.accept()

                    # Get the order of the widgets
                    orderList = []
                    for k in range(gridLayout.count()):
                        try:
                            Control = gridLayout.itemAt(k).widget().children()[1]
                            if type(Control) is RibbonToolButton:
                                for child in Control.children():
                                    if (
                                        type(child) == QToolButton
                                        and child.objectName() == "CommandButton"
                                    ):
                                        orderList.append(child.defaultAction().data())
                        except Exception:
                            pass
                    
                    # Update the order in the ribbon structure
                    StandardFunctions.add_keys_nested_dict(
                        self.ribbonStructure,
                        [
                            "workbenches",
                            WorkBenchName,
                            "toolbars",
                            panel.objectName(),
                            "order",
                        ],
                    )
                    self.ribbonStructure["workbenches"][WorkBenchName]["toolbars"][
                        panel.objectName()
                    ]["order"] = orderList
                    
                    # Writing to ribbonStructure.json
                    JsonFile = Parameters_Ribbon.RIBBON_STRUCTURE_JSON
                    with open(JsonFile, "w") as outfile:
                        json.dump(self.ribbonStructure, outfile, indent=4)
                    outfile.close()
        except Exception:
            pass
        return

    def find_drop_location(self, e):
        """
        Determines the drop location in a grid layout based on the position of a drag-and-drop event.
        Args:
            e (QEvent): The drag-and-drop event containing the position and source widget.
        Returns:
            list: A list containing the following elements:
                - xPos (int): The row index in the grid layout where the drop occurred.
                - yPos (int): The column index in the grid layout where the drop occurred.
                - w_origin_height (int): The height of the original widget at the drop location.
                - widget_height (int): The height of the widget being dropped.
        Notes:
            - The method calculates the grid position (row and column) by comparing the event's position
              with the global positions of widgets in the grid layout.
            - Assumes the parent widget has a `_actionsLayout` attribute that is a QGridLayout.
        """

        # Get the position as a point
        pos = e.position().toPoint()
        # Get the widget
        widget = e.source()
        # Get the grid layout
        parent = widget.parent().parent()
        # Define the placeholders for x- and y-coordinates as grid positions
        xPos = 0
        yPos = 0

        # Get the column
        Column = 0
        for Column in range(parent._actionsLayout.columnCount()):
            item = parent._actionsLayout.itemAtPosition(0, Column)
            if item is not None:
                w: QWidget = item.widget()
                Widget_X = w.parentWidget().mapTo(self, w.pos()).x()

                if pos.x() < Widget_X + w.size().width() // 2:
                    yPos = Column
                    break

        # Get the row
        Row = 0
        for Row in range(parent._actionsLayout.rowCount()):
            item = parent._actionsLayout.itemAtPosition(Row, Column)
            if item is not None:
                w: QWidget = item.widget()
                Widget_y = w.parentWidget().mapTo(self, w.pos()).y()

                if pos.y() < Widget_y:
                    xPos = Row
                    break

        w_origin = parent._actionsLayout.itemAtPosition(xPos, yPos).widget()
        # print(f"original button size: {w_origin.size().height()}")
        # print(f"drop button size: {widget.size().height()}")

        # Return then coordinates as grid positions
        return [xPos, yPos, w_origin.size(), widget.size()]
    
    # def UpdateRibbonStructure(self, WorkBenchName, panel: RibbonPanel, widget, text = "", size = "", ):
    #     gridLayout: QGridLayout = panel._actionsLayout
        
    #     # Get the order of the widgets
    #     orderList = []
    #     for k in range(gridLayout.count()):
    #         try:
    #             Control = gridLayout.itemAt(k).widget().children()[1]
    #             if type(Control) is RibbonToolButton:
    #                 for child in Control.children():
    #                     if (
    #                         type(child) == QToolButton
    #                         and child.objectName() == "CommandButton"
    #                     ):
    #                         orderList.append(child.defaultAction().data())
    #         except Exception:
    #             pass
            
    #     # Update the order in the ribbon structure
    #     StandardFunctions.add_keys_nested_dict(
    #         self.ribbonStructure,
    #         [
    #             "workbenches",
    #             WorkBenchName,
    #             "toolbars",
    #             panel.objectName(),
    #             "order",
    #         ],
    #     )
    #     self.ribbonStructure["workbenches"][WorkBenchName]["toolbars"][
    #         panel.objectName()
    #     ]["order"] = orderList
        
    #     # Update the command properties
    #     for widget in panel.widgets():
    #         action = None
    #         WidgetType = widget.objectName()
    #         size = "small"
    #         if WidgetType == "MediumWidget":
    #             size = "medium"
    #         if WidgetType == "LargeWidget":
    #             size = "large"
            
        
    #     # Writing to ribbonStructure.json
    #     JsonFile = Parameters_Ribbon.RIBBON_STRUCTURE_JSON
    #     with open(JsonFile, "w") as outfile:
    #         json.dump(self.ribbonStructure, outfile, indent=4)
    #     outfile.close()
        
    #     return

    # endregion


    # region - standard class functions
    #
    # implementation to add actions to the Filemenu. Needed for the accessories menu
    def addAction(self, action: QAction):
        menu = self.findChild(RibbonMenu, "Ribbon")
        StyleSheet_Menu = (
            "* {font-size: " + str(Parameters_Ribbon.FONTSIZE_MENUS) + "px;}"
        )
        menu.setStyleSheet(StyleSheet_Menu)
        if menu is None:
            menu = self.addFileMenu()
        menu.addAction(action)
        return

    # endregion

    # region - Standard ribbon functions
    def connectSignals(self):
        self.tabBar().currentChanged.connect(self.onUserChangedWorkbench)
        mw.workbenchActivated.connect(self.onWbActivated)
        return

    def disconnectSignals(self):
        self.tabBar().currentChanged.disconnect(self.onUserChangedWorkbench)
        mw.workbenchActivated.disconnect(self.onWbActivated)
        return

    def onUserChangedWorkbench(self, tabActivated=True):
        """
        Import selected workbench toolbars to ModernMenu section.
        """
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
                self.UnfoldRibbon()
            # else:
            #     self.FoldRibbon(True)

        index = self.tabBar().currentIndex()
        tabName = self.tabBar().tabText(index)

        if tabName is not None and tabName != "" and tabName != "test":
            # activate selected workbench
            tabName = tabName.replace("&", "")
            if self.wbNameMapping[tabName] is not None:
                Gui.activateWorkbench(self.wbNameMapping[tabName])

            if tabActivated is True:
                self.onWbActivated()
                self.ApplicationMenus()

            # hide normal toolbars
            self.hideClassicToolbars()

        # if self.DesignMenuLoaded is True:
        #     # Disable the quick toolbar, righttoolbar and application menu
        #     self.rightToolBar().setDisabled(True)
        #     self.quickAccessToolBar().setDisabled(True)
        #     self.applicationOptionButton().setDisabled(True)
        #     Gui.updateGui()
        return

    def onWbActivated(self):
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
                self.UnfoldRibbon()
            # else:
            #     self.FoldRibbon(True)

        # Set the text color depending in tabstyle
        if Parameters_Ribbon.TABBAR_STYLE != 1:
            self.tabBar().setStyleSheet(
                "QTabBar::tab {color: "
                + StyleMapping_Ribbon.ReturnStyleItem("FontColor")
                + ";}"
            )
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            self.tabBar().setStyleSheet(
                "QTabBar::tab {background: "
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color", True, True)
                + ";color: "
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color", True, True)
                + ";min-width: "
                + str(self.TabBar_Size-3)
                + "px;max-width: "
                + str(self.TabBar_Size-3)
                + "px;"
                + "padding-left: 6px;"
                + "padding-right: 3px;"
                + "margin: 3px"
                + ";}"
                + "QTabBar::tab:selected, QTabBar::tab:hover { "
                + "background: "
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + ";color: "
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + ";}"
            )

        # ensure that workbench is already loaded
        workbench = Gui.activeWorkbench()
        if not hasattr(workbench, "__Workbench__"):
            # XXX for debugging purposes
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(f"wb {workbench.MenuText} not loaded", "Log")

            # wait for 0.1s hoping that after that time the workbench is loaded
            timer.timeout.connect(self.onWbActivated)
            timer.setSingleShot(True)
            timer.start(1000)
            return

        # hide normal toolbars
        self.hideClassicToolbars()

        # switch tab if necessary
        self.updateCurrentTab()

        # create panels. Do this after updateCurrentTab.
        # Otherwise, the sketcher workbench won;t be loaded properly the first time
        self.buildPanels()

        # if self.DesignMenuLoaded is True:
        #     # Disable the quick toolbar, righttoolbar and application menu
        #     self.rightToolBar().setDisabled(True)
        #     self.quickAccessToolBar().setDisabled(True)
        #     self.applicationOptionButton().setDisabled(True)
        #     Gui.updateGui()
        return

    def onTabBarClicked(self):
        self.UnfoldRibbon()
        self.setRibbonVisible(True)

        # hide normal toolbars
        self.hideClassicToolbars()
        return

    def updateCurrentTab(self):
        currentWbIndex = self.tabBar().indexOf(Gui.activeWorkbench().MenuText)
        currentTabIndex = self.tabBar().currentIndex()

        if currentWbIndex != currentTabIndex:
            self.disconnectSignals()
            self.tabBar().setCurrentIndex(currentWbIndex)
            self.connectSignals()
        self.ApplicationMenus()

        if self.DesignMenuLoaded is True:
            # Disable the quick toolbar, righttoolbar and application menu
            self.rightToolBar().setDisabled(True)
            self.quickAccessToolBar().setDisabled(True)
            self.applicationOptionButton().setDisabled(True)
            Gui.updateGui()
        return

    # endregion

    # region - Functions for building the ribbon
    def createModernMenu(self):
        """
        Create menu tabs.
        """
        # Define a label for the menu
        Text = QLabel()
        Text.setText(translate("FreeCAD Ribbon", "Menu"))
        # Get its metrics
        FontMetrics = QFontMetrics(Text.font())
        # Define a layout and add the label
        Layout = QHBoxLayout()
        Layout.addWidget(Text, 0, Qt.AlignmentFlag.AlignRight)
        Layout.setContentsMargins(0, 0, 0, 0)
        # Add the layout to the menu button
        self.applicationOptionButton().setLayout(Layout)
        self.applicationOptionButton().setContentsMargins(0, 0, 9, 0)
        # Set the size of the menu button
        self.applicationOptionButton().setFixedSize(
            self.QuickAccessButtonSize
            + FontMetrics.boundingRect(Text.text()).width()
            + 12,
            self.QuickAccessButtonSize,
        )
        # Set the icon
        self.setApplicationIcon(Gui.getIcon("freecad"))
        # Set the styling of the button including padding (Text widht + 2*maring)
        self.applicationOptionButton().setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet(
                "applicationbutton",
                padding_right=str(FontMetrics.horizontalAdvance(Text.text(), -1) + 12)
                + "px",
                radius="4px",
            )
        )
        # Add the default tooltip
        self.applicationOptionButton().setToolTip(
            translate("FreeCAD Ribbon", "FreeCAD Ribbon")
        )

        # add the menus from the menubar to the application button
        self.ApplicationMenus()

        # add quick access buttons
        i = 1  # Start value for button count. Used for width of quickaccess toolbar
        toolBarWidth = (
            (self.QuickAccessButtonSize * self.sizeFactor) * i
        ) + self.applicationOptionButton().width()
        for commandName in self.ribbonStructure["quickAccessCommands"]:
            i = i + 1
            # Define a width
            width = 0
            # Define a button
            button = QToolButton()
            # set the default padding to zero
            padding = 0

            try:
                # If it is a standard freecad button, set the command accordingly
                if commandName.endswith("_ddb") is False:
                    try:
                        # Check if the workbench is loaded. If not, actions will be an empty list
                        # Find the command its workbench and activate it
                        QuickAction = Gui.Command.get(commandName).getAction()
                        if len(QuickAction) == 0:
                            for CommandItem in self.List_Commands:
                                if CommandItem[0] == commandName:
                                    Gui.activateWorkbench(CommandItem[3])
                                    break
                    except Exception:
                        pass
                    QuickAction = Gui.Command.get(commandName).getAction()

                    if len(QuickAction) == 1:
                        button.setDefaultAction(QuickAction[0])
                        width = self.QuickAccessButtonSize
                        height = self.QuickAccessButtonSize
                        button.setFixedSize(width, height)
                        # Set the stylesheet
                        button.setStyleSheet(
                            StyleMapping_Ribbon.ReturnStyleSheet(
                                "toolbutton", "2px", f"{padding}px"
                            )
                        )
                    elif len(QuickAction) > 1:
                        # set the padding for a dropdown button
                        padding = self.PaddingRight

                        button.addActions(QuickAction)
                        button.setDefaultAction(QuickAction[0])
                        # Set the width and height
                        width = self.QuickAccessButtonSize + padding
                        height = self.QuickAccessButtonSize
                        button.setFixedSize(width, height)
                        # Set the PopupMode
                        button.setPopupMode(
                            QToolButton.ToolButtonPopupMode.InstantPopup
                        )
                        # Set the stylesheet
                        button.setStyleSheet(
                            StyleMapping_Ribbon.ReturnStyleSheet(
                                "toolbutton", "2px", f"{padding}px"
                            )
                        )

                # If it is a custom dropdown, add the actions one by one.
                if commandName.endswith("_ddb") is True:
                    # set the padding for a dropdown button
                    padding = self.PaddingRight
                    # Get the actions and add them one by one
                    QuickAction = self.returnCustomDropDown(commandName)
                    for action in QuickAction:
                        if len(action) > 0:
                            button.addAction(action[0])
                    # Set the default action
                    button.setDefaultAction(button.actions()[0])
                    # Set the width and height
                    width = self.QuickAccessButtonSize + padding
                    height = self.QuickAccessButtonSize
                    button.setFixedSize(width, height)
                    # Set the PopupMode
                    button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

                    # Set the stylesheet
                    button.setStyleSheet(
                        StyleMapping_Ribbon.ReturnStyleSheet(
                            "toolbutton", "2px", padding_right=f"{padding}px"
                        )
                    )

                # Set the height
                self.setQuickAccessButtonHeight(self.RibbonMinimalHeight)

                button.setContentsMargins(3, 3, 3, 3)

                # Add the button to the quickaccess toolbar
                if len(button.actions()) > 0:
                    self.addQuickAccessButton(button)
                else:
                    StandardFunctions.Print(
                        f"{commandName} did not contain any actions!", "Log"
                    )

                toolBarWidth = toolBarWidth + width
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    StandardFunctions.Print(f"{commandName}, {e}", "Warning")
                # raise (e)
                continue

        self.quickAccessToolBar().show()
        # Set the height of the quickaccess toolbar
        self.quickAccessToolBar().setMinimumHeight(self.QuickAccessButtonSize)

        # Set the width of the quickaccess toolbar.
        self.quickAccessToolBar().setMinimumWidth(toolBarWidth)
        # Set the size policy
        self.quickAccessToolBar().setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        # needed for excluding from hiding toolbars
        self.quickAccessToolBar().setObjectName("quickAccessToolBar")
        self.quickAccessToolBar().setWindowTitle("quickAccessToolBar")

        # Set the tabbar height and textsize
        self.tabBar().setContentsMargins(0, 0, 0, 0)
        font = self.tabBar().font()
        font.setPixelSize(Parameters_Ribbon.FONTSIZE_TABS)
        self.tabBar().setFont(font)

        self.tabBar().setIconSize(QSize(self.TabBar_Size - 6, self.TabBar_Size - 6))
        self.tabBar().setStyleSheet(
            "margin: 0px;padding: 0px;height: " + str(self.TabBar_Size) + ";"
        )

        # Correct colors when no stylesheet is selected for FreeCAD.
        self.quickAccessToolBar().setStyleSheet("")
        if Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED is True:
            FreeCAD_preferences = App.ParamGet(
                "User parameter:BaseApp/Preferences/MainWindow"
            )
            currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")
            if currentStyleSheet == "":
                hexColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                # Set the quickaccess toolbar background color
                self.quickAccessToolBar().setStyleSheet(
                    "background-color: " + hexColor + ";"
                )

        # Get the order of workbenches from Parameters
        WorkbenchOrderedList: list = Parameters_Ribbon.TAB_ORDER.split(",")
        # Check if there are workbenches that are not in the orderlist
        IsInList = False
        for InstalledWB in Gui.listWorkbenches():
            for i in range(len(WorkbenchOrderedList)):
                if WorkbenchOrderedList[i] == InstalledWB:
                    IsInList = True
            if IsInList is False:
                WorkbenchOrderedList.append(InstalledWB)
            IsInList = False
        # There is an issue with the internal assembly wb showing the wrong panel
        # when assembly4 wb is installed and positioned for the internal assembly wb
        for i in range(len(WorkbenchOrderedList)):
            if (
                WorkbenchOrderedList[i] == "Assembly4Workbench"
                or WorkbenchOrderedList[i] == "Assembly3Workbench"
            ):
                try:
                    index_1 = WorkbenchOrderedList.index(WorkbenchOrderedList[i])
                    index_2 = WorkbenchOrderedList.index("AssemblyWorkbench")

                    WorkbenchOrderedList.pop(index_2)
                    WorkbenchOrderedList.insert(index_1, "AssemblyWorkbench")

                    break
                except Exception:
                    pass
        param_string = ""
        for i in range(len(WorkbenchOrderedList)):
            if WorkbenchOrderedList[i] != "":
                param_string = param_string + "," + WorkbenchOrderedList[i]
        Parameters_Ribbon.Settings.SetStringSetting("TabOrder", param_string)

        # add category for each workbench
        for i in range(len(WorkbenchOrderedList)):
            for workbenchName, workbench in list(Gui.listWorkbenches().items()):
                if workbenchName == WorkbenchOrderedList[i]:
                    name = workbench.MenuText.replace("&", "")
                    if (
                        name != ""
                        and name not in self.ribbonStructure["ignoredWorkbenches"]
                        and name != "<none>"
                        and name is not None
                    ):
                        self.wbNameMapping[name] = workbenchName
                        self.isWbLoaded[name] = False

                        # Set the title
                        category = self.addCategory(name)
                        category.setObjectName(workbenchName)

                        # Set the tabbar according the style setting
                        if Parameters_Ribbon.TABBAR_STYLE <= 1:
                            # set tab icon
                            icon: QIcon = self.ReturnWorkbenchIcon(workbenchName)
                            self.tabBar().setTabIcon(len(self.categories()) - 1, icon)
                        if Parameters_Ribbon.TABBAR_STYLE == 2:
                            self.tabBar().setTabIcon(
                                len(self.categories()) - 1, QIcon()
                            )

                        # Set the tab data
                        self.tabBar().setTabData(
                            len(self.categories()) - 1, workbenchName
                        )

                        # Set the tooltip
                        MenuText = workbench.MenuText
                        ToolTipText = workbench.ToolTip
                        if (
                            ToolTipText.lower() != MenuText.lower() + " workbench"
                            and MenuText.lower() != ToolTipText.lower()
                        ):
                            MenuText = (
                                f"<b>{workbench.MenuText}</b><br>{workbench.ToolTip}"
                            )
                        else:
                            MenuText = f"<b>{MenuText}<b>"

                        self.tabBar().setTabToolTip(
                            len(self.categories()) - 1, MenuText
                        )

        # Set the size of the collapseRibbonButton
        self.collapseRibbonButton().setFixedSize(
            self.RightToolBarButtonSize, self.RightToolBarButtonSize
        )

        # add the searchbar if available
        SearchBarWidth = self.AddSearchBar()
        if Parameters_Ribbon.TOOLBAR_POSITION == 0:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            spacer.setFixedWidth(10)
            if SearchBarWidth > 10:
                BeforeAction = self.rightToolBar().actions()[2]
            else:
                BeforeAction = self.rightToolBar().actions()[1]
            self.rightToolBar().insertWidget(BeforeAction, spacer)

        # add an overlay menu if Ribbon's overlay is enabled
        if self.OverlayMenu is not None:
            OverlayMenu = QToolButton()
            OverlayMenu.setIcon(QIcon(os.path.join(pathIcons, "Draft_Layer.svg")))
            OverlayMenu.setToolTip(
                translate("FreeCAD Ribbon", "Overlay functions") + "..."
            )
            OverlayMenu.setMenu(self.OverlayMenu)
            OverlayMenu.setFixedSize(
                self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize
            )
            OverlayMenu.setStyleSheet(
                StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton", padding_right="12px"
                )
            )
            OverlayMenu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            Font = OverlayMenu.font()
            Font.setPixelSize(Parameters_Ribbon.FONTSIZE_MENUS)
            OverlayMenu.setFont(Font)
            # add the settingsmenu to the right toolbar
            self.rightToolBar().addWidget(OverlayMenu)

        # add a settings button with menu
        SettingsMenu = QToolButton()
        # Get the freecad preference button
        editMenu = mw.findChildren(QMenu, "&Edit")[0]
        for action in editMenu.actions():
            if action.objectName() == "Std_DlgPreferences":
                preferenceButton_FreeCAD = action
                SettingsMenu.addAction(preferenceButton_FreeCAD)
        # Get the customize button from FreeCAD
        toolsMenu = mw.findChildren(QMenu, "&Tools")[0]
        for action in toolsMenu.actions():
            if action.objectName() == "Std_DlgCustomize":
                CustomizeButton_FreeCAD = action
                SettingsMenu.addAction(CustomizeButton_FreeCAD)
        # Add a save and restore button
        try:
            toolsMenu = mw.findChildren(QMenu, "&Tools")[0]
            for action in toolsMenu.actions():
                if action.objectName() == "SaveAndRestore":
                    SaveAndRestore = action
                    SettingsMenu.addAction(SaveAndRestore)
                    break
        except Exception:
            pass
        # add the ribbon settings menu
        SettingsMenu.addAction(self.RibbonMenu.menuAction())
        SettingsMenu.setIcon(Gui.getIcon("Std_DlgParameter.svg"))
        SettingsMenu.setToolTip(translate("FreeCAD Ribbon", "Preferences") + "...")
        SettingsMenu.setFixedSize(
            self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize
        )
        SettingsMenu.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet(
                control="toolbutton", padding_right="12px"
            )
        )
        SettingsMenu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        # add the settingsmenu to the right toolbar
        self.rightToolBar().addWidget(SettingsMenu)

        # Set the helpbutton
        self.helpRibbonButton().setEnabled(True)
        self.helpRibbonButton().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.helpRibbonButton().setToolTip(translate("FreeCAD Ribbon", "Help") + "...")
        # Get the default help action from FreeCAD
        helpMenu = mw.findChildren(QMenu, "&Help")[0]
        helpAction = helpMenu.actions()[0]
        self.helpRibbonButton().setIcon(helpAction.icon())
        self.helpRibbonButton().setMenu(self.HelpMenu)
        self.helpRibbonButton().setFixedSize(
            self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize
        )
        self.helpRibbonButton().setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet(
                control="toolbutton", padding_right="12px"
            )
        )
        self.helpRibbonButton().setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )

        # Add a button the enable or disable AutoHide
        pinButton = QToolButton()
        pinButton.setCheckable(True)
        pinButton.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        pinButton.setFixedSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize)
        # Set the correct icon
        pinButtonIcon = None
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButtonIcon = StyleMapping_Ribbon.ReturnStyleItem("PinButton_closed")
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButtonIcon = StyleMapping_Ribbon.ReturnStyleItem("PinButton_open")
        # Set the icon
        if pinButtonIcon is not None:
            pinButton.setIcon(pinButtonIcon)
        # Set the text and objectname
        pinButton.setText(translate("FreeCAD Ribbon", "Pin Ribbon"))
        pinButton.setObjectName("Pin Ribbon")
        # Set the correct checkstate
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButton.setChecked(False)
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButton.setChecked(True)
        pinButton.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet("toolbutton", "2px")
        )
        ShortcutKey = "Alt+T"
        try:
            CustomShortCuts = App.ParamGet(
                "User parameter:BaseApp/Preferences/Shortcut"
            )
            if "Ribbon_Pin" in CustomShortCuts.GetStrings():
                ShortcutKey = CustomShortCuts.GetString("Ribbon_Pin")
            if ShortcutKey != "" and ShortcutKey is not None:
                pinButton.setShortcut(ShortcutKey)
        except Exception:
            pass
        # Set the tooltip
        ToolTip = translate(
            "FreeCAD Ribbon", "Click to toggle the autohide function on or off"
        )
        if ShortcutKey != "none":
            ToolTip = ToolTip + f"<br></br><i>{ShortcutKey}</i>"
        pinButton.setToolTip(
            translate(
                "FreeCAD Ribbon",
                "Click to toggle the autohide function on or off"
                + f"<br></br><i>{ShortcutKey}</i>",
            )
        )

        # If FreeCAD's overlay function is active, set the pinbutton to checked and then to disabled
        preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
        if preferences.GetBool("ActivateOverlay") is True:
            pinButton.setChecked(True)
            pinButton.setDisabled(True)
        else:
            pinButton.clicked.connect(self.on_Pin_clicked)
            self.rightToolBar().addWidget(pinButton)

        # if the FreeCAD titlebar is hidden,add close, minimize and maximize buttons
        if Parameters_Ribbon.HIDE_TITLEBAR_FC is True:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            spacer.setFixedWidth(30)
            if Parameters_Ribbon.TOOLBAR_POSITION == 1:
                spacer.setFixedWidth(5)
            self.rightToolBar().addWidget(spacer)

            # Minimize button
            MinimzeButton = QToolButton()
            MinimzeButton.setStyleSheet(
                StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                    padding_left="3px",
                    padding_top="3px",
                    padding_bottom="3px",
                    padding_right="3px",
                )
            )
            MinimzeButton.setIcon(
                StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[3]
            )
            MinimzeButton.clicked.connect(self.MinimizeFreeCAD)
            MinimzeButton.setFixedSize(
                self.RightToolBarButtonSize, self.RightToolBarButtonSize
            )
            self.rightToolBar().addWidget(MinimzeButton)
            # Restore button
            RestoreButton = QToolButton()
            RestoreButton.setObjectName("RestoreButton")
            RestoreButton.setStyleSheet(
                StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                    padding_left="3px",
                    padding_top="3px",
                    padding_bottom="3px",
                    padding_right="3px",
                )
            )
            RestoreButton.setIcon(
                StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[2]
            )
            RestoreButton.clicked.connect(self.RestoreFreeCAD)
            RestoreButton.setFixedSize(
                self.RightToolBarButtonSize, self.RightToolBarButtonSize
            )
            self.rightToolBar().addWidget(RestoreButton)
            # Close button
            CloseButton = QToolButton()
            CloseButton.setStyleSheet(
                StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                    padding_left="3px",
                    padding_top="3px",
                    padding_bottom="3px",
                    padding_right="3px",
                    HoverColor="#e62424",
                )
            )
            CloseButton.setIcon(
                StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[0]
            )
            CloseButton.clicked.connect(self.CloseFreeCAD)
            CloseButton.setFixedSize(
                self.RightToolBarButtonSize, self.RightToolBarButtonSize
            )
            self.rightToolBar().addWidget(CloseButton)

        # Add a switch to enable beta functions
        BetaLabel = QLabel(translate("FreeCAD Ribbon", "Experimental functions"))
        BeforeAction = self.rightToolBar().actions()[1]
        self.rightToolBar().insertWidget(BeforeAction, BetaLabel)
        switch = Toggle()
        switch.setObjectName("bétaSwitch")
        switch.setToolTip(translate("FreeCAD Ribbon",
    """
    Right click on the ribbon (outside the buttons) and click customize.
    The customization enviroment is enabled.
    Now right click on any button to change its properties.
    Current functions are:
    - Enable text
    - Set the icon size
    - Set the button type to:
        - Small  -> three rows of buttons, text on the right side.
        - Medium -> two rows of buttons, text on the right side.
        - Large -> One button row, text below the button.
    """
    ))
        switch.setMaximumHeight(self.RightToolBarButtonSize)
        switch.setMaximumWidth(self.RightToolBarButtonSize * 1.8)
        switch.toggled.connect(
            lambda: self.on_ToggleBetaFunctions_toggled(switch.isChecked())
        )
        BeforeAction = self.rightToolBar().actions()[2]
        self.rightToolBar().insertWidget(BeforeAction, switch)

        # Set the width of the right toolbar
        RightToolbarWidth = (
            SearchBarWidth
            + 3 * (self.RightToolBarButtonSize + 16)
            + self.RightToolBarButtonSize
        )
        if Parameters_Ribbon.USE_FC_OVERLAY is True:
            RightToolbarWidth = SearchBarWidth + 2 * (self.RightToolBarButtonSize + 16)
        self.rightToolBar().setMinimumWidth(RightToolbarWidth)
        self.setRightToolBarHeight(self.RibbonMinimalHeight)
        # Set the size policy
        self.rightToolBar().setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        self.rightToolBar().setSizeIncrement(1, 1)
        # Set the objectName for the right toolbar. needed for excluding from hiding.
        self.rightToolBar().setObjectName("rightToolBar")
        return

    # Add the searchBar if it is present
    def AddSearchBar(self):
        TB: QToolBar = mw.findChildren(QToolBar, "SearchBar")
        width = 10
        if TB is not None:
            try:
                import SearchBoxLight

                width = 10 * self.RightToolBarButtonSize

                sea = SearchBoxLight.SearchBoxLight(
                    getItemGroups=lambda: __import__("GetItemGroups").getItemGroups(),
                    getToolTip=lambda groupId, setParent: __import__(
                        "GetItemGroups"
                    ).getToolTip(groupId, setParent),
                    getItemDelegate=lambda: __import__(
                        "IndentedItemDelegate"
                    ).IndentedItemDelegate(),
                )
                sea.resultSelected.connect(
                    lambda index, groupId: __import__("GetItemGroups").onResultSelected(
                        index, groupId
                    )
                )
                sea.setFixedSize(width, self.RightToolBarButtonSize)
                BeforeAction = self.rightToolBar().actions()[1]
                self.rightToolBar().insertWidget(BeforeAction, sea)
                # width = sea.width()
            except Exception:
                pass
        return width

    # Function to create the application menu
    def ApplicationMenus(self):
        # Add a file menu
        ApplictionMenu = self.addFileMenu()

        # add the menus from the menubar to the application button
        MenuBar = mw.menuBar()

        # Set a stylesheet specific for the menubar. Otherwise the fontsize of the menus will not be applied
        StyleSheet_MenuBar = (
            "* {font-size: " + str(Parameters_Ribbon.FONTSIZE_MENUS) + "px;}"
        )
        MenuBar.setStyleSheet(StyleSheet_MenuBar)
        # # Add the actions of the menubar to the application menu
        for child in MenuBar.actions():
            if child.objectName() != "&Help" and child.objectName != "AccessoriesMenu":
                ApplictionMenu.addAction(child)
            if (
                child.objectName == "AccessoriesMenu"
                and self.AccessoriesMenu is not None
            ):
                ApplictionMenu.addMenu(self.AccessoriesMenu)

        # if you on macOS, add the ribbon menus to the menubar
        if platform.system().lower() == "darwin":
            for action in MenuBar.actions():
                if action.text() == translate("FreeCAD Ribbon", "Ribbon UI"):
                    MenuBar.removeAction(action)
                    break

            beforeAction = None
            for child in MenuBar.children():
                if child.objectName() == "&Windows":
                    beforeAction = child.menuAction()
                    Menu = self.RibbonMenu
                    Menu.setTitle(translate("FreeCAD Ribbon", "Ribbon UI"))
                    MenuBar.insertMenu(beforeAction, self.RibbonMenu)
                    # Remove the menu from the Ribbon Application Menu
                    for action in ApplictionMenu.actions():
                        if action.text() == translate("FreeCAD Ribbon", "Ribbon UI"):
                            ApplictionMenu.removeAction(action)
                            break

        # if you are on a developer version, add a label
        if self.DeveloperVersion != "":
            ApplictionMenu.addSeparator()
            color = StyleMapping_Ribbon.ReturnStyleItem("DevelopColor")
            Label = QLabel()
            Label.setText("Development version")
            Label.setStyleSheet(
                f"color: {color};border: 1px solid {color};border-radius: 2px;"
            )
            ApplictionMenu.addWidget(Label)
        # if there is an update, add a button that opens the addon manager
        if self.UpdateVersion != "" and self.DeveloperVersion == "":
            ApplictionMenu.addSeparator()
            color = StyleMapping_Ribbon.ReturnStyleItem("UpdateColor")
            Button = QToolButton()
            Button.setText(translate("FreeCAD Ribbon", "Update available"))
            Button.setStyleSheet(
                "QToolButton{"
                + f"color: {color};border: 1px solid {color};border-radius: 2px;background: none"
                + "}QToolButton:hover{background-color: "
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + ";}"
            )

            def OpenAddOnManager():
                Gui.runCommand("Std_AddonMgr", 0)

            Button.clicked.connect(OpenAddOnManager)
            ApplictionMenu.addWidget(Button)

        return

    # Function to create the extra menus on the right toolbar
    def CreateMenus(self):
        MenuBar = mw.menuBar()

        # Create a accessories menu
        AccessoriesMenu = None
        for action in MenuBar.children():
            if action.objectName() == "AccessoriesMenu":
                AccessoriesMenu = action.menu()
                self.AccessoriesMenu = QMenu()
                subMenus = []
                for subAction in AccessoriesMenu.actions():
                    subMenus.append(subAction)
                self.AccessoriesMenu.addActions(subMenus)

        # Create the overlay menu when the native overlay function is not used
        if (
            Parameters_Ribbon.USE_FC_OVERLAY is False
            and Parameters_Ribbon.USE_OVERLAY is True
        ):
            OverlayMenu = QMenu(translate("FreeCAD Ribbon", "Overlay") + "...", self)
            OverlayMenu.setToolTipsVisible(True)

            # Toggle overlay for all -----------------------------------------------------
            OverlayButton_All = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle overlay for all")
            )
            OverlayButton_All.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the overlay function for all panels",
                )
            )
            OverlayButton_All.triggered.connect(self.ToggleOverlay_All)
            # Get the shortcut from the original command
            ShortcutKey = "F4"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayAll" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString("Std_DockOverlayAll")
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "F4"
            OverlayButton_All.setShortcut(ShortcutKey)

            # Toggle transparancy for all -----------------------------------------------------
            TransparancyButton_All = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle transparancy")
            )
            TransparancyButton_All.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Toggle transparancy for all panels when overlay is enabled",
                )
            )
            TransparancyButton_All.triggered.connect(self.CustomTransparancy)
            # Get the shortcut from the original command
            ShortcutKey = "Shift+F4"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayTransparentAll" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString(
                        "Std_DockOverlayTransparentAll"
                    )
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "Shift+F4"
            TransparancyButton_All.setShortcut(ShortcutKey)

            OverlayMenu.addSeparator()
            # Toggle overlay for active panel-----------------------------------------------------
            OverlayButton_Active = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle overlay")
            )
            OverlayButton_Active.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the overlay function for the active panel",
                )
            )
            OverlayButton_Active.triggered.connect(self.CustomOverlay_Focus)
            # Get the shortcut from the original command
            ShortcutKey = "F3"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayToggle" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString("Std_DockOverlayToggle")
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "F3"
            OverlayButton_Active.setShortcut(ShortcutKey)

            # Toggle transparancy for active panel-----------------------------------------------------
            TransparancyButton = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle transparant mode")
            )
            TransparancyButton.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Toggle transparancy for the active panel when overlay is enabled",
                )
            )
            TransparancyButton.triggered.connect(self.CustomTransparancy_Focus)
            # Get the shortcut from the original command
            ShortcutKey = "Shift+F3"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayToggleTransparent" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString(
                        "Std_DockOverlayToggleTransparent"
                    )
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "Shift+F3"
            TransparancyButton.setShortcut(ShortcutKey)

            OverlayMenu.addSeparator()
            # Toggle mouse bypass-----------------------------------------------------
            ToggleMouseByPass = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Bypass mouse events")
            )
            ToggleMouseByPass.setToolTip(
                translate(
                    "FreeCAD Ribbon", "Bypass mouse events in docked overlay windows"
                )
            )
            ToggleMouseByPass.triggered.connect(self.ToggleMouseByPass)
            # Get the shortcut from the original command
            ShortcutKey = "T,T"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayMouseTransparent" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString(
                        "Std_DockOverlayMouseTransparent"
                    )
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "T,T"
            ToggleMouseByPass.setShortcut(ShortcutKey)

            OverlayMenu.addSeparator()
            # Toggle overlay for left panels-----------------------------------------------------
            OverlayButton_Left = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle left")
            )
            OverlayButton_Left.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the overlay function for the active panel",
                )
            )
            OverlayButton_Left.triggered.connect(self.ToggleOverlay_Left)
            # Get the shortcut from the original command
            ShortcutKey = "Ctrl+left"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayToggleLeft" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString("Std_DockOverlayToggleLeft")
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "Ctrl+left"
            OverlayButton_Left.setShortcut(ShortcutKey)
            # Toggle overlay for right panels-----------------------------------------------------
            OverlayButton_Right = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle right")
            )
            OverlayButton_Right.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the overlay function for the active panel",
                )
            )
            OverlayButton_Right.triggered.connect(self.ToggleOverlay_Right)
            # Get the shortcut from the original command
            ShortcutKey = "Ctrl+right"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayToggleRight" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString(
                        "Std_DockOverlayToggleRight"
                    )
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "Ctrl+right"
            OverlayButton_Right.setShortcut(ShortcutKey)
            # Toggle overlay for Bottom panels-----------------------------------------------------
            OverlayButton_Bottom = OverlayMenu.addAction(
                translate("FreeCAD Ribbon", "Toggle bottom")
            )
            OverlayButton_Bottom.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the overlay function for the active panel",
                )
            )
            OverlayButton_Bottom.triggered.connect(self.ToggleOverlay_Bottom)
            # Get the shortcut from the original command
            ShortcutKey = "Ctrl+down"
            try:
                CustomShortCuts = App.ParamGet(
                    "User parameter:BaseApp/Preferences/Shortcut"
                )
                if "Std_DockOverlayToggleBottom" in CustomShortCuts.GetStrings():
                    ShortcutKey = CustomShortCuts.GetString(
                        "Std_DockOverlayToggleBottom"
                    )
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    print(e.with_traceback())
                ShortcutKey = "Ctrl+down"
            OverlayButton_Bottom.setShortcut(ShortcutKey)

            # Store the overlay menu
            self.OverlayMenu = OverlayMenu

        # Create a ribbon menu
        RibbonMenu = QMenu(
            translate("FreeCAD Ribbon", "Ribbon UI preferences") + " ...", self
        )
        RibbonMenu.setToolTipsVisible(True)
        # Add the ribbon design button
        DesignButton = RibbonMenu.addAction(
            translate("FreeCAD Ribbon", "Ribbon layout")
        )
        DesignButton.setToolTip(
            translate("FreeCAD Ribbon", "Design the ribbon to your preference")
        )
        DesignButton.triggered.connect(self.loadDesignMenu)
        ShortcutKey = "Alt+L"
        try:
            CustomShortCuts = App.ParamGet(
                "User parameter:BaseApp/Preferences/Shortcut"
            )
            if "Ribbon_Layout" in CustomShortCuts.GetStrings():
                ShortcutKey = CustomShortCuts.GetString("Ribbon_Layout")
        except Exception:
            pass
        if ShortcutKey != "" and ShortcutKey is not None:
            DesignButton.setShortcut(ShortcutKey)
            self.LayoutMenuShortCut = ShortcutKey
        # Add the preference button
        PreferenceButton = RibbonMenu.addAction(
            translate("FreeCAD Ribbon", "Preferences")
        )
        PreferenceButton.setToolTip(
            translate("FreeCAD Ribbon", "Set preferences for the Ribbon UI")
        )
        PreferenceButton.setMenuRole(QAction.MenuRole.NoRole)
        PreferenceButton.triggered.connect(self.loadSettingsMenu)
        ShortcutKey = "Alt+P"
        try:
            CustomShortCuts = App.ParamGet(
                "User parameter:BaseApp/Preferences/Shortcut"
            )
            if "Ribbon_Preferences" in CustomShortCuts.GetStrings():
                ShortcutKey = CustomShortCuts.GetString("Ribbon_Preferences")
        except Exception:
            pass
        if ShortcutKey != "" and ShortcutKey is not None:
            PreferenceButton.setShortcut(ShortcutKey)
        # Add the script submenu with items
        ScriptDir = os.path.join(os.path.dirname(__file__), "Scripts")
        if os.path.exists(ScriptDir) is True:
            ListScripts = os.listdir(ScriptDir)
            if len(ListScripts) > 0:
                ScriptButtonMenu = RibbonMenu.addMenu(
                    translate("FreeCAD Ribbon", "Scripts")
                )
                ScriptButtonMenu.setToolTip(
                    translate("FreeCAD Ribbon", "Scripts to help setup the ribbon.")
                )
                for i in range(len(ListScripts)):
                    ScriptButtonMenu.addAction(
                        ListScripts[i],
                        lambda i=i + 1: self.LoadMarcoFreeCAD(ListScripts[i - 1]),
                    )
        # Set the RibbonMenu
        self.RibbonMenu = RibbonMenu

        # Create a help menu
        HelpMenu = QMenu(self)
        HelpMenu.setToolTipsVisible(True)
        # Get the icons
        HelpIcon = QIcon()
        AboutIcon = Gui.getIcon("freecad")

        actions = [QAction()]

        # Get the standard help menu from FreeCAD
        for action in MenuBar.children():
            if action.objectName() == "&Help":
                actions = action.actions()
                # change help to FreeCAD help
                actions[0].setText(translate("FreeCAD Ribbon", "Help"))
                HelpMenu.addActions(actions)
                # Store the help icon for the Ribbon help
                HelpIcon = action.actions()[0].icon()
                # Remove the menu from the Ribbon Application Menu
                MenuBar.removeAction(action.menuAction())

        # Add the ribbon helpbutton under the FreeCAD
        RibbonHelpButton = QAction(translate("FreeCAD Ribbon", "Ribbon UI help"))
        RibbonHelpButton.setToolTip(
            translate(
                "FreeCAD Ribbon", "Open the help page for the Ribbon UI in your browser"
            )
        )
        RibbonHelpButton.setIcon(HelpIcon)
        RibbonHelpButton.triggered.connect(self.on_RibbonHelpButton_clicked)
        HelpMenu.insertAction(actions[1], RibbonHelpButton)

        # create an about button to store FreeCAD about, Ribbon about and what's new
        AboutMenu = QMenu(translate("FreeCAD Ribbon", "About") + " ...", self)
        # set the icon for the menu
        AboutMenu.setIcon(AboutIcon)
        # get the the about button from freecad
        AboutAction_FreeCAD = actions[len(actions) - 1]
        for action in actions:
            if action.menuRole() == QAction.MenuRole.AboutRole:
                AboutAction_FreeCAD = action
                AboutAction_FreeCAD.setIcon(AboutIcon)
        # add the FreeCAd about button to the aboutmenu
        AboutMenu.addAction(AboutAction_FreeCAD)
        # remove the FreeCAd about button from the help menu
        HelpMenu.removeAction(AboutAction_FreeCAD)
        # Get the version of this addon
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        version = StandardFunctions.ReturnXML_Value(PackageXML, "version")
        # Create the ribbon about button
        AboutButton_Ribbon = AboutMenu.addAction(
            translate("FreeCAD Ribbon", "About Ribbon UI ") + version
        )
        AboutButton_Ribbon.setIcon(AboutIcon)
        AboutButton_Ribbon.triggered.connect(self.on_AboutButton_clicked)
        # Create the what's new button
        WhatsNewButton_Ribbon = AboutMenu.addAction(
            translate("FreeCAD Ribbon", "What's new?")
        )
        WhatsNewButton_Ribbon.triggered.connect(self.on_WhatsNewButton_clicked)
        # add the aboutmenu to the help menu
        HelpMenu.addMenu(AboutMenu)

        self.HelpMenu = HelpMenu
        return

    # Function for loading the design menu
    def loadDesignMenu(self):
        # Get the form
        Dialog = LoadDesign_Ribbon.LoadDialog()
        # Show the form
        Dialog.form.show()

        # Disable the quick toolbar, righttoolbar and application menu
        self.rightToolBar().setDisabled(True)
        self.quickAccessToolBar().setDisabled(True)
        self.applicationOptionButton().setDisabled(True)
        Gui.updateGui()
        # indicate that the design menu is loaded
        self.DesignMenuLoaded = True

        # Connect the close signal of the designmenu
        Dialog.closeSignal.connect(self.EnableRibbonToolbarsAndMenus)

        return

    # Function for loading the settings menu
    def loadSettingsMenu(self):
        # Get the form
        Dialog = LoadSettings_Ribbon.LoadDialog()
        # Show the form
        Dialog.form.show()

        # Disable the quick toolbar, righttoolbar and application menu
        self.rightToolBar().setDisabled(True)
        self.quickAccessToolBar().setDisabled(True)
        self.applicationOptionButton().setDisabled(True)
        Gui.updateGui()
        # indicate that the design menu is loaded
        self.DesignMenuLoaded = True

        # Connect the close signal of the designmenu
        Dialog.closeSignal.connect(self.EnableRibbonToolbarsAndMenus)

        return

    # Function to activate the toolbars and menus
    # after closing the design menu or settings menu
    def EnableRibbonToolbarsAndMenus(self):
        self.rightToolBar().setEnabled(True)
        self.quickAccessToolBar().setEnabled(True)
        self.applicationOptionButton().setEnabled(True)
        Gui.updateGui()

        # self.loadDesignMenu = False

        return

    def buildPanels(self):
        processedPanels = []
        # Get the active workbench and get its name
        #
        workbenchTitle = self.tabBar().tabText(self.tabBar().currentIndex())
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        if workbenchName is None:
            return

        # check if the panel is already loaded. If so exit this function
        tabName = workbenchTitle
        if tabName in self.isWbLoaded and (self.isWbLoaded[tabName] or tabName == ""):
            return

        workbench = Gui.getWorkbench(workbenchName)
        # Get the list of toolbars from the active workbench
        ListToolbars: list = workbench.listToolbars()
        # Get custom toolbars that are created in the toolbar environment and add them to the list of toolbars
        CustomToolbars = self.List_ReturnCustomToolbars()
        for CustomToolbar in CustomToolbars:
            # Check if a toolbar with the same name already exists
            isInList = False
            for ToolBar in ListToolbars:
                if ToolBar == CustomToolbar[0]:
                    isInList = True
            # if the toolbar doesn't exist yet and is part of this workbench, add it.
            if CustomToolbar[1] == workbenchName and isInList is False:
                ListToolbars.append(CustomToolbar[0])
        # Get the global custom toolbars that are created in the toolbar environment and add them to the list of toolbars
        CustomToolbars_Global = self.List_ReturnCustomToolbars_Global()
        for CustomToolbar in CustomToolbars_Global:
            ListToolbars.append(CustomToolbar[0])

        # Get the custom panels and add them to the list of toolbars
        try:
            if workbenchName in self.ribbonStructure["customToolbars"]:
                for CustomPanel in self.ribbonStructure["customToolbars"][
                    workbenchName
                ]:
                    ListToolbars.append(CustomPanel)

                    # remove the original toolbars from the list
                    Commands = self.ribbonStructure["customToolbars"][workbenchName][
                        CustomPanel
                    ]["commands"]
                    for Command in Commands:
                        try:
                            OriginalToolbar = self.ribbonStructure["customToolbars"][
                                workbenchName
                            ][CustomPanel]["commands"][Command]

                            # ignore cases to prevent issues with different versions of FreeCAD
                            for item in ListToolbars:
                                if OriginalToolbar.lower() == item.lower():
                                    OriginalToolbar = item

                            ListToolbars.remove(OriginalToolbar)
                        except Exception:
                            continue
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(f"{e}, 1", "Warning")
            pass

        # Add the new panels to the toolbar list
        try:
            for WorkBenchItem in self.ribbonStructure["newPanels"]:
                if WorkBenchItem == workbenchName or WorkBenchItem == "Global":
                    for Panel in self.ribbonStructure["newPanels"][WorkBenchItem]:
                        ListToolbars.append(Panel)
        except Exception:
            pass

        try:
            # Get the order of toolbars
            ToolbarOrder: list = self.ribbonStructure["workbenches"][workbenchName][
                "toolbars"
            ]["order"]

            # Sort the list of toolbars according the toolbar order
            def SortToolbars(toolbar):
                if toolbar == "":
                    return -1

                position = None
                try:
                    position = ToolbarOrder.index(toolbar) + 1
                except ValueError:
                    position = 999999
                    if toolbar.endswith("_custom") or toolbar.endswith("_newPanel"):
                        if Parameters_Ribbon.DEFAULT_PANEL_POSITION_CUSTOM == "Right":
                            position = 999999
                        else:
                            position = 0
                return position

            ListToolbars.sort(key=SortToolbars)
        except Exception:
            pass
      
        # If the toolbar must be ignored, skip it        
        for toolbar in ListToolbars:
            Skip = False
            for ToolbarToIgnore in self.ribbonStructure["ignoredToolbars"]:
                if toolbar.lower() == ToolbarToIgnore.lower():
                    Skip = True
            if toolbar == "" or Skip is True:
                continue
            if toolbar in self.currentCategory().panels().keys():
                continue

            # Create the panel, use the toolbar name as title
            title = StandardFunctions.TranslationsMapping(workbenchName, toolbar)
            panel: RibbonPanel = self.currentCategory().addPanel(
                title=title,
                showPanelOptionButton=True,
            )
            panel.setObjectName(toolbar)
            panel.panelOptionButton().hide()
            panel.setAcceptDrops(True)

            # get list of all buttons in toolbar
            allButtons: list = []
            try:
                TB = mw.findChildren(QToolBar, toolbar)
                allButtons = TB[0].findChildren(QToolButton)
                # remove empty buttons
                for i in range(len(allButtons)):
                    button: QToolButton = allButtons[i]
                    if allButtons[i].text() == "":
                        allButtons.pop(i)
            except Exception:
                pass

            # Add custom panels
            customList = self.List_AddCustomToolBarToWorkbench(workbenchName, toolbar)
            allButtons.extend(customList)

            # Add new Panels
            NewPanelList = self.List_AddNewPanelToWorkbench(workbenchName, toolbar)
            allButtons.extend(NewPanelList)
            # Add new global Panels
            NewPanelList = self.List_AddNewPanelToWorkbench("Global", toolbar)
            allButtons.extend(NewPanelList)

            # add separators to the command list.
            if workbenchName in self.ribbonStructure["workbenches"]:
                if (
                    toolbar != ""
                    and toolbar
                    in self.ribbonStructure["workbenches"][workbenchName]["toolbars"]
                ):
                    for orderedToolbar in self.ribbonStructure["workbenches"][
                        workbenchName
                    ]["toolbars"]:
                        if orderedToolbar.lower() == toolbar.lower():
                            if (
                                "order"
                                in self.ribbonStructure["workbenches"][workbenchName][
                                    "toolbars"
                                ][toolbar]
                            ):
                                for j in range(
                                    len(
                                        self.ribbonStructure["workbenches"][
                                            workbenchName
                                        ]["toolbars"][toolbar]["order"]
                                    )
                                ):
                                    if (
                                        "separator"
                                        in self.ribbonStructure["workbenches"][
                                            workbenchName
                                        ]["toolbars"][toolbar]["order"][j].lower()
                                    ):
                                        separator = QToolButton()
                                        separator.setText(
                                            self.ribbonStructure["workbenches"][
                                                workbenchName
                                            ]["toolbars"][toolbar]["order"][j]
                                        )
                                        allButtons.insert(j, separator)

            if workbenchName in self.ribbonStructure["workbenches"]:
                # order buttons like defined in ribbonStructure
                if (
                    toolbar
                    in self.ribbonStructure["workbenches"][workbenchName]["toolbars"]
                    and "order"
                    in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][
                        toolbar
                    ]
                ):
                    OrderList: list = self.ribbonStructure["workbenches"][
                        workbenchName
                    ]["toolbars"][toolbar]["order"]

                    # XXX check that positionsList consists of strings only
                    def sortButtons(button: QToolButton):
                        # Use the text from the button
                        Text = button.text()
                        if (
                            StandardFunctions.checkFreeCADVersion(
                                Parameters_Ribbon.FreeCAD_Version["mainVersion"],
                                Parameters_Ribbon.FreeCAD_Version["subVersion"],
                                Parameters_Ribbon.FreeCAD_Version["patchVersion"],
                                Parameters_Ribbon.FreeCAD_Version["gitVersion"],
                            )
                            is True
                        ):
                            # if it is not a custom button or separator, update the Text
                            if not "ddb" in Text and not "separator" in Text:
                                if (
                                    button.actions()[0].data() != ""
                                    and button.actions()[0].data() is not None
                                ):
                                    Text = button.actions()[0].data()

                        position = None
                        try:
                            position = OrderList.index(Text)
                        except ValueError:
                            position = 999999

                        return position

                    allButtons.sort(key=sortButtons)

            # add buttons to panel
            shadowList = (
                []
                # if buttons are used in multiple workbenches, they can show up double. (Sketcher_NewSketch)
            )
            # for button in allButtons:
            # needed to count the number of small buttons in a column. (bug fix with adding separators)
            NoSmallButtons_spacer = 0
            # needed to count the number of medium buttons in a column. (bug fix with adding separators)
            NoMediumButtons_spacer = 0

            # Define number of rows used per button size
            LargeButtonRows = 3
            MediumButtonRows = 2
            SmallButtonRows = 1
            # Define the rowCount and column count
            rowCount = 0
            columnCount = 0
            # Set the maximum columns
            maxColumns = Parameters_Ribbon.MAX_COLUMN_PANELS

            # Define an action list of the actions that are byond the maximum columns
            ButtonList = []

            # Go through the button list:
            for i in range(len(allButtons)):
                button = allButtons[i]

                # count the number of buttons per type. Needed for proper sorting the buttons later.
                buttonSize = "small"
                try:
                    action = button.defaultAction()
                    buttonSize = self.ribbonStructure["workbenches"][workbenchName][
                        "toolbars"
                    ][toolbar]["commands"][action.data()]["size"]
                    if buttonSize == "small":
                        NoSmallButtons_spacer += 1
                    if buttonSize == "medium":
                        NoMediumButtons_spacer += 1
                except Exception:
                    pass

                # Panel overflow behaviour ----------------------------------------------------------------
                #
                # get the number of rows in the panel
                if buttonSize == "small":
                    rowCount = rowCount + SmallButtonRows
                if buttonSize == "medium":
                    rowCount = rowCount + MediumButtonRows
                if buttonSize == "large" or "separator" in button.text():
                    rowCount = rowCount + LargeButtonRows

                # If the number of rows divided by 3 is a whole number,
                # the number of columns is the rowcount divided by 3.
                columnCount = math.ceil(rowCount / 3)
                # if buttonSize == "medium":
                #     columnCount = rowCount / 2
                # if buttonSize == "large":
                #     columnCount = rowCount
                # ----------------------------------------------------------------------------------------

                # if the button has not text, remove it, skip it and increase the counter.
                if button.text() == "":
                    continue
                # If the command is already there, remove it, skip it and increase the counter.
                elif shadowList.__contains__(button.text()) is True:
                    continue
                else:
                    # If the number of columns is more than allowed,
                    # Add the actions to the OptionPanel instead.
                    if maxColumns > 0:
                        # if the last item before the optionpanel is an separator, skip it
                        if columnCount > maxColumns and "separator" in button.text():
                            continue
                        if columnCount > maxColumns + 2:
                            ButtonList.append(button)
                            panel.panelOptionButton().show()
                            continue

                    # If the last item is not an separator, you can add an separator
                    # With an paneloptionbutton, use an offset of 2 instead of 1 for i.
                    if "separator" in button.text() and i < len(allButtons):
                        separator = panel.addLargeVerticalSeparator(
                            width=6,
                            alignment=Qt.AlignmentFlag.AlignCenter,
                            fixedHeight=False,
                        )
                        separator.setObjectName("separator")
                        # there is a bug in pyqtribbon where the separator is placed in the wrong position
                        # despite the correct order of the button list.
                        # To correct this, empty and disabled buttons are added for spacing.
                        # (adding spacers did not work)
                        if float((NoSmallButtons_spacer + 1) / 3).is_integer():
                            spacer_1 = panel.addSmallButton()
                            spacer_1.setFixedWidth(self.iconSize)
                            spacer_1.setEnabled(False)
                            spacer_1.setStyleSheet("background-color: none")
                        if float((NoSmallButtons_spacer + 2) / 3).is_integer():
                            spacer_1 = panel.addSmallButton()
                            spacer_1.setFixedWidth(self.iconSize)
                            spacer_1.setEnabled(False)
                            spacer_1.setStyleSheet("background-color: none")
                            spacer_2 = panel.addSmallButton()
                            spacer_2.setFixedWidth(self.iconSize)
                            spacer_2.setEnabled(False)
                            spacer_2.setStyleSheet("background-color: none")
                        # reset the counter after a separator is added.
                        NoSmallButtons_spacer = 0
                        # Same principle for medium buttons
                        if float((NoMediumButtons_spacer + 1) / 2).is_integer():
                            spacer_1 = panel.addMediumButton()
                            spacer_1.setFixedWidth(Parameters_Ribbon.ICON_SIZE_MEDIUM)
                            spacer_1.setEnabled(False)
                            spacer_1.setStyleSheet("background-color: none")
                        NoMediumButtons_spacer = 0
                        continue
                    else:
                        try:
                            action = button.defaultAction()

                            # get the action text
                            text = action.text()
                            try:
                                # If the text is not from a hardcoded dropdown:
                                if len(action.data().split(", ")) <= 1:
                                    text = StandardFunctions.CommandInfoCorrections(
                                        action.data()
                                    )["ActionText"]
                            except Exception:
                                pass

                            # try to get alternative text from ribbonStructure
                            try:
                                textJSON = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][action.data()][
                                    "text"
                                ]

                                # There is a bug in freecad with the comp-sketch menu hase the wrong text
                                if (
                                    action.data() == "PartDesign_CompSketches"
                                    and self.ribbonStructure["workbenches"][
                                        workbenchName
                                    ]["toolbars"][toolbar]["commands"][action.data()][
                                        "text"
                                    ]
                                    == "Create datum"
                                ):
                                    textJSON = "Create sketch"

                                # Check if the original menutext is different
                                # if so use the alternative, otherwise use original
                                for CommandName in Gui.listCommands():
                                    # if it is a normal command:
                                    if len(action.data().split(", ")) <= 1:
                                        Command = Gui.Command.get(CommandName)
                                        MenuName = CommandInfoCorrections(CommandName)[
                                            "menuText"
                                        ].replace("&", "")
                                        if CommandName == action.data():
                                            if (
                                                MenuName
                                                != self.ribbonStructure["workbenches"][
                                                    workbenchName
                                                ]["toolbars"][toolbar]["commands"][
                                                    action.data()
                                                ][
                                                    "text"
                                                ]
                                                and MenuName != ""
                                                and textJSON != ""
                                            ):
                                                text = textJSON
                                    # if it is a member of a FreeCAD dropdown:
                                    if len(action.data().split(", ")) > 1:
                                        MenuName = action.text()
                                        if (
                                            MenuName
                                            != self.ribbonStructure["workbenches"][
                                                workbenchName
                                            ]["toolbars"][toolbar]["commands"][
                                                action.data()
                                            ][
                                                "text"
                                            ]
                                            and MenuName != ""
                                            and textJSON != ""
                                        ):
                                            text = textJSON

                                # the text would be overwritten again when the state of the action changes
                                # (e.g. when getting enabled / disabled), therefore the action itself
                                # is manipulated.
                                action.setText(text)
                            except KeyError as e:
                                if Parameters_Ribbon.DEBUG_MODE is True:
                                    print(f"{workbenchName}, {action.data()}, {e}")
                                text = action.text()

                            # Get the icon from cache. Use the pixmap as backup
                            pixmap = ""
                            CommandName = action.data()
                            if button.menu() is not None:
                                CommandName = button.text()
                            # If the command is an dropdown, use the button text instead of action data
                            if button.text().endswith("_ddb"):
                                CommandName = button.text()

                            try:
                                pixmap = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][CommandName]["icon"]
                            except Exception:
                                pass
                            actionIcon = self.ReturnCommandIcon(action.data(), pixmap)
                            if actionIcon is not None:
                                action.setIcon(actionIcon)

                            # try to get alternative icon from ribbonStructure
                            try:
                                icon_Json = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][CommandName]["icon"]
                                if icon_Json != "":
                                    action.setIcon(Gui.getIcon(icon_Json))
                            except KeyError:
                                pass

                            # If the icon is still none, try to retrieve it from the data file
                            if action.icon() is None or (
                                action.icon() is not None and action.icon().isNull()
                            ):
                                StandardFunctions.Print(
                                    f"An icon retrieved from data file for '{CommandName}'"
                                )
                                DataFile = os.path.join(
                                    os.path.dirname(__file__), "RibbonDataFile.dat"
                                )

                                if os.path.exists(DataFile) is True:
                                    Data = {}
                                    # read ribbon structure from JSON file
                                    with open(DataFile, "r") as file:
                                        Data.update(json.load(file))
                                    file.close()
                                    try:
                                        # Load the lists for the deserialized icons
                                        for IconItem in Data["Command_Icons"]:
                                            # This works only for FreeCAD Commands
                                            CommandName_Icon = action.data()
                                            if CommandName_Icon == IconItem[0]:
                                                Icon: QIcon = (
                                                    Serialize_Ribbon.deserializeIcon(
                                                        IconItem[1]
                                                    )
                                                )
                                                action.setIcon(Icon)
                                    except Exception as e:
                                        if Parameters_Ribbon.DEBUG_MODE is True:
                                            StandardFunctions.Print(
                                                f"Trying the get an icon for {CommandName}\n{e}",
                                                "Warning",
                                            )
                                        pass

                            # get button size from ribbonStructure
                            try:
                                buttonSize = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][CommandName]["size"]
                                if buttonSize == "":
                                    buttonSize = "small"
                            except KeyError:
                                pass

                            # Check if this is an icon only toolbar
                            IconOnly = False
                            for iconToolbar in self.ribbonStructure["iconOnlyToolbars"]:
                                if iconToolbar == toolbar:
                                    IconOnly = True

                            btn = RibbonToolButton()
                            # Make sure that no strange "&" symbols are remainging
                            action.setText(action.text().replace("&", ""))
                            if buttonSize == "small":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_SMALL
                                if (
                                    IconOnly is True
                                    or Parameters_Ribbon.USE_FC_OVERLAY is True
                                ):
                                    showText = False
                                try:
                                    if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                        showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["textEnabled"]
                                except Exception:
                                    pass

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                )
                                if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                    try:
                                        size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["ButtonSize_large"]
                                        IconSize = QSize(size, size)
                                        ButtonSize = IconSize
                                    except Exception:
                                        pass
                                    
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn: RibbonToolButton = CustomControls.CustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                                    showText=showText,
                                    setWordWrap=False,
                                    ElideMode=False,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                    parent=self,
                                )
                                # add the button as a small button
                                panel.addSmallWidget(
                                    btn,
                                    alignment=Qt.AlignmentFlag.AlignTop,
                                    fixedHeight=False,
                                ).setObjectName("SmallWidget")  # Set fixedheight to false. This is set in the custom widgets

                            elif buttonSize == "medium":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
                                if (
                                    IconOnly is True
                                    or Parameters_Ribbon.USE_FC_OVERLAY is True
                                ):
                                    showText = False
                                try:
                                    if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                        showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["textEnabled"]
                                except Exception:
                                    pass

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                )
                                if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                    try:
                                        size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["ButtonSize_medium"]
                                        IconSize = QSize(size, size)
                                        ButtonSize = IconSize
                                    except Exception:
                                        pass
                                    
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn: RibbonToolButton = CustomControls.CustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                                    showText=showText,
                                    setWordWrap=Parameters_Ribbon.WRAPTEXT_MEDIUM,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                    parent=self,
                                )
                                # add the button as large button
                                panel.addMediumWidget(
                                    btn,
                                    alignment=Qt.AlignmentFlag.AlignTop,
                                    fixedHeight=False,
                                ).setObjectName("MediumWidget")  # Set fixedheight to false. This is set in the custom widgets
                            elif buttonSize == "large":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE
                                if (
                                    IconOnly is True
                                    or Parameters_Ribbon.USE_FC_OVERLAY is True
                                ):
                                    showText = False
                                try:
                                    if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                        if "textEnabled" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]:
                                            showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["textEnabled"]
                                except Exception as e:
                                    print(e)
                                    pass

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                )
                                if Parameters_Ribbon.BETA_FUNCTIONS_ENABLED is True:
                                    try:
                                        if "ButtonSize_large" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]:
                                            size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["ButtonSize_large"]
                                            IconSize = QSize(size, size)
                                            ButtonSize = IconSize
                                    except Exception as e:
                                        print(e)
                                        pass
                                    
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn: RibbonToolButton = CustomControls.LargeCustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                                    showText=showText,
                                    setWordWrap=Parameters_Ribbon.WRAPTEXT_LARGE,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                    parent=self,
                                )
                                # add the button as large button
                                panel.addLargeWidget(
                                    btn,
                                    fixedHeight=False,
                                    alignment=Qt.AlignmentFlag.AlignTop,
                                ).setObjectName("LargeWidget")
                                # Set fixedheight to false. This is set in the custom widgets
                            else:
                                if Parameters_Ribbon.DEBUG_MODE is True:
                                    if buttonSize != "none":
                                        print(
                                            f"{action.text()} is ignored. Its size was: {buttonSize}"
                                        )
                                pass

                            if btn.menu() is not None:
                                btn.popupMode(
                                    QToolButton.ToolButtonPopupMode.MenuButtonPopup
                                )

                            # Set the background always to background color.
                            # Styling is managed in the custom button class
                            StyleSheet_Addition_Button = (
                                "QToolButton, QToolButton:hover {background-color: "
                                + StyleMapping_Ribbon.ReturnStyleItem(
                                    "Background_Color"
                                )
                                + ";border: none"
                                + ";}"
                            )
                            btn.setStyleSheet(StyleSheet_Addition_Button)

                            # add the button text to the shadowList for checking if buttons are already there.
                            shadowList.append(button.text())

                        except Exception as e:
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                raise e
                            continue

            # Change the name of the view panels to "View"
            if (
                panel.title() in "Views - Ribbon_newPanel"
                or panel.title().lower() in str("Individual views").lower()
            ):
                panel.setTitle(" Views ")
            else:                          
                # Remove possible workbench names from the titles
                if (
                    not "_custom" in title
                    and not "_global" in title
                    and not "_newPanel" in title
                ):
                    List = [
                        workbenchName,
                        workbenchTitle,
                        workbenchTitle.replace(" ", ""),
                    ]
                    for Name in List:                            
                        ListDelimiters = [" - ", "-", "_"]
                        for delimiter in ListDelimiters:
                            if f"{delimiter}{Name}" in title:
                                title = title.replace(f"{delimiter}{Name}", "")
                            elif f"{Name}{delimiter}" in title:
                                title = title.replace(f"{Name}{delimiter}", "")
                        if title != Name:
                            title = title.replace(Name, "")
                    panel.setTitle(title)
            # remove any suffix from the panel title
            if panel.title().endswith("_custom"):
                panel.setTitle(panel.title().replace("_custom", ""))
            if panel.title().endswith("_global"):
                panel.setTitle(panel.title().replace("_global", ""))
            if panel.title().endswith("_newPanel"):
                panel.setTitle(panel.title().replace("_newPanel", ""))

            # Set the panelheigth. setting the ribbonheigt, cause the first tab to be shown to large
            # add an offset to make room for the panel titles and icons
            panel._actionsLayout.setHorizontalSpacing(self.PaddingRight * 0.5)
            # panel._actionsLayout.setSpacing(0)
            # panel._actionsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            panel.layout().setSpacing(0)
            panel.setContentsMargins(0, 0, 0, 0)
            panel.setFixedHeight(self.ReturnRibbonHeight(self.PanelHeightOffset))
            # panel._actionsLayout.setContentsMargins(0, 0, 0, 0)
            Font = QFont()
            Font.setPixelSize(Parameters_Ribbon.FONTSIZE_PANELS)
            panel._titleLabel.setFont(Font)
            self.RibbonHeight = self.ReturnRibbonHeight(self.RibbonOffset) + 6

            # Setup the panelOptionButton
            actionList = []
            for i in range(len(ButtonList)):
                button = ButtonList[i]
                StyleSheet_Menu = (
                    "* {font-size: " + str(Parameters_Ribbon.FONTSIZE_MENUS) + "px;}"
                )
                button.setStyleSheet(StyleSheet_Menu)
                if len(button.actions()) == 1:
                    actionList.append(button.actions()[0])
                if len(button.actions()) > 1:
                    actionList.append(button.actions())
            OptionButton = panel.panelOptionButton()
            if len(actionList) > 0:
                Menu = CustomControls.CustomOptionMenu(
                    OptionButton.menu(), actionList, self
                )
                OptionButton.setMenu(Menu)
                StyleSheet_Menu = (
                    "* {font-size: " + str(Parameters_Ribbon.FONTSIZE_MENUS) + "px;}"
                )
                Menu.setStyleSheet(StyleSheet_Menu)
                # Set the behavior of the option button
                OptionButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
                # Remove the image to avoid double arrows
                OptionButton.setStyleSheet(
                    "RibbonPanelOptionButton::menu-indicator {image: none;}"
                )
                Menu = OptionButton.menu()

                # Set the icon
                OptionButton_Icon = StyleMapping_Ribbon.ReturnStyleItem("OptionButton")
                if OptionButton_Icon is not None:
                    OptionButton.setIcon(OptionButton_Icon)
                else:
                    OptionButton.setArrowType(Qt.ArrowType.DownArrow)
                    OptionButton.setToolButtonStyle(
                        Qt.ToolButtonStyle.ToolButtonTextBesideIcon
                    )
                    OptionButton.setText("more...")
            if len(actionList) == 0:
                panel.panelOptionButton().hide()

        self.isWbLoaded[tabName] = True

        # Set the previous/next buttons
        category = self.currentCategory()
        ScrollLeftButton_Category: RibbonCategoryLayoutButton = category.findChildren(
            RibbonCategoryLayoutButton
        )[0]
        ScrollRightButton_Category: RibbonCategoryLayoutButton = category.findChildren(
            RibbonCategoryLayoutButton
        )[1]
        ScrollLeftButton_Category.setMinimumWidth(self.iconSize * 0.5)
        ScrollRightButton_Category.setMinimumWidth(self.iconSize * 0.5)
        # get the icons
        ScrollLeftButton_Category_Icon = StyleMapping_Ribbon.ReturnStyleItem(
            "ScrollLeftButton_Category"
        )
        ScrollRightButton_Category_Icon = StyleMapping_Ribbon.ReturnStyleItem(
            "ScrollRightButton_Category"
        )
        # Set the icons
        if ScrollLeftButton_Category_Icon is not None:
            ScrollLeftButton_Category.setIcon(ScrollLeftButton_Category_Icon)
        else:
            ScrollLeftButton_Category.setArrowType(Qt.ArrowType.LeftArrow)
        if ScrollRightButton_Category_Icon is not None:
            ScrollRightButton_Category.setIcon(ScrollRightButton_Category_Icon)
        else:
            ScrollRightButton_Category.setArrowType(Qt.ArrowType.RightArrow)
        # Set the heihgt of the buttons
        ScrollLeftButton_Category.setFixedHeight(Parameters_Ribbon.ICON_SIZE_SMALL * 3)
        ScrollRightButton_Category.setFixedHeight(Parameters_Ribbon.ICON_SIZE_SMALL * 3)
        # Set the stylesheet
        ScrollLeftButton_Category.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet("toolbutton")
        )
        ScrollRightButton_Category.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet("toolbutton")
        )
        # Connect the custom click event
        ScrollLeftButton_Category.mousePressEvent = (
            lambda clickLeft: self.on_ScrollButton_Category_clicked(
                clickLeft, ScrollLeftButton_Category
            )
        )
        ScrollRightButton_Category.mousePressEvent = (
            lambda clickRight: self.on_ScrollButton_Category_clicked(
                clickRight, ScrollRightButton_Category
            )
        )

        # Set the maximum height to a high value to prevent from the ribbon to be clipped off
        self.currentCategory().setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        self.currentCategory().setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        self.setRibbonHeight(self.RibbonHeight)

        if self.DesignMenuLoaded is True:
            # Disable the quick toolbar, righttoolbar and application menu
            self.rightToolBar().setDisabled(True)
            self.quickAccessToolBar().setDisabled(True)
            self.applicationOptionButton().setDisabled(True)
            Gui.updateGui()
        return

    # endregion

    # region - Control functions
    def on_AboutButton_clicked(self):
        LoadLicenseForm_Ribbon.main()
        return

    def on_Help_clicked(self):
        self.helpRibbonButton().showMenu()

    def on_RibbonHelpButton_clicked(self):
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            Adress = self.ReproAdress + "wiki"
            webbrowser.open(Adress, new=2, autoraise=True)
        return

    def on_WhatsNewButton_clicked(self):
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            Adress = self.ReproAdress + """wiki/06-%E2%80%90-Change-log"""
            webbrowser.open(Adress, new=2, autoraise=True)
        return

    def on_Pin_clicked(self):
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            self.FoldRibbon()
            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", True)
            Parameters_Ribbon.AUTOHIDE_RIBBON = True

            pinButton: QToolButton = self.rightToolBar().findChildren(
                QToolButton, "Pin Ribbon"
            )[0]
            pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_closed"))

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            self.UnfoldRibbon()

            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", False)
            Parameters_Ribbon.AUTOHIDE_RIBBON = False

            pinButton: QToolButton = self.rightToolBar().findChildren(
                QToolButton, "Pin Ribbon"
            )[0]
            pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_open"))

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        return

    def on_ApplicationButton_toggled(self):
        self.applicationOptionButton().showMenu()

    def on_ScrollButton_Category_clicked(
        self, event, ScrollButton: RibbonCategoryLayoutButton
    ):
        for i in range(Parameters_Ribbon.RIBBON_CLICKSPEED):
            ScrollButton.click()
        return

    def on_ToggleBetaFunctions_toggled(self, switchStatus):
        self.BetaFunctionsEnabled = switchStatus
        if switchStatus is True:
            Parameters_Ribbon.Settings.SetBoolSetting("BetaFunctions", True)
            print("Béta functions enabled")
        if switchStatus is False:
            Parameters_Ribbon.Settings.SetBoolSetting("BetaFunctions", False)
            Stylesheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
            self.setStyleSheet(Stylesheet)
            self.CustomizeEnabled = False
            print("Béta functions disabled")
        return

    def on_ShowTextToggled(self, widget):
        # state = checkbox
        print("widget")
        # for child in widget.children():
        #     print(widget.children())
        #     if type(child) == QTextEdit:
        #         if state is True:
        #             child.setMaximumWidth(200)
        #             child.show()
        #         if state is False:
        #             child.hide()
        return

    # endregion

    # region - helper functions

    def hideClassicToolbars(self):
        for toolbar in mw.findChildren(QToolBar):
            parentWidget = toolbar.parentWidget()
            toolbar.setHidden(True)
            # hide toolbars that are not in the statusBar and show toolbars that are in the statusbar.
            if (
                parentWidget.objectName() == "statusBar"
                or parentWidget.objectName() == "StatusBarArea"
            ):
                toolbar.setEnabled(True)
                toolbar.setVisible(True)
            #
            if (
                mw.toolBarArea(toolbar) == Qt.ToolBarArea.LeftToolBarArea
                or mw.toolBarArea(toolbar) == Qt.ToolBarArea.RightToolBarArea
                or mw.toolBarArea(toolbar) == Qt.ToolBarArea.BottomToolBarArea
            ):
                toolbar.setEnabled(True)
                toolbar.setVisible(True)
            # # # Show specific toolbars and go to the next
            if toolbar.objectName() != "" and toolbar.objectName() in [
                self.quickAccessToolBar().objectName(),
                self.rightToolBar().objectName(),
            ]:
                toolbar.setEnabled(True)
                toolbar.setVisible(True)
        StatusArea = mw.findChildren(QWidget, "StatusBarArea")
        for Widget in StatusArea:
            Widget.show()
        return

    def UnfoldRibbon(self):
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
                self.setRibbonHeight(self.RibbonHeight)
        return

    def FoldRibbon(self, Ignore=False):
        if (
            Parameters_Ribbon.AUTOHIDE_RIBBON is True
            and self.isLoaded is True
            and Ignore is False
        ):
            if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
                TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
                TB.setMinimumHeight(self.RibbonMinimalHeight)
                TB.setMaximumHeight(self.RibbonMinimalHeight)
        return

    def List_ReturnCustomToolbars(self):
        Toolbars = []

        List_Workbenches = Gui.listWorkbenches()
        for WorkBenchName in List_Workbenches:
            if str(WorkBenchName) != "" or WorkBenchName is not None:
                if str(WorkBenchName) != "NoneWorkbench":
                    CustomToolbars: list = App.ParamGet(
                        "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar"
                    ).GetGroups()

                    for Group in CustomToolbars:
                        Parameter = App.ParamGet(
                            "User parameter:BaseApp/Workbench/"
                            + WorkBenchName
                            + "/Toolbar/"
                            + Group
                        )
                        Name = Parameter.GetString("Name")
                        Toolbars.append([Name, WorkBenchName])

        return Toolbars

    def List_ReturnCustomToolbars_Global(self):
        Toolbars = []
        CustomToolbars: list = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar"
        ).GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet(
                "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
            )
            Name = Parameter.GetString("Name")
            Toolbars.append([Name, "Global"])

        return Toolbars

    def List_AddCustomToolBarToWorkbench(self, WorkBenchName, CustomToolbar):
        ButtonList = []

        # Get the commands from the custom panel
        if WorkBenchName in self.ribbonStructure["customToolbars"]:
            for toolbar in self.ribbonStructure["customToolbars"][WorkBenchName]:
                if CustomToolbar.lower() == toolbar.lower():
                    Commands = self.ribbonStructure["customToolbars"][WorkBenchName][
                        toolbar
                    ]["commands"]

                    # Get the command and its original toolbar
                    for key, value in list(Commands.items()):
                        # get the menu text from the command list
                        for CommandName in Gui.listCommands():
                            # Get the english menutext
                            MenuName = CommandInfoCorrections(CommandName)["menuText"]
                            # Get the translated menutext
                            MenuNameTtranslated = CommandInfoCorrections(CommandName)[
                                "ActionText"
                            ]

                            if MenuName.lower() == key.lower():
                                try:
                                    toolbarToFind = value
                                    # check the toolbar name with the latest FreeCAD Version and update the cases.
                                    WorkBench = Gui.getWorkbench(WorkBenchName)
                                    ListToolbars = WorkBench.listToolbars()
                                    for ToolBar in ListToolbars:
                                        if ToolBar.lower() == value.lower():
                                            toolbarToFind = ToolBar

                                    # Get the original toolbar as QToolbar
                                    OriginalToolBar = mw.findChild(
                                        QToolBar, toolbarToFind
                                    )
                                    # Go through all it's QtoolButtons
                                    for Child in OriginalToolBar.findChildren(
                                        QToolButton
                                    ):
                                        # If the text of the QToolButton matches the menu text
                                        # Add it to the button list.
                                        IsInList = False
                                        for Toolbutton in ButtonList:
                                            if Toolbutton.text() == Child.text():
                                                IsInList = True

                                        if (
                                            Child.text() == MenuNameTtranslated
                                            and IsInList is False
                                        ):
                                            ButtonList.append(Child)
                                except Exception as e:
                                    # if Parameters_Ribbon.DEBUG_MODE is True:
                                    StandardFunctions.Print(
                                        f"{e.with_traceback(e.__traceback__)}, 3",
                                        "Warning",
                                    )
                                    continue

        return ButtonList

    def List_AddNewPanelToWorkbench(self, WorkBenchName, NewPanel):
        ButtonList = []

        try:
            if WorkBenchName in self.ribbonStructure["newPanels"]:
                if NewPanel in self.ribbonStructure["newPanels"][WorkBenchName]:
                    # Get the commands from the custom panel
                    Commands = self.ribbonStructure["newPanels"][WorkBenchName][
                        NewPanel
                    ]

                    # Get the command and its original toolbar
                    for CommandItem in Commands:
                        CommandName = CommandItem[0]
                        # Define a new toolbutton
                        NewToolbutton = RibbonToolButton()
                        if CommandName.endswith("_ddb") is False:
                            CommandActionList = None
                            # Get the translated menutext
                            # if the commandname cannot be split, it is a nromal command
                            if len(CommandName.split(", ")) <= 1:
                                # Get the command
                                Command = Gui.Command.get(CommandName)
                                if Command is not None:
                                    # Get tis action
                                    CommandActionList = Command.getAction()
                                if Command is None:
                                    if Parameters_Ribbon.DEBUG_MODE is True:
                                        StandardFunctions.Print(
                                            f"{CommandName} was None", "Warning"
                                        )
                            # If the commandname can be splitted, it is a FreeCAD dropdown
                            if len(CommandName.split(", ")) > 1:
                                CommandActionList = self.LoadDropDownAction(CommandName)
                            if CommandActionList is None:
                                continue
                            # if there are actions, proceed
                            if len(CommandActionList) > 0:
                                # if there is only one action, add it directly
                                if len(CommandActionList) == 1:
                                    NewToolbutton.addAction(CommandActionList[0])
                                    NewToolbutton.setDefaultAction(
                                        NewToolbutton.actions()[0]
                                    )
                                    # If the commandname is from a FreeCAD dropdown, set the commandname as text
                                    if len(CommandName.split(", ")) > 1:
                                        NewToolbutton.setText(
                                            NewToolbutton.actions()[0].text()
                                        )
                                # if there are more actions, create a menu
                                elif len(CommandActionList) > 1:
                                    menu = QMenu()
                                    # menu.addActions(CommandActionList)
                                    for action in CommandActionList:
                                        menu.addAction(action)
                                    NewToolbutton.setMenu(menu)
                                    NewToolbutton.setDefaultAction(menu.actions()[0])
                                    # Add the commandname as the objectname to detect if it is a dropdownbutton
                                    NewToolbutton.setObjectName(CommandName)

                                    # Do something with the menu. For some reason it will not be loaded otherwise
                                    len(NewToolbutton.menu().actions())

                                # Set the text for the toolbutton
                                if len(CommandName.split(", ")) <= 1:
                                    NewToolbutton.setText(
                                        CommandInfoCorrections(CommandName)[
                                            "menuText"
                                        ].replace("&", "")
                                    )
                                # # If the commandname is from a FreeCAD dropdown, set the commandname as text
                                # if len(CommandName.split(", ")) > 1:
                                #     NewToolbutton.setText(CommandName)
                                # add it to the list
                                ButtonList.append(NewToolbutton)
                        if CommandName.endswith("_ddb") is True:
                            CommandActionList = self.returnCustomDropDown(CommandName)
                            if CommandActionList is None or len(CommandActionList) < 1:
                                continue

                            # if there are actions, proceed
                            if len(CommandActionList) > 0:
                                # if there is only one action, add it directly
                                if len(CommandActionList) == 1:
                                    NewToolbutton.addAction(CommandActionList[0])
                                    NewToolbutton.setDefaultAction(
                                        NewToolbutton.actions()[0]
                                    )
                                # if there are more actions, create a menu
                                if len(CommandActionList) > 1:
                                    menu = QMenu()
                                    for action in CommandActionList:
                                        if len(action) > 0:
                                            menu.addAction(action[0])
                                    NewToolbutton.setMenu(menu)
                                    NewToolbutton.setDefaultAction(menu.actions()[0])
                                    # Add the commandname as the objectname to detect if it is a dropdownbutton
                                    NewToolbutton.setObjectName(CommandName)

                                    # Do something with the menu. For some reason it will not be loaded otherwise
                                    len(NewToolbutton.menu().actions())

                                # Set the text for the toolbutton
                                NewToolbutton.setText(CommandName)

                                # add it to the list
                                ButtonList.append(NewToolbutton)

        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}, 4", "Warning"
                )
            pass
        return ButtonList

    def LoadDropDownAction(self, CommandName):
        try:
            # If the commandname can be split into a name and number, it is part of a FreeCAD dropdown
            if len(CommandName.split(", ")) > 1:
                # Split the commandname
                CommandName_1 = CommandName.split(", ")[0]
                ActionNumber = int(CommandName.split(", ")[1])
                # Get the parent command
                ParentCommand = Gui.Command.get(CommandName_1)
                # If parent is not none, get the action based on the number
                if ParentCommand is not None:
                    action = ParentCommand.getAction()[ActionNumber]
                    # Set the commandname as data
                    action.setData(CommandName)
                    # return as a list
                    return [action]
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                print(e)
            # raise (e)
            pass

    def LoadMarcoFreeCAD(self, scriptName):
        if self.MainWindowLoaded is True:
            script = os.path.join(pathScripts, scriptName)
            if script.endswith(".py"):
                App.loadFile(script)
        return

    def ReturnRibbonHeight(self, offset=0):
        # Set the ribbon height.
        ribbonHeight = 0
        # If text is enabled for large button, the height is modified.
        LargeButtonHeight = Parameters_Ribbon.ICON_SIZE_LARGE
        # Check whichs is has the most height: 3 small buttons, 2 medium buttons or 1 large button
        # and set the height accordingly
        if (
            Parameters_Ribbon.ICON_SIZE_SMALL * 3
            >= Parameters_Ribbon.ICON_SIZE_MEDIUM * 2
            and Parameters_Ribbon.ICON_SIZE_SMALL * 3 >= LargeButtonHeight
        ):
            ribbonHeight = ribbonHeight + Parameters_Ribbon.ICON_SIZE_SMALL * 3 + 6
        elif (
            Parameters_Ribbon.ICON_SIZE_MEDIUM * 2
            >= Parameters_Ribbon.ICON_SIZE_SMALL * 3
            and Parameters_Ribbon.ICON_SIZE_MEDIUM * 2 >= LargeButtonHeight
        ):
            ribbonHeight = ribbonHeight + Parameters_Ribbon.ICON_SIZE_MEDIUM * 2 + 4
        else:
            ribbonHeight = ribbonHeight + LargeButtonHeight
        return ribbonHeight + offset

    def ReturnCommandIcon(self, CommandName: str, pixmap: str = "") -> QIcon:
        """_summary_

        Args:
            CommandName (str): Name of the command
            pixmap (str, optional): Add a pixmap as backup. Defaults to "".

        Returns:
            QIcon: the command icon.
        """

        icon = QIcon()
        for item in self.List_CommandIcons:
            if item[0] == CommandName:
                icon = item[1]
        if icon is None or (icon is not None and icon.isNull()):
            icon = StandardFunctions.returnQiCons_Commands(CommandName, pixmap)
        return icon

    def ReturnWorkbenchIcon(self, WorkBenchName: str, pixmap: str = "") -> QIcon:
        """_summary_

        Args:
            CommandName (str): Name of the command
            pixmap (str, optional): Add a pixmap as backup. Defaults to "".

        Returns:
            QIcon: the command icon.
        """
        icon = QIcon()
        for item in self.List_WorkBenchIcons:
            if item[0] == WorkBenchName:
                icon = item[1]
                return icon
        if icon is None or (icon is not None and icon.isNull()):
            workbench = Gui.getWorkbench(WorkBenchName)
            icon = QIcon(workbench.Icon)
            return icon
        if icon is None or (icon is not None and icon.isNull()):
            if pixmap != "":
                icon = Gui.getIcon(pixmap)
                return icon
        return icon

    def RunCommand(self, Command: str):
        # print(Command)
        try:
            Gui.doCommand(Command)
        except Exception:
            pass
        return

    def ToggleOverlay_All(self):
        try:
            self.CustomOverlay("")
        except Exception:
            pass
        return

    def ToggleOverlay_Left(self):
        try:
            self.CustomOverlay("left")
        except Exception:
            pass
        return

    def ToggleOverlay_Right(self):
        try:
            self.CustomOverlay("right")
        except Exception:
            pass
        return

    def ToggleOverlay_Bottom(self):
        try:
            self.CustomOverlay("bottom")
        except Exception:
            pass
        return

    def ToggleMouseByPass(self):
        if self.isLoaded is True:
            try:
                Gui.runCommand("Std_DockOverlayMouseTransparent")
            except Exception:
                pass
            return

    def CustomOverlay(self, side=""):
        # Toggle the overlay
        State = None
        if side == "left":
            State = self.OverlayToggled_Left
        if side == "right":
            State = self.OverlayToggled_Left
        if side == "bottom":
            State = self.OverlayToggled_Left
        if side == "":
            State = self.OverlayToggled

        Enable = True
        if State is True:
            Enable = False

        # Get the different overlay areas
        OverlayParam_Left = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft"
        )
        OverlayParam_Right = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayRight"
        )
        OverlayParam_Top = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayTop"
        )
        OverlayParam_Bottom = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom"
        )

        # If overlay is enabled, go here
        PanelsLeft = []
        PanelsRight = []
        PanelsBottom = []
        PanelsTop = []

        if Enable is True:
            # Get all the dockwidgets
            DockWidgets = mw.findChildren(QDockWidget)
            for DockWidget in DockWidgets:
                # If the dockwidget is not the ribbon, continue
                if DockWidget.objectName() != "Ribbon" and DockWidget.isVisible():
                    # Get the location of the dockwidget
                    Area = mw.dockWidgetArea(DockWidget)
                    if Area == Qt.DockWidgetArea.LeftDockWidgetArea:
                        PanelsLeft.append(DockWidget.objectName())
                    if Area == Qt.DockWidgetArea.RightDockWidgetArea:
                        PanelsRight.append(DockWidget.objectName())
                    if Area == Qt.DockWidgetArea.TopDockWidgetArea:
                        PanelsTop.append(DockWidget.objectName())
                    if Area == Qt.DockWidgetArea.BottomDockWidgetArea:
                        PanelsBottom.append(DockWidget.objectName())

            if side == "left" or side == "":
                EntryLeft = ""
                for panel in PanelsLeft:
                    EntryLeft = EntryLeft + "," + panel
                # Set the parameter
                OverlayParam_Left.SetString("Widgets", EntryLeft)
                # Set the overlay state to be toggled
                self.OverlayToggled_Left = True

            if side == "right" or side == "":
                # Define the parameter value for the overlay on the right
                EntryRight = ""
                for panel in PanelsRight:
                    EntryRight = EntryRight + "," + panel
                # Set the parameter
                OverlayParam_Right.SetString("Widgets", EntryRight)
                # Set the overlay state to be toggled
                self.OverlayToggled_Right = True

            if side == "bottom" or side == "":
                # Define the parameter value for the overlay on the right
                EntryBottom = ""
                for panel in PanelsBottom:
                    EntryBottom = EntryBottom + "," + panel
                # Set the parameter
                OverlayParam_Bottom.SetString("Widgets", EntryBottom)
                # Set the overlay state to be toggled
                self.OverlayToggled_Bottom = True

            if side == "":
                # Define the parameter value for the overlay on the right
                EntryTop = ""
                for panel in PanelsTop:
                    EntryTop = EntryTop + "," + panel
                # Set the parameter
                OverlayParam_Top.SetString("Widgets", EntryTop)
                # Set the overlay state to be toggled
                self.OverlayToggled = True

        if Enable is False:
            # Set the parameters to empty
            if side == "left" or side == "":
                OverlayParam_Left.SetString("Widgets", "")
                self.OverlayToggled_Left = False
            if side == "Right" or side == "":
                OverlayParam_Right.SetString("Widgets", "")
                self.OverlayToggled_Right = False
            if side == "Bottom" or side == "":
                OverlayParam_Bottom.SetString("Widgets", "")
                self.OverlayToggled_Bottom = False

        return Enable

    def CustomOverlay_Focus(self):
        OverlayParam_Left = None
        OverlayParam_Right = None
        OverlayParam_Bottom = None
        # Get the different overlay areas
        OverlayParam_Left = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft"
        )
        OverlayParam_Right = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayRight"
        )
        # OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
        OverlayParam_Bottom = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom"
        )

        # Ge the focused dockwidget
        FocusWidget = mw.focusWidget().parent().objectName()
        if FocusWidget == "Ribbon":
            return
        if isinstance(mw.focusWidget(), QTreeWidget):
            FocusWidget = "Tree view"
        position = ""
        try:
            DockWidget_Focus = mw.findChild(QDockWidget, FocusWidget)
            if DockWidget_Focus is not None:
                Area = mw.dockWidgetArea(DockWidget_Focus)
                if Area == Qt.DockWidgetArea.LeftDockWidgetArea:
                    position = "left"
                if Area == Qt.DockWidgetArea.RightDockWidgetArea:
                    position = "right"
                if Area == Qt.DockWidgetArea.TopDockWidgetArea:
                    position = "top"
                if Area == Qt.DockWidgetArea.BottomDockWidgetArea:
                    position = "bottom"
        except Exception:
            pass

        if position == "left":
            LeftPanels = OverlayParam_Left.GetString("Widgets")
            OverlayParam_Left.SetString("Widgets", f"{LeftPanels},{FocusWidget}")
            return
        if position == "right":
            RightPanels = OverlayParam_Right.GetString("Widgets")
            OverlayParam_Right.SetString("Widgets", f"{RightPanels},{FocusWidget}")
            return
        if position == "bottom":
            BottomPanels = OverlayParam_Bottom.GetString("Widgets")
            OverlayParam_Bottom.SetString("Widgets", f"{BottomPanels},{FocusWidget}")
            return
        if position == "":
            LeftPanels = OverlayParam_Left.GetString("Widgets")
            if FocusWidget in LeftPanels:
                LeftPanels = OverlayParam_Left.GetString("Widgets")
                LeftPanels = LeftPanels.replace(f"{FocusWidget}", "").replace(",,", ",")
                OverlayParam_Left.SetString("Widgets", f"{LeftPanels}")
                return
            RightPanels = OverlayParam_Right.GetString("Widgets")
            if FocusWidget in RightPanels:
                RightPanels = OverlayParam_Left.GetString("Widgets")
                RightPanels = RightPanels.replace(f"{FocusWidget}", "").replace(
                    ",,", ","
                )
                OverlayParam_Right.SetString("Widgets", f"{RightPanels}")
                return
            BottomPanels = OverlayParam_Bottom.GetString("Widgets")
            if FocusWidget in BottomPanels:
                BottomPanels = OverlayParam_Bottom.GetString("Widgets")
                BottomPanels = BottomPanels.replace(f"{FocusWidget}", "").replace(
                    ",,", ","
                )
                OverlayParam_Bottom.SetString("Widgets", f"{BottomPanels}")
                return
        return

    def CustomTransparancy(self):
        OverlayParam_Left = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft"
        )
        OverlayParam_Right = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayRight"
        )
        # OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
        OverlayParam_Bottom = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom"
        )

        Enable = None
        if OverlayParam_Left.GetBool("Transparent") is False:
            Enable = True
        if OverlayParam_Left.GetBool("Transparent") is True:
            Enable = False

        OverlayParam_Left.SetBool("Transparent", Enable)
        OverlayParam_Right.SetBool("Transparent", Enable)
        # OverlayParam_Top.SetBool("Transparent", Enable)
        OverlayParam_Bottom.SetBool("Transparent", Enable)

        self.TransparancyToggled = True

        return self.TransparancyToggled

    def CustomTransparancy_Focus(self):
        OverlayParam_Left = None
        OverlayParam_Right = None
        OverlayParam_Bottom = None
        # Get the different overlay areas
        OverlayParam_Left = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft"
        )
        OverlayParam_Right = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayRight"
        )
        # OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
        OverlayParam_Bottom = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom"
        )

        # Ge the focused dockwidget
        FocusWidget = mw.focusWidget().parent().objectName()
        if FocusWidget == "Ribbon":
            return
        if isinstance(mw.focusWidget(), QTreeWidget):
            FocusWidget = "Tree view"
        position = ""
        try:
            DockWidget_Focus = mw.findChild(QDockWidget, FocusWidget)
            if DockWidget_Focus is not None:
                Area = mw.dockWidgetArea(DockWidget_Focus)
                if (
                    Area == Qt.DockWidgetArea.LeftDockWidgetArea
                    or Area == Qt.DockWidgetArea.RightDockWidgetArea
                    or Area == Qt.DockWidgetArea.TopDockWidgetArea
                    or Area == Qt.DockWidgetArea.BottomDockWidgetArea
                ):
                    return
        except Exception:
            pass

        if position == "":
            LeftPanels = OverlayParam_Left.GetString("Widgets")
            if FocusWidget in LeftPanels:
                OverlayParam_Left.SetBool(
                    "Transparent", not OverlayParam_Left.GetBool("Transparent")
                )
                return
            RightPanels = OverlayParam_Right.GetString("Widgets")
            if FocusWidget in RightPanels:
                OverlayParam_Right.SetBool(
                    "Transparent", not OverlayParam_Right.GetBool("Transparent")
                )
                return
            BottomPanels = OverlayParam_Bottom.GetString("Widgets")
            if FocusWidget in BottomPanels:
                OverlayParam_Bottom.SetBool(
                    "Transparent", not OverlayParam_Bottom.GetBool("Transparent")
                )
                return
        return

    def returnCustomDropDown(self, CommandName):
        actionList = []

        try:
            for DropDownCommand, Commands in self.ribbonStructure[
                "dropdownButtons"
            ].items():
                if CommandName == DropDownCommand:
                    for CommandItem in Commands:
                        Command = Gui.Command.get(CommandItem[0])
                        if Command is not None:
                            action = Command.getAction()
                            if action is not None:
                                actionList.append(action)
            return actionList
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}", "Warning"
                )
            return []

    def CheckLanguage(self):
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        if self.ribbonStructure["language"] != FreeCAD_preferences.GetString(
            "Language"
        ):
            if "workbenches" in self.ribbonStructure:
                for workbenchName in self.ribbonStructure["workbenches"]:
                    if "toolbars" in self.ribbonStructure["workbenches"][workbenchName]:
                        for ToolBar in self.ribbonStructure["workbenches"][
                            workbenchName
                        ]["toolbars"]:
                            if (
                                "commands"
                                in self.ribbonStructure["workbenches"][workbenchName][
                                    "toolbars"
                                ][ToolBar]
                            ):
                                for Command in self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][ToolBar]["commands"]:
                                    self.ribbonStructure["workbenches"][workbenchName][
                                        "toolbars"
                                    ][ToolBar]["commands"][Command]["text"] = ""

            print("Ribbon UI: Custom text are reset because the language was changed")
        return
    
    # Needs to be updated/optimalised
    def returnDropWidgets(self, widget, panel, ButtonType = "Small", showText = True):
        btn= widget
        for child in widget.children():
            if (child.objectName() == "CommandButton"):
                btn = child        
        
        # Define a menu
        arrowButton = None
        Menu = None
        try:
            arrowButton = widget.findChildren(QToolButton)[1]
            Menu = arrowButton.menu()
        except Exception:
            pass
        
        # get the actions
        action = btn.actions()
        if type(action) is list:
            if len(action) > 0:
                for i in range(len(action)):
                    if Menu is not None:
                        Menu.addAction(action[i])
                action = action[0]                        
        if btn.defaultAction() is not None:
            action = btn.defaultAction()
            
        # Get the command name
        CommandName = action.data()
        
        # Get the workbench name
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())

        # Check if this is an icon only toolbar
        IconOnly = False
        for iconToolbar in self.ribbonStructure["iconOnlyToolbars"]:
            if iconToolbar == panel.title():
                IconOnly = True

        if showText is False:
            for child in widget.children():
                if type(child) == QLabel:
                    showText = child.isVisible()

        if IconOnly is True or Parameters_Ribbon.USE_FC_OVERLAY is True:
            showText = False

        if ButtonType.lower() == "small":
            showText = Parameters_Ribbon.SHOW_ICON_TEXT_SMALL
            if (
                IconOnly is True
                or Parameters_Ribbon.USE_FC_OVERLAY is True
            ):
                showText = False
            try:
                showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]["textEnabled"]
            except Exception:
                pass

            # Create a custom toolbutton
            ButtonSize = QSize(
                Parameters_Ribbon.ICON_SIZE_SMALL,
                Parameters_Ribbon.ICON_SIZE_SMALL,
            )
            IconSize = QSize(
                Parameters_Ribbon.ICON_SIZE_SMALL,
                Parameters_Ribbon.ICON_SIZE_SMALL,
            )
            try:
                size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]["ButtonSize_large"]
                IconSize = QSize(size, size)
                ButtonSize = IconSize
            except Exception:
                pass
                                    
            btn: RibbonToolButton = CustomControls.CustomToolButton(
                Text=action.text(),
                Action=action,
                Icon=action.icon(),
                IconSize=IconSize,
                ButtonSize=ButtonSize,
                FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                showText=showText,
                setWordWrap=False,
                ElideMode=False,
                MaxNumberOfLines=2,
                Menu=Menu,
                MenuButtonSpace=16,
                parent=self,
            )
        if ButtonType.lower() == "medium":
            showText = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
            if (
                IconOnly is True
                or Parameters_Ribbon.USE_FC_OVERLAY is True
            ):
                showText = False
            try:
                showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]["textEnabled"]
            except Exception:
                pass

            # Create a custom toolbutton
            ButtonSize = QSize(
                Parameters_Ribbon.ICON_SIZE_MEDIUM,
                Parameters_Ribbon.ICON_SIZE_MEDIUM,
            )
            IconSize = QSize(
                Parameters_Ribbon.ICON_SIZE_MEDIUM,
                Parameters_Ribbon.ICON_SIZE_MEDIUM,
            )
            try:
                size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]["ButtonSize_medium"]
                IconSize = QSize(size, size)
                ButtonSize = IconSize
            except Exception:
                pass
                
            btn: RibbonToolButton = CustomControls.CustomToolButton(
                Text=action.text(),
                Action=action,
                Icon=action.icon(),
                IconSize=IconSize,
                ButtonSize=ButtonSize,
                FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                showText=showText,
                setWordWrap=Parameters_Ribbon.WRAPTEXT_MEDIUM,
                MaxNumberOfLines=2,
                Menu=Menu,
                MenuButtonSpace=16,
                parent=self,
            )
            
        if ButtonType.lower() == "large":
            showText = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE
            if (
                IconOnly is True
                or Parameters_Ribbon.USE_FC_OVERLAY is True
            ):
                showText = False
            try:
                if "textEnabled" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]:
                    showText = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][panel.title()]["commands"][CommandName]["textEnabled"]
            except Exception as e:
                print(e)
                pass
                                
            # Create a custom toolbutton
            ButtonSize = QSize(
                Parameters_Ribbon.ICON_SIZE_LARGE,
                Parameters_Ribbon.ICON_SIZE_LARGE,
            )
            IconSize = QSize(
                Parameters_Ribbon.ICON_SIZE_LARGE,
                Parameters_Ribbon.ICON_SIZE_LARGE,
            )
            try:
                if "ButtonSize_large" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]:
                    size = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][CommandName]["ButtonSize_large"]
                    IconSize = QSize(size, size)
                    ButtonSize = IconSize
            except Exception as e:
                print(e)
                pass
                                    
            btn: RibbonToolButton = CustomControls.LargeCustomToolButton(
                Text=action.text(),
                Action=action,
                Icon=action.icon(),
                IconSize=IconSize,
                ButtonSize=ButtonSize,
                FontSize=Parameters_Ribbon.FONTSIZE_BUTTONS,
                showText=showText,
                setWordWrap=Parameters_Ribbon.WRAPTEXT_LARGE,
                MaxNumberOfLines=2,
                Menu=Menu,
                MenuButtonSpace=16,
                parent=self,
            )
        return btn
    
    def ReturnTextWidth(self, Label_Text: QLabel, Width, Menu: QMenu = None, setWordWrap = False, ElideMode= False, TextAlignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,MaxNumberOfLines=2,):
        # Define the parameters
        TextWidth = 0
        Space = 6

        Font = QFont()
        Font.setPixelSize(Parameters_Ribbon.FONTSIZE_BUTTONS)
        Text = Label_Text.text()
        Label_Text.setFont(Font)
        FontMetrics = QFontMetrics(Font)
        # Determine the height of a single row
        SingleHeight = QFontMetrics(Font).boundingRect(Text).height() + 3
        # If there is no WordWrap, set the ElideMode and the max number of lines to 1.
        if setWordWrap is False:
            if ElideMode is True:
                # Determine the maximum length per line
                FontMetrics = QFontMetrics(Text)
                maxWidth = 0
                maxLength = 0
                for c in Text:
                    maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                    if maxWidth < Width:
                        maxLength = maxLength + 1
                    if maxWidth >= Width:
                        limit = maxLength - 3
                        Text = Text[:limit].strip() + "..."
                        break
            # Set the text with a placeholder
            Label_Text.setWordWrap(False)
            Label_Text.setText(Text)
            # Set the maximum number of lines to 1
            MaxNumberOfLines = 1
            # Set the proper alignment
            Label_Text.setAlignment(TextAlignment)
            # Lower the height when there is a menu
            if Menu is not None and len(Menu.actions()) > 1:
                Label_Text.setFixedHeight(SingleHeight)
            else:
                Label_Text.setFixedHeight(SingleHeight + Space)
                
            # Update the width parameter
            TextWidth = FontMetrics.boundingRect(Text).width() + Space
            Label_Text.setMaximumWidth(TextWidth)

        # If wordwrap is enabled, set the text and height accordingly
        if setWordWrap is True:
            # Set the wrap mode
            Label_Text.setWordWrap(True)
            # Determine the maximum length per line
            maxWidth = 0
            maxLength = 0
            for c in Text:
                maxWidth = maxWidth + FontMetrics.horizontalAdvance(c, -1)
                if maxWidth < Width:
                    maxLength = maxLength + 1
                if maxWidth >= Width:
                    break
            maxLength = maxLength + 3

            # Get the first text line
            line1 = StandardFunctions.ReturnWrappedText(
                Text, maxLength, MaxNumberOfLines, True
            )[0]
            # Set the alignment
            Label_Text.setAlignment(TextAlignment)
            # Add the line
            Label_Text.setText(line1)
            # get the text width
            TextWidth = FontMetrics.tightBoundingRect(line1).width()
            # Try to get the second line if there is one
            try:
                line2 = StandardFunctions.ReturnWrappedText(
                    Text, maxLength, MaxNumberOfLines, True
                )[1]
                # Set the alignment
                Label_Text.setAlignment(TextAlignment)
                # Add the line
                Label_Text.setText(line1 + "\n" +line2)
                # Update the text width if neccesary
                if FontMetrics.tightBoundingRect(line2).width() > TextWidth:
                    TextWidth = FontMetrics.tightBoundingRect(line2).width()
            except Exception:
                pass
            Label_Text.setMaximumWidth(TextWidth + Space)

        return Label_Text.maximumWidth()
    
    def WriteButtonSettings(self, ButtonWidget, panel, property: dict = {"size": "small",}):
        # Get tabBar
        parent = panel.parent()
        count = 0
        while (count < 10):
            if type(parent) == RibbonNormalCategory or type(parent) == RibbonContextCategory:
                break
            else:
                parent = parent.parent()
        # Get the workbench name                    
        WorkBenchName = parent.objectName()
        # Get the grid layout
        gridLayout: QGridLayout = panel._actionsLayout

        # Get the current data from the ribbonstructure
        CommandName = ""
        for child in ButtonWidget.children():
            if (
                type(child) == QToolButton
                and child.objectName() == "CommandButton"
            ):
                CommandName = child.defaultAction().data()
        if CommandName != "":
            StandardFunctions.add_keys_nested_dict(
                self.ribbonStructure,
                [
                    "workbenches",
                    WorkBenchName,
                    "toolbars",
                    panel.objectName(),
                    "order",
                ],
            )
                        
            # Get the order of the widgets
            orderList = []
            for k in range(gridLayout.count()):
                try:
                    Control = gridLayout.itemAt(k).widget().children()[1]
                    if type(Control) is RibbonToolButton:
                        for child in Control.children():
                            if (
                                type(child) == QToolButton
                                and child.objectName() == "CommandButton"
                            ):
                                orderList.append(child.defaultAction().data())
                except Exception:
                    pass
            self.ribbonStructure["workbenches"][WorkBenchName]["toolbars"][
                panel.objectName()
            ]["order"] = orderList
                               
            for key, value in property.items():
                StandardFunctions.add_keys_nested_dict(
                    self.ribbonStructure,
                    [
                        "workbenches",
                        WorkBenchName,
                        "toolbars",
                        panel.objectName(),
                        "commands",
                        CommandName,
                        key,
                    ],
                )
                self.ribbonStructure["workbenches"][WorkBenchName]["toolbars"][panel.objectName()]["commands"][CommandName][key] = value       

            # Writing to ribbonStructure.json
            JsonFile = Parameters_Ribbon.RIBBON_STRUCTURE_JSON
            with open(JsonFile, "w") as outfile:
                json.dump(self.ribbonStructure, outfile, indent=4)
            outfile.close()
    # endregion

    # region - Titlebar functions
    def CloseFreeCAD(self):
        mw.close()
        return

    def MinimizeFreeCAD(self):
        mw.showMinimized()
        return

    def RestoreFreeCAD(self, event):
        # This function only works when evertyhing is loaded.
        # if self.isLoaded:
        StatusBarState = mw.findChild(QStatusBar, "statusBar").isVisible()
        # Get the style and restore button
        RestoreButton: QToolButton = self.rightToolBar().findChildren(
            QToolButton, "RestoreButton"
        )[0]
        # If the mainwindow is maximized, set the mainwindow to normal, set a size and icon
        if mw.isMaximized() is True:
            try:
                # Set the main window to normal
                mw.setWindowState(Qt.WindowState.WindowNoState)
                mw.showNormal()
                # Set the statusbar again if it was enabled
                mw.statusBar().setVisible(StatusBarState)
                # Resize the mainwindow to be smaller than the screen
                mw.resize(mw.width() - 50, mw.height() - 50)
                mw.move(50, 50)
                mw.adjustSize()
                RestoreButton.clearFocus()
            except Exception:
                pass
            return
        # if the mainwindow is normal, maximize it
        if mw.isMaximized() is False:
            try:
                # Set the main window maximized
                mw.setWindowState(Qt.WindowState.WindowMaximized)
                mw.showMaximized()
                # Set the statusbar again if it was enabled
                mw.statusBar().setVisible(StatusBarState)
                RestoreButton.clearFocus()
            except Exception:
                pass
            return
        return

    def ToggleFullScreen(self):
        if mw.isFullScreen():
            mw.showMaximized()
            return
        if mw.isFullScreen() is False:
            mw.showFullScreen()
            return

    def ToggleMenuBar(self):
        MenuBar = mw.menuBar()
        if MenuBar.isVisible():
            MenuBar.hide()
            return
        if MenuBar.isVisible() is False:
            MenuBar.show()
            return

    # endregion

    # region - Function for data files updates
    def CheckDataFile(self):
        Data = {}
        if self.isLoaded:
            DataFile2 = os.path.join(os.path.dirname(__file__), "RibbonDataFile2.dat")
            if os.path.exists(DataFile2) is False:
                Question = translate(
                    "FreeCAD Ribbon",
                    "The first time, a data file must be generated!\n"
                    + "It is important to create a data file to avoid any issues.\n"
                    + f"Open the layout menu ({self.LayoutMenuShortCut}) and click on 'Reload workbenches'.",
                )
                StandardFunctions.Mbox(text=Question, title="FreeCAD Ribbon", style=30)
                return
            if os.path.exists(DataFile2) is True:
                # read ribbon structure from JSON file
                with open(DataFile2, "r") as file:
                    Data.update(json.load(file))
                file.close()

            # Add the most important checks on startup.
            # Less important ones will be done when opening the Layout menu
            DataUpdateNeeded = False
            try:
                FileVersion = Data["dataVersion"]
                if FileVersion != self.DataFileVersion:
                    DataUpdateNeeded = True
            except Exception:
                DataUpdateNeeded = True
            if DataUpdateNeeded is True:
                Question = translate(
                    "FreeCAD Ribbon",
                    "The current data file is based on an older format!\n"
                    + "It is important to update the data file to avoid any issues.\n"
                    + f"Open the layout menu ({self.LayoutMenuShortCut}) and click on 'Reload workbenches'.",
                )
                StandardFunctions.Mbox(text=Question, title="FreeCAD Ribbon", style=30)
        return True

    def ConvertRibbonStructure(self):
        # Define a result parameter
        isConverted = False
        # Get the FreeCAD Version
        version = App.Version()

        # Check if version is stored in the ribbon structure.
        # If so check if it is an older version.
        # If it is the same or newer version, return.
        if "convertedWithVersion" in self.ribbonStructure:
            main = self.ribbonStructure["convertedWithVersion"][0]
            sub = self.ribbonStructure["convertedWithVersion"][1]
            patch = self.ribbonStructure["convertedWithVersion"][2]
            git_version = self.ribbonStructure["convertedWithVersion"][3]
            if main >= int(version[0]):
                if sub >= int(version[1]):
                    if patch >= int(version[2]):
                        if git_version >= int(version[3].split(" ")[0]):
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                print("no conversion needed")
                            return

        # Convert the commands from menuname to the commandames
        #
        # Check if there are workbenches and toolbars in the ribbon structure
        if "workbenches" in self.ribbonStructure:
            for WorkBenchName in self.ribbonStructure["workbenches"]:
                if "toolbars" in self.ribbonStructure["workbenches"][WorkBenchName]:
                    for ToolBar in self.ribbonStructure["workbenches"][WorkBenchName][
                        "toolbars"
                    ]:
                        # Skip the toolbar order
                        if ToolBar != "order":
                            # If a toolbar has an order for its commands, continue
                            if (
                                "order"
                                in self.ribbonStructure["workbenches"][WorkBenchName][
                                    "toolbars"
                                ][ToolBar]
                            ):
                                # Get the current order list
                                OrderList = self.ribbonStructure["workbenches"][
                                    WorkBenchName
                                ]["toolbars"][ToolBar]["order"]
                                # Define a new list for the conversion
                                ConvertedList = []
                                # Go through the current order list
                                for i in range(len(OrderList)):
                                    MenuText = OrderList[i]
                                    # if it is an separator of custom dropdown button, just added ti the coverted list.
                                    # For everything else, find the commandname in the datafile
                                    if "separator" in MenuText or "ddb" in MenuText:
                                        ConvertedList.append(MenuText)
                                    else:
                                        for DataItem in self.List_Commands:
                                            if DataItem[3] == WorkBenchName:
                                                # If the data item is already converted to a command. append that to the list
                                                if (
                                                    MenuText.lower()
                                                    == DataItem[0].lower()
                                                ):
                                                    ConvertedList.append(DataItem[0])
                                                    break
                                                # If the data item is still a menutext, add the command instead.
                                                if (
                                                    MenuText.lower()
                                                    == DataItem[4].lower()
                                                ):
                                                    ConvertedList.append(DataItem[0])
                                                    break

                                # Update the ordered list
                                if len(ConvertedList) > 0:
                                    self.ribbonStructure["workbenches"][WorkBenchName][
                                        "toolbars"
                                    ][ToolBar]["order"] = ConvertedList
                                    isConverted = True

        if isConverted is True:
            # Add the version of FreeCAD on which this conversion is done, to the ribbonstructure
            # Create a key if not present
            StandardFunctions.add_keys_nested_dict(
                self.ribbonStructure,
                [
                    "convertedWithVersion",
                ],
            )
            self.ribbonStructure["convertedWithVersion"] = [
                int(version[0]),
                int(version[1]),
                int(version[2]),
                int(version[3].split(" ")[0]),
            ]

            # Update the json file but make also an backup
            # get the path for the Json file
            JsonFile = Parameters_Ribbon.RIBBON_STRUCTURE_JSON

            # create a copy and rename it as a backup if enabled
            if Parameters_Ribbon.ENABLE_BACKUP is True:
                Suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
                BackupName = f"RibbonStructure_{Suffix}.json"
                if os.path.exists(pathBackup) is False:
                    os.makedirs(pathBackup)
                BackupFile = os.path.join(pathBackup, BackupName)
                shutil.copy(JsonFile, BackupFile)

            # Writing to sample.json
            with open(JsonFile, "w") as outfile:
                json.dump(self.ribbonStructure, outfile, indent=4)

            outfile.close()

        return isConverted

    # endregion


class EventInspector(QObject):
    def __init__(self, parent):
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event):
        # Show the mainwindow after the application is activated
        if event.type() == QEvent.Type.ApplicationActivated:
            mw = Gui.getMainWindow()
            mw.setWindowState(Qt.WindowState.WindowMaximized)
            mw.showMaximal()
            Style = mw.style()
            RibbonBar = mw.findChild(ModernMenu, "Ribbon")
            RestoreButton: QToolButton = RibbonBar.rightToolBar().findChildren(
                QToolButton, "RestoreButton"
            )[0]
            try:
                RestoreButton.setIcon(
                    Style.standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton)
                )
            except Exception:
                pass
            return QObject.eventFilter(self, obj, event)
        # This is a workaround for windows
        # If the window stat changes and the titlebar is hidden, catch the event
        if (
            event.type() == QEvent.Type.WindowStateChange
            or event.type() == QEvent.Type.DragMove
        ) and Parameters_Ribbon.HIDE_TITLEBAR_FC is True:
            # Get the main window, its style, the ribbon and the restore button
            mw = Gui.getMainWindow()
            Style = mw.style()
            RibbonBar = mw.findChild(ModernMenu, "Ribbon")
            RestoreButton: QToolButton = RibbonBar.rightToolBar().findChildren(
                QToolButton, "RestoreButton"
            )[0]
            # If the mainwindow is maximized, set the window state to maximize and set the correct icon
            if mw.isMaximized():
                try:
                    # RestoreButton.setIcon(Style.standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton))
                    RestoreButton.setIcon(
                        StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[2]
                    )
                except Exception:
                    pass
                return QObject.eventFilter(self, obj, event)
            # If the mainwindow is not maximized, set the window state to no state and set the correct icon
            if mw.isMaximized() is False:
                try:
                    # RestoreButton.setIcon(Style.standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
                    RestoreButton.setIcon(
                        StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[1]
                    )
                except Exception:
                    pass
                return QObject.eventFilter(self, obj, event)
        # If the event is a modfied event, update the title
        # This is done when switching from one part to another
        if (
            event.type() == QEvent.Type.ModifiedChange
            and Parameters_Ribbon.TOOLBAR_POSITION == 0
        ):
            # Get the mainwindow, the ribbon and the title
            mw = Gui.getMainWindow()
            RibbonBar = mw.findChild(ModernMenu, "Ribbon")
            title = RibbonBar.title()
            # If there is an active document, continue here
            if App.ActiveDocument is not None:
                # Define the standard title as a prefix
                Prefix = (
                    f"FreeCAD {App.Version()[0]}.{App.Version()[1]}.{App.Version()[2]}"
                )
                # if the title is not equal to the prefix with the active document label,
                # Get the text from the active tab from the viewport and combine it with the prefix
                # Set it as the new title
                if title != Prefix + " - " + App.ActiveDocument.Label:
                    CentralWidget = mw.centralWidget()
                    TabBar: QTabBar = CentralWidget.findChild(QTabBar, "mdiAreaTabBar")
                    CurrentText = TabBar.tabText(TabBar.currentIndex())
                    RibbonBar.setTitle(Prefix + " - " + CurrentText)
            # If there is no active document, set just the standard title
            if App.ActiveDocument is None:
                RibbonBar.setTitle(
                    f"FreeCAD {App.Version()[0]}.{App.Version()[1]}.{App.Version()[2]}"
                )
            return QObject.eventFilter(self, obj, event)

        # print(event)

        return False


class run:
    """
    Activate Modern UI.
    """

    def __init__(self, name):
        """
        Constructor
        """
        disable = 0
        if name != "NoneWorkbench":
            mw: QMainWindow = Gui.getMainWindow()
            # Disable connection after activation
            mw.workbenchActivated.disconnect(run)
            if disable:
                return

            ribbon = ModernMenu()
            # Get the layout
            layout = ribbon.layout()
            # Set spacing and content margins to zero
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            # update the layout
            ribbon.setLayout(layout)
            ribbonDock = QDockWidget()
            # set the name of the object and the window title
            ribbonDock.setObjectName("Ribbon")
            ribbonDock.setWindowTitle("Ribbon")
            # Set the titlebar to an empty widget (effectively hide it)
            ribbonDock.setTitleBarWidget(QWidget())
            ribbonDock.setContentsMargins(0, 0, 0, 0)
            # attach the ribbon to the dockwidget
            ribbonDock.setWidget(ribbon)
            ribbonDock.setEnabled(True)
            ribbonDock.setVisible(True)

            # # make sure that there are no negative valules
            if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
                ribbonDock.setMaximumHeight(ribbon.RibbonMinimalHeight)
            # Add the dockwidget to the main window
            mw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, ribbonDock)
            return
