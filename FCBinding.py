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
)
from PySide.QtWidgets import (
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
)
from CustomWidgets import CustomControls

import json
import os
import sys
import webbrowser
import LoadDesign_Ribbon
import Parameters_Ribbon
import LoadSettings_Ribbon
import LoadLicenseForm_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
from Standard_Functions_RIbbon import CommandInfoCorrections
import Serialize_Ribbon
import StyleMapping
import platform
import math

# Get the resources
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(os.path.dirname(__file__), "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)

translate = App.Qt.translate

import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar
from pyqtribbon_local.panel import RibbonPanel
from pyqtribbon_local.toolbutton import RibbonToolButton
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategoryLayoutButton

# import pyqtribbon_local as pyqtribbon
# from pyqtribbon.ribbonbar import RibbonMenu, RibbonBar
# from pyqtribbon.panel import RibbonPanel, RibbonPanelTitle
# from pyqtribbon.toolbutton import RibbonToolButton
# from pyqtribbon.separator import RibbonSeparator
# from pyqtribbon.category import RibbonCategoryLayoutButton

# Get the main window of FreeCAD
mw = Gui.getMainWindow()

# Define a timer
timer = QTimer()


class ModernMenu(RibbonBar):
    """
    Create ModernMenu QWidget.
    """

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
    RibbonOffset = 46 + QuickAccessButtonSize  # Set to zero to hide the panel titles

    # Set the minimum height for the ribbon
    RibbonMinimalHeight = QuickAccessButtonSize + 10
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
    TransparancyToggled = False

    RibbonMenu = QMenu()
    HelpMenu = QMenu()
    OverlayMenu = None

    UpdateVersion = ""
    DeveloperVersion = ""

    def __init__(self):
        """
        Constructor
        """
        super().__init__(title="", iconSize=self.iconSize)
        self.setObjectName("Ribbon")

        self.setWindowFlags(self.windowFlags() | Qt.Dialog)

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
                ["Std_ViewGroup", "AssemblyWorkbench"],
                ["Std_ViewFitAll", "AssemblyWorkbench"],
                ["Std_ViewFitSelection", "AssemblyWorkbench"],
                ["Std_ViewZoomOut", "Global"],
                ["Std_ViewZoomIn", "Global"],
                ["Std_ViewBoxZoom", "Global"],
                ["Std_AlignToSelection", "AssemblyWorkbench"],
                ["Part_SelectFilter", "Global"],
            ]
        else:
            try:
                if "Views - Ribbon_newPanel" in self.ribbonStructure["newPanels"]["Global"]:
                    del self.ribbonStructure["newPanels"]["Global"]["Views - Ribbon_newPanel"]
            except Exception:
                pass
        # # Add a toolbar "tools"
        #
        UseToolsPanel = Parameters_Ribbon.Settings.GetBoolSetting("UseToolsPanel")
        # Create a key if not present
        try:
            if "Tools_newPanel" not in self.ribbonStructure["newPanels"]["Global"] and UseToolsPanel is True:
                StandardFunctions.add_keys_nested_dict(
                    self.ribbonStructure,
                    ["newPanels", "Global", "Tools_newPanel"],
                )
                self.ribbonStructure["newPanels"]["Global"]["Tools_newPanel"] = [
                    ["Std_Measure", "Global"],
                    ["Std_UnitsCalculator", "Global"],
                    ["Std_Properties", "Global"],
                    ["Std_BoxElementSelection", "Global"],
                    ["Std_BoxSelection", "Global"],
                    ["Std_WhatsThis", "AssemblyWorkbench"],
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
        self.ReproAdress = StandardFunctions.ReturnXML_Value(PackageXML, "url", "type", "repository")
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(translate("FreeCAD Ribbon", "FreeCAD Ribbon: ") + self.ReproAdress)

        # Set the icon size if parameters has none
        Parameters_Ribbon.Settings.WriteSettings()

        # Activate the workbenches used in the new panels otherwise the panel stays empty
        try:
            if "newPanels" in self.ribbonStructure:
                for WorkBenchName in self.ribbonStructure["newPanels"]:
                    for NewPanel in self.ribbonStructure["newPanels"][WorkBenchName]:
                        # Get the commands from the custom panel
                        Commands = self.ribbonStructure["newPanels"][WorkBenchName][NewPanel]

                        # Get the command and its original toolbar
                        for CommandItem in Commands:
                            if CommandItem[1] != "General" and CommandItem[1] != "Global":
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
                for DropDownCommand, Commands in self.ribbonStructure["dropdownButtons"].items():
                    for CommandItem in Commands:
                        if CommandItem[1] != "General" and CommandItem[1] != "Global":
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
        User = "APEbbers"
        Repo = "FreeCAD-Ribbon"
        Branch = "main"
        File = "package.xml"
        ElementName = "version"
        LatestVersion = StandardFunctions.ReturnXML_Value_Git(User, Repo, Branch, File, ElementName)
        # Get the current version
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        CurrentVersion = StandardFunctions.ReturnXML_Value(PackageXML, "version")
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
            for i in range(ArrayLenght - 1):
                if LatestVersionArray[i] > CurrentVersionArray[i]:
                    print(f"{LatestVersionArray[i]}, {CurrentVersionArray[i]}")
                    self.UpdateVersion = LatestVersion

        # Create the ribbon
        self.CreateMenus()  # Create the menus
        self.createModernMenu()  # Create the ribbon
        self.onUserChangedWorkbench(False)  # Set the dockwidget and ribbonheight as done after changing from workbench

        # Set the custom stylesheet
        StyleSheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
        # modify the stylesheet to set the border and background for a toolbar and menu
        hexColor = StyleMapping.ReturnStyleItem("Background_Color")
        hexColorTab = StyleMapping.ReturnStyleItem("Background_Color", True, True)
        if hexColor is not None and hexColor != "" and Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED is True:
            # Set the quickaccess toolbar background color. This fixes a transparant toolbar.
            self.quickAccessToolBar().setStyleSheet("QToolBar {background: " + hexColor + ";}")
            self.tabBar().setStyleSheet("background: " + hexColorTab + ";")
            # Set the background color. This fixes transparant backgrounds when FreeCAD has no stylesheet
            StyleSheet_Addition = "\n\nQToolButton {background: solid " + hexColor + ";}"
            StyleSheet_Addition_2 = (
                "\n\nRibbonBar {border: none;background: solid " + hexColor + ";color: " + hexColor + ";}"
            )
            StyleSheet = StyleSheet_Addition_2 + StyleSheet + StyleSheet_Addition
        self.setStyleSheet(StyleSheet)

        # If the text for the tabs is set to be disabled, update the stylesheet
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            StyleSheet_Addition_3 = (
                """QTabBar::tab {
                    background: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover", True, True)
                + """;color: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover", True, True)
                + """;min-width: """
                + str(self.TabBar_Size)
                + """px;
                            max-width: """
                + str(self.TabBar_Size)
                + """px;
                            padding-left: 6px;
                            padding-right: 0px;
                            margin: 3px
                        }"""
            )
            StyleSheet = StyleSheet_Addition_3 + StyleSheet
            self.setStyleSheet(StyleSheet)

        # Add an addition for selected tabs
        StyleSheet_Addition_4 = (
            """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
            + StyleMapping.ReturnStyleItem("Background_Color_Hover")
            + """;}"""
        )
        # If the tabs are set to icon only, set the text to the hover background color also
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            StyleSheet_Addition_4 = (
                """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                + """;color: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                + """;}"""
            )
        StyleSheet = StyleSheet_Addition_4 + StyleSheet
        self.setStyleSheet(StyleSheet)

        # Add an addition for Font sizes
        StyleSheet_Addition_5 = """
        QWidgetItem,
        QMenu, QMenu::item,
        QAction,
        RibbonApplicationButton,
        RibbonMenu,
        RibbonMenu::item,
        RibbonPanelTitle,
        RibbonToolButton::item,
        QToolButton, QToolButton::menu,
        QLabel,
        QTextEdit,
        SearchBoxLight
            { font-size:11px;}
                QTabBar {font-size:14px;}"""
        StyleSheet = StyleSheet_Addition_5 + StyleSheet
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
        self.tabBar().wheelEvent = lambda event_tabBar: self.wheelEvent_TabBar(event_tabBar)
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
        ScrollLeftButton_Tab_Icon = StyleMapping.ReturnStyleItem("ScrollLeftButton_Tab")
        ScrollRightButton_Tab_Icon = StyleMapping.ReturnStyleItem("ScrollRightButton_Tab")
        # Set the icons
        StyleSheet = "QToolButton {image: none};QToolButton::arrow {image: none};"
        BackgroundColor = StyleMapping.ReturnStyleItem("Background_Color")
        if int(App.Version()[0]) == 0 and int(App.Version()[1]) <= 21 and BackgroundColor is not None:
            StyleSheet = (
                """QToolButton {image: none;background: """
                + BackgroundColor
                + """};QToolButton::arrow {image: none};"""
            )
        if ScrollLeftButton_Tab_Icon is not None:
            ScrollLeftButton_Tab.setStyleSheet(StyleSheet)
            ScrollLeftButton_Tab.setIcon(ScrollLeftButton_Tab_Icon)
        else:
            ScrollRightButton_Tab.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        if ScrollRightButton_Tab_Icon is not None:
            ScrollRightButton_Tab.setStyleSheet(StyleSheet)
            ScrollRightButton_Tab.setIcon(ScrollRightButton_Tab_Icon)
        else:
            ScrollRightButton_Tab.setArrowType(Qt.ArrowType.RightArrow)

        # Add a custom close event to show the original menubar again
        self.closeEvent = lambda close: self.closeEvent(close)

        # Remove persistant toolbars
        PersistentToolbars = App.ParamGet("User parameter:Tux/PersistentToolbars/User").GetGroups()
        for Group in PersistentToolbars:
            Parameter = App.ParamGet("User parameter:Tux/PersistentToolbars/User/" + Group)
            Parameter.SetString("Top", "")
            Parameter.SetString("Left", "")
            Parameter.SetString("Right", "")
            Parameter.SetString("Bottom", "")

        # Connect shortcuts
        #
        # Application menu
        KeyCombination = Parameters_Ribbon.SHORTCUT_APPLICATION
        self.ShortCutApp = QShortcut(QKeySequence(KeyCombination), self)
        self.ShortCutApp.activated.connect(self.ToggleApplicationButton)
        # ToolTip = self.applicationOptionButton().toolTip()
        ToolTip = f"{KeyCombination}"
        self.applicationOptionButton().setToolTip(ToolTip)

        return

    def closeEvent(self, event):
        if self.isEnabled() is False:
            mw.menuBar().show()
        return True

    def eventFilter(self, obj, event):
        if int(App.Version()[0]) > 1:
            if event.type() == QEvent.Type.HoverMove:
                # swallow events
                # print("Event swallowed")
                event.ignore()
                return False
            else:
                # bubble events
                return True
        else:
            return True

    def enterEvent(self, QEvent):
        # In FreeCAD 1.0, Overlays are introduced. These have also an enterEvent which results in strange behavior
        # Therefore this function is only activated on older versions of FreeCAD.
        if Parameters_Ribbon.SHOW_ON_HOVER is True and Parameters_Ribbon.USE_FC_OVERLAY is False:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
                self.setRibbonHeight(self.RibbonHeight)

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return

    def leaveEvent(self, QEvent):
        if self.LeaveEventEnabled is True:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
                TB.setMinimumHeight(self.RibbonMinimalHeight)
                TB.setMaximumHeight(self.RibbonMinimalHeight)

                # Make sure that the ribbon remains visible
                self.setRibbonVisible(True)
                pass

    # implementation to add actions to the Filemenu. Needed for the accessories menu
    def addAction(self, action: QAction):
        menu = self.findChild(RibbonMenu, "Ribbon")
        if menu is None:
            menu = self.addFileMenu()
        menu.addAction(action)
        return

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

    def connectSignals(self):
        self.tabBar().currentChanged.connect(self.onUserChangedWorkbench)
        mw.workbenchActivated.connect(self.onWbActivated)
        return

    def disconnectSignals(self):
        self.tabBar().currentChanged.disconnect(self.onUserChangedWorkbench)
        mw.workbenchActivated.disconnect(self.onWbActivated)
        return

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
            self.QuickAccessButtonSize + FontMetrics.boundingRect(Text.text()).width() + 12,
            self.QuickAccessButtonSize,
        )
        # Set the icon
        self.setApplicationIcon(Gui.getIcon("freecad"))
        # Set the styling of the button including padding (Text widht + 2*maring)
        self.applicationOptionButton().setStyleSheet(
            StyleMapping.ReturnStyleSheet(
                "applicationbutton",
                padding_right=str(FontMetrics.horizontalAdvance(Text.text(), -1) + 12) + "px",
                radius="4px",
            )
        )
        # Add the default tooltip
        self.applicationOptionButton().setToolTip(translate("FreeCAD Ribbon", "FreeCAD Ribbon"))

        # add the menus from the menubar to the application button
        self.ApplicationMenus()

        # add quick access buttons
        i = 1  # Start value for button count. Used for width of quickaccess toolbar
        toolBarWidth = ((self.QuickAccessButtonSize * self.sizeFactor) * i) + self.applicationOptionButton().width()
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
                        button.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton", "2px", f"{padding}px"))
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
                        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
                        # Set the stylesheet
                        button.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton", "2px", f"{padding}px"))

                # If it is a custom dropdown, add the actions one by one.
                if commandName.endswith("_ddb") is True:
                    # set the padding for a dropdown button
                    padding = self.PaddingRight
                    # Get the actions and add them one by one
                    QuickAction = self.returnCustomDropDown(commandName)
                    for action in QuickAction:
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
                    button.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton", "2px", f"{padding}px"))

                # Set the height
                self.setQuickAccessButtonHeight(self.RibbonMinimalHeight)

                button.setContentsMargins(3, 3, 3, 3)

                # Add the button to the quickaccess toolbar
                if len(button.actions()) > 0:
                    self.addQuickAccessButton(button)
                else:
                    StandardFunctions.Print(f"{commandName} did not contain any actions!", "Log")

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
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        # needed for excluding from hiding toolbars
        self.quickAccessToolBar().setObjectName("quickAccessToolBar")
        self.quickAccessToolBar().setWindowTitle("quickAccessToolBar")

        # Set the tabbar height and textsize
        self.tabBar().setContentsMargins(0, 0, 0, 0)
        font = self.tabBar().font()
        font.setPixelSize(14)
        self.tabBar().setFont(font)

        self.tabBar().setIconSize(QSize(self.TabBar_Size - 6, self.TabBar_Size - 6))
        self.tabBar().setStyleSheet("margin: 0px;padding: 0px;height: " + str(self.QuickAccessButtonSize) + ";")
        # self.RibbonOffset = self.RibbonOffset + (self.tabBar().height() - self.QuickAccessButtonSize)

        # Correct colors when no stylesheet is selected for FreeCAD.
        self.quickAccessToolBar().setStyleSheet("")
        if Parameters_Ribbon.BUTTON_BACKGROUND_ENABLED is True:
            FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
            currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")
            if currentStyleSheet == "":
                hexColor = StyleMapping.ReturnStyleItem("Background_Color")
                # Set the quickaccess toolbar background color
                self.quickAccessToolBar().setStyleSheet("background-color: " + hexColor + ";")

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
            if WorkbenchOrderedList[i] == "Assembly4Workbench" or WorkbenchOrderedList[i] == "Assembly3Workbench":
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
                        self.addCategory(name)

                        # Set the tabbar according the style setting
                        if Parameters_Ribbon.TABBAR_STYLE <= 1:
                            # set tab icon
                            icon: QIcon = self.ReturnWorkbenchIcon(workbenchName)
                            self.tabBar().setTabIcon(len(self.categories()) - 1, icon)
                        if Parameters_Ribbon.TABBAR_STYLE == 2:
                            self.tabBar().setTabIcon(len(self.categories()) - 1, QIcon())

                        # Set the tab data
                        self.tabBar().setTabData(len(self.categories()) - 1, workbenchName)

                        # Set the tooltip
                        MenuText = workbench.MenuText
                        ToolTipText = workbench.ToolTip
                        if (
                            ToolTipText.lower() != MenuText.lower() + " workbench"
                            and MenuText.lower() != ToolTipText.lower()
                        ):
                            MenuText = f"<b>{workbench.MenuText}</b><br>{workbench.ToolTip}"
                        else:
                            MenuText = f"<b>{MenuText}<b>"

                        self.tabBar().setTabToolTip(len(self.categories()) - 1, MenuText)

        # Set the size of the collapseRibbonButton
        self.collapseRibbonButton().setFixedSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize)

        # add the searchbar if available
        SearchBarWidth = self.AddSearchBar()

        # add an overlay menu if Ribbon's overlay is enabled
        if self.OverlayMenu is not None:
            OverlayMenu = QToolButton()
            OverlayMenu.setIcon(QIcon(QPixmap(os.path.join(pathIcons, "Draft_Layer.svg"))))
            OverlayMenu.setToolTip(translate("FreeCAD Ribbon", "Overlay functions") + "...")
            OverlayMenu.setMenu(self.OverlayMenu)
            OverlayMenu.setFixedSize(self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize)
            OverlayMenu.setStyleSheet(StyleMapping.ReturnStyleSheet(control="toolbutton", padding_right="12px"))
            OverlayMenu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            # add the settingsmenu to the right toolbar
            self.rightToolBar().addWidget(OverlayMenu)

        # add a settings button with menu
        SettingsMenu = QToolButton()
        # Get the freecad preference button
        editMenu = mw.findChildren(QMenu, "&Edit")[0]
        preferenceButton_FreeCAD = editMenu.actions()[len(editMenu.actions()) - 1]
        # preferenceButton_FreeCAD.setText(translate("FreeCAD Ribbon", "FreeCAD prefences"))
        # add the preference button for FreeCAD
        SettingsMenu.addAction(preferenceButton_FreeCAD)
        # add the ribbon settings menu
        SettingsMenu.addAction(self.RibbonMenu.menuAction())
        SettingsMenu.setIcon(Gui.getIcon("Std_DlgParameter.svg"))
        SettingsMenu.setToolTip(translate("FreeCAD Ribbon", "Preferences") + "...")
        SettingsMenu.setFixedSize(self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize)
        SettingsMenu.setStyleSheet(StyleMapping.ReturnStyleSheet(control="toolbutton", padding_right="12px"))
        SettingsMenu.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        # add the settingsmenu to the right toolbar
        self.rightToolBar().addWidget(SettingsMenu)

        # Set the helpbutton
        self.helpRibbonButton().setEnabled(True)
        self.helpRibbonButton().setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.helpRibbonButton().setToolTip(translate("FreeCAD Ribbon", "Help") + "...")
        # Get the default help action from FreeCAD
        helpMenu = mw.findChildren(QMenu, "&Help")[0]
        helpAction = helpMenu.actions()[0]
        self.helpRibbonButton().setIcon(helpAction.icon())
        self.helpRibbonButton().setMenu(self.HelpMenu)
        self.helpRibbonButton().setFixedSize(self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize)
        self.helpRibbonButton().setStyleSheet(StyleMapping.ReturnStyleSheet(control="toolbutton", padding_right="12px"))
        self.helpRibbonButton().setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        # Add a button the enable or disable AutoHide
        pinButton = QToolButton()
        pinButton.setCheckable(True)
        pinButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        pinButton.setFixedSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize)
        pinButton.setIconSize(QSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize))
        # Set the correct icon
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButtonIcon = StyleMapping.ReturnStyleItem("PinButton_closed")
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButtonIcon = StyleMapping.ReturnStyleItem("PinButton_open")
        # Set the icon
        if pinButtonIcon is not None:
            pinButton.setIcon(pinButtonIcon)
        # Set the text and objectname
        pinButton.setText(translate("FreeCAD Ribbon", "Pin Ribbon"))
        pinButton.setObjectName("Pin Ribbon")
        # Set the tooltip
        pinButton.setToolTip(translate("FreeCAD Ribbon", "Click to toggle the autohide function on or off"))
        # Set the correct checkstate
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButton.setChecked(False)
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButton.setChecked(True)
        pinButton.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton", "2px"))

        # If FreeCAD's overlay function is active, set the pinbutton to checked and then to disabled
        preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
        if preferences.GetBool("ActivateOverlay") is True:
            pinButton.setChecked(True)
            pinButton.setDisabled(True)
        else:
            pinButton.clicked.connect(self.onPinClicked)
            self.rightToolBar().addWidget(pinButton)

        # Set the width of the right toolbar
        RightToolbarWidth = SearchBarWidth + 3 * (self.RightToolBarButtonSize + 16) + self.RightToolBarButtonSize
        if Parameters_Ribbon.USE_FC_OVERLAY is True:
            RightToolbarWidth = SearchBarWidth + 2 * (self.RightToolBarButtonSize + 16)
        self.rightToolBar().setMinimumWidth(RightToolbarWidth)
        # Set the size policy
        self.rightToolBar().setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
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

                width = 5 * self.RightToolBarButtonSize

                sea = SearchBoxLight.SearchBoxLight(
                    getItemGroups=lambda: __import__("GetItemGroups").getItemGroups(),
                    getToolTip=lambda groupId, setParent: __import__("GetItemGroups").getToolTip(groupId, setParent),
                    getItemDelegate=lambda: __import__("IndentedItemDelegate").IndentedItemDelegate(),
                )
                sea.resultSelected.connect(
                    lambda index, groupId: __import__("GetItemGroups").onResultSelected(index, groupId)
                )
                sea.setFixedSize(width, self.RightToolBarButtonSize)
                BeforeAction = self.rightToolBar().actions()[1]
                self.rightToolBar().insertWidget(BeforeAction, sea)
                # width = sea.width()
            except Exception:
                pass
            return width

    def ApplicationMenus(self):
        # Add a file menu
        ApplictionMenu = self.addFileMenu()

        # add the menus from the menubar to the application button
        MenuBar = mw.menuBar()
        ApplictionMenu.addActions(MenuBar.actions())

        for child in MenuBar.children():
            if child.objectName() == "&Help":
                # Remove the menu from the Ribbon Application Menu
                MenuBar.removeAction(child.menuAction())

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
            color = StyleMapping.ReturnStyleItem("DevelopColor")
            Label = QLabel()
            Label.setText("Development version")
            Label.setStyleSheet(f"color: {color};border: 1px solid {color};border-radius: 2px;")
            ApplictionMenu.addWidget(Label)
        # if there is an update, add a button that opens the addon manager
        if self.UpdateVersion != "" and self.DeveloperVersion == "":
            ApplictionMenu.addSeparator()
            color = StyleMapping.ReturnStyleItem("UpdateColor")
            Button = QToolButton()
            Button.setText(translate("FreeCAD Ribbon", "Update available"))
            Button.setStyleSheet(
                "QToolButton{"
                + f"color: {color};border: 1px solid {color};border-radius: 2px;background: none"
                + "}QToolButton:hover{background-color: "
                + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                + ";}"
            )

            def OpenAddOnManager():
                Gui.runCommand("Std_AddonMgr", 0)

            Button.clicked.connect(OpenAddOnManager)
            ApplictionMenu.addWidget(Button)

        return

    def CreateMenus(self):
        MenuBar = mw.menuBar()

        # Create the overlay menu when the native overlay function is not used
        if Parameters_Ribbon.USE_FC_OVERLAY is False:
            OverlayMenu = QMenu(translate("FreeCAD Ribbon", "Overlay") + "...", self)
            OverlayButton = OverlayMenu.addAction(translate("FreeCAD Ribbon", "Toggle overlay"))
            OverlayButton.setToolTip(translate("FreeCAD Ribbon", "Click to toggle the overlay function"))
            OverlayButton.triggered.connect(self.CustomOverlay)
            OverlayButton.setShortcut("F4")

            TransparancyButton = OverlayMenu.addAction(translate("FreeCAD Ribbon", "Toggle transparancy"))
            TransparancyButton.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Toggle transparancy for panels when overlay is enabled",
                )
            )
            TransparancyButton.triggered.connect(self.CustomTransparancy)
            TransparancyButton.setShortcut("Shift+F4")

            self.OverlayMenu = OverlayMenu

        # Create a ribbon menu
        RibbonMenu = QMenu(translate("FreeCAD Ribbon", "Ribbon UI preferences") + " ...", self)

        # Add the ribbon design button
        DesignButton = RibbonMenu.addAction(translate("FreeCAD Ribbon", "Ribbon layout"))
        DesignButton.setToolTip(translate("FreeCAD Ribbon", "Design the ribbon to your preference"))
        DesignButton.triggered.connect(self.loadDesignMenu)
        # Add the preference button
        PreferenceButton = RibbonMenu.addAction(translate("FreeCAD Ribbon", "Preferences"))
        PreferenceButton.setToolTip(translate("FreeCAD Ribbon", "Set preferences for the Ribbon UI"))
        PreferenceButton.setMenuRole(QAction.MenuRole.NoRole)
        PreferenceButton.triggered.connect(self.loadSettingsMenu)
        # Add the script submenu with items
        ScriptDir = os.path.join(os.path.dirname(__file__), "Scripts")
        if os.path.exists(ScriptDir) is True:
            ListScripts = os.listdir(ScriptDir)
            if len(ListScripts) > 0:
                ScriptButtonMenu = RibbonMenu.addMenu(translate("FreeCAD Ribbon", "Scripts"))
                ScriptButtonMenu.setToolTip(translate("FreeCAD Ribbon", "Scripts to help setup the ribbon."))
                for i in range(len(ListScripts)):
                    ScriptButtonMenu.addAction(
                        ListScripts[i],
                        lambda i=i + 1: self.LoadMarcoFreeCAD(ListScripts[i - 1]),
                    )
        # Set the RibbonMenu
        self.RibbonMenu = RibbonMenu

        # Create a help menu
        HelpMenu = QMenu(self)
        # Get the icons
        HelpIcon = QIcon()
        AboutIcon = Gui.getIcon("freecad")

        actions = None

        # Get the standard help menu from FreeCAD
        for child in MenuBar.children():
            if child.objectName() == "&Help":
                actions = child.actions()
                # change help to FreeCAD help
                actions[0].setText(translate("FreeCAD Ribbon", "Help"))
                HelpMenu.addActions(actions)
                # Store the help icon for the Ribbon help
                HelpIcon = child.actions()[0].icon()
                # Remove the menu from the Ribbon Application Menu
                MenuBar.removeAction(child.menuAction())

        # Add the ribbon helpbutton under the FreeCAD
        RibbonHelpButton = QAction(translate("FreeCAD Ribbon", "Ribbon UI help"))
        RibbonHelpButton.setToolTip(translate("FreeCAD Ribbon", "Open the help page for the Ribbon UI in your browser"))
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
        AboutButton_Ribbon = AboutMenu.addAction(translate("FreeCAD Ribbon", "About Ribbon UI ") + version)
        AboutButton_Ribbon.setIcon(AboutIcon)
        AboutButton_Ribbon.triggered.connect(self.on_AboutButton_clicked)
        # Create the what's new button
        WhatsNewButton_Ribbon = AboutMenu.addAction(translate("FreeCAD Ribbon", "What's new?"))
        WhatsNewButton_Ribbon.triggered.connect(self.on_WhatsNewButton_clicked)
        # add the aboutmenu to the help menu
        HelpMenu.addMenu(AboutMenu)

        self.HelpMenu = HelpMenu
        return

    def loadDesignMenu(self):
        LoadDesign_Ribbon.main()
        return

    def loadSettingsMenu(self):
        LoadSettings_Ribbon.main()
        return

    def on_AboutButton_clicked(self):
        LoadLicenseForm_Ribbon.main()
        return

    def onHelpClicked(self):
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

    def onPinClicked(self):
        TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            TB.setMinimumHeight(self.RibbonMinimalHeight)
            TB.setMaximumHeight(self.RibbonMinimalHeight)
            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", True)
            Parameters_Ribbon.AUTOHIDE_RIBBON = True

            pinButton: QToolButton = self.rightToolBar().findChildren(QToolButton, "Pin Ribbon")[0]
            pinButton.setIcon(StyleMapping.ReturnStyleItem("PinButton_closed"))

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
                self.setRibbonHeight(self.RibbonHeight)

            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", False)
            Parameters_Ribbon.AUTOHIDE_RIBBON = False

            pinButton: QToolButton = self.rightToolBar().findChildren(QToolButton, "Pin Ribbon")[0]
            pinButton.setIcon(StyleMapping.ReturnStyleItem("PinButton_open"))

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        return

    def onUserChangedWorkbench(self, tabActivated=True):
        """
        Import selected workbench toolbars to ModernMenu section.
        """
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
                self.setRibbonHeight(self.RibbonHeight)

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
        return

    def onWbActivated(self):
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
                self.setRibbonHeight(self.RibbonHeight)

        # Set the text color depending in tabstyle
        if Parameters_Ribbon.TABBAR_STYLE != 1:
            self.tabBar().setStyleSheet("QTabBar::tab {color: " + StyleMapping.ReturnStyleItem("FontColor") + ";}")
        if Parameters_Ribbon.TABBAR_STYLE == 1:
            self.tabBar().setStyleSheet(
                """QTabBar::tab {background: """
                + StyleMapping.ReturnStyleItem("Background_Color", True, True)
                + """;color: """
                + StyleMapping.ReturnStyleItem("Background_Color", True, True)
                + """;}"""
                + """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                + """;color: """
                + StyleMapping.ReturnStyleItem("Background_Color_Hover")
                + """;}"""
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
        return

    def onTabBarClicked(self):
        TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        if self.RibbonHeight > 0:
            TB.setFixedHeight(self.RibbonHeight)
            self.setRibbonHeight(self.RibbonHeight)
        self.setRibbonVisible(True)

        # hide normal toolbars
        self.hideClassicToolbars()
        return

    def ToggleApplicationButton(self):
        self.applicationOptionButton().showMenu()

    def buildPanels(self):
        # Get the active workbench and get its name
        #
        workbenchTitle = self.tabBar().tabText(self.tabBar().currentIndex())
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        if workbenchName is None:
            return
        workbench = Gui.getWorkbench(workbenchName)

        # check if the panel is already loaded. If so exit this function
        tabName = workbenchTitle
        if tabName in self.isWbLoaded and (self.isWbLoaded[tabName] or tabName == ""):
            return

        # Get the list of toolbars from the active workbench
        ListToolbars: list = workbench.listToolbars()
        # Get custom toolbars that are created in the toolbar environment and add them to the list of toolbars
        CustomToolbars = self.List_ReturnCustomToolbars()
        for CustomToolbar in CustomToolbars:
            if CustomToolbar[1] == workbenchName:
                ListToolbars.append(CustomToolbar[0])
        # Get the global custom toolbars that are created in the toolbar environment and add them to the list of toolbars
        CustomToolbars_Global = self.List_ReturnCustomToolbars_Global()
        for CustomToolbar in CustomToolbars_Global:
            ListToolbars.append(CustomToolbar[0])

        # Get the custom panels and add them to the list of toolbars
        try:
            if workbenchName in self.ribbonStructure["customToolbars"]:
                for CustomPanel in self.ribbonStructure["customToolbars"][workbenchName]:
                    ListToolbars.append(CustomPanel)

                    # remove the original toolbars from the list
                    Commands = self.ribbonStructure["customToolbars"][workbenchName][CustomPanel]["commands"]
                    for Command in Commands:
                        try:
                            OriginalToolbar = self.ribbonStructure["customToolbars"][workbenchName][CustomPanel][
                                "commands"
                            ][Command]
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
            ToolbarOrder: list = self.ribbonStructure["workbenches"][workbenchName]["toolbars"]["order"]

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
            if toolbar in self.ribbonStructure["ignoredToolbars"]:
                continue
            if toolbar == "":
                continue

            # Create the panel, use the toolbar name as title
            title = StandardFunctions.TranslationsMapping(workbenchName, toolbar)
            panel: RibbonPanel = self.currentCategory().addPanel(
                title=title,
                showPanelOptionButton=True,
            )
            panel.panelOptionButton().hide()

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
                if toolbar != "" and toolbar in self.ribbonStructure["workbenches"][workbenchName]["toolbars"]:
                    if "order" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]:
                        for j in range(
                            len(self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["order"])
                        ):
                            if (
                                "separator"
                                in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["order"][
                                    j
                                ].lower()
                            ):
                                separator = QToolButton()
                                separator.setText(
                                    self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["order"][j]
                                )
                                allButtons.insert(j, separator)

            if workbenchName in self.ribbonStructure["workbenches"]:
                # order buttons like defined in ribbonStructure
                if (
                    toolbar in self.ribbonStructure["workbenches"][workbenchName]["toolbars"]
                    and "order" in self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]
                ):
                    OrderList: list = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["order"]

                    # XXX check that positionsList consists of strings only
                    def sortButtons(button: QToolButton):
                        Text = button.text()

                        if Text == "":
                            return -1

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
            )  # if buttons are used in multiple workbenches, they can show up double. (Sketcher_NewSketch)
            # for button in allButtons:
            NoSmallButtons_spacer = (
                0  # needed to count the number of small buttons in a column. (bug fix with adding separators)
            )
            NoMediumButtons_spacer = (
                0  # needed to count the number of medium buttons in a column. (bug fix with adding separators)
            )

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
                    buttonSize = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar]["commands"][
                        action.data()
                    ]["size"]
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
                                text = StandardFunctions.CommandInfoCorrections(action.data())["ActionText"]
                            except Exception:
                                pass

                            # try to get alternative text from ribbonStructure
                            try:
                                textJSON = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                    "commands"
                                ][action.data()]["text"]

                                # There is a bug in freecad with the comp-sketch menu hase the wrong text
                                if (
                                    action.data() == "PartDesign_CompSketches"
                                    and self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                        "commands"
                                    ][action.data()]["text"]
                                    == "Create datum"
                                ):
                                    textJSON = "Create sketch"

                                # Check if the original menutext is different
                                # if so use the alternative, otherwise use original
                                for CommandName in Gui.listCommands():
                                    Command = Gui.Command.get(CommandName)
                                    MenuName = CommandInfoCorrections(CommandName)["menuText"].replace("&", "")
                                    if CommandName == action.data():
                                        if (
                                            MenuName
                                            != self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                                "commands"
                                            ][action.data()]["text"]
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
                                pixmap = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                    "commands"
                                ][CommandName]["icon"]
                            except Exception:
                                pass
                            actionIcon = self.ReturnCommandIcon(action.data(), pixmap)
                            if actionIcon is not None:
                                action.setIcon(actionIcon)

                            # try to get alternative icon from ribbonStructure
                            try:
                                icon_Json = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                    "commands"
                                ][CommandName]["icon"]
                                if icon_Json != "":
                                    action.setIcon(Gui.getIcon(icon_Json))
                            except KeyError:
                                pass

                            # If the icon is still none, try to retrieve it from the data file
                            if action.icon() is None or (action.icon() is not None and action.icon().isNull()):
                                StandardFunctions.Print(f"An icon retrieved from data file for '{CommandName}'")
                                DataFile = os.path.join(os.path.dirname(__file__), "RibbonDataFile.dat")

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
                                                Icon: QIcon = Serialize_Ribbon.deserializeIcon(IconItem[1])
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
                                buttonSize = self.ribbonStructure["workbenches"][workbenchName]["toolbars"][toolbar][
                                    "commands"
                                ][CommandName]["size"]
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
                                if IconOnly is True or Parameters_Ribbon.USE_FC_OVERLAY is True:
                                    showText = False

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                    Parameters_Ribbon.ICON_SIZE_SMALL,
                                )
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn = CustomControls.CustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=11,
                                    showText=showText,
                                    setWordWrap=False,
                                    ElideMode=False,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                )
                                # add the button as large button
                                panel.addSmallWidget(
                                    btn,
                                    alignment=Qt.AlignmentFlag.AlignLeft,
                                    fixedHeight=False,
                                )  # Set fixedheight to false. This is set in the custom widgets

                            elif buttonSize == "medium":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
                                if IconOnly is True or Parameters_Ribbon.USE_FC_OVERLAY is True:
                                    showText = False

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                    Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                )
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn = CustomControls.CustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=11,
                                    showText=showText,
                                    setWordWrap=Parameters_Ribbon.WRAPTEXT_MEDIUM,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                )
                                # add the button as large button
                                panel.addMediumWidget(
                                    btn,
                                    alignment=Qt.AlignmentFlag.AlignLeft,
                                    fixedHeight=False,
                                )  # Set fixedheight to false. This is set in the custom widgets
                            elif buttonSize == "large":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE
                                if IconOnly is True or Parameters_Ribbon.USE_FC_OVERLAY is True:
                                    showText = False

                                # Create a custom toolbutton
                                ButtonSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                )
                                IconSize = QSize(
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                    Parameters_Ribbon.ICON_SIZE_LARGE,
                                )
                                Menu = QMenu(self)
                                if button.menu() is not None:
                                    Menu = button.menu()
                                btn: QToolButton = CustomControls.LargeCustomToolButton(
                                    Text=action.text(),
                                    Action=action,
                                    Icon=action.icon(),
                                    IconSize=IconSize,
                                    ButtonSize=ButtonSize,
                                    FontSize=11,
                                    showText=showText,
                                    setWordWrap=Parameters_Ribbon.WRAPTEXT_LARGE,
                                    MaxNumberOfLines=2,
                                    Menu=Menu,
                                    MenuButtonSpace=16,
                                )
                                # add the button as large button
                                panel.addLargeWidget(
                                    btn,
                                    fixedHeight=False,
                                    alignment=Qt.AlignmentFlag.AlignTop,
                                )  # Set fixedheight to false. This is set in the custom widgets
                            else:
                                if Parameters_Ribbon.DEBUG_MODE is True:
                                    if buttonSize != "none":
                                        print(f"{action.text()} is ignored. Its size was: {buttonSize}")
                                pass

                            # Set the background always to background color.
                            # Styling is managed in the custom button class
                            StyleSheet_Addition_Button = (
                                "QToolButton, QToolButton:hover {background-color: "
                                + StyleMapping.ReturnStyleItem("Background_Color")
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
            if panel.title() in "Views - Ribbon_newPanel" or panel.title() in "Individual views":
                panel.setTitle(" Views ")
            else:
                # Remove possible workbench names from the titles
                ListDelimiters = [" - ", "-"]
                for delimiter in ListDelimiters:
                    if len(title.split(delimiter, 1)) > 1:
                        title = title.split(delimiter, 1)[1]
                if title.startswith(workbenchTitle) is True and title != workbenchTitle:
                    title = title.replace(workbenchTitle, "")
                if title.startswith(" ") is True:
                    title = title.replace(" ", "")
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
            Font.setPixelSize(11)
            panel._titleLabel.setFont(Font)
            self.RibbonHeight = self.ReturnRibbonHeight(self.RibbonOffset) + 6

            # Setup the panelOptionButton
            actionList = []
            for i in range(len(ButtonList)):
                button = ButtonList[i]
                if len(button.actions()) == 1:
                    actionList.append(button.actions()[0])
                if len(button.actions()) > 1:
                    actionList.append(button.actions())
            OptionButton = panel.panelOptionButton()
            if len(actionList) > 0:
                for i in range(len(actionList)):
                    action = actionList[i]
                    if isinstance(action, QAction):
                        OptionButton.addAction(action)
                    if isinstance(action, list):
                        # if it is a submenu, it is a list with two items
                        # The first, is the default action with text
                        # The second is the action with all the subactions, but without text or icon

                        # Get the first action
                        action_0 = action[0]
                        # Get the second action
                        action_1 = action[1]
                        # Set the text and icon for the second action with those from the first action
                        action_1.setText(action_0.text())
                        action_1.setIcon(action_0.icon())
                        # Add the second action
                        OptionButton.addAction(action_1)
                if len(actionList) == 0:
                    panel.panelOptionButton().hide()

                # Set the behavior of the option button
                OptionButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
                # Remove the image to avoid double arrows
                OptionButton.setStyleSheet("RibbonPanelOptionButton::menu-indicator {image: none;}")
                Menu = OptionButton.menu()
                if Menu is not None:
                    hexColor = StyleMapping.ReturnStyleItem("Background_Color")
                    Menu.setStyleSheet("background-color: " + hexColor)
                # Set the icon
                OptionButton_Icon = StyleMapping.ReturnStyleItem("OptionButton")
                if OptionButton_Icon is not None:
                    OptionButton.setIcon(OptionButton_Icon)
                else:
                    OptionButton.setArrowType(Qt.ArrowType.DownArrow)
                    OptionButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
                    OptionButton.setText("more...")

        self.isWbLoaded[tabName] = True

        # Set the previous/next buttons
        category = self.currentCategory()
        ScrollLeftButton_Category: RibbonCategoryLayoutButton = category.findChildren(RibbonCategoryLayoutButton)[0]
        ScrollRightButton_Category: RibbonCategoryLayoutButton = category.findChildren(RibbonCategoryLayoutButton)[1]
        ScrollLeftButton_Category.setMinimumWidth(self.iconSize * 0.5)
        ScrollRightButton_Category.setMinimumWidth(self.iconSize * 0.5)
        # get the icons
        ScrollLeftButton_Category_Icon = StyleMapping.ReturnStyleItem("ScrollLeftButton_Category")
        ScrollRightButton_Category_Icon = StyleMapping.ReturnStyleItem("ScrollRightButton_Category")
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
        ScrollLeftButton_Category.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton"))
        ScrollRightButton_Category.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton"))
        # Connect the custom click event
        ScrollLeftButton_Category.mousePressEvent = lambda clickLeft: self.on_ScrollButton_Category_clicked(
            clickLeft, ScrollLeftButton_Category
        )
        ScrollRightButton_Category.mousePressEvent = lambda clickRight: self.on_ScrollButton_Category_clicked(
            clickRight, ScrollRightButton_Category
        )

        # Set the maximum height to a high value to prevent from the ribbon to be clipped off
        self.currentCategory().setMinimumHeight(self.RibbonHeight)
        self.currentCategory().setMaximumHeight(self.RibbonHeight)
        self.setRibbonHeight(self.RibbonHeight)
        return

    def on_ScrollButton_Category_clicked(self, event, ScrollButton: RibbonCategoryLayoutButton):
        for i in range(Parameters_Ribbon.RIBBON_CLICKSPEED):
            ScrollButton.click()
        return

    def updateCurrentTab(self):
        currentWbIndex = self.tabBar().indexOf(Gui.activeWorkbench().MenuText)
        currentTabIndex = self.tabBar().currentIndex()

        if currentWbIndex != currentTabIndex:
            self.disconnectSignals()
            self.tabBar().setCurrentIndex(currentWbIndex)
            self.connectSignals()
        self.ApplicationMenus()
        return

    def hideClassicToolbars(self):
        for toolbar in mw.findChildren(QToolBar):
            parentWidget = toolbar.parentWidget()
            toolbar.setHidden(True)
            # hide toolbars that are not in the statusBar and show toolbars that are in the statusbar.
            if parentWidget.objectName() == "statusBar" or parentWidget.objectName() == "StatusBarArea":
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
                            "User parameter:BaseApp/Workbench/" + WorkBenchName + "/Toolbar/" + Group
                        )
                        Name = Parameter.GetString("Name")
                        Toolbars.append([Name, WorkBenchName])

        return Toolbars

    def List_ReturnCustomToolbars_Global(self):
        Toolbars = []
        CustomToolbars: list = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar").GetGroups()

        for Group in CustomToolbars:
            Parameter = App.ParamGet("User parameter:BaseApp/Workbench/Global/Toolbar/" + Group)
            Name = Parameter.GetString("Name")
            Toolbars.append([Name, "Global"])

        return Toolbars

    def List_AddCustomToolBarToWorkbench(self, WorkBenchName, CustomToolbar):
        ButtonList = []

        try:
            # Get the commands from the custom panel
            Commands = self.ribbonStructure["customToolbars"][WorkBenchName][CustomToolbar]["commands"]

            # Get the command and its original toolbar
            for key, value in list(Commands.items()):
                # get the menu text from the command list
                for CommandName in Gui.listCommands():
                    # Get the english menutext
                    MenuName = CommandInfoCorrections(CommandName)["menuText"]
                    # Get the translated menutext
                    MenuNameTtranslated = CommandInfoCorrections(CommandName)["ActionText"]

                    if MenuName == key:
                        try:
                            # Get the original toolbar as QToolbar
                            OriginalToolBar = mw.findChild(QToolBar, value)
                            # Go through all it's QtoolButtons
                            for Child in OriginalToolBar.findChildren(QToolButton):
                                # If the text of the QToolButton matches the menu text
                                # Add it to the button list.
                                IsInList = False
                                for Toolbutton in ButtonList:
                                    if Toolbutton.text() == Child.text():
                                        IsInList = True

                                if Child.text() == MenuNameTtranslated and IsInList is False:
                                    ButtonList.append(Child)
                        except Exception as e:
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                StandardFunctions.Print(f"{e.with_traceback(e.__traceback__)}, 3", "Warning")
                            continue
        except Exception:
            pass

        return ButtonList

    def List_AddNewPanelToWorkbench(self, WorkBenchName, NewPanel):
        ButtonList = []

        try:
            if WorkBenchName in self.ribbonStructure["newPanels"]:
                if NewPanel in self.ribbonStructure["newPanels"][WorkBenchName]:
                    # Get the commands from the custom panel
                    Commands = self.ribbonStructure["newPanels"][WorkBenchName][NewPanel]

                    # Get the command and its original toolbar
                    for CommandItem in Commands:
                        CommandName = CommandItem[0]
                        # Define a new toolbutton
                        NewToolbutton = RibbonToolButton()
                        if CommandName.endswith("_ddb") is False:
                            # Get the translated menutext
                            Command = Gui.Command.get(CommandName)

                            if Command is not None:
                                CommandActionList = Command.getAction()
                                if CommandActionList is None:
                                    continue
                                # if there are actions, proceed
                                if len(CommandActionList) > 0:
                                    # if there is only one action, add it directly
                                    if len(CommandActionList) == 1:
                                        NewToolbutton.addAction(CommandActionList[0])
                                        NewToolbutton.setDefaultAction(NewToolbutton.actions()[0])
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
                                    NewToolbutton.setText(
                                        CommandInfoCorrections(CommandName)["menuText"].replace("&", "")
                                    )
                                    # add it to the list
                                    ButtonList.append(NewToolbutton)

                            if Command is None:
                                if Parameters_Ribbon.DEBUG_MODE is True:
                                    StandardFunctions.Print(f"{CommandName} was None", "Warning")
                        if CommandName.endswith("_ddb") is True:
                            CommandActionList = self.returnCustomDropDown(CommandName)
                            if CommandActionList is None or len(CommandActionList) < 1:
                                continue

                            # if there are actions, proceed
                            if len(CommandActionList) > 0:
                                # if there is only one action, add it directly
                                if len(CommandActionList) == 1:
                                    NewToolbutton.addAction(CommandActionList[0])
                                    NewToolbutton.setDefaultAction(NewToolbutton.actions()[0])
                                # if there are more actions, create a menu
                                if len(CommandActionList) > 1:
                                    menu = QMenu()
                                    for action in CommandActionList:
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
                StandardFunctions.Print(f"{e.with_traceback(e.__traceback__)}, 4", "Warning")
            pass
        return ButtonList

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
            Parameters_Ribbon.ICON_SIZE_SMALL * 3 >= Parameters_Ribbon.ICON_SIZE_MEDIUM * 2
            and Parameters_Ribbon.ICON_SIZE_SMALL * 3 >= LargeButtonHeight
        ):
            ribbonHeight = ribbonHeight + Parameters_Ribbon.ICON_SIZE_SMALL * 3 + 6
        elif (
            Parameters_Ribbon.ICON_SIZE_MEDIUM * 2 >= Parameters_Ribbon.ICON_SIZE_SMALL * 3
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

    def CustomOverlay(self):
        # Toggle the overlay
        Enable = True
        if self.OverlayToggled is True:
            Enable = False

        # mw.findChildren(PySide.QtWidgets.QDockWidget)
        # mw.dockWidgetArea(child)

        # Get the different overlay areas
        OverlayParam_Left = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft")
        OverlayParam_Right = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayRight")
        OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
        OverlayParam_Bottom = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom")

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
                if DockWidget.objectName() != "Ribbon":
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

            EntryLeft = ""
            for panel in PanelsLeft:
                EntryLeft = EntryLeft + "," + panel
            # Set the parameter
            OverlayParam_Left.SetString("Widgets", EntryLeft)

            # Define the parameter value for the overlay on the right
            EntryRight = ""
            for panel in PanelsRight:
                EntryRight = EntryRight + "," + panel
            # Set the parameter
            OverlayParam_Right.SetString("Widgets", EntryRight)

            # Define the parameter value for the overlay on the right
            EntryTop = ""
            for panel in PanelsTop:
                EntryTop = EntryTop + "," + panel
            # Set the parameter
            OverlayParam_Top.SetString("Widgets", EntryTop)

            # Define the parameter value for the overlay on the right
            EntryBottom = ""
            for panel in PanelsBottom:
                EntryBottom = EntryBottom + "," + panel
            # Set the parameter
            OverlayParam_Bottom.SetString("Widgets", EntryBottom)

            # Set the overlay stat to be toggled
            self.OverlayToggled = True

        if Enable is False:
            # Set the parameters to empty
            OverlayParam_Left.SetString("Widgets", "")
            OverlayParam_Right.SetString("Widgets", "")

            # Set the overlay stat to be untoggled
            self.OverlayToggled = False

        return self.OverlayToggled

    def CustomTransparancy(self):
        OverlayParam_Left = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayLeft")
        OverlayParam_Right = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayRight")
        OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
        OverlayParam_Bottom = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayBottom")

        Enable = None
        if OverlayParam_Left.GetBool("Transparent") is False:
            Enable = True
        if OverlayParam_Left.GetBool("Transparent") is True:
            Enable = False

        OverlayParam_Left.SetBool("Transparent", Enable)
        OverlayParam_Right.SetBool("Transparent", Enable)
        OverlayParam_Top.SetBool("Transparent", Enable)
        OverlayParam_Bottom.SetBool("Transparent", Enable)

        self.TransparancyToggled = True

        return self.TransparancyToggled

    def returnCustomDropDown(self, CommandName):
        actionList = []

        try:
            for DropDownCommand, Commands in self.ribbonStructure["dropdownButtons"].items():
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
                StandardFunctions.Print(f"{e.with_traceback(e.__traceback__)}", "Warning")
            return

    # def UpdateRibbonStructureFile_Proxy(self, RibbonStructureDict: dict):
    #     # get the path for the Json file
    #     JsonFile: dict = Parameters_Ribbon.RIBBON_STRUCTURE_JSON

    #     # Writing to sample.json
    #     with open(JsonFile, "w") as outfile:
    #         JsonFile.update(RibbonStructureDict)
    #         json.dump(self.ribbonStructure, outfile, indent=4)

    #     outfile.close()
    #     return


# region - alternative loading
# class run:
#     """
#     Activate Modern UI.
#     """

#     def __init__(self, name):
#         """
#         Constructor
#         """
#         disable = 0
#         if name != "NoneWorkbench":
#             mw = Gui.getMainWindow()

#             # Disable connection after activation
#             mw.workbenchActivated.disconnect(run)
#             if disable:
#                 return

#             ribbon = ModernMenu()
#             # Get the layout
#             layout = ribbon.layout()
#             # Set spacing and content margins to zero
#             layout.setSpacing(0)
#             layout.setContentsMargins(3, 0, 3, 3)
#             # update the layout
#             ribbon.setLayout(layout)
#             # Create the ribbon
#             mw.setMenuBar(ribbon)
# endregion


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
            mw = Gui.getMainWindow()
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
            # ribbonDock.setMaximumHeight(ribbon.ReturnRibbonHeight() - 20)
            # Add the dockwidget to the main window
            mw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, ribbonDock)


