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
)

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
import StyleMapping
import platform

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
# from pyqtribbon.panel import RibbonPanel
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
    RightToolBarButtonSize = Parameters_Ribbon.RIGHT_ICON_SIZE
    TabBar_Size = Parameters_Ribbon.TABBAR_SIZE

    # Set a sixe factor for the buttons
    sizeFactor = 1.3

    # Placeholders for toggle function of the ribbon
    RibbonMinimalHeight = ApplicationButtonSize + 10
    RibbonMaximumHeight = 240  # Will be redefined later

    CategoryList = []

    Position = []

    def __init__(self):
        """
        Constructor
        """
        super().__init__(title="", iconSize=self.iconSize)
        self.setObjectName("Ribbon")

        self.setWindowFlags(self.windowFlags() | Qt.Dialog)

        # Get the style from the main window
        palette = mw.palette()
        self.setPalette(palette)
        Style = mw.style()
        self.setStyle(Style)

        # connect the signals
        self.connectSignals()

        # read ribbon structure from JSON file
        with open(Parameters_Ribbon.RIBBON_STRUCTURE_JSON, "r") as file:
            self.ribbonStructure.update(json.load(file))
        file.close()

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
        # Add a toolbar "Views - Ribbon"
        StandardFunctions.CreateToolbar(
            Name="Views - Ribbon",
            WorkBenchName="Global",
            ButtonList=[
                "Std_ViewGroup",
                "Std_ViewFitAll",
                "Std_ViewZoomOut",
                "Std_ViewZoomIn",
                "Std_ViewBoxZoom",
                "Std_ViewFitAll",
                "Std_AlignToSelection",
                "Part_SelectFilter",
            ],
        )
        # Add a toolbar "tools"
        StandardFunctions.CreateToolbar(
            Name="Tools",
            WorkBenchName="Global",
            ButtonList=[
                "Std_Measure",
                "Std_UnitsCalculator",
                "Std_Properties",
                "Std_BoxElementSelection",
                "Std_BoxSelection",
                "Std_WhatsThis",
            ],
        )

        # Set the preferred toolbars
        PreferredToolbar = Parameters_Ribbon.Settings.GetIntSetting("Preferred_view")
        ListIgnoredToolbars: list = self.ribbonStructure["ignoredToolbars"]
        if PreferredToolbar == 0:
            ListIgnoredToolbars.append("View")
            ListIgnoredToolbars.append("Views - Ribbon")
            if "Individual views" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("Individual views")
        if PreferredToolbar == 1:
            ListIgnoredToolbars.append("Individual views")
            ListIgnoredToolbars.append("Views - Ribbon")
            if "View" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("View")
        if PreferredToolbar == 2:
            ListIgnoredToolbars.append("Individual views")
            ListIgnoredToolbars.append("Views")
            if "Views - Ribbon" in ListIgnoredToolbars:
                ListIgnoredToolbars.remove("Views - Ribbon")
        if PreferredToolbar == 3:
            ListIgnoredToolbars.append("Individual views")
            ListIgnoredToolbars.append("Views")
            ListIgnoredToolbars.append("Views - Ribbon")
        self.ribbonStructure["ignoredToolbars"] = ListIgnoredToolbars

        # Get the address of the repository address
        self.ReproAdress = StandardFunctions.getRepoAdress(os.path.dirname(__file__))
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(translate("FreeCAD Ribbon", "FreeCAD Ribbon: ") + self.ReproAdress)

        # Set the icon size if parameters has none
        Parameters_Ribbon.Settings.WriteSettings()

        # Create the ribbon
        self.createModernMenu()
        self.onUserChangedWorkbench()

        # Set the custom stylesheet
        StyleSheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
        # modify the stylesheet to set the border for a toolbar menu
        hexColor = StyleMapping.ReturnStyleItem("Background_Color")
        if hexColor is not None and hexColor != "":
            # Set the quickaccess toolbar background color. This fixes a transparant toolbar.
            self.quickAccessToolBar().setStyleSheet(
                "QToolBar {background: " + hexColor + ";}"
            )
            self.tabBar().setStyleSheet("background: " + hexColor + ";")
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
        self

        # get the state of the mainwindow
        self.MainWindowLoaded = True

        # Set these settings and connections at init
        # Set the autohide behavior of the ribbon
        self.setAutoHideRibbon(Parameters_Ribbon.AUTOHIDE_RIBBON)

        # Remove the collapseble button
        RightToolbar = self.rightToolBar()
        RightToolbar.removeAction(RightToolbar.actions()[0])

        # make sure that the ribbon cannot "disappear"
        self.setMinimumHeight(self.RibbonMinimalHeight)

        # Set the menuBar hidden as standard
        mw.menuBar().hide()
        if self.isEnabled() is False:
            mw.menuBar().show()

        # connect a tabbar click event to the tarbar click funtion
        # this used to replaced the native functions
        self.tabBar().tabBarClicked.connect(self.onTabBarClicked)

        # Set the maximum heigth for the ribbon
        self.RibbonMaximumHeight = (
            self.currentCategory().height() + self.RibbonMinimalHeight
        )

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
        ScrollLeftButton_Tab_Icon = StyleMapping.ReturnStyleItem("ScrollLeftButton_Tab")
        ScrollRightButton_Tab_Icon = StyleMapping.ReturnStyleItem(
            "ScrollRightButton_Tab"
        )
        # Set the icons
        StyleSheet = "QToolButton {image: none};QToolButton::arrow {image: none};"
        BackgroundColor = StyleMapping.ReturnStyleItem("Background_Color")
        if (
            int(App.Version()[0]) == 0
            and int(App.Version()[1]) <= 21
            and BackgroundColor is not None
        ):
            StyleSheet = (
                """QToolButton {image: none;background: """
                + BackgroundColor
                + """};QToolButton::arrow {image: none};"""
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

        # # store the position coordinates from the ribbon
        # X1 = self.pos().x()
        # Y1 = self.pos().y()
        # X2 = X1 + self.width()
        # Y2 = Y1 - self.height()
        # self.Position = [X1, Y1, X2, Y2]
        return

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
        if (
            int(App.Version()[0]) == 0
            and int(App.Version()[1]) <= 21
            and Parameters_Ribbon.Settings.GetBoolSetting("ShowOnHover") is True
        ):
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            TB.setMinimumHeight(self.RibbonMaximumHeight)
            TB.setMaximumHeight(self.RibbonMaximumHeight)
            self.setFixedHeight(self.RibbonMaximumHeight)

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
        # add quick access buttons
        i = 1  # Start value for button count. Used for width of quickaccess toolbar
        toolBarWidth = (
            (self.QuickAccessButtonSize * self.sizeFactor) * i
        ) + self.ApplicationButtonSize
        for commandName in self.ribbonStructure["quickAccessCommands"]:
            i = i + 1
            width = 0
            button = QToolButton()
            try:
                QuickAction = Gui.Command.get(commandName).getAction()

                if len(QuickAction) <= 1:
                    button.setDefaultAction(QuickAction[0])
                    width = self.QuickAccessButtonSize
                    height = self.QuickAccessButtonSize
                    button.setFixedSize(width, height)
                elif len(QuickAction) > 1:
                    button.addActions(QuickAction)
                    button.setDefaultAction(QuickAction[0])
                    width = (self.QuickAccessButtonSize) + self.QuickAccessButtonSize
                    height = self.QuickAccessButtonSize
                    button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
                    button.setFixedSize(width, height)
                button.setStyleSheet(StyleMapping.ReturnStyleSheet("toolbutton"))
                self.setQuickAccessButtonHeight(self.QuickAccessButtonSize)

                # Add the button to the quickaccess toolbar
                self.addQuickAccessButton(button)

                toolBarWidth = toolBarWidth + width
            except Exception:
                continue

        self.quickAccessToolBar().show()
        # Set the height of the quickaccess toolbar
        self.quickAccessToolBar().setMinimumHeight(self.RibbonMinimalHeight)

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
        self.tabBar().setContentsMargins(3, 3, 3, 3)
        font = self.tabBar().font()
        font.setPixelSize(self.TabBar_Size * 0.6)
        self.tabBar().setFont(font)
        self.tabBar().setIconSize(QSize(self.TabBar_Size - 6, self.TabBar_Size - 6))

        # Set the tabbar height and textsize
        self.tabBar().setIconSize(QSize(self.iconSize, self.iconSize))

        # Correct colors when no stylesheet is selected for FreeCAD.
        FreeCAD_preferences = App.ParamGet(
            "User parameter:BaseApp/Preferences/MainWindow"
        )
        currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")
        if currentStyleSheet == "":
            hexColor = StyleMapping.ReturnStyleItem("Background_Color")
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
                    WorkbenchOrderedList.insert(index_1 - 1, "AssemblyWorkbench")
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
                        if Parameters_Ribbon.TABBAR_STYLE == 0:
                            # set tab icon
                            self.tabBar().setTabIcon(
                                len(self.categories()) - 1, QIcon(workbench.Icon)
                            )
                        if Parameters_Ribbon.TABBAR_STYLE == 1:
                            self.tabBar().setTabIcon(
                                len(self.categories()) - 1, QIcon()
                            )

        # Set the size of the collapseRibbonButton
        self.collapseRibbonButton().setFixedSize(
            self.RightToolBarButtonSize, self.RightToolBarButtonSize
        )

        # add the searchbar if available
        SearchBarWidth = self.AddSearchBar()

        # Set the helpbutton
        self.helpRibbonButton().setEnabled(True)
        self.helpRibbonButton().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.helpRibbonButton().setToolTip(
            translate("FreeCAD Ribbon", "Go to the FreeCAD help page")
        )
        # Get the default help action from FreeCAD
        helpMenu = mw.findChildren(QMenu, "&Help")[0]
        helpAction = helpMenu.actions()[0]
        self.helpRibbonButton().setDefaultAction(helpAction)
        self.helpRibbonButton().setFixedSize(
            self.RightToolBarButtonSize, self.RightToolBarButtonSize
        )

        # Add a button the enable or disable AutoHide
        pinButton = QToolButton()
        pinButton.setCheckable(True)
        pinButton.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        pinButton.setFixedSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize)
        pinButton.setIconSize(
            QSize(self.RightToolBarButtonSize, self.RightToolBarButtonSize)
        )
        pinButtonIcon = StyleMapping.ReturnStyleItem("PinButton_open")
        if pinButtonIcon is not None:
            pinButton.setIcon(pinButtonIcon)
        pinButton.setText(translate("FreeCAD Ribbon", "Pin Ribbon"))
        pinButton.setToolTip(
            translate(
                "FreeCAD Ribbon", "Click to toggle the autohide function on or off"
            )
        )
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButton.setChecked(False)
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButton.setChecked(True)
        pinButton.clicked.connect(self.onPinClicked)
        self.rightToolBar().addWidget(pinButton)

        # Set the width of the right toolbar
        RightToolbarWidth = SearchBarWidth
        for child in self.rightToolBar().actions():
            RightToolbarWidth = RightToolbarWidth + self.RightToolBarButtonSize
        self.rightToolBar().setMinimumWidth(
            RightToolbarWidth - self.RightToolBarButtonSize * 1.5
        )
        # Set the size policy
        self.rightToolBar().setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )
        # Set the objectName for the right toolbar. needed for excluding from hiding.
        self.rightToolBar().setObjectName("rightToolBar")

        # Set the application button
        self.applicationOptionButton().setToolTip(
            translate("FreeCAD Ribbon", "FreeCAD Ribbon")
        )
        self.applicationOptionButton().setFixedSize(
            self.ApplicationButtonSize, self.ApplicationButtonSize
        )
        self.setApplicationIcon(Gui.getIcon("freecad"))

        # Set the border color and shape
        radius = str((self.applicationOptionButton().width() * 0.49) - 1) + "px"
        self.applicationOptionButton().setStyleSheet(
            StyleMapping.ReturnStyleSheet("applicationbutton", radius)
        )

        # add the menus from the menubar to the application button
        self.ApplicationMenu()
        # Set the size policy for the ribbon
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )
        return

    # Add the searchBar if it is present
    def AddSearchBar(self):
        TB: QToolBar = mw.findChildren(QToolBar, "SearchBar")
        width = 0
        if TB is not None:
            try:
                import SearchBoxLight

                width = 200

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
                sea.setFixedSize(width, self.iconSize)
                BeforeAction = self.rightToolBar().actions()[1]
                self.rightToolBar().insertWidget(BeforeAction, sea)
                width = sea.width()
            except Exception:
                pass
            return width

    def ApplicationMenu(self):
        # Add a file menu
        Menu = self.addFileMenu()

        # Remove the border, cause by creating it for the applicationOptionButton
        StyleSheet = """border: none;"""
        Menu.setStyleSheet(StyleSheet)

        # add the menus from the menubar to the application button
        MenuBar = mw.menuBar()
        Menu.addActions(MenuBar.actions())

        # Add the ribbon design button
        Menu.addSeparator()
        DesignMenu = Menu.addMenu(translate("FreeCAD Ribbon", "Customize..."))
        DesignButton = DesignMenu.addAction(
            translate("FreeCAD Ribbon", "Ribbon layout")
        )
        DesignButton.triggered.connect(self.loadDesignMenu)
        # Add the preference button
        PreferenceButton = DesignMenu.addAction(
            translate("FreeCAD Ribbon", "Ribbon preferences")
        )
        PreferenceButton.triggered.connect(self.loadSettingsMenu)
        # Add the script submenu with items
        ScriptDir = os.path.join(os.path.dirname(__file__), "Scripts")
        if os.path.exists(ScriptDir) is True:
            ListScripts = os.listdir(ScriptDir)
            if len(ListScripts) > 0:
                ScriptButtonMenu = DesignMenu.addMenu(
                    translate("FreeCAD Ribbon", "Scripts")
                )
                for i in range(len(ListScripts)):
                    ScriptButtonMenu.addAction(
                        ListScripts[i],
                        lambda i=i + 1: self.LoadMarcoFreeCAD(ListScripts[i - 1]),
                    )
        # Add a about button, a What's new? and a help button for this ribbon
        #
        # Get the version of this addon
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        version = StandardFunctions.ReturnXML_Value(PackageXML, "version")

        Menu.addSeparator()
        WhatsNewButton = Menu.addAction(translate("FreeCAD Ribbon", "What's new?"))
        WhatsNewButton.triggered.connect(self.on_WhatsNewButton_clicked)
        RibbonHelpButton = Menu.addAction(translate("FreeCAD Ribbon", "Ribbon help"))
        RibbonHelpButton.triggered.connect(self.on_RibbonHelpButton_clicked)
        AboutButton = Menu.addAction(
            translate("FreeCAD Ribbon", "About FreeCAD Ribbon ") + version
        )
        AboutButton.triggered.connect(self.on_AboutButton_clicked)

        return

    def loadDesignMenu(self):
        message = translate(
            "FreeCAD Ribbon",
            "All workbenches need to be loaded.\nThis can take a couple of minutes.\nDo you want to proceed?",
        )
        result = StandardFunctions.Mbox(message, "", 1, IconType="Question")
        if result == "yes":
            LoadDesign_Ribbon.main()
        return

    def loadSettingsMenu(self):
        LoadSettings_Ribbon.main()
        return

    def on_AboutButton_clicked(self):
        LoadLicenseForm_Ribbon.main()
        return

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

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            TB.setMinimumHeight(self.RibbonMaximumHeight)
            TB.setMaximumHeight(self.RibbonMaximumHeight)
            self.setFixedHeight(self.RibbonMaximumHeight)
            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", False)
            Parameters_Ribbon.AUTOHIDE_RIBBON = False

            # Make sure that the ribbon remains visible
            self.setRibbonVisible(True)
            return
        return

    def onUserChangedWorkbench(self):
        """
        Import selected workbench toolbars to ModernMenu section.
        """

        index = self.tabBar().currentIndex()
        tabName = self.tabBar().tabText(index)

        if tabName is not None and tabName != "":
            Color = QColor(StyleMapping.ReturnStyleItem("Border_Color"))
            self.tabBar().setTabTextColor(index, Color)

            # activate selected workbench
            tabName = tabName.replace("&", "")
            if self.wbNameMapping[tabName] is not None:
                Gui.activateWorkbench(self.wbNameMapping[tabName])
            self.onWbActivated()
            self.ApplicationMenu()
        return

    def onWbActivated(self):
        # Make sure that the text is readable
        self.tabBar().setStyleSheet(
            "color: " + StyleMapping.ReturnStyleItem("Border_Color") + ";"
        )

        # switch tab if necessary
        self.updateCurrentTab()

        # hide normal toolbars
        self.hideClassicToolbars()

        # ensure that workbench is already loaded
        workbench = Gui.activeWorkbench()
        if not hasattr(workbench, "__Workbench__"):
            # XXX for debugging purposes
            if Parameters_Ribbon.DEBUG_MODE is True:
                print(f"wb {workbench.MenuText} not loaded")

            Gui.activateWorkbench(workbench.name())
            # wait for 0.1s hoping that after that time the workbench is loaded
            timer.timeout.connect(self.onWbActivated)
            timer.setSingleShot(True)
            timer.start(500)
            # return

        # create panels
        self.buildPanels()
        return

    def onTabBarClicked(self):
        TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        TB.setMinimumHeight(self.RibbonMaximumHeight)
        TB.setMaximumHeight(self.RibbonMaximumHeight)
        self.setFixedHeight(self.RibbonMaximumHeight)
        self.setRibbonVisible(True)

    def buildPanels(self):
        # Get the active workbench and get tis name
        workbench = Gui.activeWorkbench()
        workbenchName = workbench.name()

        # check if the panel is already loaded. If so exit this function
        tabName = self.tabBar().tabText(self.tabBar().currentIndex()).replace("&", "")
        if self.isWbLoaded[tabName] or tabName == "":
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
            for CustomPanel in self.ribbonStructure["customToolbars"][workbenchName]:
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
                        ListToolbars.remove(OriginalToolbar)
                    except Exception:
                        continue
        except Exception as e:
            if Parameters_Ribbon.DEBUG_MODE is True:
                print(f"{e.with_traceback(e.__traceback__)}, 1")
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
                    position = ToolbarOrder.index(toolbar)
                except ValueError:
                    position = 999999
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
            panel = self.currentCategory().addPanel(
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

            customList = self.List_AddCustomToolbarsToWorkbench(workbenchName, toolbar)
            allButtons.extend(customList)

            # add separators to the command list.
            if workbenchName in self.ribbonStructure["workbenches"]:
                if (
                    toolbar != ""
                    and toolbar
                    in self.ribbonStructure["workbenches"][workbenchName]["toolbars"]
                ):
                    if (
                        "order"
                        in self.ribbonStructure["workbenches"][workbenchName][
                            "toolbars"
                        ][toolbar]
                    ):
                        for j in range(
                            len(
                                self.ribbonStructure["workbenches"][workbenchName][
                                    "toolbars"
                                ][toolbar]["order"]
                            )
                        ):
                            if (
                                self.ribbonStructure["workbenches"][workbenchName][
                                    "toolbars"
                                ][toolbar]["order"][j]
                                .lower()
                                .__contains__("separator")
                            ):
                                separator = QToolButton()
                                separator.setText(
                                    self.ribbonStructure["workbenches"][workbenchName][
                                        "toolbars"
                                    ][toolbar]["order"][j]
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
                        Text = button.text().replace("...", "")

                        try:
                            action = None
                            if len(button.actions()) > 0:
                                action = button.actions()[0]
                            if action is not None:
                                Text = CommandInfoCorrections(action.data())[
                                    "menuText"
                                ].replace("...", "")
                                # There is a bug in freecad with the comp-sketch menu hase the wrong text
                                if (
                                    action.data() == "PartDesign_CompSketches"
                                    and Text.replace("...", "") == "Create datum"
                                ):
                                    Text = "Create sketch"

                        except Exception:
                            pass

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
            NoSmallButtons_spacer = 0  # needed to count the number of small buttons in a column. (bug fix with adding separators)
            NoMediumButtons_spacer = 0  # needed to count the number of medium buttons in a column. (bug fix with adding separators)

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
                if buttonSize == "large" or button.text().__contains__("separator"):
                    rowCount = rowCount + LargeButtonRows

                # If the number of rows divided by 3 is a whole number,
                # the number of columns is the rowcount divided by 3.
                columnCount = rowCount / 3
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
                        if columnCount > maxColumns + 1:
                            ButtonList.append(button)
                            panel.panelOptionButton().show()
                            continue

                    # If the last item is not an separator, you can add an separator
                    # With an paneloptionbutton, use an offset of 2 instead of 1 for i.
                    if button.text().__contains__("separator") and i < len(allButtons):
                        separator = panel.addLargeVerticalSeparator(
                            alignment=Qt.AlignmentFlag.AlignLeft, fixedHeight=False
                        )
                        # there is a bug in pyqtribbon where the separator is placed in the wrong position
                        # despite the correct order of the button list.
                        # To correct this, empty and disabled buttons are added for spacing.
                        # (adding spacers did not work)
                        if float((NoSmallButtons_spacer + 1) / 3).is_integer():
                            panel.addSmallButton().setEnabled(False)
                        if float((NoSmallButtons_spacer + 2) / 3).is_integer():
                            panel.addSmallButton().setEnabled(False)
                            panel.addSmallButton().setEnabled(False)
                        # reset the counter after a separator is added.
                        NoSmallButtons_spacer = 0
                        # Same principle for medium buttons
                        if float((NoMediumButtons_spacer + 1) / 2).is_integer():
                            panel.addMediumButton().setEnabled(False)
                        NoMediumButtons_spacer = 0
                        continue
                    else:
                        try:
                            action = button.defaultAction()

                            # get the action text
                            text = StandardFunctions.TranslationsMapping(
                                workbenchName, action.text()
                            )

                            # There is a bug in freecad with the comp-sketch menu hase the wrong text
                            if (
                                action.data() == "PartDesign_CompSketches"
                                and action.text().replace("...", "") == "Create datum"
                            ):
                                text = "Create sketch"

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
                                    Command = Gui.Command.get(CommandName)
                                    MenuName = CommandInfoCorrections(CommandName)[
                                        "menuText"
                                    ].replace("...", "")

                                    if (
                                        CommandName
                                        == self.ribbonStructure["workbenches"][
                                            workbenchName
                                        ]["toolbars"][toolbar]["commands"][
                                            action.data()
                                        ]
                                    ):
                                        if (
                                            MenuName
                                            != self.ribbonStructure["workbenches"][
                                                workbenchName
                                            ]["toolbars"][toolbar]["commands"][
                                                action.data()
                                            ][
                                                "text"
                                            ]
                                        ):
                                            text = textJSON

                                # the text would be overwritten again when the state of the action changes
                                # (e.g. when getting enabled / disabled), therefore the action itself
                                # is manipulated.
                                action.setText(text)
                            except KeyError:
                                text = action.text()

                            if action.icon() is None:
                                CommandName = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][action.data()]
                                action.setIcon(
                                    Gui.getIcon(
                                        CommandInfoCorrections(CommandName)["pixmap"]
                                    )
                                )

                            # try to get alternative icon from ribbonStructure
                            try:
                                icon_Json = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][action.data()][
                                    "icon"
                                ]
                                if icon_Json != "":
                                    action.setIcon(Gui.getIcon(icon_Json))
                            except KeyError:
                                icon_Json = action.icon()

                            # get button size from ribbonStructure
                            try:
                                buttonSize = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][action.data()][
                                    "size"
                                ]
                            except KeyError:
                                buttonSize = "small"  # small as default

                            # Check if this is an icon only toolbar
                            IconOnly = False
                            for iconToolbar in self.ribbonStructure["iconOnlyToolbars"]:
                                if iconToolbar == toolbar:
                                    IconOnly = True

                            btn = RibbonToolButton()
                            if buttonSize == "small":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_SMALL
                                if IconOnly is True:
                                    showText = False

                                btn = panel.addSmallButton(
                                    action.text(),
                                    action.icon(),
                                    alignment=Qt.AlignmentFlag.AlignLeft,
                                    showText=showText,
                                    fixedHeight=Parameters_Ribbon.ICON_SIZE_SMALL,
                                )

                                # Set the stylesheet
                                # Set the padding to align the icons to the left
                                padding = btn.height() / 3
                                btn.setStyleSheet(
                                    StyleMapping.ReturnStyleSheet(
                                        "toolbutton", "2px", f"{padding}px"
                                    )
                                )

                            elif buttonSize == "medium":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM
                                if IconOnly is True:
                                    showText = False

                                btn = panel.addMediumButton(
                                    action.text(),
                                    action.icon(),
                                    alignment=Qt.AlignmentFlag.AlignLeft,
                                    showText=showText,
                                    fixedHeight=Parameters_Ribbon.ICON_SIZE_MEDIUM,
                                )

                                # Set the stylesheet
                                # Set the padding to align the icons to the left
                                padding = btn.height() / 4
                                btn.setStyleSheet(
                                    StyleMapping.ReturnStyleSheet(
                                        "toolbutton", "2px", f"{padding}px"
                                    )
                                )

                            elif buttonSize == "large":
                                showText = Parameters_Ribbon.SHOW_ICON_TEXT_LARGE
                                if IconOnly is True:
                                    showText = False

                                btn = panel.addLargeButton(
                                    action.text(),
                                    action.icon(),
                                    alignment=Qt.AlignmentFlag.AlignLeft,
                                    showText=showText,
                                    fixedHeight=Parameters_Ribbon.ICON_SIZE_LARGE,
                                )

                                # if text is enabled for large buttons. The text will be behind the icon
                                # To fix this, increase the height of the button with 20 and the set the icon size
                                # to the heigt minus 20.
                                if Parameters_Ribbon.SHOW_ICON_TEXT_LARGE is True:
                                    btn.setFixedHeight(btn.height() + 20)
                                    btn.setMaximumIconSize(btn.height() - 20)

                                # Set the stylesheet
                                # Set the padding to align the icons to the left
                                padding = 0
                                if button.menu() is not None:
                                    padding = btn.height() / 6
                                btn.setStyleSheet(
                                    StyleMapping.ReturnStyleSheet(
                                        "toolbutton", "2px", f"{padding}px"
                                    )
                                )
                            else:
                                raise NotImplementedError(
                                    translate(
                                        "FreeCAD Ribbon",
                                        "Given button size not implemented, only small, medium and large are available.",
                                    )
                                )

                            # Set the default actiom
                            btn.setDefaultAction(action)

                            # add dropdown menu if necessary
                            if button.menu() is not None:
                                btn.setMenu(button.menu())
                                btn.setPopupMode(
                                    QToolButton.ToolButtonPopupMode.MenuButtonPopup
                                )
                                if btn.height() == Parameters_Ribbon.ICON_SIZE_LARGE:
                                    btn.setMinimumWidth(btn.height())
                                else:
                                    btn.setMinimumWidth(btn.minimumWidth() + 5)
                                btn.setDefaultAction(btn.actions()[0])

                            # add the button text to the shadowList for checking if buttons are already there.
                            shadowList.append(button.text())

                        except Exception as e:
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                print(f"{e.with_traceback(None)}, 2")
                            continue

            # Set the size policy and increment. It has to be MinimumExpanding.
            panel.setSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
            )
            panel.setSizeIncrement(self.iconSize, self.iconSize)

            # remove any suffix from the panel title
            if panel.title().endswith("_custom"):
                panel.setTitle(panel.title().replace("_custom", ""))

            # Change the name of the view panels to "View"
            if panel.title() == "Views - Ribbon" or panel.title() == "Individual views":
                panel.setTitle(" Views ")

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
                OptionButton.setStyleSheet(
                    "RibbonPanelOptionButton::menu-indicator {image: none;}"
                )
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
                    OptionButton.setToolButtonStyle(
                        Qt.ToolButtonStyle.ToolButtonTextBesideIcon
                    )
                    OptionButton.setText("more...")

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
        ScrollLeftButton_Category_Icon = StyleMapping.ReturnStyleItem(
            "ScrollLeftButton_Category"
        )
        ScrollRightButton_Category_Icon = StyleMapping.ReturnStyleItem(
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

        return

    def on_ScrollButton_Category_clicked(
        self, event, ScrollButton: RibbonCategoryLayoutButton
    ):
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
        self.ApplicationMenu()
        return

    def hideClassicToolbars(self):
        for toolbar in mw.findChildren(QToolBar):
            parentWidget = toolbar.parentWidget()
            # hide toolbars that are not in the statusBar and show toolbars that are in the statusbar.
            toolbar.hide()
            if (
                parentWidget.objectName() == "statusBar"
                or parentWidget.objectName() == "StatusBarArea"
            ):
                toolbar.show()
            # Show specific toolbars and go to the next
            if toolbar.objectName() in [
                self.quickAccessToolBar().objectName(),
                self.rightToolBar().objectName(),
            ]:
                toolbar.show()
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

    def List_AddCustomToolbarsToWorkbench(self, WorkBenchName, CustomToolbar):
        ButtonList = []

        try:
            # Get the commands from the custom panel
            Commands = self.ribbonStructure["customToolbars"][WorkBenchName][
                CustomToolbar
            ]["commands"]

            # Get the command and its original toolbar
            for key, value in list(Commands.items()):
                # get the menu text from the command list
                for CommandName in Gui.listCommands():
                    Command = Gui.Command.get(CommandName)
                    MenuText = CommandInfoCorrections(CommandName)["menuText"]

                    if MenuText == key.replace("&", "").replace("...", ""):
                        try:
                            # Get the original toolbar as QToolbar
                            OriginalToolBar = mw.findChild(QToolBar, value)
                            # Go through all it's QtoolButtons
                            for Child in OriginalToolBar.findChildren(QToolButton):
                                CommandAction = Command.getAction()[0]
                                MenuNameTranslated = CommandAction.text().replace(
                                    "&", ""
                                )
                                # If the text of the QToolButton matches the menu text
                                # Add it to the button list.
                                IsInList = False
                                for Toolbutton in ButtonList:
                                    if Toolbutton.text() == Child.text():
                                        IsInList = True

                                if (
                                    Child.text() == MenuNameTranslated
                                    and IsInList is False
                                ):
                                    ButtonList.append(Child)
                        except Exception as e:
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                print(f"{e.with_traceback(None)}, 3")
                            continue
        except Exception:
            pass

        return ButtonList

    def LoadMarcoFreeCAD(self, scriptName):
        if self.MainWindowLoaded is True:
            script = os.path.join(pathScripts, scriptName)
            if script.endswith(".py"):
                App.loadFile(script)
        return


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
            layout.setContentsMargins(3, 0, 3, 0)
            # update the layout
            ribbon.setLayout(layout)
            ribbonDock = QDockWidget()
            # set the name of the object and the window title
            ribbonDock.setObjectName("Ribbon")
            ribbonDock.setWindowTitle("Ribbon")
            # Set the titlebar to an empty widget (effectively hide it)
            ribbonDock.setTitleBarWidget(QWidget())
            # attach the ribbon to the dockwidget
            ribbonDock.setWidget(ribbon)

            # if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            #     ribbonDock.setMaximumHeight(ribbon.RibbonMinimalHeight)
            ribbonDock.setSizePolicy(
                QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
            )

            # Add the dockwidget to the main window
            mw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, ribbonDock)