# def UpdateRibbonStructureFile(RibbonStructureDict: dict = None, silent=True):
#     """Function for add-on developers to update the RibbonStructureFile with their specific settings.
#     The RibbonStructureFile must have at least one of the following keys:
#     - "igonreWorkbenches"
#     - "customToolbars"
#     - "newPanels"
#     - "dropdownButtons"
#     - "iconOnlyToolbars"
#     - "workbenches"

#     Args:
#         RibbonStructureFile (dict): a dictionary that follows the RibbonStructureFile format.\n
#         See the RibbonStructureFile.json for the format. (Located in the add-on directory)
#     """
#     result = False

#     if RibbonStructureDict is not None:
#         try:
#             preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/FreeCAD-Ribbon")
#             JsonFile = preferences.GetString("RibbonStructure")
#             if JsonFile is not None or JsonFile != "":
#                 with open(JsonFile, "r") as outfile:
#                     data = json.load(outfile)
#                 outfile.close()

#                 merged_dict = data.copy()
#                 merged_dict.update(RibbonStructureDict)

#                 with open(JsonFile, "w") as outfile:
#                     json.dump(merged_dict, outfile, indent=4)
#                 outfile.close()
#             result = True

#         except Exception as e:
#             if silent is False:
#                 raise e
#             else:
#                 print(e)
#     return result
