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
import CustomWidgets
import FreeCAD as App
import FreeCADGui as Gui
from pathlib import Path
import traceback

from PySide.QtGui import (
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QDropEvent,
    QContextMenuEvent,
    QMouseEvent,
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
    QDrag,
    QScreen,
    QPen,
    )
from PySide.QtWidgets import (
    QCheckBox,
    QFrame,
    QLineEdit,
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
    QListWidget,
    QListWidgetItem,
    QAbstractButton,
    QStackedWidget,
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
    QSignalBlocker,
    QMimeData,
    QEventLoop,      
)
from CustomWidgets import (
    CustomControls, 
    DragTargetIndicator, 
    Toggle, 
    ToggleAction, 
    CheckBoxAction, 
    SpinBoxAction, 
    ComboBoxAction, 
    CustomSeparator, 
    QuickAccessToolButton, 
    QuickAccessSeparator,
)
import json
import os
import sys
import webbrowser
import LoadDesign_Ribbon
import Parameters_Ribbon
from Parameters_Ribbon import Parameters
import LoadSettings_Ribbon
import LoadLicenseForm_Ribbon
import LoadCombinePanel_Ribbon
import LoadAddCommands
import CacheFunctions
import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Serialize_Ribbon
import Standard_Functions_Ribbon
import StyleMapping_Ribbon
import platform
from datetime import datetime
import shutil

# import Ribbon. This contains the ribbon commands for FreeCAD
import RibbonUI

# Get the resources
ConfigDirectory = Parameters.CONFIG_DIR
pathIcons = Parameters.ICON_LOCATION
pathStylSheets = Parameters.STYLESHEET_LOCATION
pathUI = Parameters.UI_LOCATION
pathScripts = os.path.join(ConfigDirectory, "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
pathBackup = Parameters.BACKUP_LOCATION
sys.path.append(ConfigDirectory)
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)
sys.path.append(pathBackup)

translate = App.Qt.translate

import pyqtribbon_local
import pyqtribbon_local as pyqtribbon
from pyqtribbon_local.ribbonbar import RibbonMenu, RibbonBar, RibbonTitleWidget, RibbonApplicationButton
from pyqtribbon_local.panel import RibbonPanel, RibbonPanelItemWidget, RibbonPanelTitle
from pyqtribbon_local.toolbutton import RibbonToolButton, RibbonButtonStyle
from pyqtribbon_local.separator import RibbonSeparator
from pyqtribbon_local.category import RibbonCategory, RibbonCategoryLayoutButton, RibbonNormalCategory, RibbonContextCategory

# Get the main window of FreeCAD
mw: QMainWindow = Gui.getMainWindow()

# Define a timer
timer = QTimer()

# Write all settings, if they are not present yet
Parameters_Ribbon.Settings.WriteMissingSettings(Parameters_Ribbon.Settings)

class ModernMenu(RibbonBar):
    """
    Create ModernMenu QWidget.
    """
    
    # region - class parameters
    # Add workbenches that need to be loaded first or early here
    WBtoLoadFirst = ["BillOfMaterialsWB"]

    # The datafile version is set in LoadDesign.py
    DataFileVersion = CacheFunctions.DataFileVersion

    # Define a placeholder for the repro adress
    ReproAdress: str = ""
    HelpAdress: str = ""
    # Placeholders for building the ribbonbar
    ribbonStructure = {}
    wbNameMapping = {}
    isWbLoaded = {}
    MainWindowLoaded = False
    LeaveEventEnabled = True

    # use icon size from FreeCAD preferences
    iconSize = Parameters.ICON_SIZE_SMALL
    ApplicationButtonSize = Parameters.APP_ICON_SIZE
    # QuickAccessButtonSize = Parameters.QUICK_ICON_SIZE    
    QuickAccessButtonSize = Parameters.ICON_SIZE_SMALL 
    TabBar_Size = Parameters.FONTSIZE_TABS + 6
    LargeButtonSize = Parameters.ICON_SIZE_LARGE
    
    # Define a placeholder for the ribbon height
    RibbonHeight = 0

    # Set a size factor for the buttons
    sizeFactor = Parameters.SIZE_FACTOR
    # Create an offset for the panelheight
    PanelHeightOffset = Parameters.PANEL_HEIGHT_OFFSET
    # PanelHeightOffset = 22
    # Create an offset for the whole ribbon height
    RibbonOffset = (
        20 + QuickAccessButtonSize * 2
    )  # Set to zero to hide the panel titles

    # Set the minimum height for the ribbon
    RibbonMinimalHeight = QuickAccessButtonSize + TabBar_Size + Parameters.RIBBON_MINIMUM_HEIGHT    
    # RightToolBarButtonSize = Parameters.RIGHT_ICON_SIZE  # Is overruled
    RightToolBarButtonSize = QuickAccessButtonSize

    # Declare the right padding for dropdown menus
    PaddingRight = 10
    
    # Declare the spacing between buttons
    ButtonSpacing = Parameters.BUTTON_SPACING
    
    # Declare the alignment of the buttons
    ButtonAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
    
    # Declare the top and bottom margin for the tabbar (category)
    TopMargin = 3
    BottomMargin = 0
    
    # Set the value for the menubutton width
    MenuButtonSpace = 12

    # Create the lists and ditcs for the lists in the ribbon structure, 
    ignoredToolbars = []
    iconOnlyToolbars = []
    quickAccessCommands = []
    ignoredWorkbenches = []
    customToolbars = {}
    dropdownButtons = {}
    newPanels = {}

    # Create the list for the commands
    List_Commands = []

    # Create the lists for the deserialized icons
    List_CommandIcons = []
    List_WorkBenchIcons = []

    # Declare the custom overlay function states
    OverlayToggled = False
    OverlayToggled_Left = False
    OverlayToggled_Right = False
    OverlayToggled_Top = False
    OverlayToggled_Bottom = False
    TransparancyToggled = False

    # Define the menus
    RibbonMenu = QMenu()
    HelpMenu = QMenu()
    SettingsMenu = QMenu()
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
    # a action list for the right click event in the customize enviroment.
    # Used to store the button states
    actionList = []
    
    # Create a dict for the active workbench only
    workBenchDict = {}
    
    # Create a empty context menu
    contextMenu = None
    
    # Create a holder for the last customized workbench
    LastCustomized = []
    
    # Create a list for panels that have a option button which have to be restored when exitiing the customisation enviroment
    longPanels = []
    
    # Define a placeholder for the AddButton Dialog
    AddCommandsDialog = None
    
    # Create a list for new dragged buttons
    newButtons = []
    
    # Create a list to store the pin buttons off each category
    pinButtonList = []
    
    # Store the number of rows for each wb
    MaxRowsPerWB = {}
    
    # Create variant to store a custom offset for the ribbon
    CustomizeOffset = 0
    
    # Set a value for the titlebar height if the ribbon is floating
    FloatingTitleBarHeight = 20
    
    # Create a list for customized categories
    CustomizedCategories = []
    
    # Create a signal to indicate that there is a different tab active.
    TabChanged = Signal()
    
    # store the CentralWidget width
    CentralWidgetWidth = None
    
    # Define panel lists for the customise enviroment
    HiddenPanels = []
    ReplacedPanels = []
    CombinePanels = []
    RemovedPanels = []
    AddedPanels = []
    
    # Define a variable for storing the current category when the customise enviroment is activated
    CurrentCategoryToRestore = None
    # endregion

    def __init__(self):
        """
        Constructor
        """
        super().__init__(title="")
        self.setObjectName("Ribbon")

        # Enable dragdrop
        self.setAcceptDrops(True)
        self.tabBar().setAcceptDrops(True)
        self._titleWidget.quickAccessToolBar().setAcceptDrops(True)
                        
        # connect the signals
        self.connectSignals()

        # read ribbon structure from JSON file
        if os.path.exists(Parameters.RIBBON_STRUCTURE_JSON) is False:
            #Create the new folder for the data
            if not os.path.exists(ConfigDirectory):
                os.makedirs(ConfigDirectory)
            Parameters.RIBBON_STRUCTURE_JSON = os.path.join(ConfigDirectory, "RibbonStructure.json")        
        with open(Parameters.RIBBON_STRUCTURE_JSON, "r") as file:
            self.ribbonStructure.update(json.load(file))
        file.close()
        
        DataFile2 = os.path.join(ConfigDirectory, "RibbonDataFile2.dat")
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
                Parameters.FreeCAD_Version["mainVersion"],
                Parameters.FreeCAD_Version["subVersion"],
                Parameters.FreeCAD_Version["patchVersion"],
                Parameters.FreeCAD_Version["gitVersion"],
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
        with open(Parameters.RIBBON_STRUCTURE_JSON, "w") as outfile:
            json.dump(self.ribbonStructure, outfile, indent=4)
        outfile.close()

        # Get the address of the repository address
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.ReproAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "repository"
        )
        LocalVersion = StandardFunctions.ReturnXML_Value(
            PackageXML, "version",
        )
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(translate("FreeCAD Ribbon", "Ribbon UI: ") + self.ReproAdress)
            print(translate("FreeCAD Ribbon", "Ribbon UI: Installed version: ") + LocalVersion)
        
        # Get the location of the help documentation
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        self.HelpAdress = StandardFunctions.ReturnXML_Value(
            PackageXML, "url", "type", "website"
        )
        
        # Activate the workbenches used in the new panels otherwise the panel stays empty
        try:
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
                            self.isWbLoaded[CommandItem[1]] = True
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"new panels have wrong format. Please create them again!\n{e}",
                    "Error",
                )
            pass

        # Activate the workbenches used in the dropdown buttons otherwise the button stays empty
        try:
            for DropDownCommand, Commands in self.ribbonStructure["dropdownButtons"].items():
                for CommandItem in Commands:
                    if (
                        CommandItem[1] != "General"
                        and CommandItem[1] != "Global"
                        and CommandItem[1] != "Standard"
                    ):
                        # Activate the workbench if not loaded
                        Gui.activateWorkbench(CommandItem[1])
                        self.isWbLoaded[CommandItem[1]] = True
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"dropdownbuttons have wrong format. Please create them again!\n{e}",
                    "Warning",
                )
            pass

        # Check if there is a new version
        # Get the latest version
        try:
            # User = "apebbers"
            User = "APEbbers"
            Repo = "FreeCAD-Ribbon"
            Branch = "main"
            File = "package.xml"
            ElementName = "version"
            attribKey = ""
            attribValue = ""
            # host: str ="https://codeberg.org"
            host = "https://github.com"
            LatestVersion = StandardFunctions.ReturnXML_Value_Git(
                User=User, Repository=Repo, Branch=Branch, File=File, ElementName=ElementName, attribKey=attribKey, attribValue=attribValue, host=host
            )
            print(translate("FreeCAD Ribbon", "Ribbon UI: Latest released version: ") + str(LatestVersion))
            # Get the current version
            PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
            CurrentVersion = StandardFunctions.ReturnXML_Value(
                PackageXML, "version"
            )
            # Check if you are on a developer version. If so set developer version
            if CurrentVersion.lower().endswith("dev"):
                self.DeveloperVersion = CurrentVersion
                self.UpdateVersion = ""
            # If you are not on a developer version, check if you have the latest version
            if CurrentVersion.lower().endswith("dev") is False:
                if LatestVersion is not None:
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
                            self.UpdateVersion = LatestVersion
        except Exception as e:
            raise e
            pass

        # Create the ribbon
        self.CreateMenus()  # Create the menus
        self.createModernMenu()  # Create the ribbon
        
        # Set the custom stylesheet
        self.StyleSheet = Path(Parameters.STYLESHEET).read_text()
        # Set the tooltip colors, so that they are uniform accros FreeCAD.
        mw.setStyleSheet(""" QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }""")
        # modify the stylesheet to set the border and background for a toolbar and menu
        hexColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        hexColorTab = StyleMapping_Ribbon.ReturnStyleItem(
            "Background_Color", True, True
        )
        if Parameters.CUSTOM_COLORS_ENABLED is True:            
            hexColorTab = Parameters.COLOR_BACKGROUND_TABS
            
            self.quickAccessToolBar().setStyleSheet("background: " + hexColor + ";")
            self.rightToolBar().setStyleSheet("background: " + hexColor + ";")
            
            StyleSheet_Addition_Tabs = "QTabBar::tab {background: " + hexColorTab + ";}"
            StyleSheet_Addition_TitleWidget = "RibbonTitleWidget {background: " + Parameters.COLOR_BACKGROUND_TITLEBAR + ";}"
            # StyleSheet_Addition_ToolBars = "QToolBar {background: " + Parameters.COLOR_BACKGROUND_TITLEBAR + ";}"

            # self.StyleSheet = self.StyleSheet + StyleSheet_Addition_TitleWidget + StyleSheet_Addition_Tabs + StyleSheet_Addition_ToolBars 
            self.StyleSheet = self.StyleSheet + StyleSheet_Addition_TitleWidget + StyleSheet_Addition_Tabs
            self.setStyleSheet(self.StyleSheet)
            
        if (
            hexColor is not None
            and hexColor != ""
            and Parameters.BUTTON_BACKGROUND_ENABLED is True
        ):
            # Set the quickaccess toolbar background color. This fixes a transparant toolbar.
            self.quickAccessToolBar().setStyleSheet(
                "QToolBar {background: " + hexColor + ";}"
            )
            self.tabBar().setStyleSheet("background: " + hexColorTab + ";")
            # Set the background color. This fixes transparant backgrounds when FreeCAD has no stylesheet
            StyleSheet_Addition_Tabs = (
                "\n\nQToolButton {background: solid " + hexColor + ";}"
            )
            StyleSheet_Addition_2 = (
                "\n\nRibbonBar {border: none;background: solid "
                + hexColor
                + ";color: "
                + hexColor
                + ";}"
            )
            self.StyleSheet = StyleSheet_Addition_2 + self.StyleSheet + StyleSheet_Addition_Tabs
        self.setStyleSheet(self.StyleSheet)

        # If the text for the tabs is set to be disabled, update the stylesheet
        if Parameters.TABBAR_STYLE == 1:
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
            self.StyleSheet = StyleSheet_Addition_3 + self.StyleSheet
            self.setStyleSheet(self.StyleSheet)
            self.StyleSheet = StyleSheet_Addition_3 + self.StyleSheet
            self.setStyleSheet(self.StyleSheet)

        # Add an addition for selected tabs
        StyleSheet_Addition_4 = (
            """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
            + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
            + """;}"""
        )
        # If the tabs are set to icon only, set the text to the hover background color also
        if Parameters.TABBAR_STYLE == 1:
            StyleSheet_Addition_4 = (
                """QTabBar::tab:selected, QTabBar::tab:hover {
                background: """
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + """;color: """
                + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                + """;}"""
            )
        self.StyleSheet = StyleSheet_Addition_4 + self.StyleSheet
        self.setStyleSheet(self.StyleSheet)

        # add a stylesheet entry for the fontsize for menus
        StyleSheet_Addition_5 = (
            "QMenu::item, QMenu::menuAction, QMenuBar::item, RibbonMenu, RibbonToolButton, RibbonMenu::item, QMenu>QLabel {font-size: "
            + str(Parameters.FONTSIZE_MENUS)
            + "px;}"
        )
        self.StyleSheet = self.StyleSheet + StyleSheet_Addition_5
        self.setStyleSheet(self.StyleSheet)
        
        # get the state of the mainwindow
        self.MainWindowLoaded = True

        # Set these settings and connections at init
        # Set the autohide behavior of the ribbon
        preferences = App.ParamGet("User parameter:BaseApp/Preferences/DockWindows")
        if preferences.GetBool("ActivateOverlay") is True:
            Parameters.USE_OVERLAY = True
        else:
            Parameters.USE_OVERLAY = False
        if preferences.GetBool("ActivateOverlay") is True or Parameters.USE_OVERLAY is True:
            Parameters.AUTOHIDE_RIBBON = False
        self.setAutoHideRibbon(Parameters.AUTOHIDE_RIBBON)
        
        # Get the parameter group
        OverlayParam_Top = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayTop"
        )
        if Parameters.USE_OVERLAY is False:
            # Parameters.USE_FC_OVERLAY = False
            self.OverlayToggled_Top = False

            # Create a new string without "Ribbon"       
            newString = OverlayParam_Top.GetString("Widgets").replace("Ribbon,", "")
            # Set the new string in parameters
            OverlayParam_Top.SetString("Widgets",newString)
        
        if Parameters.USE_OVERLAY is True:
            self.OverlayToggled_Top = True
            if Parameters.OVERLAYSTATE == 1:
                # Get the current string, if Ribbon is not in it, add it
                newString = OverlayParam_Top.GetString("Widgets")
                if "Ribbon" not in newString:
                    newString = "Ribbon," + newString
                    OverlayParam_Top.SetString("Widgets",newString)
            if Parameters.OVERLAYSTATE == 0:
                self.OverlayToggled_Top = False
                # Create a new string without "Ribbon"       
                newString = OverlayParam_Top.GetString("Widgets").replace("Ribbon,", "")
                # Set the new string in parameters
                OverlayParam_Top.SetString("Widgets",newString)
        App.saveParameter()

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
        #
        # Create a floating button
        FloatingButton = QToolButton()
        FloatingButton.setObjectName("FloatButton")
        FloatingButton.setFixedSize(QSize(self.iconSize * 0.8,self.iconSize * 0.8))
        FloatingButton.clicked.connect(self.on_DockWidget_Toggled)
        FloatingButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[2])
        FloatingButton.setToolTip(translate("FreeCAD Ribbon", "Set the ribbon docked or floating"))
        FloatingButton.setStyleSheet(""" QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }"""
                )
        #
        # Create an overlay button  
        overlayButton = QToolButton()
        overlayButton.setFixedSize(QSize(self.iconSize * 0.8,self.iconSize * 0.8))
        overlayButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("TitleBarButtons")[1])
        overlayButton.setToolTip(translate("FreeCAD Ribbon", "Toggle overlay "))
        overlayButton.setObjectName("overlayButton")
        overlayButton.clicked.connect(self.ToggleOverlay)
        overlayButton.setStyleSheet(""" QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }"""
                )
        if Parameters.USE_OVERLAY is True:
            overlayButton.animateClick() # Otherwise, the first time you need to click twice
        if Parameters.USE_OVERLAY is False:
            overlayButton.setDisabled(True)
            overlayButton.setIcon(QIcon())
            overlayButton.setFixedSize(QSize(0.1,self.iconSize * 0.8))
        if (
            Parameters.TOOLBAR_POSITION == 0
            or Parameters.TOOLBAR_POSITION == 1
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
            if Parameters.TOOLBAR_POSITION == 0:  # Toolbars above tabbar
                # Set the font size for the label
                font: QFont = _titleLabel.font()
                font.setPixelSize(Parameters.FONTSIZE_MENUS + 1)
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
                    _quickAccessToolBarWidget, 0, 0, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _titleLabel, 0, 1, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _rightToolBar, 0, 3, 1, 3, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    spacer, 1, 4, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _tabBar, 1, 0, 1, 4, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    overlayButton, 1, 4, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    FloatingButton, 1, 5, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                # Change the offsets
                self.RibbonMinimalHeight = self.QuickAccessButtonSize * 2 + 20
                self.RibbonOffset = self.QuickAccessButtonSize + self.TabBar_Size + 27 + Parameters.RIBBON_HEIGHT_OFFSET
                self._titleWidget._tabBarLayout.setRowMinimumHeight(
                    0, self.QuickAccessButtonSize
                )
                self._titleWidget._tabBarLayout.setRowMinimumHeight(1, self.TabBar_Size)
            if Parameters.TOOLBAR_POSITION == 1:  # Toolbars inline with tabbar
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
                    overlayButton, 0, 3, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    FloatingButton, 0, 4, 1, 1, Qt.AlignmentFlag.AlignVCenter
                )
                self._titleWidget._tabBarLayout.addWidget(
                    _rightToolBar, 0, 5, 1, 2, Qt.AlignmentFlag.AlignVCenter
                )
                # Change the offsets
                self.RibbonMinimalHeight = self.QuickAccessButtonSize + 10
                if self.TabBar_Size > self.QuickAccessButtonSize:
                    self.RibbonOffset = 15 + self.TabBar_Size + Parameters.RIBBON_HEIGHT_OFFSET
                else:
                    self.RibbonOffset = 15 + self.QuickAccessButtonSize + Parameters.RIBBON_HEIGHT_OFFSET
                self._titleWidget._tabBarLayout.setRowMinimumHeight(
                    0, self.QuickAccessButtonSize
                )

        # Set the font color
        self._titleWidget.setStyleSheet(f"color: {StyleMapping_Ribbon.ReturnStyleItem('FontColor')}")
                
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

        # mw.setAcceptDrops(True)
        # mw.dragEnterEvent = lambda e: self.dragEnterEvent(e)

        # Install an event filter to catch events from the main window and act on it.
        mw.installEventFilter(EventInspector(mw))
        # self.installEventFilter(RibbonEventInspector(self))
        
        # Set isLoaded to True, to show that the loading is finished
        self.isLoaded = True
        # Fold the ribbon if unpinned
        self.FoldRibbon()
        
        # Activate some WB's first to ensure proper loading of the panels
        for Wb in self.WBtoLoadFirst:
            try:
                Gui.activateWorkbench(Wb)
                self.isWbLoaded[Wb] = True
            except Exception:
                pass
        
         # Activate the last used wb 
         # This is needed when buttons from other workbenches are added to a panel
        preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        result = preferences.GetString("LastModule")
        try:
            cmd = Gui.Command.get('Std_Workbench')
            actions = cmd.getAction()
            for action in actions:
                if action.objectName() == result:
                    index = action.data()
                    Gui.runCommand('Std_Workbench',index)
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                print(e.with_traceback(e.__traceback__))
            pass
        
        # This is needed to be able to drag the main window properly when the titlebar is hidden
        self._titleWidget.mousePressEvent = lambda e: self.mousePress_Titlebar(e)
        mw.moveEvent = lambda e: self.mouseMove_Titlebar(e)
        
        # Check if an reload of the datafile is needed an show an message
        CacheFunctions.CheckDataFileVersion()
        
        if Parameters.BETA_FUNCTIONS_ENABLED is True:
                self.BetaFunctionsEnabled = True   
        else:
            self.BetaFunctionsEnabled = False 
        
        return

    # region - Ribbon event fuctions
    
    # Mouse event funtions are needed to allow properly drag the window.
    initialPos = None
    def mousePress_Titlebar(self, event):
        try:
            self.initialPos = event.pos().toPoint()
        except Exception:
            pass
    
    def mouseMove_Titlebar(self, event):
        if self.initialPos is not None:
            delta = event.pos().toPoint() - self.initialPos
            mw.move(
                mw.window().x() + delta.x(),
                mw.window().y() + delta.y(),
            )
    
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
        self.hideClassicToolbars()
        TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
        TB.show()
                
        # In FreeCAD 1.0, Overlays are introduced. These have also an enterEvent which results in strange behavior
        # Therefore this function is only activated when FreeCAD's overlay function is disabled.
        if (
            Parameters.SHOW_ON_HOVER is True
            and Parameters.USE_OVERLAY is False
        ):
            self.UnfoldRibbon()
            self.setRibbonVisible(True)
            
        if self.CustomizeEnabled:
            # If not activated, activate all buttons    
            self.activateButtons() 
        return

    def leaveEvent(self, QEvent):
        if Parameters.AUTOHIDE_RIBBON is True and self.MenuEntered is False:
            self.FoldRibbon()

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
    # endregion

    # region - Context event functions
    #            
    def contextMenuEvent(self, event: QContextMenuEvent):
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())

        # Create the menu
        self.contextMenu = QMenu(self)
        self.contextMenu.setStyleSheet("spacing: 0px;margin: 0px;padding: 0px;")
    
        # If betaFunctions is enabled, coninue
        if self.BetaFunctionsEnabled is True:
            # Get the widget and the panel
            widget = self.childAt(event.pos()).parent()
            panel = widget.parent().parent().parent()     
            separator = widget.findChild(CustomSeparator)
            titleWidget = widget.findChild(RibbonPanelTitle)
            # try to get a quickaccess button or separator if the mouse is over it
            quickaccessbutton = None
            quickaccessseparator = None
            quickaccesstoolbar = None
            if type(widget) is QToolBar:
                quickaccesstoolbar = widget
                for button in widget.findChildren(QToolButton):
                    # Map the for corners of the button to global
                    pos_tl = button.mapToGlobal(button.rect().topLeft())
                    pos_tr = button.mapToGlobal(button.rect().topRight())
                    pos_bl = button.mapToGlobal(button.rect().bottomLeft())
                    pos_br = button.mapToGlobal(button.rect().bottomRight())

                    # If the position of the context menu event is within the global corners
                    # redefine the quickaccess button or control
                    if event.globalPos().x() > pos_tl.x() and event.globalPos().x() < pos_tr.x():
                        if event.globalPos().y() > pos_tl.y() and event.globalPos().y() < pos_bl.y():
                            if type(button) is QuickAccessToolButton:
                                quickaccessbutton = button
                            if type(button) is QuickAccessSeparator:
                                quickaccessseparator = button
            
            # Check if the panel is not none and of type RibbonPanel. If so, continue
            if panel is not None and type(panel) is RibbonPanel:
                if (
                    (type(widget) is QToolButton or type(widget) is RibbonPanelItemWidget)
                    and self.CustomizeEnabled is True and titleWidget is None
                ):
                    if separator is None:
                        # Define the context menu for buttons
                        self.contextMenu.setContentsMargins(3,3,3,3)
                        self.contextMenu.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
    
                        # Check if the widget has text enabled
                        textVisible = None
                        try:
                            CommandName = ""
                            for child in widget.children():
                                if (
                                    type(child) is QToolButton
                                    and child.objectName() == "CommandButton"
                                ):
                                    CommandName = child.objectName()
                            textVisible = self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["commands"][CommandName]["textEnabled"]
                        except Exception:
                            pass
                        if textVisible is None:
                            for child in widget.children():
                                if type(child) is QLabel:
                                    textVisible = child.isVisible()
                        if textVisible is None:
                            textVisible = False                                    
                        # set the checkbox for enabling text
                        RibbonButtonAction_Text = ToggleAction(self, translate("FreeCAD Ribbon", "Show button text"), textVisible)
                        RibbonButtonAction_Text.setText(translate("FreeCAD Ribbon", "Show button text"))
                        # Set the checkbox action checked or unchecked
                        RibbonButtonAction_Text.setChecked(textVisible)
                        if textVisible is True:
                            RibbonButtonAction_Text.setCheckState(Qt.CheckState.Checked)
                        if textVisible is False:
                            RibbonButtonAction_Text.setCheckState(Qt.CheckState.Unchecked)
                        RibbonButtonAction_Text.setFixedSize(82,41)
                        RibbonButtonAction_Text.checkStateChanged.connect(lambda: self.on_TextState_Changed(panel, widget, RibbonButtonAction_Text.isChecked()))
                        # Add the checkbox action to the contextmenu
                        self.contextMenu.addAction(RibbonButtonAction_Text)
                        
                        # Set the spinbox for the button size
                        RibbonButtonAction_Size = SpinBoxAction(self, translate("FreeCAD Ribbon", "Set button size"))
                        RibbonButtonAction_Size.setMinimum(16)
                        RibbonButtonAction_Size.setMaximum(120)                        
                        RibbonButtonAction_Size.setValue(widget.height())
                        RibbonButtonAction_Size.setFixedWidth(82)
                        if Parameters.LINK_ICON_SIZES is False:    
                            RibbonButtonAction_Size.valueChanged.connect(lambda: self.on_ButtonSize_Changed(panel, widget, RibbonButtonAction_Size))
                            self.contextMenu.addAction(RibbonButtonAction_Size)
                        
                        # Set the dropdown for the button style
                        RibbonButtonAction_Style = ComboBoxAction(self, translate("FreeCAD Ribbon", "Set button type"))
                        RibbonButtonAction_Style.addItem("Small")
                        RibbonButtonAction_Style.addItem("Medium")
                        RibbonButtonAction_Style.addItem("Large")

                        if widget.parent().ButtonStyle == RibbonButtonStyle.Small:
                            RibbonButtonAction_Style.setCurrentText("Small")
                        if widget.parent().ButtonStyle == RibbonButtonStyle.Medium:
                            RibbonButtonAction_Style.setCurrentText("Medium")
                        if widget.parent().ButtonStyle == RibbonButtonStyle.Large:
                            RibbonButtonAction_Style.setCurrentText("Large")
                        RibbonButtonAction_Style.setFixedWidth(82)
                        RibbonButtonAction_Style.currentTextChanged.connect(lambda: self.on_ButtonStyle_Clicked(panel, widget, RibbonButtonAction_Style, RibbonButtonAction_Size))                      
                        self.contextMenu.addAction(RibbonButtonAction_Style)
                        
                        # Add a line edit for changing the text
                        ChangeButtonText = CustomWidgets.LineEditAction(self, translate("FreeCAD Ribbon", "Set button text"))
                        ChangeButtonText.setText("")
                        text = ""
                        label = widget.parent().findChild(QLabel)
                        if label is not None:
                            text = label.text().replace("\n", " ")
                        ChangeButtonText.setPlaceholderText(text)
                        ChangeButtonText.setFixedSize(200,21)
                        ChangeButtonText.setClearButtonEnabled(True)
                        ChangeButtonText.textChanged.connect(lambda e: self.on_ButtonLabel_Changing(e, panel, widget, ChangeButtonText))
                        ChangeButtonText.editingFinished.connect(lambda: lambda: self.contextMenu.close())
                        self.contextMenu.addAction(ChangeButtonText)
                        
                        # Create the buttons for adding a separator
                        AddSeparator_Left = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Add separator left"))
                        AddSeparator_Left.triggered.connect(lambda: self.on_AddSeparator_Clicked(panel, widget,"left"))
                        AddSeparator_Right = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Add separator right"))
                        AddSeparator_Right.triggered.connect(lambda: self.on_AddSeparator_Clicked(panel, widget,"right"))                        
                        
                        # create the context menu action
                        self.contextMenu.exec_(self.mapToGlobal(event.pos()))

                        # Disconnect the widgetActions
                        RibbonButtonAction_Style.currentTextChanged.disconnect()
                        RibbonButtonAction_Text.checkStateChanged.disconnect()
                        if Parameters.LINK_ICON_SIZES is False:
                            RibbonButtonAction_Size.valueChanged.disconnect()
                        AddSeparator_Left.triggered.disconnect()                                
                        AddSeparator_Right.triggered.disconnect()
                        ChangeButtonText.textChanged.disconnect()                            
                        ChangeButtonText.editingFinished.disconnect()
                       
                        return

            # Create a context menu to change a panel title
            if titleWidget is not None and self.CustomizeEnabled is True and titleWidget.underMouse():
                panel = titleWidget.parent().parent()
                ChangePanelTitle = CustomWidgets.LineEditAction(self, translate("FreeCAD Ribbon", "Change panel title"))
                ChangePanelTitle.setText("")
                ChangePanelTitle.setPlaceholderText(panel.title())
                ChangePanelTitle.setClearButtonEnabled(True)
                ChangePanelTitle.textChanged.connect(lambda e: self.on_PanelTitle_Changing(e, panel, ChangePanelTitle))
                ChangePanelTitle.editingFinished.connect(lambda: self.contextMenu.close())
                self.contextMenu.addAction(ChangePanelTitle)
                
                # create the context menu action
                self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                
                # Disconnect the widgetActions
                ChangePanelTitle.textChanged.disconnect()
                ChangePanelTitle.editingFinished.disconnect()
                    
            # if the separator is not none, its class is correct and it is under the mouse cursor,
            # Create a menu with an remove button
            if separator is not None and type(separator) is CustomSeparator and separator.underMouse():
                if self.CustomizeEnabled is True:
                    panel = separator.parent().parent()
                    # Create the menu
                    RemoveSeparator = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Remove separator"))
                    # create the context menu action
                    RemoveSeparator.triggered.connect(lambda: self.on_RemoveSeparator_Clicked(panel, separator))
                    
                    # create the context menu action
                    self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                    return
            
            # Add the context menu for the ribbon
            if panel is not None and type(panel) is not RibbonPanel and quickaccessbutton is None and quickaccesstoolbar is None:                
                # Add Customize buttons for entering and exiting customize enviroment
                self.contextMenu.addSeparator()
                title = translate("FreeCAD Ribbon", "Customize...")
                if self.CustomizeEnabled is True:
                    title = translate("FreeCAD Ribbon", "Save and exit customize...")
                CustomizeStartAct = self.contextMenu.addAction(title)
                # Add a cancel button
                CustomizeCancelAct = QAction()
                if self.CustomizeEnabled is True:
                    CustomizeCancelAct = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Cancel"))
                                
                # Create the action
                action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                
                # Perfom the action depending on which button is clicked
                if action == CustomizeStartAct:
                    if self.CustomizeEnabled is False:
                        # add keys if they don´t exist
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName], endEmpty=True)
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.ribbonStructure, ["workbenches", workbenchName], endEmpty=True) # Just to prevent any errors
                        # Create the workbench dict
                        self.workBenchDict["workbenches"] = self.ribbonStructure["workbenches"]
                        self.workBenchDict["quickAccessCommands"] = self.ribbonStructure["quickAccessCommands"]
                        self.workBenchDict["newPanels"] = self.ribbonStructure["newPanels"]
                        self.workBenchDict["dropdownButtons"] = self.ribbonStructure["dropdownButtons"]
                        self.workBenchDict["ignoredToolbars"] = self.ribbonStructure["ignoredToolbars"]
                        self.workBenchDict["ignoredWorkbenches"] = self.ribbonStructure["ignoredWorkbenches"]
                        self.workBenchDict["iconOnlyToolbars"] = self.ribbonStructure["iconOnlyToolbars"]
                        self.workBenchDict["customToolbars"] = self.ribbonStructure["customToolbars"]

                        self.on_Customize_Clicked()
                                
                        # Load the dialog
                        # 
                        # Get the form
                        DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
                        if os.path.exists(DataFile) is False:
                            Question = translate(
                                "FreeCAD Ribbon",
                                "a data file must be generated first!\n"
                                "Do you want to create one now?\n",
                            )
                            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
                            if Answer == "yes":
                                CacheFunctions.CreateCache()
                                DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
                            else:
                                self.on_Cancel_Clicked()
                                return
                        if os.path.exists(DataFile) is True:
                            self.AddCommandsDialog = LoadAddCommands.LoadDialog(mw, self.workBenchDict)
                            if Parameters.DOCKED_DIALOGS is False:
                                # Show the form
                                self.AddCommandsDialog.form.show()
                            else:
                                RibbonLayoutDock = QDockWidget()
                                # set the name of the object and the window title
                                RibbonLayoutDock.setObjectName("RibbonLayout")
                                RibbonLayoutDock.setWindowTitle("Ribbon Layout")
                                RibbonLayoutDock.setContentsMargins(0, 0, 0, 0)
                                RibbonLayoutDock.setWidget(self.AddCommandsDialog.form)                            
                                # Set the allowed areas to dock
                                RibbonLayoutDock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea|Qt.DockWidgetArea.RightDockWidgetArea)
                                # Add the dockwidget
                                mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, RibbonLayoutDock, Qt.Orientation.Horizontal)

                            
                        
                        return
                    if self.CustomizeEnabled is True:
                        for category in self.CustomizedCategories:
                            self.setCurrentCategory(category)
                            self.on_Ok_Clicked()
                        self.CustomizedCategories.clear()
                        return
 
                if action == CustomizeCancelAct:
                    for category in self.CustomizedCategories:
                        self.setCurrentCategory(category)
                        self.on_Cancel_Clicked()
                    self.CustomizedCategories.clear()
                    return
            
            # Add a context menu to the quickaccess button
            if panel is not None and type(panel) is not RibbonPanel and quickaccessbutton is not None and self.CustomizeEnabled is True and quickaccessbutton.underMouse():
                # Create the buttons for adding a separator
                AddSeparator_Left = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Add separator left"))
                AddSeparator_Left.triggered.connect(lambda: self.on_AddSeparator_QC_Clicked(quickaccessbutton, event.pos(), "left"))
                AddSeparator_Right = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Add separator right"))
                AddSeparator_Right.triggered.connect(lambda: self.on_AddSeparator_QC_Clicked(quickaccessbutton, event.pos(),"right"))
                
                # Create a button to clear the entire quickaccess toolbar
                self.contextMenu.addSeparator()
                ClearToolBar = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Clear toolbar"))
                ClearToolBar.triggered.connect(self.on_ClearToolBar_QC_Clicked)
                
                # create the context menu action
                self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                
                # Disconnect the widgetActions
                AddSeparator_Left.triggered.disconnect()                                
                AddSeparator_Right.triggered.disconnect()
                
            if panel is not None and type(panel) is not RibbonPanel and quickaccessseparator is not None and self.CustomizeEnabled is True and quickaccessseparator.underMouse():
                # Create the buttons for removing the separator
                removeSeparator = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Remove separator"))
                removeSeparator.triggered.connect(lambda: self.on_RemoveSeparator_QC_Clicked(quickaccessseparator, event.pos()))
                
                # Create a button to clear the entire quickaccess toolbar
                self.contextMenu.addSeparator()
                ClearToolBar = self.contextMenu.addAction(translate("FreeCAD Ribbon", "Clear toolbar"))
                ClearToolBar.triggered.connect(self.on_ClearToolBar_QC_Clicked)
                
                # create the context menu action
                self.contextMenu.exec_(self.mapToGlobal(event.pos()))
                
                # Disconnect the widgetActions
                removeSeparator.triggered.disconnect()
             
        widget = None
        panel = None
        return
    
    def on_Customize_Clicked(self):
        # Get the name of the current workbench
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        if self.currentCategory() not in self.CustomizedCategories:
            self.CustomizedCategories.append(self.currentCategory())
        self.CurrentCategoryToRestore = self.currentCategory()
                
       # Set a stylesheet to indicate that you are in the customize enviroment
        HoverColor = StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
        Color = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        Addition = (
        """RibbonCategory, QToolBar {
            border-top: 0.5px solid red;
            background: """
            + Color +
        """;}
        RibbonPanelTitle:hover {
            background: 0.5px solid """
            + HoverColor
            + """;
            RibbonToolButton {
                background: 0.5px solid """
            + HoverColor
            + """;
            }
        }""")
        StyleSheet = self.StyleSheet + Addition
        self.currentCategory().setStyleSheet(StyleSheet)
        self.quickAccessToolBar().setStyleSheet(StyleSheet)
        self.CustomizeEnabled = True
        # Just incase
        self.CustomizeOffset = 6
        # self.setRibbonHeight(self.RibbonHeight + self.CustomizeOffset)
        self.currentCategory().setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3 + self.CustomizeOffset
        )
        self.currentCategory().setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3 + self.CustomizeOffset
        )
                                
        # Store the workbench name as the last customized name
        self.LastCustomized = [workbenchName, self.currentCategory().title()]
        
        # Store the state of the buttons
        for title, objPanel in self.currentCategory().panels().items():
            try:
                panelName = objPanel.objectName()
                gridLayout: QGridLayout = objPanel._actionsLayout
                for n in range(gridLayout.count()):
                    try:
                        control: QToolButton = gridLayout.itemAt(n).widget().findChild(CustomControls)
                        if control is not None:
                            StandardFunctions.add_keys_nested_dict(self.ButtonState, [panelName, control.actions().data()])
                            self.ButtonState[panelName][control.actions().data()] = control.actions().isEnabled()
                    except Exception:
                        pass     
            except Exception as e:
                if Parameters.DEBUG_MODE is True:
                    print(f"{title} had a problem with storing the state of its buttons")
                    print(e.args)
                    print(e.__traceback__)
                pass
                
        # Enable all buttons, so you can access them with a right click
        self.actionList = []
        # Activate all buttons
        self.activateButtons()
                                
        # Create all order lists and commands, incase they are not all present
        dictPanels = self.currentCategory().panels()
        # for panel in self.HiddenPanels:
        #     dictPanels[panel.title()] = panel
        for title, objPanel in dictPanels.items():
            
            # Test if the panel is not already deleted.
            # This is needed, if a combined panel was added and then removed by clicking cancel
            try:
                objPanel.objectName()
            except Exception as e:
                if Parameters.DEBUG_MODE is True:
                    print(f"{title} had an error")
                    print(e.args)
                    print(e.__traceback__)
                continue
            # If panels are just removed in this session, they might be still present int the panel list of this category
            # Make sure by comparing the panel with the panels that are replaced by a new custom panel and close it.
            skip = False
            if workbenchName in self.workBenchDict["customToolbars"]:
                for toolbar in self.workBenchDict["customToolbars"][workbenchName].keys():
                    for toolbar in self.workBenchDict["customToolbars"][workbenchName][toolbar]["commands"].values():
                        if toolbar == objPanel.objectName():
                            skip = True
            for panel in self.RemovedPanels:
                if panel.objectName() == objPanel.objectName():
                    skip = True            
            if skip is True:
                objPanel.close()
            # If  the panel is not replaced by a custom panel, show it
            if skip is False:
                objPanel.show()
                # Get the panel name and the gridlayout
                panelName = objPanel.objectName()
                gridLayout: QGridLayout = objPanel._actionsLayout
                
                # show the enable checkboxes  
                titleLayout: QHBoxLayout = objPanel._titleLayout
                EnableControl = titleLayout.itemAt(0).widget()
                if EnableControl is not None:
                    EnableControl.setEnabled(True)
                    EnableControl.setVisible(True)

                # Recreate the order list for the new panel. 
                # This makes sure that all controls are added to the order list
                orderList = []
                for n in range(gridLayout.count()):
                    control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                    if control is not None:                                    
                        # Update the orderlist
                        command = self.ReturnCommand_string(self.workBenchDict, objPanel, control)
                        if command != "" and command is not None:
                            orderList.append(command)

                            # Add the command if they don't exist
                            Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panelName, "commands", command, "size"], "small")
                            # Set the sizes
                            style = control.ButtonStyle
                            if style == RibbonButtonStyle.Small:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "small"
                            if style == RibbonButtonStyle.Medium:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "medium"
                            if style == RibbonButtonStyle.Large:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "large"
                    
                    separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                    if separator is not None:
                        # Set the separator enabled, so that hovering works
                        separator.setEnabled(True)
                        # Make the separator wider, for easier clicking
                        separator.setFixedWidth(16)
                        # Add the separator to the orderlist
                        orderList.append(separator.objectName())
                                                    
                    # Write the order list
                    Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panelName, "order"], endEmpty=True)                         
                    self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["order"] = orderList                                                        

                    
                # If the panel has an overflow menu, replace it with a complete (long) panel
                if objPanel.panelOptionButton().isVisible():
                    newPanel = self.CreatePanel(workbenchName=workbenchName, panelName=objPanel.objectName(), addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)                                
                    replacedPanel = self.currentCategory().replacePanel(objPanel, newPanel)
                    # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
                    self.setPanelProperties(replacedPanel)
                    # Add the newPanel to the list of longPanels
                    self.longPanels.append(newPanel)
                    # Close the old panel
                    objPanel.close()
                    
                    # Recreate the order list from the new panel
                    # Get the panel name and the gridlayout
                    panelName = newPanel.objectName()
                    gridLayout: QGridLayout = newPanel._actionsLayout
                    for n in range(gridLayout.count()):
                        control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                        if control is not None:                                                                       
                            # Update the orderlist
                            command = self.ReturnCommand_string(self.workBenchDict, newPanel, control)
                            if command != "" and command is not None:
                                orderList.append(command)

                            # Add the command if they don't exist
                            Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panelName, "commands", command, "size"], "small")
                            # Set the sizes
                            style = control.ButtonStyle
                            if style == RibbonButtonStyle.Small:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "small"
                            if style == RibbonButtonStyle.Medium:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "medium"
                            if style == RibbonButtonStyle.Large:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = "large"

                        separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                        if separator is not None:
                            # Set the separator enabled, so that hovering works
                            separator.setEnabled(True)
                            # Make the separator wider, for easier clicking
                            separator.setFixedWidth(16)
                            # Add the separator to the orderlist
                            orderList.append(separator.objectName())
                                                
                # Write the order list
                Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panelName, "order"], [])                         
                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["order"] = orderList                                      
                                       
            # Enable all buttons, so you can access them with a right click
            self.activateButtons()            
            
        # StyleSheet_QC = self.quickAccessToolBar().styleSheet()
        # for action in self.quickAccessToolBar().actions():
        #     if "separator" in action.objectName().lower():
        #         self.quickAccessToolBar().setStyleSheet(StyleSheet_QC +
        #             """QuickAccessToolButton#"""
        #                 + action.objectName()
        #                 + """ {background: """
        #                 + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
        #                 + ";}"
        #         )
        return
    
    def on_ApplyClicked(self):
        self.AddedPanels.clear()
        self.RemovedPanels.clear()
        self.ribbonStructure.update(self.workBenchDict)
        # Writing to ribbonStructure.json
        JsonFile = Parameters.RIBBON_STRUCTURE_JSON
        with open(JsonFile, "w") as outfile:
            json.dump(self.ribbonStructure, outfile, indent=4)
        
    
    def on_Ok_Clicked(self, workbenchName = ""):
        # Set the wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        # QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        
        # Get the name of the current workbench
        if workbenchName == "":
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())

        # Set stylesheets
        self.currentCategory().setStyleSheet(self.StyleSheet)
        Color = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        Addition = (
        """RibbonCategory, QToolBar {
            background: """
            + Color +
        """;}"""
        )
        self.StyleSheet = self.StyleSheet + Addition
        self.quickAccessToolBar().setStyleSheet(self.StyleSheet)
        
        # Set the state for the enviroment to False again
        self.CustomizeEnabled = False
        
        # reset the ribbonheight
        self.currentCategory().setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        self.currentCategory().setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )

        # Return the original state of the buttons
        for item in self.actionList:
            if item[1] is False:
                item[0].setDisabled(True)
            else:
                item[0].setEnabled(True)
        Gui.updateGui()       

        # Restore the original panel with the overflow menu
        for title, objPanel in self.currentCategory().panels().items():
            # Test iff the panel is not already deleted.
            # This is needed, if a combined panel was added and then removed by clicking cancel
            try:
                objPanel.objectName()
            except Exception:
                continue
            
            # If it is an new panel without a set title, remove it
            if objPanel.title() == "<New panel>" or objPanel.title() == "":
                objPanel.close()
                continue
            
            for panel in self.RemovedPanels:
                if objPanel.objectName() == panel.objectName():
                    objPanel.close()
                    continue
            
            # hide the enable checkboxes and hide the panel if it is unchecked
            titleLayout: QHBoxLayout = objPanel._titleLayout
            EnableControl = titleLayout.itemAt(0).widget()
            if EnableControl is not None:
                if EnableControl.checkState() == Qt.CheckState.Unchecked:
                    # Hide the panel
                    objPanel.hide()
                    self.HiddenPanels.append(objPanel)
                    # Write the state to the structure
                    StandardFunctions.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", objPanel.objectName(), "Enabled"])
                    self.workBenchDict["workbenches"][workbenchName]["toolbars"][objPanel.objectName()]["Enabled"] = False
                    # If it is not a new panel, add the current panel to temporary panel dict
                    continue
                if EnableControl.checkState() == Qt.CheckState.Checked:
                    # Write the state to the structure
                    StandardFunctions.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", objPanel.objectName(), "Enabled"])
                    self.workBenchDict["workbenches"][workbenchName]["toolbars"][objPanel.objectName()]["Enabled"] = True
                    objPanel.show()
                    for panel in self.HiddenPanels:
                        if panel.objectName() == objPanel.objectName():
                            self.HiddenPanels.remove(panel)
                    for panel in self.ReplacedPanels:
                        if panel.objectName() == objPanel.objectName():
                            self.ReplacedPanels.remove(panel)
                EnableControl.setVisible(False)

            # Create a bool to state if a panel is new or not
            IsNewPanel = False                            
            for longPanel in self.longPanels:
                # Test if the panel is not already deleted.
                # This is needed, if a combined panel was added and then removed by clicking cancel
                try:
                    longPanel.objectName()
                except Exception:
                    continue
                
                for panel in self.RemovedPanels:
                    if longPanel.objectName() == panel.objectName():
                        longPanel.close()
                        continue
                
                if longPanel.objectName() == objPanel.objectName() and longPanel.objectName() != "" and objPanel.objectName() != "":
                    if longPanel.objectName() in self.workBenchDict["workbenches"][workbenchName]["toolbars"]:
                        if self.workBenchDict["workbenches"][workbenchName]["toolbars"][longPanel.objectName()]["Enabled"] is False:
                            continue                               
                    
                    # Create a panel and replace the long panel with this one
                    newPanel = self.CreatePanel(workbenchName=workbenchName, panelName=objPanel.objectName(), addPanel=False, Dict=self.workBenchDict, ActivateButtons=True)  
                    if newPanel is not None:
                        # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
                        self.setPanelProperties(newPanel)
                        try:
                            self.currentCategory().replacePanel(longPanel, newPanel)
                        except Exception:
                            pass
                        try:
                            self.currentCategory().replacePanel(objPanel, newPanel)
                        except Exception:
                            pass
                        # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
                        self.setPanelProperties(newPanel)
                        # Close the old panel
                        objPanel.deleteLater()
                        longPanel.deleteLater()
                        # Update the temporary panel dict
                        self.currentCategory().panels()[title] = newPanel
                        # Set the bool to True
                        IsNewPanel = True
                        break
            # If it is not a new panel, add the current panel to temporary panel dict
            if IsNewPanel is False:
                self.currentCategory().panels()[title] = objPanel
        
        # Set the buttonstate back as it was
        for title, objPanel in self.currentCategory().panels().items():
            # Test if the panel is not already deleted.
            # This is needed, if a combined panel was added and then removed by clicking cancel
            try:
                objPanel.objectName()
            except Exception:
                continue
            
            # Get the panel name and the gridlayout
            panelName = objPanel.objectName()
            gridLayout: QGridLayout = objPanel._actionsLayout
            for n in range(gridLayout.count()):
                control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                if control is not None:
                    try:
                        ButtonState = self.ButtonState[panelName][control.actions().data()]
                        control.actions().setEnabled(ButtonState)
                    except Exception:
                        pass
                
                separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                if separator is not None:
                    # Disable the separators to avoid highlighting when hovering
                    separator.setEnabled(False)
                    # Set the separator to its original width
                    separator.setFixedWidth(6)
                    
            # Hide the panels that are toggled off
            titleLayout: QHBoxLayout = objPanel._titleLayout
            EnableControl: Toggle = titleLayout.itemAt(0).widget()
            if EnableControl is not None:
                if EnableControl.isChecked() is False: 
                    objPanel.hide()
                                                                   
        # Clear the list with the long panels, so that it can be filled again next time
        self.longPanels.clear()
        
        for panel in self.RemovedPanels:
            try:
                self.currentCategory().removePanel(panel.objectName())
            except Exception:
                pass
            panel.close()
        
        # update the ribbonstructure before writing it to disk
        self.ribbonStructure.update(self.workBenchDict)
        
        # Writing to ribbonStructure.json
        JsonFile = Parameters.RIBBON_STRUCTURE_JSON
        with open(JsonFile, "w") as outfile:
            json.dump(self.ribbonStructure, outfile, indent=4)
                
        # Close the temporary document
        try:
            App.closeDocument("Temporary")
        except Exception:
            pass
        
        # Close the AddCommands dialog
        if self.AddCommandsDialog is not None:
            self.AddCommandsDialog.form.close()
            self.AddCommandsDialog = None
            # Close the dockwidget is there is one
            DockWidget = mw.findChild(QDockWidget, "RibbonLayout")
            if DockWidget is not None:
                DockWidget.deleteLater()
                
         # Restore the cursor
        QApplication.restoreOverrideCursor()

        # Hide the replaced panels (by a combined panel)
        for objPanel in self.currentCategory().panels().values():
            for panel in self.ReplacedPanels:
                if panel.objectName() == objPanel.objectName():
                    panel.hide()
                    objPanel.hide()
        
        # Clear the workbench dict
        self.workBenchDict.clear()
        
        # Clear the panel lists
        self.HiddenPanels.clear()
        self.ReplacedPanels.clear()
        self.CombinePanels.clear()
        # self.AddedPanels.clear()
        # self.RemovedPanels.clear()
        
        # Activate the stored category when the customise enviroment was started
        self.setCurrentCategory(self.CurrentCategoryToRestore)
        self.hideClassicToolbars()  
        
        # for action in self.quickAccessToolBar().actions():
        #     if "separator" in action.objectName().lower():
        #         self.quickAccessToolBar().setStyleSheet(
        #             """QToolButton#"""
        #                 + action.objectName()
        #                 + """{background: """
        #                 + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #                 + ";}"
        #         )
        
        # Print a message
        print(translate("FreeCAD Ribbon", "RibbonUI: Changes are saved"))
        return
    
    def on_Cancel_Clicked(self, workbenchName = ""):
        # Set the wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        # QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)

        # Get the name of the current workbench
        if workbenchName == "":
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        
        # Set stylesheets
        self.currentCategory().setStyleSheet(self.StyleSheet)
        Color = StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        Addition = (
        """RibbonCategory, QToolBar {
            background: """
            + Color +
        """;}"""
        )
        self.StyleSheet = self.StyleSheet + Addition
        self.quickAccessToolBar().setStyleSheet(self.StyleSheet)
        
        # define a boolan for the enviroment state
        self.CustomizeEnabled = False
        
        # Change the height of the ribbon for the border line
        self.currentCategory().setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        self.currentCategory().setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        
        # read ribbon structure from JSON file
        Dict = {}
        with open(Parameters.RIBBON_STRUCTURE_JSON, "r") as file:
            Dict.update(json.load(file))
        
        # Restore the original panels used with combine panels
        dictPanels = self.currentCategory().panels()
        for panel in self.ReplacedPanels:
            isInList = False
            for objPanel in dictPanels.values():
                if panel.objectName() == objPanel.objectName():
                    isInList = True
            if isInList is False:
                dictPanels[panel.title()] = panel

        for title, objPanel in dictPanels.items():
            # Test if the panel is not already deleted.
            # This is needed, if a combined panel was added and then removed by clicking cancel
            try:
                objPanel.objectName()
            except Exception:
                continue
            # If it is an new panel without a set title, remove it
            if objPanel.title() == "<New panel>":
                objPanel.close()
                continue
            # If the panel is not in the ribbon structure, remove it
            if objPanel.objectName() not in Dict["workbenches"][workbenchName]["toolbars"]:
                objPanel.close()
                continue
            # Close any combined panels
            for panel in self.CombinePanels:
                if panel.objectName() == objPanel.objectName():
                    objPanel.close()
                    continue
            # if the panel was just added, close it again
            for panel in self.AddedPanels:
                if panel.objectName() == objPanel.objectName():
                    objPanel.close()
                    continue
            
            # Create a panel and replace the long panel with this one
            newPanel = self.CreatePanel(workbenchName=workbenchName, panelName=objPanel.objectName(), addPanel=False, Dict=Dict, ActivateWorkbench=False)
            if newPanel is None:
                continue
            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
            self.setPanelProperties(newPanel)
            # try:
            self.currentCategory().replacePanel(objPanel, newPanel)
            # except Exception:
            #     pass
            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
            # if newPanel is not None:
            self.setPanelProperties(newPanel)
            # Update the panel dict            
            dictPanels[title] = newPanel
            # Delete the old panel
            objPanel.deleteLater()
            
            # Set the buttonstate back as it was
            panelName = newPanel.objectName()
            gridLayout: QGridLayout = newPanel._actionsLayout
            for n in range(gridLayout.count()):
                control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                if control is not None:
                    try:
                        ButtonState = self.ButtonState[panelName][control.actions().data()]
                        control.actions().setEnabled(ButtonState)
                    except Exception:
                        pass
                
                separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                if separator is not None:
                    # Disable the separators to avoid highlighting when hovering
                    separator.setEnabled(False)
                    # Set the separator to its original width
                    separator.setFixedWidth(6)
                                                                                         
            # Hide the panels that are toggled off
            titleLayout: QHBoxLayout = newPanel._titleLayout
            EnableControl: Toggle = titleLayout.itemAt(0).widget()
            if EnableControl is not None:
                if EnableControl.isChecked() is False: 
                    newPanel.hide()
        
        # Restore the replaced panels
        for panel in self.ReplacedPanels:
            panel.show()
        
        # Restore closed panels
        for panel in self.RemovedPanels:
            panel.show()
            
        for panel in self.AddedPanels:
            panel.close()   
            try:
                self.currentCategory().removePanel(panel.objectName())
            except Exception:
                pass   
                
        # Remove panels that newly added by combining panels
        for objPanel in self.CombinePanels:
            if objPanel.objectName() not in Dict["customToolbars"][workbenchName]:                     
                objPanel.deleteLater()
            try:
                 self.currentCategory().removePanel(objPanel.title())
            except Exception:
                pass      

        # Restore the ribbonstructure
        self.ribbonStructure = Dict
        
        # Restore the quickaccess toolbar
        #
        # Remove the current buttons
        for child in self.quickAccessToolBar().findChildren(QToolButton):
            if type(child) is QuickAccessSeparator or type(child) is QuickAccessToolButton or type(child) is DragTargetIndicator:
                child.deleteLater()
        # Create new buttons and add them to the quickacces toolbar based on the original order
        for commandName in self.ribbonStructure["quickAccessCommands"]:
            button = self.CreateQuickButtonFromCommand(commandName=commandName)
            self.addQuickAccessButton(button)
                                           
        # Clear the workbench dict
        self.workBenchDict.clear()
        
        # Clear the panel lists
        self.HiddenPanels.clear()
        self.ReplacedPanels.clear()
        self.CombinePanels.clear()
        # self.AddedPanels.clear()
        # self.RemovedPanels.clear()
                   
        # Close the AddCommands dialog
        if self.AddCommandsDialog is not None:
            self.AddCommandsDialog.form.close()
            self.AddCommandsDialog = None
            # Close the dockwidget is there is one
            DockWidget = mw.findChild(QDockWidget, "RibbonLayout")
            if DockWidget is not None:
                DockWidget.deleteLater()
        
        # Restore the cursor
        QApplication.restoreOverrideCursor()
        
        # Activate the stored category when the customise enviroment was started
        self.setCurrentCategory(self.CurrentCategoryToRestore)
        self.hideClassicToolbars()
        
        # for action in self.quickAccessToolBar().actions():
        #     if "separator" in action.objectName().lower():
        #         self.quickAccessToolBar().setStyleSheet(
        #             """QToolButton#"""
        #                 + action.objectName()
        #                 + """{background: """
        #                 + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
        #                 + ";}"
        #         )
        
        # Print a message
        print(translate("FreeCAD Ribbon", "RibbonUI: Changes are rolled back"))
        return
        
    def on_ButtonStyle_Clicked(self, panel: RibbonPanel, ButtonWidget: CustomControls, ButtonStyleWidget: ComboBoxAction, ButtonSizeWidget: SpinBoxAction):     
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
                                    
        # get the size to set
        Size = "small"
        if ButtonStyleWidget.currentText() == "Medium":
            Size = "medium"
        if ButtonStyleWidget.currentText() == "Large":
            Size = "large"

        # write the changes to the ribbonstruture file 
        property = {"size": Size}
        self.WriteButtonSettings(ButtonWidget, panel, property)
        
        # Create a new panel
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)
        # Add the panel to the list with long panels
        if newPanel.panelOptionButton().isVisible():
            self.longPanels.append(newPanel)
        
        # Replace the panel with the new panel
        self.currentCategory().replacePanel(panel, newPanel)
        # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
        self.setPanelProperties(newPanel)
        
        # Update the dict of the currentCategory with the new panel
        self.currentCategory()._panels[newPanel.objectName()] = newPanel
        
        # Close the old panel
        try:
            # if panel.objectName() == newPanel.objectName():
            panel.close()
        except Exception:
            pass
        
        # Enable all buttons, so you can access them with a right click
        self.activateButtons()
        
        # Check if there are other large or medium buttons
        LargeButtons = 0
        MediumButtons = 0
        SmallButtons = 0
        self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] = 0
        self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"] = 0
        self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] = 0
        for panel in self.currentCategory().panels().values():
            for widget in panel.widgets():
                if type(widget) is CustomControls:
                    if widget.ButtonStyle is RibbonButtonStyle.Small:
                        SmallButtons = SmallButtons + 1
                    if widget.ButtonStyle is RibbonButtonStyle.Medium:
                        MediumButtons = MediumButtons + 1
                    if widget.ButtonStyle is RibbonButtonStyle.Large:
                        LargeButtons = LargeButtons + 1                
        if LargeButtons > 0:
            self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] = 1
        if MediumButtons >= 2:  
            self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"] = 2
        if SmallButtons >= 3:
            self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] = 3
            
        # Correct the height of each panel
        for objPanel in self.currentCategory().panels().values():
            self.setPanelProperties(objPanel)

        # reset the ribbonheight
        self.currentCategory().setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        self.currentCategory().setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        # Make sure that the ribbon is completly unfolded.
        self.UnfoldRibbon()

        # Close the context menu
        self.contextMenu.close()
        return
    
    def on_ButtonSize_Changed(self, panel: RibbonPanel, ButtonWidget: QToolButton, ButtonSizeWidget: SpinBoxAction):              
        # Get the menubutton height for large buttons
        menuButtonWidth = 0
        if "CustomWidget_Large" not in ButtonWidget.objectName():
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
        
        # Set the height to the value of the spinbox
        ButtonWidget.setFixedHeight(ButtonSizeWidget.value())
        # Adjust the with including menubutton and label
        if "CustomWidget_Large" not in ButtonWidget.objectName():
            ButtonWidget.setFixedWidth(ButtonSizeWidget.value() + labelWidth + menuButtonWidth)
        if "CustomWidget_Large" in ButtonWidget.objectName():
            ButtonWidget.setFixedWidth(ButtonSizeWidget.value())
            ButtonWidget.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
            ButtonWidget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
            for child in ButtonWidget.children():
                if type(child) == QLabel:
                        child.setFixedWidth(ButtonSizeWidget.value())

        # Set the Button width size to that of its parent
        ButtonWidget.parent().setFixedSize(ButtonWidget.size())
        
        # write the changes to the ribbonstruture file 
        property = {"ButtonSize_small": ButtonSizeWidget.value()}
        if "CustomWidget_Medium" in ButtonWidget.objectName():
            property = {"ButtonSize_medium": ButtonSizeWidget.value()}
        if "CustomWidget_Large" in ButtonWidget.objectName():
            property = {"ButtonSize_large": ButtonSizeWidget.value()}
        self.WriteButtonSettings(ButtonWidget, panel, property)
        return
    
    def on_TextState_Changed(self, panel: RibbonPanel, ButtonWidget: CustomControls, TextEnabled: bool):
        # If the widget has no text, show it with the correct width
        if TextEnabled is True:
            self.WriteButtonSettings(ButtonWidget, panel, {"textEnabled": TextEnabled})
        # if the widget has text, find its QTextEdit and hide it. Update the width
        if TextEnabled is False:           
            self.WriteButtonSettings(ButtonWidget, panel, {"textEnabled": TextEnabled})
        
         # Create a new panel
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())        
        newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)
        # Add the panel to the list with long panels
        if newPanel.panelOptionButton().isVisible():
            self.longPanels.append(newPanel)
                
        # Replace the panel with the new panel
        self.currentCategory().replacePanel(panel, newPanel)
        # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
        self.setPanelProperties(newPanel)

        # Update the dict of the currentCategory with the new panel
        self.currentCategory()._panels[newPanel.objectName()] = newPanel

        # Enable all buttons, so you can access them with a right click
        self.activateButtons()
        
        # Close the old panel
        panel.close()
        
        # Close the context menu
        self.contextMenu.close() 
        return
    
    def on_ClearToolBar_QC_Clicked(self):
        # Remove the buttons from the quickaccess toolbar
        for child in self.quickAccessToolBar().findChildren(QToolButton):
            if type(child) is QuickAccessSeparator or type(child) is QuickAccessToolButton or type(child) is DragTargetIndicator:
                child.deleteLater()
        self.quickAccessToolBar().setMinimumWidth(self.applicationOptionButton().width())
        self.workBenchDict["quickAccessCommands"].clear()
        return
    
    def on_AddSeparator_QC_Clicked(self, ButtonWidget: QuickAccessToolButton, pos: QPoint, Side = "left"):
        # Determine the index of the Button that is clicked on
        buttonList = self._titleWidget._quickAccessToolBar.findChildren(QToolButton)
        buttonAction = ButtonWidget.actions()[0]
        index = -1
        for i in range(len(buttonList)):
            action = buttonList[i].defaultAction()
            if action is not None:
                if action.data() == buttonAction.data():
                    index = i-2 # minus the application button and some hidden button
                    break
        
        # Get the relative position of the cursor. Either left or right from the button that is clicked on
        ExtraOffset = 0
        if Side.lower() == "right":
            ExtraOffset = ButtonWidget.width()
        point = QPoint(pos.x() + ExtraOffset , pos.y())
        buttonPos = self._titleWidget._quickAccessToolBar.mapTo(self._titleWidget._quickAccessToolBar ,point)
        
        # Get the before action
        beforeAction = self._titleWidget._quickAccessToolBar.actionAt(buttonPos)

        # Create the separator
        separator = QuickAccessSeparator(self.quickAccessToolBar())
        separator.setObjectName("separator")
        separator.setFixedSize(12, ButtonWidget.height())
        
        # Add the separator to the quicktoolbar
        self._titleWidget._quickAccessToolBar.insertWidget(beforeAction, separator)
        
        # Update the quickAccessCommands list
        self.workBenchDict["quickAccessCommands"].insert(index, separator.objectName())
        return       
    
    def on_RemoveSeparator_QC_Clicked(self, separator: QuickAccessSeparator, pos: QPoint):
        # Get a list of all buttons
        buttonList = self._titleWidget._quickAccessToolBar.findChildren(QToolButton)
        # Start with the index at -1. This way, the index is zero based
        index = -1
        # Go through the button list. if the passed position is withing the edges of a button,
        # You got the right one
        for button in buttonList:
            index = index + 1
            # Map the for corners of the button to global
            pos_tl = button.mapToGlobal(button.rect().topLeft())
            pos_tr = button.mapToGlobal(button.rect().topRight())
            pos_bl = button.mapToGlobal(button.rect().bottomLeft())
            pos_br = button.mapToGlobal(button.rect().bottomRight())

            # If the position of the context menu event is within the global corners
            # delete the button if it is a separator
            if pos.x() > pos_tl.x() and pos.x() < pos_tr.x():
                if pos.y() > pos_tl.y() and pos.y() < pos_bl.y():
                    if type(button) is QuickAccessSeparator:
                        button.deleteLater()
                        break
        
        # Update the quickAccessCommands list
        self.workBenchDict["quickAccessCommands"].pop(index-2)

        return
    
    def on_AddSeparator_Clicked(self, panel: RibbonPanel, ButtonWidget: CustomControls, Side = "left"):
        # Get the workbench hame and the panel name
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        panelName = panel.objectName()
        # Declare an order list
        OrderList = []
        # Copy the workbench dict
        Dict = self.workBenchDict
        # Get the order of toolbars
        if "workbenches" in Dict:
            if workbenchName in Dict["workbenches"]:
                if panelName in Dict["workbenches"][workbenchName]["toolbars"]:
                    if "order" in Dict["workbenches"][workbenchName]["toolbars"][panelName]:
                        OrderList: list = Dict["workbenches"][workbenchName]["toolbars"][panelName]["order"]
        
        # if the orderlist is not empty, you may add a separator.
        # An empty list, results in the separator at the start of the panel                        
        if len(OrderList) > 0:
            index = None
            # Get the command name and its index in the list
            CommandName = ButtonWidget.findChild(QToolButton).defaultAction().data()
            if CommandName in OrderList:
                index = OrderList.index(CommandName)
            else:
                StandardFunctions.Mbox(
                    translate("FreeCAD Ribbon", "The command is not present in the Ribbon Layout.\n Close the customize enviroment to update the layout file and try again."),
                "",
                "Warning",
                )
            
            # Add the separator either let or right
            if index is not None:
                if Side == "left" :
                    if index > 0:
                        OrderList.insert(index, f"{index}_separator_{workbenchName}")
                else:
                    if index < len(OrderList)-1:
                        OrderList.insert(index+1, f"{index+1}_separator_{workbenchName}")
            
            # Set the orderlist in the dict and update the workbench dict
            Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["order"] = OrderList
            self.workBenchDict.update(Dict)
       
            # Create a new panel
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
            newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict,  ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)
            # Add the panel to the list with long panels
            if newPanel.panelOptionButton().isVisible():
                self.longPanels.append(newPanel)

            # Replace the panel with the new panel
            self.currentCategory().replacePanel(panel, newPanel)
            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
            self.setPanelProperties(newPanel)
            
            # Update the dict of the currentCategory with the new panel
            self.currentCategory()._panels[newPanel.objectName()] = newPanel

            # Enable all buttons, so you can access them with a right click
            self.activateButtons()
            
            # Close the old panel
            panel.close()
            
            # Close the context menu
            self.contextMenu.close()
        return
            
    def on_RemoveSeparator_Clicked(self, panel: RibbonPanel, separator: CustomSeparator):
        # Get the workbench hame and the panel name
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        panelName = panel.objectName()
        # Declare an order list
        OrderList = []
        # Copy the workbench dict
        Dict = self.workBenchDict.copy()
        # Get the order of toolbars
        if "workbenches" in Dict:
            if workbenchName in Dict["workbenches"]:
                if panelName in Dict["workbenches"][workbenchName]["toolbars"]:
                    if "order" in Dict["workbenches"][workbenchName]["toolbars"][panelName]:
                        OrderList: list = Dict["workbenches"][workbenchName]["toolbars"][panelName]["order"]
        
        # if the orderlist is not empty, you can remove a separator.
        if len(OrderList) > 0:
            # Get the index of the separator and remove it from the list
            index = OrderList.index(separator.objectName())
            OrderList.pop(index)
            
            # Set the orderlist in the dict and update the workbench dict
            Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["order"] = OrderList 
            self.workBenchDict.update(Dict)
            
            # Create a new panel
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
            newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)
            # Add the panel to the list with long panels
            if newPanel.panelOptionButton().isVisible():
                self.longPanels.append(newPanel)
            
            # Replace the panel with the new panel
            self.currentCategory().replacePanel(panel, newPanel)
            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
            self.setPanelProperties(newPanel)
            
            # Enable all buttons, so you can access them with a right click
            self.activateButtons()
            
            # Close the old panel
            panel.close()
            
            # Close the context menu
            self.contextMenu.close()

    def on_ButtonLabel_Changing(self, event, panel: RibbonPanel, ButtonWidget: CustomControls, widgetAction: CustomWidgets.LineEditAction):
        widgetAction.setClearButtonEnabled(True)
        Text = event
        # If the text is empty, restore the original name
        if Text == "":
            CommandName = ""
            for child in ButtonWidget.children():
                if (
                    type(child) is QToolButton
                    and child.objectName() == "CommandButton"
                ):
                    CommandName = child.defaultAction().data()
                    Text = CommandInfoCorrections(CommandName)["menuText"].replace("&", "")
                    widgetAction.setPlaceholderText(Text)
                
        # write the changes to the ribbonstructure file
        property = {"text": Text}
        self.WriteButtonSettings(ButtonWidget, panel, property)
        
        # Set the text also in the label widget
        LabelWidget: QLabel = ButtonWidget.findChild(QLabel)
        LabelWidget.setText(Text)
        return

    def on_PanelTitle_Changing(self, event, panel: RibbonPanel, widgetAction: CustomWidgets.LineEditAction):
        # Get the workbench name and the panel name
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        panelName = panel.objectName()
        widgetAction.setClearButtonEnabled(True)
        
        Text = event
        # If the text is empty, restore the original name
        if Text == "":
            Text = self.ReturnPanelTitle(panel, self.workBenchDict, filterOnly=True)
            widgetAction.setPlaceholderText(Text)

        # Create an entry in the dict if there isn't one
        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panelName, "title"])
        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["title"] = Text
        # Set the panel title
        panel.setTitle(Text)
        return
    # endregion

    # region - drag drop event functions
    #
    # Drag indicators
    dragIndicator_Buttons = DragTargetIndicator(orientation="top", margins=0)
    dragIndicator_Panels = DragTargetIndicator(orientation="right")
    dragIndicator_QuickAccess = DragTargetIndicator(orientation="right")
    #
    # QuickAccess
    dragAction_QuickAccess = None
    DropIndex_QuickAccess = None
    #
    # General
    position = None
    spaceWidget_Left = RibbonToolButton()
    spaceWidget_Right = RibbonToolButton()
    target = None
    targetPanel = None
    StartPositionDrag = None
    #
    # AddCommands
    dropPanel = None
    dropPanelName = ""
    AddCommand_ActionData = ""
    AddCommand_Icon = None
    AddCommand_Text = ""
    
    def dragEnterEvent(self, event: QDragEnterEvent):         
        if self.CustomizeEnabled is True:
            if self.dragIndicator_QuickAccess is None:
                self.dragIndicator_QuickAccess = DragTargetIndicator(orientation="right")
            
            # Get the widget from the source
            widget = event.source()
                
            # If not activated, activate all buttons    
            self.activateButtons()                              
                
            # Store the position were the drag is started
            if self.StartPositionDrag is None:
                self.StartPositionDrag = [event.pos(), widget.rect()]
            
            count = 0
            parent = widget.parent()
            panel = RibbonPanel()
            while (count < 100):
                try:
                    try:    
                        parent.setAcceptDrop(True)
                    except Exception:
                        pass
                    parent = parent.parent()
                    if type(parent) is RibbonPanel:
                        panel = parent
                        break
                    count = count + 1
                except Exception:
                    break
            
            # Check if there are more than one buttons. If not there is no point to drag and exit
            if len(panel.widgets()) <= 2 and type(widget) is not RibbonPanel and panel.findChild(QWidget, "ExtraSpacer") is not None:
                event.ignore()
            else:
                self.dropPanel = panel
                event.acceptProposedAction()
                event.setAccepted(True)
                event.accept()
        return
                       
    def dragLeaveEvent(self, event: QDragLeaveEvent):
        if self.CustomizeEnabled is True:
            # Hide the drag indicator when you leave the drag area
            self.dragIndicator_Buttons.close()
            self.dragIndicator_Panels.close()
            self.dragIndicator_QuickAccess.close()
            self.target = None
            self.targetPanel = None
            self.dropPanelName = None
            
            # Enable all buttons, so you can access them with a right click
            self.actionList = []
            # Activate all buttons
            self.activateButtons()
        
        return
     
    def dragMoveEvent(self, event: QDragMoveEvent):
        if self.CustomizeEnabled is True:
            widget = event.source()
            
             # If you drag and drop a new command, you actually dragging the complete QListWidget
            if type(widget) is QListWidget:
                position = event.pos()
                # If the position is within a panel, store the panel name
                for panelName, panel in self.currentCategory().panels().items():
                    panelPos = panel.pos()
                    xMin = panelPos.x()
                    xMax = xMin + panel.rect().width()
                    
                    if position.x() >= xMin and position.x() < xMax:
                        self.dropPanelName = panelName

            # If the widget is not a panel, continue here
            if type(widget) is not RibbonPanel  and type(widget) is not QListWidget:
                count = 0
                while (count < 10):                    
                    if type(widget) is CustomControls:
                        break
                    if type(widget) is QuickAccessToolButton:
                        break
                    if type(widget) is CustomSeparator:
                        break
                    if type(widget) is QuickAccessSeparator:
                        break
                    else:
                        if widget is not None:
                            widget = widget.parent()
                    count = count + 1

                # Get the panel
                panel = RibbonPanel()
                QuickAccessToolBar = QToolBar()
                count = 0
                parent = None
                if widget is not None:
                    parent = widget.parent()
                    while (count < 10):
                        if type(parent) is RibbonPanel:
                            panel = parent
                            break
                        if type(parent) is QToolBar:
                            QuickAccessToolBar = parent
                            break
                        else:
                            parent = parent.parent()
                        count = count + 1
                        
                if type(parent) is RibbonPanel:
                    gridLayout: QGridLayout = panel._actionsLayout
                    position = None
                    # Find the correct location of the drop target, so we can move it there.
                    position: object= self.find_drop_location(event)
                    if position is None:
                        return
                    # If the widget is a separator or the extra widget for large buttons, skip it
                    if type(position[3].children()[1]) is CustomSeparator or position[3].children()[1].objectName() == "ExtraSpacer" or type(position[3].children()[1]) is RibbonApplicationButton:
                        return

                    # Inserting moves the item if its already in the layout.
                    rowSpan = position[2]
                    try:
                        widgetHoveredOver = gridLayout.itemAtPosition(position[0], position[1]).widget().findChild(CustomControls)
                        self.target = position
                        try:
                            Button = self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=widgetHoveredOver)
                            self.target = [position[0], position[1], Button]
                        except Exception:
                            pass
                                    
                        if position[0] == 0:
                            self.dragIndicator_Buttons._orientation = "left"
                        else:
                            self.dragIndicator_Buttons._orientation = "top"
                        # Add the drag indicator
                        gridLayout.addWidget(
                            self.dragIndicator_Buttons, position[0], position[1], rowSpan, 1
                        )
                                                            
                        # When you hide the source, the dragged widget disapears from the panel.
                        # For now It is left in, to keep the panel at the same size.
                        # e.source().hide()
                        # Show the target.
                        self.dragIndicator_Buttons.show()
                    except Exception:
                        pass

                if type(parent) is QToolBar and parent.objectName() == "quickAccessToolBar":
                    # Get the relative position of the cursor
                    # point = QPoint(event.pos().x() + widget.width(), event.pos().y())
                    point = QPoint(event.pos().x(), event.pos().y())
                    buttonPos = QuickAccessToolBar.mapTo(QuickAccessToolBar ,point)
                    # Get the button
                    Button = QuickAccessToolBar.childAt(buttonPos)
                    # Get the action before which the drag indicator has to be placed
                    beforeAction = QuickAccessToolBar.actionAt(buttonPos)
                                        
                    if Button is None:
                        return
                                            
                    if beforeAction is not None and Button is not None:
                        if type(Button) is QuickAccessToolButton or type(Button) is QToolButton or type(Button) is QuickAccessSeparator:
                            # Store the beforeAction globally
                            self.dropWidget_QuickAccess = beforeAction                            
                            # Store the index of the current beforeAction. This is needed for the drop function to save the order
                            self.DropIndex_QuickAccess = QuickAccessToolBar.actions().index(beforeAction)
                            # If the button is an Target indicator or is None, remove it.
                            if type(Button) is DragTargetIndicator:
                                QuickAccessToolBar.removeAction(self.dragAction_QuickAccess)
                                return
                                
                            # If the button is an quickaccessbutton, show a drag indicator in the quickaccess toolbar
                            dragIndicator = self.dragIndicator_QuickAccess
                            if self.dragAction_QuickAccess is None:
                                self.dragAction_QuickAccess = QuickAccessToolBar.insertWidget(beforeAction, dragIndicator)
                                dragIndicator.show()                        
                            else:
                                QuickAccessToolBar.insertAction(beforeAction, self.dragAction_QuickAccess)
                                self.dragAction_QuickAccess.setVisible(True)
                            self.dragAction_QuickAccess.setObjectName(Button.objectName())
                                                
                    # # If the beforeAction is None, you are at the end of the QuickAccess Toolbar
                    # if len(QuickAccessToolBar.actions()) + 1 == self.DropIndex_QuickAccess:
                    #     dragIndicator = self.dragIndicator_QuickAccess
                    #     self.dragIndicator_QuickAccess_Action = QuickAccessToolBar.addWidget(dragIndicator)
                    #     self.dragIndicator_QuickAccess_Action.setVisible(True)
                                        
            if type(widget) is RibbonPanel:
                position: object= self.find_drop_location(event)
                try:                     
                    self.currentCategory().insertWidget(self.dragIndicator_Panels, position[0])
                    self.dragIndicator_Panels.show()
                except Exception:
                    pass            
            event.acceptProposedAction()
            event.setAccepted(True)
            event.accept()
        return
  
    def dropEvent(self, event:QDropEvent, widget = None):        
        # Get the widget
        if widget is None:
            widget = event.source()
        
        # Define a parent
        parent = widget.parent()

        # Get the current category
        currentCategory = self.currentCategory()
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())

        # Add a new button by drag & drop
        #
        # If you drag and drop a new command, you actually dragging the complete QListWidget with the sekected item as current item
        if type(widget) is QListWidget:
            # Add buttons to panels
            if self.quickAccessToolBar().underMouse() is False:
                # Set the default size depending on the max size of the button
                Size = "small"
                if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  == 2 and self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] == 0 and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 3:
                    Size = "medium"
                if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  <= 2 and self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] == 1 and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 3:
                    Size = "medium"
                if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  == 0 and self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] == 1 and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 3:
                    Size = "large"
                
                for panelName, panel in currentCategory.panels().items():
                    # If the panelName is equal to the panel name on which the command is dropped, continue.
                    if panelName == self.dropPanelName and panel not in self.RemovedPanels:
                        # Get the command to be added
                        ExtraCommand = widget.currentItem().data(Qt.ItemDataRole.UserRole)
                        # If the commands is part of a dropdown, get the actual command name
                        if len(ExtraCommand.split(", ")) > 1:
                            Command = Gui.Command.get(ExtraCommand.split(", ")[0])
                            if Command is not None:
                                i = int(ExtraCommand.split(", ")[1])
                                action = Command.getAction()[i]
                                ExtraCommand = action.objectName()

                        # Define a holder for the Menu Text
                        MenuText = ""
                        ExtraCommand_WB = ""
                        for CommandItem in self.List_Commands:
                            if CommandItem[0] == ExtraCommand:
                                MenuText = CommandItem[4]
                                ExtraCommand_WB = CommandItem[3]
                        
                        if ExtraCommand.endswith("_ddb"):
                            MenuText = ExtraCommand.replace("_ddb", "")
                            ExtraCommand_WB = "General"
                                            
                        # Get the workbench name and the panel name                  
                        title = panel.objectName()
                        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
                        
                        # Get the order list, if there isn't one, create it
                        StandardFunctions.add_keys_nested_dict(
                            self.workBenchDict,
                            [
                                "workbenches",
                                workbenchName,
                                "toolbars",
                                panel.objectName(),
                            ],
                            endEmpty=True,
                        )
                        OrderList = []            
                        if panel.objectName() in self.workBenchDict["workbenches"][workbenchName]["toolbars"]:
                            if "order" in self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]:
                                OrderList = self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["order"]
                            else:
                                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["order"] = OrderList

                        # Add the extra command to the order list
                        OrderList.append(ExtraCommand)
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][title]["order"] = OrderList
                        # Add the command to the panel in the dict
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panel.objectName(), "commands", ExtraCommand, "size"], endEmpty=True)
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panel.objectName(), "commands", ExtraCommand, "text"], endEmpty=True)
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panel.objectName(), "commands", ExtraCommand, "icon"], endEmpty=True)
                        Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", panel.objectName(), "commands", ExtraCommand, "IsExtra"], endEmpty=True)
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["commands"][ExtraCommand]["size"] = Size
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["commands"][ExtraCommand]["text"] = MenuText
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["commands"][ExtraCommand]["icon"] = ""
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["commands"][ExtraCommand]["IsExtra"] = True
                        
                        # if this is a newPanel, update the newpanel dict as well
                        if panel.objectName().endswith("_newPanel"):
                            if workbenchName not in self.workBenchDict["newPanels"]:
                                Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["newPanels", workbenchName], endEmpty=True)
                            if panel.objectName() not in self.workBenchDict["newPanels"][workbenchName]:
                                Standard_Functions_Ribbon.add_keys_nested_dict(self.workBenchDict, ["newPanels", workbenchName, panel.objectName()], endEmpty=True)
                                self.workBenchDict["newPanels"][workbenchName][panel.objectName()] = []
                            self.workBenchDict["newPanels"][workbenchName][panel.objectName()].append([ExtraCommand, ExtraCommand_WB])
                        
                        # Get the name from  current workbench
                        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
                        # Create a new panel with the extra command
                        newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict, UpdateDict=False, ignoreColumnLimit=True,showEnableControl=True, enableSeparator=True, ExtraCommand=ExtraCommand, ActivateButtons=True)
                                                
                        # Add the panel to the list with long panels
                        if newPanel is not None:
                            if newPanel.panelOptionButton().isVisible():
                                self.longPanels.append(newPanel)
                                                    
                            # Replace the panel with the new panel
                            self.currentCategory().replacePanel(panel, newPanel)
                            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
                            self.setPanelProperties(newPanel)
                            
                            # Update the dict of the currentCategory with the new panel
                            self.currentCategory()._panels[panel.objectName()] = newPanel

                            # Close the old panel and the dragindicator
                            panel.close()
                            
                            # Enable all buttons, so you can access them with a right click
                            self.activateButtons()
                            
                            event.accept()
                            return
            
            # Add buttons to the quickaccess toolbar
            if self.quickAccessToolBar().underMouse() is True:
                padding = 0
                # Get the command to be added
                commandName = widget.currentItem().data(Qt.ItemDataRole.UserRole)
                # Define a button
                button = None
                QuickAction = None
                # If it is a standard freecad button, set the command accordingly
                if commandName.endswith("_ddb") is False and "separator" not in commandName:
                    try:
                        # Check if the workbench is loaded. If not, actions will be an empty list
                        # Find the command its workbench and activate it
                        for CommandItem in self.List_Commands:
                            if CommandItem[0] == commandName and CommandItem[3] not in self.isWbLoaded:
                                Gui.activateWorkbench(CommandItem[3])
                                self.isWbLoaded[CommandItem[3]] = True
                                break
                    except Exception:
                        pass
                    QuickAction = Gui.Command.get(commandName).getAction()

                    if len(QuickAction) == 1:
                        button = self.CreateQuickButtonFromCommand(commandName)
                    elif len(QuickAction) > 1:
                        # set the padding for a dropdown button
                        padding = self.PaddingRight
                        button = self.CreateQuickButtonFromCommand(commandName, padding)

                # If it is a custom dropdown, add the actions one by one.
                if commandName.endswith("_ddb") is True and "separator" not in commandName:
                    # set the padding for a dropdown button
                    padding = self.PaddingRight
                    button = self.CreateQuickButtonFromCommand(commandName, padding)

                # Add the button to the quickaccess toolbar
                if button is not None:
                    self.addQuickAccessButton(button)
                
                # Add the command to the quickaccess command list
                self.workBenchDict["quickAccessCommands"].append(commandName)
                
                # Enable all buttons, so you can access them with a right click
                self.activateButtons()
                
                event.accept()
                return
         
        # Reorder buttons on panel by Drag        
        if type(widget) is not RibbonPanel and type(widget) is not QToolBar:
            # Get the panel
            panel = RibbonPanel()
            QuickAccessToolBar = QToolBar()
            count = 0
            parent = widget.parent()
            while (count < 10):
                if type(parent) is RibbonPanel:
                    panel = parent
                    break
                if type(parent) is QToolBar:
                    QuickAccessToolBar = parent
                    break
                else:
                    parent = parent.parent()
                count = count + 1
                
            # Get the gridlayout
            gridLayout: QGridLayout = panel._actionsLayout
            # Hide the dragIndicater and the spacer widgets
            self.dragIndicator_Buttons.hide()
            self.spaceWidget_Left.hide()
            self.spaceWidget_Right.hide()

            if type(parent) is RibbonPanel:
                replace = False
                if not widget.geometry().contains(event.pos()):   
                    # Get the workbench name and the panel name                  
                    title = panel.objectName()
                    workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
                        
                    # Get the coordinates of the drag location
                    xPos_drag = self.target[0]
                    yPos_drag = self.target[1]
                    # Define the original widget
                    OriginalItem = gridLayout.itemAtPosition(xPos_drag, yPos_drag)
                    OriginalWidget = OriginalItem.widget().findChild(CustomControls)
                    
                    # Get the old position of the dragged widget
                    n = 0
                    OldPos = []
                    widgetType = None
                    # Get the type of widget
                    widgetType = widget.parent().parent().findChild(CustomControls)
                    if type(widget) is CustomSeparator:
                        widgetType = widget
                    # If the widgetType is still None, exit
                    if widgetType is None:
                        return
                    
                    # Get the order list, if there isn't one, create it
                    StandardFunctions.add_keys_nested_dict(
                        self.workBenchDict,
                        [
                            "workbenches",
                            workbenchName,
                            "toolbars",
                            title,
                            "order"
                        ],
                    )
                    OrderList: list = self.workBenchDict["workbenches"][workbenchName]["toolbars"][title]["order"]

                    if type(widgetType) is CustomControls:
                        for n in range(gridLayout.count()):
                            if gridLayout.itemAt(n).widget().findChild(CustomControls) == widgetType:
                                OldPos = gridLayout.getItemPosition(n)
                                break
                            
                        # if counter and old position is not empty, Swap the widgets
                        if n > -1 and len(OldPos) > 0 :
                            # Define the dragged widgets
                            DraggedItem = gridLayout.itemAt(n)
                            DraggedWidget = DraggedItem.widget().findChild(CustomControls)

                            OrderList_Compare = []
                            for n in range(gridLayout.count()):
                                control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                                separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                                if control is not None and type(control) is CustomControls:
                                    OrderList_Compare.append(self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=control))
                                if separator is not None and type(separator) is CustomSeparator:
                                    OrderList_Compare.append(separator.objectName())
                            if OrderList != OrderList_Compare:
                                OrderList = OrderList_Compare
                            
                            # Get the indexes of the widgets
                            index_originalWidget = OrderList.index(self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=OriginalWidget)) # This is the location were will be dropped
                            if DraggedWidget is not None:
                                index_newWidget = OrderList.index(self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=DraggedWidget)) # This is the original location of the dragged widget                                                        
                                if replace is True:                                
                                    # Remove the command name of the original widget from the order list and
                                    # Add the command of the dragged widget in its place
                                    OrderList.pop(index_originalWidget)
                                    OrderList.insert(index_originalWidget, self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=DraggedWidget))
                                    # Remove the command name of the dragged widget from the order list and
                                    # Add the command of the original widget in its place
                                    OrderList.pop(index_newWidget)                                    
                                    OrderList.insert(index_newWidget, self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=OriginalWidget))
                                else:
                                    # Remove the dragged item from the list
                                    OrderList.pop(index_newWidget)
                                    # Inserted it at the new location
                                    OrderList.insert(index_originalWidget, self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=DraggedWidget))

                    if type(widgetType) is CustomSeparator:
                        for n in range(gridLayout.count()):
                            if gridLayout.itemAt(n).widget().findChild(CustomSeparator) == widgetType:
                                OldPos = gridLayout.getItemPosition(n)
                                break
                            
                        # if counter and old position is not empty, Swap the widgets
                        if n > -1 and len(OldPos) > 0 :
                            # Define the dragged widgets
                            DraggedItem = gridLayout.itemAt(n)
                            DraggedWidget = DraggedItem.widget().findChild(CustomSeparator)

                            OrderList_Compare = []
                            for n in range(gridLayout.count()):
                                control = gridLayout.itemAt(n).widget().findChild(CustomControls)
                                separator = gridLayout.itemAt(n).widget().findChild(CustomSeparator)
                                if control is not None and type(control) is CustomControls:
                                    OrderList_Compare.append(self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=control))
                                if separator is not None and type(separator) is CustomSeparator:
                                    OrderList_Compare.append(separator.objectName())
                            if OrderList != OrderList_Compare:
                                OrderList = OrderList_Compare
                            
                            # Get the indexes of the widgets
                            index_originalWidget = OrderList.index(self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=OriginalWidget)) # This is the location were will be dropped
                            if DraggedWidget is not None:
                                index_newWidget = OrderList.index(DraggedWidget.objectName()) # This is the original location of the dragged widget                        
                                if replace is True:                                
                                    # Remove the command name of the original widget from the order list and
                                    # Add the command of the dragged widget in its place
                                    OrderList.pop(index_originalWidget)
                                    OrderList.insert(index_originalWidget, DraggedWidget.objectName())
                                    # Remove the command name of the dragged widget from the order list and
                                    # Add the command of the original widget in its place
                                    OrderList.pop(index_newWidget)
                                    # OrderList.insert(index_newWidget, OriginalWidget.actions().data())
                                    OrderList.insert(index_newWidget, self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=OriginalWidget))
                                else:
                                    # Remove the dragged item from the list
                                    OrderList.pop(index_newWidget)
                                    # Inserted it at the new location
                                    OrderList.insert(index_originalWidget, DraggedWidget.objectName())
                                               
                    # Safe the order
                    self.workBenchDict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["order"] = OrderList     
                                                        
                    # Create a new panel
                    workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
                    newPanel = self.CreatePanel(workbenchName, panel.objectName(), addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True)
                                            
                    # Add the panel to the list with long panels
                    if newPanel.panelOptionButton().isVisible():
                        self.longPanels.append(newPanel)
                                            
                    # Replace the panel with the new panel
                    self.currentCategory().replacePanel(panel, newPanel)
                    # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
                    self.setPanelProperties(newPanel)
                    
                    # Update the dict of the currentCategory with the new panel
                    self.currentCategory()._panels[newPanel.objectName()] = newPanel
                    
                    # Close the old panel and the dragindicator
                    panel.close()
                    self.dragIndicator_Buttons.close()
                    
                    # Enable all buttons, so you can access them with a right click
                    self.activateButtons()
                    
                    event.accept()
                    return

            if QuickAccessToolBar.objectName() == "quickAccessToolBar":
                widget = event.source()
                
                # Use the action stored during the dragmove function
                beforeAction = self.dragAction_QuickAccess
                # insert the dragged widget
                QuickAccessToolBar.insertWidget(beforeAction, widget)

                # Update the orderlist
                #
                # Define the orderlist as the current list of quickaccess commands
                try:
                    OrderList = self.workBenchDict["quickAccessCommands"]
                    OrderList.remove(widget.objectName())
                    index = OrderList.index(beforeAction.objectName())
                    OrderList.insert(index, widget.objectName())

                    # Set the quickaccessCommands
                    self.workBenchDict["quickAccessCommands"] = OrderList
                    
                    # Delete the drag indicater
                    try:
                        QuickAccessToolBar.removeAction(self.dragAction_QuickAccess)
                        QuickAccessToolBar.removeAction(self.dragIndicator_QuickAccess)
                    except Exception:
                        pass
                except Exception:
                    try:
                        QuickAccessToolBar.removeAction(self.dragAction_QuickAccess)
                        QuickAccessToolBar.removeAction(self.dragIndicator_QuickAccess)
                    except Exception:
                        pass
                
            # Enable all buttons, so you can access them with a right click
            self.activateButtons()

            event.accept()
            return
        
        # Reorder panels by drag           
        if type(widget) is RibbonPanel:
            # Get the position (index, position)
            position = self.find_drop_location(event)

            # Create a new panel
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
            newPanel = self.CreatePanel(workbenchName, widget.objectName(), False, self.workBenchDict,  ignoreColumnLimit=True, showEnableControl=True, ActivateButtons=True)

            # Add the new panel
            self.currentCategory().insertWidget(newPanel,position[0])
            # For some reason, the font of the panel title will be reset after replacing a panel, set its properties again.
            self.setPanelProperties(newPanel)
            
            # Update the dict of the currentCategory with the new panel
            panels = {}
            for title, panel in self.currentCategory().panels().items():
                StandardFunctions.add_keys_nested_dict(panels, [title])
                if panel.objectName() == newPanel.objectName():
                    panels[title] = newPanel
                else:
                    panels[title] = panel
            self.currentCategory()._panels = panels
            
            # Close the current panel
            widget.close()

            # Create the current orderlist from the panels
            if "order" not in self.workBenchDict["workbenches"][workbenchName]["toolbars"]:
                StandardFunctions.add_keys_nested_dict(self.workBenchDict, ["workbenches", workbenchName, "toolbars", "order"], endEmpty=True)
                self.workBenchDict["workbenches"][workbenchName]["toolbars"]["order"] = []
            OrderList:list = self.workBenchDict["workbenches"][workbenchName]["toolbars"]["order"]
            # if a panel is not in the orderlist, add it
            for title, panel in self.currentCategory().panels().items():
                if panel.objectName() not in OrderList:
                    OrderList.append(panel.objectName())
            # if an item in the orderlist is not in the panel list, remove it from the order list
            for panelItem in OrderList:
                isInList = False
                for title, panel in self.currentCategory().panels().items():
                    if title == panelItem:
                        isInList = True
                if isInList is False:
                    OrderList.remove(panelItem)
            
            # Add the widget in the new place of the order list
            OrderIndex = position[0]
            if widget.objectName() in OrderList:
                OrderList.remove(widget.objectName())
            OrderList.insert(OrderIndex, widget.objectName())
            
            # Update the workbench dict
            self.workBenchDict["workbenches"][workbenchName]["toolbars"]["order"] = OrderList
            
            # Close the drag indicator
            self.dragIndicator_Panels.close()
                           
        event.accept()
        return


    def find_drop_location(self, event, panel=None):
        """
        Determines the drop location in a grid layout based on the position of a drag-and-drop event.
        Args:
            event (QEvent): The drag-and-drop event containing the position and source widget.
        Returns:
            list: A list containing the following elements:
                - Row
                - Column
                - Rowspan
                - Columnspan
        Notes:
            - The method calculates the grid position (row and column) by comparing the event's position
              with the global positions of widgets in the grid layout.
            - Assumes the parent widget has a `_actionsLayout` attribute that is a QGridLayout.
        """

        # Get the position as a point
        pos = event.pos()       
        # Get the widget
        widget = event.source()
        # Give the position an offset for a more natural drag
        pos.setX(pos.x() - (widget.width()/2))
        pos.setY(pos.y() - (widget.height()/2))
        
        if type(widget) is not RibbonPanel:
            # Get the panel
            if panel is None:
                panel = RibbonPanel()
                count = 0
                parent = widget.parent()
                while (count < 10):
                    if type(parent) is RibbonPanel:
                        panel = parent
                        break
                    else:
                        parent = parent.parent()
                    count = count + 1
            gridLayout: QGridLayout = panel._actionsLayout
            # Define the placeholders for x- and y-coordinates as grid positions
            xPos = 0
            yPos = 0

            # Get the column
            Column = 0
            for Column in range(gridLayout.columnCount()):
                item = gridLayout.itemAtPosition(0, Column)
                if item is not None:
                    w = item.widget()
                    if w is not None:
                        Widget_X = w.mapTo(self,w.pos()).x()

                        if w.mapTo(panel, pos).x() < Widget_X:
                            yPos = Column
                            break

            # Get the row
            Row = 0
            for Row in range(gridLayout.rowCount()):
                item = gridLayout.itemAtPosition(Row, Column)
                if item is not None:
                    w = item.widget()
                    if w is not None:
                        Widget_y = w.mapTo(self,w.pos()).y()

                        if w.mapTo(panel, pos).y() < Widget_y:
                            xPos = Row
                            break

            # Return then coordinates as grid positions
            w_origin = None
            try:
                w_origin = gridLayout.itemAtPosition(xPos, yPos).widget()
                widget = w_origin.children()[1]
                if widget.objectName() == "spacer":
                    return None
                index = gridLayout.indexOf(w_origin)
                position: object = gridLayout.getItemPosition(index)
                return [position[0], position[1], position[2], w_origin]
            except Exception as e:
                # raise e
                return None
        
        if type(widget) is RibbonPanel:
            layout = self.currentCategory()._categoryLayout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item is not None:
                    w= item.widget()
                    Widget_X = w.mapTo(self,w.pos()).x() 
                    # Widget_X = Widget_X + w.width() * 0.5
                    
                    if w.mapTo(self.currentCategory(), pos).x() < Widget_X:
                        return [i, Widget_X]
        return None
    # endregion
    
    # region - standard class functions
    #
    # implementation to add actions to the Filemenu. Needed for the accessories menu
    def addAction(self, action: QAction):
        menu = self.findChild(RibbonMenu, "Ribbon")
        StyleSheet_Menu = (
            "* {font-size: " + str(Parameters.FONTSIZE_MENUS) + "px;}"
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
            if Parameters.AUTOHIDE_RIBBON is False:
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
        
        if self.CustomizeEnabled:
            self.on_Customize_Clicked()
            # Activate all commands
            self.activateButtons()
        
        # Emit a signal when switching to a new tab. Used to update the "addcommands" panel
        self.TabChanged.emit()
        return

    def onWbActivated(self):        
        if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
            if Parameters.AUTOHIDE_RIBBON is False:
                self.UnfoldRibbon()
            # else:
            #     self.FoldRibbon(True)

        # Set the text color depending in tabstyle
        if Parameters.TABBAR_STYLE != 1:
            self.tabBar().setStyleSheet(
                "QTabBar::tab {color: "
                + StyleMapping_Ribbon.ReturnStyleItem("FontColor")
                + ";}"
                # + """ QToolTip {
                #     background-color: #FFFFE1;
                #     color: black;
                #     border: black solid 1px;
                #     border-radius: 2px;
                #     }"""
            )
        if Parameters.TABBAR_STYLE == 1:
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
        # Make sure that the tooltip has the correct color settings
        styleSheet = self.tabBar().styleSheet()
        self.tabBar().setStyleSheet(styleSheet + """\n QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }""")

        # ensure that workbench is already loaded
        workbench = Gui.activeWorkbench()
        if not hasattr(workbench, "__Workbench__"):
            # XXX for debugging purposes
            if Parameters.DEBUG_MODE is True:
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
        if self.CustomizeEnabled is False: 
            self.buildPanels()
        if self.CustomizeEnabled:
            self.buildPanels(Dict=self.workBenchDict, UpdateDict=False)
        
        # hide normal toolbars
        self.hideClassicToolbars()
        
        if self.CustomizeEnabled:
            self.on_Customize_Clicked()
            # If not activated, activate all buttons    
            self.activateButtons() 

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
                            
        if self.CustomizeEnabled:
            # If not activated, activate all buttons    
            self.activateButtons() 
        return

    def updateCurrentTab(self):
        currentWbIndex = self.tabBar().indexOf(Gui.activeWorkbench().MenuText)
        currentTabIndex = self.tabBar().currentIndex()

        if currentWbIndex != currentTabIndex:
            self.disconnectSignals()
            self.tabBar().setCurrentIndex(currentWbIndex)
            self.connectSignals()
        self.ApplicationMenus()
        
        if self.CustomizeEnabled:
            # If not activated, activate all buttons    
            self.activateButtons() 

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
        self.applicationOptionButton().setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        # Set the icon
        self.setApplicationIcon(Gui.getIcon("freecad"))
        # Set the styling of the button including padding
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

        # add quickaccess buttons        
        toolbarWidth = self.BuildQuickToolbar(self.ribbonStructure["quickAccessCommands"])

        self.quickAccessToolBar().show()
        # Set the height of the quickaccess toolbar
        self.quickAccessToolBar().setMinimumHeight(self.QuickAccessButtonSize)

        # Set the minimum width of the quickaccess toolbar.
        
        self.quickAccessToolBar().setMinimumWidth(self.applicationOptionButton().width() + toolbarWidth)
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
        font.setPixelSize(Parameters.FONTSIZE_TABS)
        self.tabBar().setFont(font)

        self.tabBar().setIconSize(QSize(self.TabBar_Size - 6, self.TabBar_Size - 6))
        self.tabBar().setStyleSheet(
            "margin: 0px;padding: 0px;height: " + str(self.TabBar_Size) + ";"
        )
        
        # Correct colors when no stylesheet is selected for FreeCAD.
        self.quickAccessToolBar().setStyleSheet(""" QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }"""
                )
        if Parameters.BUTTON_BACKGROUND_ENABLED is True:
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
        WorkbenchOrderedList: list = Parameters.TAB_ORDER.split(",")
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
        self.tabBar().setAcceptDrops(True)
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
                        if Parameters.TABBAR_STYLE <= 1:
                            # set tab icon
                            icon: QIcon = self.ReturnWorkbenchIcon(workbenchName)
                            self.tabBar().setTabIcon(len(self.categories()) - 1, icon)
                        if Parameters.TABBAR_STYLE == 2:
                            self.tabBar().setTabIcon(
                                len(self.categories()) - 1, QIcon()
                            )

                        # Set the tab data
                        self.tabBar().setTabData(
                            len(self.categories()) - 1, workbenchName
                        )
                        
                        Font = QFont()
                        Font.setPixelSize(Parameters.FONTSIZE_TABS)
                        self.tabBar().setFont(Font)

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
        if Parameters.TOOLBAR_POSITION == 0:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            spacer.setFixedWidth(10)
            if SearchBarWidth > 10:
                BeforeAction = self.rightToolBar().actions()[2]
            else:
                BeforeAction = self.rightToolBar().actions()[1]
            self.rightToolBar().insertWidget(BeforeAction, spacer)
        
        # Add an overlay toggle button if overlay is enabled
        if Parameters.USE_OVERLAY is True:
            OverlayButton = QToolButton()
            # OverlayButton.setIcon(QIcon(os.path.join(pathIcons, "Draft_Layer.svg")))
            OverlayButton.setIcon(mw.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
            OverlayButton.setToolTip(
                translate("FreeCAD Ribbon", "Toggle overlay ")
            )
            OverlayButton.setFixedSize(
                self.RightToolBarButtonSize, self.RightToolBarButtonSize
            )
            OverlayButton.clicked.connect(self.ToggleOverlay)
            # is now set to replace the pin button
            # self.rightToolBar().addWidget(OverlayButton)

        # add a settings button with menu
        SettingsMenu = QMenu()
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
        SettingsMenu.setToolTip(translate("FreeCAD Ribbon", "Preferences") + "...")
        StyleSheet_SettingsMenu = SettingsMenu.styleSheet()
        SettingsMenu.setStyleSheet(
            StyleSheet_SettingsMenu
                                   + """\n\nQToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }""")
        
        # add the settingsmenu to the right toolbar
        SettingsButton = QToolButton()   
        SettingsButton.setIcon(Gui.getIcon("Std_DlgParameter.svg"))     
        SettingsButton.setFixedSize(
            self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize
        )
        SettingsButton.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet(
                control="toolbutton", padding_right="12px"
            )
        )        
        SettingsButton.setMenu(SettingsMenu)
        SettingsButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.rightToolBar().addWidget(SettingsButton)

        # Set the helpbutton
        self.helpRibbonButton().setEnabled(True)
        self.helpRibbonButton().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.helpRibbonButton().setToolTip(translate("FreeCAD Ribbon", "Help") + "...")
        # Get the default help action from FreeCAD
        self.helpRibbonButton().setIcon(Gui.getIcon("help-browser"))
        self.helpRibbonButton().setMenu(self.HelpMenu)
        self.helpRibbonButton().setFixedSize(
            self.RightToolBarButtonSize + 12, self.RightToolBarButtonSize
        )
        self.helpRibbonButton().setStyleSheet(
            str(StyleMapping_Ribbon.ReturnStyleSheet(
                control="toolbutton", padding_right="12px"
            ))
            + """\n\nQToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }"""
        )   
        self.helpRibbonButton().setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup
        )        

        # if the FreeCAD titlebar is hidden,add close, minimize and maximize buttons
        padding = "5px"
        if Parameters.HIDE_TITLEBAR_FC is True:
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
            spacer.setFixedWidth(30)
            if Parameters.TOOLBAR_POSITION == 1:
                spacer.setFixedWidth(5)
            self.rightToolBar().addWidget(spacer)

            # Minimize button
            MinimzeButton = QToolButton()
            MinimzeButton.setStyleSheet(
                StyleMapping_Ribbon.ReturnStyleSheet(
                    control="toolbutton",
                    radius="2px",
                    padding_left=padding,
                    padding_top=padding,
                    padding_bottom=padding,
                    padding_right=padding,
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
                    padding_left=padding,
                    padding_top=padding,
                    padding_bottom=padding,
                    padding_right=padding,
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
                    padding_left=padding,
                    padding_top=padding,
                    padding_bottom=padding,
                    padding_right=padding,
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

        # Add a beta button when showing the settings menu. 
        # Otherwise the button will be removed when using the context menus for the buttons
        def LoadBetaButton():
            # Add a switch to enable beta functions            
            switch = ToggleAction(self, "Enable béta functions", Parameters.BETA_FUNCTIONS_ENABLED)
            switch.setFixedSize(40, 20)
            switch.setObjectName("bétaSwitch")
            toolTipText = (translate("FreeCAD Ribbon",
        """
        Enables the following experimental functions:
        - a new customisation enviroment. With this enviroment activated, the following customizations can be done per button:
            - Enable or disable text.
            - Set the button size.
            - Set the button type to:
                - Small  -> three rows of buttons, text on the right side.
                - Medium -> two rows of buttons, text on the right side.
                - Large -> One button row, text below the button.
            - Reorder the buttons by dragging. Currently only drag within their panels is supported.
            - Change the text of a button.
            - Add and remove separators.
            - Reorder panels by dragging.
            - Change the title of a panel.
            
            To start the customisation enviroment, right click on the ribbon (outside the buttons) and click customize.
            The customization enviroment is enabled and with a right click on a button, its properties can be changed.
            Right click on the ribbon agian to save and exit the customisation enviroment.
        """
        ))
            switch.setToolTip(toolTipText)
            switch.checkStateChanged.connect(
                lambda: self.on_ToggleBetaFunctions_toggled(switch.isChecked())
            )       
            
            if Parameters.BETA_FUNCTIONS_ENABLED is True:
                self.BetaFunctionsEnabled = True
                switch.setChecked(True)
            else:
                self.BetaFunctionsEnabled = False   
                switch.setChecked(False)            
            
            # if present remove the old switch
            for action in SettingsMenu.actions():
                if type(action) is ToggleAction:
                    SettingsMenu.removeAction(action)
            # Now added to the settings menu
            SettingsMenu.addAction(switch)
        # Connect the function to load the beta button
        SettingsMenu.aboutToShow.connect(LoadBetaButton)
        
        # Add a expanding spacer to the right toolbar
        BeforeAction = self.rightToolBar().actions()[2]     
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.rightToolBar().insertWidget(BeforeAction, spacer)
        
        # Set the width of the right toolbar
        RightToolbarWidth = (
            SearchBarWidth
            + 3 * (self.RightToolBarButtonSize + 16)
            # + self.RightToolBarButtonSize
        )
        # if Parameters.USE_FC_OVERLAY is True:
        #     RightToolbarWidth = SearchBarWidth + 2 * (self.RightToolBarButtonSize + 16)
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
                import StyleMapping_SearchBar

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
                StyleSheet = (
                        """background: """
                        + "white;"
                        + "color: black"
                        # + StyleMapping_SearchBar.ReturnStyleItem("Background_Color")
                        + """;"""
                    )
                sea.setStyleSheet(StyleSheet)
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
            "* {font-size: " + str(Parameters.FONTSIZE_MENUS) + "px;}"
            + """ QToolTip {
                    background-color: #FFFFE1;
                    color: black;
                    border: black solid 1px;
                    border-radius: 2px;
                    }"""
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
        
        # Add the repair menu
        RepairMenu: QMenu = RibbonMenu.addMenu(
            translate("FreeCAD Ribbon", "Repair functions...")
        )
        UpdateRibbonStructure = RepairMenu.addAction(translate("FreeCAD Ribbon", "Repair the Ribbon layout file"))
        UpdateRibbonStructure.triggered.connect(lambda: self.ConvertRibbonStructure(False))
        RestoreLayout = RepairMenu.addAction(translate("FreeCAD Ribbon", "Restore a Ribbon layout"))
        RestoreLayout.triggered.connect(self.RestoreJson)
        OpenBackupFolder = RepairMenu.addAction(translate("FreeCAD Ribbon", "Open the backup directory"))
        # If the backup folder doesn't exists, create it
        if os.path.exists(Parameters.BACKUP_LOCATION) is False:
            os.makedirs(Parameters.BACKUP_LOCATION)
        OpenBackupFolder.triggered.connect(lambda: StandardFunctions.OpenDirectory(Parameters.BACKUP_LOCATION))
        
        # Add the script submenu with items
        ScriptDir = os.path.join(ConfigDirectory, "Scripts")
        if os.path.exists(ScriptDir) is False:
            if os.path.exists(os.path.join(os.path.dirname(__file__), "Scripts")):
                shutil.copytree(os.path.join(os.path.dirname(__file__), "Scripts"), os.path.join(ConfigDirectory, "Scripts"))
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
                HelpIcon = Gui.getIcon("help-browser")
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
        DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
        if os.path.exists(DataFile) is False:
            Question = translate(
                "FreeCAD Ribbon",
                "a data file must be generated first!\n"
                "Do you want to create one now?\n",
            )
            Answer = StandardFunctions.Mbox(Question, "FreeCAD Ribbon", 1, "Question")
            if Answer == "yes":
                CacheFunctions.CreateCache()
                DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
            else:
                return
        
        if os.path.exists(DataFile) is True:            
            # Set the wait cursor
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
            
            # Get the form
            Dialog = LoadDesign_Ribbon.LoadDialog()
            if Parameters.DOCKED_DIALOGS is False:
                # Show the form
                Dialog.form.show()
            else:
                RibbonLayoutDock = QDockWidget()
                # set the name of the object and the window title
                RibbonLayoutDock.setObjectName("RibbonLayout")
                RibbonLayoutDock.setWindowTitle("Ribbon Layout")
                RibbonLayoutDock.setContentsMargins(0, 0, 0, 0)
                RibbonLayoutDock.setWidget(Dialog.form)
                # Set the allowed areas to dock
                RibbonLayoutDock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea|Qt.DockWidgetArea.RightDockWidgetArea)
                # Add the dockwidget
                mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, RibbonLayoutDock, Qt.Orientation.Horizontal)

            # Restore the cursor
            QApplication.restoreOverrideCursor()
        return

    # Function for loading the settings menu
    def loadSettingsMenu(self):
        # Set the wait cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        QApplication.processEvents(QEventLoop.ProcessEventsFlag.AllEvents)
        
        # Get the form
        Dialog = LoadSettings_Ribbon.LoadDialog()
        if Parameters.DOCKED_DIALOGS is False:
            # Show the form
            Dialog.form.show()
        else:
            RibbonLayoutDock = QDockWidget()
            # set the name of the object and the window title
            RibbonLayoutDock.setObjectName("RibbonSettings")
            RibbonLayoutDock.setWindowTitle("Ribbon Preferences")
            RibbonLayoutDock.setContentsMargins(0, 0, 0, 0)
            RibbonLayoutDock.setWidget(Dialog.form)
            # Set the allowed areas to dock
            RibbonLayoutDock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea|Qt.DockWidgetArea.RightDockWidgetArea)
            # Add the dockwidget
            mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, RibbonLayoutDock, Qt.Orientation.Horizontal)

        # indicate that the design menu is loaded
        self.DesignMenuLoaded = True

        # Restore the cursor
        QApplication.restoreOverrideCursor()
        return

    def buildPanels(self, Dict=ribbonStructure, UpdateDict=True):
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
            for ListItem in ListToolbars:
                if ListItem == CustomToolbar[0]:
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
            if workbenchName in Dict["customToolbars"]:
                for customPanel in Dict["customToolbars"][workbenchName]:
                    ListToolbars.append(customPanel)

                    # remove the original toolbars from the list
                    Commands = Dict["customToolbars"][workbenchName][
                        customPanel
                    ]["commands"]
                    for Command in Commands:
                        try:
                            OriginalToolbar = Dict["customToolbars"][workbenchName][customPanel]["commands"][Command]

                            # ignore cases to prevent issues with different versions of FreeCAD
                            for item in ListToolbars:
                                if OriginalToolbar.lower() == item.lower():
                                    OriginalToolbar = item

                            ListToolbars.remove(OriginalToolbar)
                        except Exception:
                            continue
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(f"{e}, 1", "Warning")
            pass

        # Add the new panels to the toolbar list
        try:
            for WorkBenchItem in Dict["newPanels"]:
                if WorkBenchItem == workbenchName or WorkBenchItem == "Global":
                    for Panel in Dict["newPanels"][WorkBenchItem]:
                        ListToolbars.append(Panel)
        except Exception:
            pass

        try:
            # Get the order of toolbars
            ToolbarOrder: list = Dict["workbenches"][workbenchName][
                "toolbars"
            ]["order"]

            # Sort the list of toolbars according the toolbar order
            def SortToolbars(toolbar):
                if toolbar == "":
                    return -1

                position = None
                try:
                    position = ToolbarOrder.index(toolbar)
                except ValueError as e:
                    position = 999999
                    if toolbar.endswith("_custom") or toolbar.endswith("_newPanel"):
                        if Parameters.DEFAULT_PANEL_POSITION_CUSTOM == "Right":
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
            for ToolbarToIgnore in Dict["ignoredToolbars"]:
                if toolbar.lower() == ToolbarToIgnore.lower():
                    Skip = True
            if toolbar == "" or Skip is True:
                continue
            if toolbar in self.currentCategory().panels().keys():
                continue
            
            # Create the panel based on the toolbars
            panel = self.CreatePanel(workbenchName=workbenchName, panelName=toolbar, addPanel=True, Dict=Dict, UpdateDict=UpdateDict)
            if panel is None:
                continue
            # Hide the panel if stated in the ribbon structure
            if workbenchName in Dict["workbenches"]:
                if panel.objectName() in Dict["workbenches"][workbenchName]["toolbars"]:
                    if "Enabled" in Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]:
                        Enabled = Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["Enabled"]
                        if Enabled is False:
                            self.HiddenPanels.append(panel)
                            panel.hide()
                                   
            # Writing to ribbonStructure.json
            if UpdateDict is True:
                JsonFile = Parameters.RIBBON_STRUCTURE_JSON
                with open(JsonFile, "w") as outfile:
                    json.dump(Dict, outfile, indent=4)
                outfile.close()

        self.isWbLoaded[tabName] = True
        
        # Correct the height of each panel
        for objPanel in self.currentCategory().panels().values():
            self.setPanelProperties(objPanel)

        # Set the previous/next buttons
        category: RibbonCategory = self.currentCategory()
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
        # ScrollLeftButton_Category.setFixedHeight(Parameters.ICON_SIZE_SMALL * 3)
        # ScrollRightButton_Category.setFixedHeight(Parameters.ICON_SIZE_SMALL * 3)
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
        category.setMinimumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        category.setMaximumHeight(
            self.RibbonHeight - self.RibbonMinimalHeight - 3
        )
        # self.setRibbonHeight(self.RibbonHeight)

        if self.DesignMenuLoaded is True:
            # Disable the quick toolbar, righttoolbar and application menu
            self.rightToolBar().setDisabled(True)
            self.quickAccessToolBar().setDisabled(True)
            self.applicationOptionButton().setDisabled(True)
            Gui.updateGui()
        
        # # Add a Floating button to the current tab in the right bottom corner
        layout: QGridLayout = self.currentCategory()._mainLayout   
        # Set the pinbutton when overlay is disabled        
        pinButton = self.CreatePinButton()
        layout.addWidget(pinButton, 3,3,1,1, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
        # Add the pinButton to a list with all pinbuttons. Needed to set all pin buttons to the same state
        self.pinButtonList.append(pinButton)
        if Parameters.USE_OVERLAY is True: 
             pinButton.setIcon(QIcon())   
             pinButton.setDisabled(True)
             pinButton.setHidden(True)    

        if self.CustomizeEnabled:
            # If not activated, activate all buttons    
            self.activateButtons() 

        return
    
    def CreatePinButton(self):
        # Add a button to enable or disable AutoHide
        pinButton = QToolButton()
        pinButton.setCheckable(True)
        pinButton.setObjectName("pinButton")
        pinButton.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        pinButton.setFixedSize(QSize(self.iconSize * 0.6,self.iconSize * 0.6))
        
        # Set the correct icon
        if Parameters.AUTOHIDE_RIBBON is False:
            pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_open"))
        else:
            pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_closed"))
            
        # Connect the pinbutton with its function
        pinButton.clicked.connect(lambda: self.on_Pin_clicked(pinButton))
        
        # Set the text and objectname
        pinButton.setText(translate("FreeCAD Ribbon", "Pin Ribbon"))
        pinButton.setObjectName("pinButton")
        
        # Set the correct checkstate
        if Parameters.AUTOHIDE_RIBBON is True:
            pinButton.setChecked(False)
        if Parameters.AUTOHIDE_RIBBON is False:
            pinButton.setChecked(True)
        pinButton.setStyleSheet(
            StyleMapping_Ribbon.ReturnStyleSheet("toolbutton", "2px")
        )
        
        ShortcutKey = ""
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
        pinButton.setToolTip(translate("FreeCAD Ribbon", "Click to toggle the autohide function on or off"))
        # If there is a shortcut key assinged, update the tooltip
        if ShortcutKey != "none" or ShortcutKey != "":
            pinButton.setToolTip(
                translate(
                    "FreeCAD Ribbon",
                    "Click to toggle the autohide function on or off"
                    + f"<br></br><i>{ShortcutKey}</i>",
                )
            )
                        
        # Store the pinbutton globally
        self.pinButton = pinButton
        
        return pinButton

    # endregion

    # region - Control functions
    def on_AboutButton_clicked(self):
        LoadLicenseForm_Ribbon.main()
        return

    def on_Help_clicked(self):
        self.helpRibbonButton().showMenu()

    def on_RibbonHelpButton_clicked(self):        
        if self.HelpAdress != "" or self.HelpAdress is not None:
            if not self.HelpAdress.endswith("/"):
                self.HelpAdress = self.HelpAdress + "/"

            webbrowser.open(self.HelpAdress, new=2, autoraise=True)
        return

    def on_WhatsNewButton_clicked(self):
        if self.HelpAdress != "" or self.HelpAdress is not None:
            if not self.HelpAdress.endswith("/"):
                self.HelpAdress = self.HelpAdress + "/"

            Adress = self.HelpAdress + """06-%E2%80%90-Change-log"""
            webbrowser.open(Adress, new=2, autoraise=True)
        return

    def on_Pin_clicked(self, pinButton = None):
        if Parameters.USE_OVERLAY is False:
            if pinButton is None:
                pinButton = self.currentCategory().findChildren(QToolButton, "pinButton")[0]
            
            if Parameters.AUTOHIDE_RIBBON is False:
                Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", True)
                Parameters.AUTOHIDE_RIBBON = True

                pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_closed"))
                # Set the pin button for all tabs
                for btn in self.pinButtonList:
                    btn.setChecked(False)
                    btn.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_closed"))

                self.FoldRibbon()
                return
            if Parameters.AUTOHIDE_RIBBON is True:
                self.UnfoldRibbon()

                Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", False)
                Parameters.AUTOHIDE_RIBBON = False

                pinButton.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_open"))
                # Set the pin button for all tabs
                for btn in self.pinButtonList:
                    btn.setChecked(True)
                    btn.setIcon(StyleMapping_Ribbon.ReturnStyleItem("PinButton_open"))

                # Make sure that the ribbon remains visible
                self.setRibbonVisible(True)
                return
        return

    def on_ApplicationButton_toggled(self):
        self.applicationOptionButton().showMenu()

    def on_ScrollButton_Category_clicked(
        self, event, ScrollButton: RibbonCategoryLayoutButton
    ):
        for i in range(Parameters.RIBBON_CLICKSPEED):
            ScrollButton.click()
        return

    def on_ToggleBetaFunctions_toggled(self, switchStatus):
        # Store the status
        self.BetaFunctionsEnabled = switchStatus
        if switchStatus is True:
            # Write the parameter
            Parameters_Ribbon.Settings.SetBoolSetting("BetaFunctions", True)
            # print a message
            print(translate("FreeCAD Ribbon", "Ribbon UI: Béta functions enabled"))
            Parameters.BETA_FUNCTIONS_ENABLED = True
            
            # Create a backup
            #
            # get the path for the Json file
            JsonFile = Parameters.RIBBON_STRUCTURE_JSON
            # Create a suffix with the date
            Suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Create a backup name
            BackupName = f"RibbonStructure_{Suffix}.json"
            # If the backup folder doesn't exists, create it
            if os.path.exists(pathBackup) is False:
                os.makedirs(pathBackup)
            BackupFile = os.path.join(pathBackup, BackupName)
            # Copy the file
            shutil.copy(JsonFile, BackupFile)
        if switchStatus is False:
            # Write the parameter
            Parameters_Ribbon.Settings.SetBoolSetting("BetaFunctions", False)
            # print a message
            print(translate("FreeCAD Ribbon", "Ribbon UI: Béta functions disabled"))
            Parameters.BETA_FUNCTIONS_ENABLED = False
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
                # TB.setFixedHeight(self.RibbonHeight)
                if TB.isFloating():
                    if self.RibbonHeight > 0:
                        TB.setFixedHeight(self.RibbonHeight + self.FloatingTitleBarHeight)
                if TB.isFloating() is False:
                    if self.RibbonHeight > 0:
                        TB.setFixedHeight(self.RibbonHeight)              
        return

    def FoldRibbon(self, Ignore=False):
        if (
            Parameters.AUTOHIDE_RIBBON is True
            and self.isLoaded is True
            and Ignore is False
        ):
            if len(mw.findChildren(QDockWidget, "Ribbon")) > 0:
                TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
                if TB.isFloating():
                    TB.setMinimumHeight(self.RibbonMinimalHeight+self.FloatingTitleBarHeight)
                    TB.setMaximumHeight(self.RibbonMinimalHeight+self.FloatingTitleBarHeight)
                if TB.isFloating() is False:
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

    def List_AddCustomToolBarToWorkbench(self, workbenchName, CustomToolbar, Dict = None):
        ButtonList = []
        
        if Dict is None:
            Dict = self.ribbonStructure["customToolbars"]
            
        # Get the commands from the custom panel
        if workbenchName in Dict:
            for toolbar in Dict[workbenchName]:
                if CustomToolbar.lower() == toolbar.lower():
                    Commands = Dict[workbenchName][
                        toolbar
                    ]["commands"]

                    # Create a QToolButton from the key and add it to the button list
                    allButtons: list = []
                    for key, value in list(Commands.items()):
                        # Get the buttons with two ways, to be sure that all buttons are present
                        #
                        # 1. Get the buttons from the mainWindow. This way you will get dropdown like "electro magnetic boundarys from the FEM wob"
                        # Get the toolbar from the mainwindow
                        try:
                            TB = mw.findChildren(QToolBar, value)
                            allButtons = TB[0].findChildren(QToolButton)
                            # remove empty buttons
                            for i in range(len(allButtons)):
                                button: QToolButton = allButtons[i]
                                if allButtons[i].text() == "":
                                    allButtons.pop(i)
                        except Exception:
                            pass
                        # Find the matching button and add it the the button list
                        for i in range(len(allButtons)):
                            button: QToolButton = allButtons[i]
                            if button.defaultAction().data() == key:
                                ButtonList.append(button)

                        # 2. Get the command and create a button from it
                        try:
                            # Get the command
                            Command = Gui.Command.get(key)
                            if Command is not None:
                                Icon = Gui.getIcon(
                                    CommandInfoCorrections(key)[
                                        "pixmap"
                                    ]
                                )
                                action = Command.getAction()
                                Button = QToolButton()                                
                                Button.addActions(action)
                                Button.setDefaultAction(action[0])
                                Button.setIcon(Icon)
                                Button.setText(CommandInfoCorrections(key)[
                                        "menuText"
                                    ])
                                # Store the commmandName as a property
                                Button.setProperty("CommandName", key)
                                # Set the commandName as objectName as backup
                                Button.setObjectName(key)
                                try:
                                    if len(action) > 1:
                                        Icon = action[0].icon()
                                        menu = QMenu(self)
                                        menu.addActions(action)
                                        Button.setMenu(menu)
                                except Exception:
                                    pass
                                # Add the button to the button list
                                ButtonList.append(Button)
                        except Exception as e:
                            if Parameters.DEBUG_MODE is True:
                                StandardFunctions.Print(
                                    f"{e.with_traceback(e.__traceback__)}, 3",
                                    "Warning",
                                )
                            continue
        return ButtonList

    # To be removed
    def List_AddNewPanelToWorkbench(self, WorkBenchName, NewPanel, dict=ribbonStructure):
        ButtonList = []

        try:
            if WorkBenchName in dict["newPanels"]:
                if NewPanel in dict["newPanels"][WorkBenchName]:
                    # Get the commands from the custom panel
                    Commands = dict["newPanels"][WorkBenchName][
                        NewPanel
                    ]
                    
                    # Get the command and its original toolbar
                    for CommandItem in Commands:
                        CommandName = CommandItem[0]
                        # Define a new toolbutton
                        # NewToolbutton = RibbonToolButton()
                        NewToolbutton = QToolButton()
                        if CommandName.endswith("_ddb") is False:
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
                            CommandActionList = self.returnCustomDropDown(CommandName, dict=self.workBenchDict)
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
                                            if action[0] is not None:
                                                menu.addAction(action[0])
                                    NewToolbutton.setMenu(menu)
                                    NewToolbutton.setDefaultAction(CommandActionList[0][0])

                                    # Do something with the menu. For some reason it will not be loaded otherwise
                                    len(NewToolbutton.menu().actions())
                                    
                                # Add the commandname as the objectname to detect if it is a dropdownbutton
                                NewToolbutton.setObjectName(CommandName)
                                NewToolbutton.setToolTip(CommandName)

                                # Set the text for the toolbutton
                                NewToolbutton.setText(CommandName)

                                # add it to the list
                                ButtonList.append(NewToolbutton)

        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}, 4", "Warning"
                )
            pass
        return ButtonList

    def CreateButtonFromCommand(self, CommandName: str, ActivateWorkBench = True):
        try:            
            # Activate the workbench, the command belongs to. Otherwise, the command wont be created later
            # Get the current category
            currentCategory = self.currentCategory()
            if ActivateWorkBench is True:
                for CommandItem in self.List_Commands:
                    if CommandItem[0] == CommandName:
                        if (CommandItem[3] != "General" and CommandItem[3] != "Global" and CommandItem[3] != "Standard" and CommandItem[3] != ""):                                
                            if CommandItem[3] not in self.isWbLoaded:
                                # Activate the workbench if not loaded
                                Gui.activateWorkbench(CommandItem[3])
                                self.isWbLoaded[CommandItem[3]] = True
                            if CommandItem[3] in self.isWbLoaded and self.isWbLoaded[CommandItem[3]] is False:    
                                # Activate the workbench if not loaded
                                Gui.activateWorkbench(CommandItem[3])
                                self.isWbLoaded[CommandItem[3]] = True
                                break
            # Set the current  category after activating the workbench
            self.setCurrentCategory(currentCategory)
            Gui.activateWorkbench(currentCategory.objectName())
            
            # Enable all buttons, so you can access them with a right click
            self.actionList = []
            # Activate all commands
            self.activateButtons()
   
            # Get the command
            Command = Gui.Command.get(CommandName)
            action = None            
            Icon = QIcon()
            if Command is not None:
                FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                for root, dirs, files in os.walk(FreeCAD_Icons):
                    for fileName in files:
                        if CommandName in fileName:
                            Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                if Icon is not None and Icon.isNull():
                    Icon = Gui.getIcon(
                        CommandInfoCorrections(CommandName)[
                            "pixmap"
                        ]
                    )
                if Icon is not None and Icon.isNull():
                    Icon = self.ReturnCommandIcon(CommandName)
                    
                action = Command.getAction()
                Button = QToolButton()                                
                try:
                    if len(action) > 1:
                        Icon = action[0].icon()  
                except Exception:
                    pass

                if type(action) is list and len(action) > 1:
                    # Button.addActions(action)
                    Button.setDefaultAction(action[0])
                    menu = QMenu()
                    menu.addActions(action)
                    Button.setMenu(menu)
                    # For some reason, the line below, activates the menus.
                    # Otherwise the button wont be an dropdown button.
                    Button.menu()
                if type(action) is QAction or (type(action) is list and len(action) == 1):
                    if isinstance(action, list):
                        Button.addAction(action[0])
                        Button.setDefaultAction(action[0])
                    if isinstance(action, QAction):
                        Button.addAction(action)
                        Button.setDefaultAction(action)
                # if there is no action or an empty action, create a new one
                if action is None or (type(action) is list and len(action) == 0):
                    # Create the action and use the runCommand from FC
                    action = QAction(mw)
                    action.setText(CommandInfoCorrections(CommandName)["menuText"])
                    action.setObjectName(CommandName)
                    action.triggered.connect(lambda: self.RunCommand(action.objectName()))
                    # Add the action to the button
                    Button.addAction(action)
                    Button.setDefaultAction(action)
                if action is None:
                    print(f"{CommandName} has no action!")
                        
                if Icon is not None and Icon.isNull():
                    Button.setIcon(Icon)
                Button.setText(CommandInfoCorrections(CommandName)[
                        "menuText"
                    ])
                if Button.text() == "":
                    Button.setText(CommandName)
                Button.setToolTip(CommandName)
                # Set the commandName as objectName as backup
                Button.setObjectName(CommandName)
                
                return Button

            # If the command is None, it is probally a command from a FreeCAD dropdow button.
            # Try to get its QAction and create a button from it.
            # The commands needs to have either the name or title of its workbench in it
            if Command is None:
                # Get the workbence
                WorkBenchName = ""
                for item in Gui.listWorkbenches():
                    if CommandName.split("_")[0] in item:
                        WorkBenchName = item
                
                # If you have a workbench name, continue
                if WorkBenchName != "":
                    # get the workbench
                    wb = Gui.getWorkbench(WorkBenchName)

                    # If you heve the workbench, continue
                    if wb is not None:
                        # Get the toolbars with their commands from the workbench
                        dictCommands: dict = wb.getToolbarItems()
                        # Go through the toolbar commands              
                        for Toolbar, ToolbarCommands in dictCommands.items():
                            for ToolbarCommand in ToolbarCommands:
                                # Get the actual command
                                command = Gui.Command.get(ToolbarCommand)
                                if command is not None:
                                    # If the command has more actions, it is a dropdown button
                                    if len(command.getAction()) > 1:
                                        # Go through its child buttons and get the action
                                        for i in range(len(command.getAction()) - 1):
                                            action = command.getAction()[i]
                                            # If the action is not empty, and the objectname maches the commandName
                                            # Create a button with this action and return it
                                            if action is not None and (action.icon() is not None and not action.icon().isNull()):
                                                if action.objectName() == CommandName:
                                                    Button = QToolButton()
                                                    if isinstance(action, list):
                                                        Button.addAction(action[0])
                                                        Button.setDefaultAction(action[0])
                                                    if isinstance(action, QAction):
                                                        Button.addAction(action)
                                                        Button.setDefaultAction(action)

                                                    return Button
                
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}, 3",
                    "Warning",
                )
            return None

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
            else:
                action = Gui.Command.get(CommandName).getAction()
                if isinstance(action, list):
                    return action
                if isinstance(action, QAction):
                    return [action]
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
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
        # Get the name of the current workbench
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        
        # Set the ribbon height.
        ribbonHeight = 0
        
        # If text is enabled for large button, the height is modified.
        LargeButtonHeight = Parameters.ICON_SIZE_LARGE
        
        # Check whichs is has the most height: 3 small buttons, 2 medium buttons or 1 large button
        # and set the height accordingly
        #
        if self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] == 3:
            if (
                Parameters.ICON_SIZE_SMALL * 3
                >= Parameters.ICON_SIZE_MEDIUM * 2
                and Parameters.ICON_SIZE_SMALL * 3 >= LargeButtonHeight
            ):
                ribbonHeight = Parameters.ICON_SIZE_SMALL * 3 + self.ButtonSpacing*2
            if (
                (Parameters.ICON_SIZE_MEDIUM * 2
                > Parameters.ICON_SIZE_SMALL * 3
                and Parameters.ICON_SIZE_MEDIUM * 2 > LargeButtonHeight)
            ):
                ribbonHeight = Parameters.ICON_SIZE_MEDIUM * 2 + self.ButtonSpacing
            if (
                Parameters.ICON_SIZE_LARGE > Parameters.ICON_SIZE_SMALL * 3
                and Parameters.ICON_SIZE_LARGE > Parameters.ICON_SIZE_MEDIUM * 2
            ):
                ribbonHeight = LargeButtonHeight
        
        # If there only medium or large buttons
        if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  == 2 and self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] == 0 and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 3:
            if Parameters.ICON_SIZE_SMALL * 2 < Parameters.ICON_SIZE_MEDIUM or self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 2:
                ribbonHeight = Parameters.ICON_SIZE_MEDIUM * 2 + self.ButtonSpacing
            if Parameters.ICON_SIZE_SMALL * 2 > Parameters.ICON_SIZE_MEDIUM and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] == 2:
                ribbonHeight = Parameters.ICON_SIZE_SMALL * 2 + self.ButtonSpacing
        
        # If there are only large buttons
        if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  <= 2 and self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] == 1 and self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] < 3:
            if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"] < 2:
                ribbonHeight = LargeButtonHeight
            if self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"] == 2:
                if Parameters.ICON_SIZE_MEDIUM * 2 > LargeButtonHeight:
                    ribbonHeight = Parameters.ICON_SIZE_MEDIUM * 2 + self.ButtonSpacing
                if Parameters.ICON_SIZE_MEDIUM * 2 <= LargeButtonHeight:
                    ribbonHeight = LargeButtonHeight

        # return ribbonHeight + offset + Parameters.RIBBON_HEIGHT_OFFSET
        return ribbonHeight + offset

    def ReturnCommandIcon(self, CommandName: str, pixmap: str = "") -> QIcon:
        """_summary_

        Args:
            CommandName (str): Name of the command
            pixmap (str, optional): Add a pixmap as backup. Defaults to "".

        Returns:
            QIcon: the command icon.
        """
        # Get the standard pixmap, if a pixmap is not provided
        if pixmap == "":
            pixmap = StandardFunctions.CommandInfoCorrections(CommandName)["pixmap"]
        # Define an empty icon
        Icon = QIcon()
        # Try to get the icon from file
        if Icon is None or (Icon is not None and Icon.isNull()):
            FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
            for root, dirs, files in os.walk(FreeCAD_Icons):
                for fileName in files:
                    if CommandName in fileName:
                        Icon = QIcon()
                        Icon.addPixmap(QPixmap(os.path.join(root, fileName)))

                    if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.ribbonStructure):
                        for (DropDownCommand,Commands) in self.ribbonStructure["dropdownButtons"].items():
                            for CommandItem in self.List_Commands:
                                if Commands[0][0] == CommandItem[0]:
                                    pixmap = StandardFunctions.CommandInfoCorrections(CommandItem[0])["pixmap"]
                                    Icon = StandardFunctions.returnQiCons_Commands(CommandItem[0], pixmap)

        # If the icon is still empty, try to get it from FreeCAD. This will only work with loaded workbenches.
        # Therefore this is the last resort
        if Icon is None or (Icon is not None and Icon.isNull()):
            Icon = StandardFunctions.returnQiCons_Commands(CommandName, pixmap)
            if (str(CommandName).endswith("_ddb") and "dropdownButtons" in self.ribbonStructure):
                    for (DropDownCommand,Commands) in self.ribbonStructure["dropdownButtons"].items():
                        for CommandItem in self.List_Commands:
                            if Commands[0][0] == CommandItem[0]:
                                pixmap = StandardFunctions.CommandInfoCorrections(CommandItem[0])["pixmap"]
                                Icon = StandardFunctions.returnQiCons_Commands(CommandItem[0], pixmap)

        if Icon is None or (Icon is not None and Icon.isNull()):
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"An icon retrieved from data file for '{CommandName}'"
                )
            DataFile = os.path.join(
                ConfigDirectory, "RibbonDataFile.dat"
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
                        if CommandName == IconItem[0]:
                            Icon: QIcon = (
                                Serialize_Ribbon.deserializeIcon(
                                    IconItem[1]
                                )
                            )
                            # Add the icons to open the dialog faster a second time
                            item = [IconItem[0], Icon]
                            
                            return Icon
                except Exception as e:
                    if Parameters.DEBUG_MODE is True:
                        StandardFunctions.Print(
                            f"Trying the get an icon for {CommandName}\n{e}",
                            "Warning",
                        )
                    pass
        if Icon is None or (Icon is not None and Icon.isNull()):
            Icon = None
        return Icon

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
        try:
            if Parameters.DEBUG_MODE is True:
                print(f"{Command} has no action and was run from console!")
            Gui.runCommand(Command)
        except Exception:
            pass
        return

    def on_DockWidget_Toggled(self):
        # Get the DockWidget for the ribbon
        ribbonDock = mw.findChild(QDockWidget, "Ribbon")

        if ribbonDock.isFloating():
            # If the DockWidget is floating, dock it
            ribbonDock.setFloating(False)
            # Set an empty titlebar widget. Effectivly hide the titlebar
            ribbonDock.setTitleBarWidget(QWidget())
            # Correct the height of the ribbon
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight)
            return
        
        if ribbonDock.isFloating() is False:
            # If the DockWidget is docked, set it floating
            ribbonDock.setFloating(True)
            
            # Increase the ribbon height
            TB: QDockWidget = mw.findChildren(QDockWidget, "Ribbon")[0]
            if self.RibbonHeight > 0:
                TB.setFixedHeight(self.RibbonHeight + self.FloatingTitleBarHeight)
            # Set a label with title as titlebar widget. This works on all OS
            try:
                ribbonDock.setTitleBarWidget(QLabel("Ribbon", alignment=Qt.AlignmentFlag.AlignCenter))
            except Exception:
                pass
            
                                    
            # Position the dialog in front of FreeCAD
            centerPoint = mw.geometry().center()
            Rectangle = ribbonDock.frameGeometry()
            Rectangle.moveCenter(centerPoint)
            ribbonDock.move(Rectangle.topLeft())
            return
        
    def ToggleOverlay(self):                
        # Get the parameter group
        OverlayParam_Top = App.ParamGet(
            "User parameter:BaseApp/MainWindow/DockWindows/OverlayTop"
        )

        if self.OverlayToggled_Top is False:
            # Create a new string without "Ribbon"       
            newString = OverlayParam_Top.GetString("Widgets").replace("Ribbon,", "")
            # Set the new string in parameters
            OverlayParam_Top.SetString("Widgets",newString)
            App.saveParameter()
            self.OverlayToggled_Top = True
            return True
            
        if self.OverlayToggled_Top is True: 
            # Get the current string, if Ribbon is not in it, add it
            newString = OverlayParam_Top.GetString("Widgets")
            if "Ribbon" not in newString:
                newString = "Ribbon," + newString
                OverlayParam_Top.SetString("Widgets",newString)
            App.saveParameter()
            self.OverlayToggled_Top = False
            return True
        return False

    def returnCustomDropDown(self, CommandName, dict = ribbonStructure):
        actionList = []

        try:
            for DropDownCommand, Commands in dict["dropdownButtons"].items():
                if CommandName == DropDownCommand:
                    for CommandItem in Commands:
                        Command = Gui.Command.get(CommandItem[0])
                        if Command is not None:
                            action = Command.getAction()
                            if action is not None:
                                actionList.append(action)
            return actionList
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                StandardFunctions.Print(
                    f"{e.with_traceback(e.__traceback__)}", "Warning"
                )
            return []

    def CheckLanguage(self):
        FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
        if "language" in self.ribbonStructure:
            if self.ribbonStructure["language"] != FreeCAD_preferences.GetString(
                "Language") and FreeCAD_preferences.GetString(
                "Language") != "":
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

        # Get the current data from the ribbonstructure
        CommandName = ""
        if type(ButtonWidget.parent()) is CustomControls:
            CommandName = ButtonWidget.parent().objectName()
        else:
            for child in ButtonWidget.children():
                if (
                    type(child) == QToolButton
                    and child.objectName() == "CommandButton"
                ):
                    CommandName = child.defaultAction().data()
                    if CommandName == "" or CommandName is None:
                        if isinstance(child.actions(), list):
                            CommandName = child.actions()[0].objectName()
                        if isinstance(child.actions(), QAction):
                            CommandName = child.actions().data()

        if CommandName != "" and CommandName is not None:        
            for key, value in property.items():
                StandardFunctions.add_keys_nested_dict(
                    self.workBenchDict,
                    [
                        "workbenches",
                        WorkBenchName,
                        "toolbars",
                        panel.objectName(),
                        "commands",
                        CommandName,
                        key,
                    ],
                    endEmpty=True
                )
                self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][panel.objectName()]["commands"][CommandName][key] = value       
        return
                      
    def ReturnPanelTitle(self, panel: RibbonPanel, dict = ribbonStructure, filterOnly = False):
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        panelName = panel.objectName()
        # Get the workbenchTitle
        index = None
        for i in range(len(self.tabBar().tabTitles())):
            name = self.tabBar().tabData(i)
            if name == workbenchName:
                index = i
                break
        workbenchTitle = self.tabBar().tabText(index)
        title = StandardFunctions.TranslationsMapping(workbenchName, panelName)
        
        if filterOnly is False:
            if "workbenches" in dict:
                if workbenchName in dict["workbenches"]:
                    if "toolbars" in dict["workbenches"][workbenchName]:
                        if panelName in dict["workbenches"][workbenchName]["toolbars"]:
                            if "title" in dict["workbenches"][workbenchName]["toolbars"][panelName]:
                                if dict["workbenches"][workbenchName]["toolbars"][panelName]["title"] != "":
                                    return dict["workbenches"][workbenchName]["toolbars"][panelName]["title"]
        # Change the name of the view panels to "View"
        if (
            title in "Views - Ribbon_newPanel"
            or title.lower() in str("Individual views").lower()
        ):
            panel.setTitle(" Views ")
        else:
            # Remove possible workbench names from the titles
            if (
                "_custom" not in title
                and "_global" not in title
                and "_newPanel" not in title
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
                    if Name in title and Name != title:                        
                        title = title.replace(Name, "")
                    if title[:1] == " ":
                        title = title[1:]
        # remove any suffix from the panel title
        if title.endswith("_custom"):
            title = title.replace("_custom", "")
        if title.endswith("_global"):
            title = title.replace("_global", "")
        if title.endswith("_newPanel"):
            title = title.replace("_newPanel", "")
        
        # remove spaces from start and end
        title = title.lstrip().rstrip()
        return title
    
    def CreatePanel(self, 
                    workbenchName: str, 
                    panelName: str, 
                    addPanel = True, 
                    Dict = ribbonStructure, 
                    UpdateDict = False, 
                    ignoreColumnLimit = False, 
                    showEnableControl = False, 
                    enableSeparator = False, 
                    ExtraCommand = "",
                    ActivateButtons = False,
                    ActivateWorkbench = True,
                    ):

        if UpdateDict is True:
            Standard_Functions_Ribbon.add_keys_nested_dict(Dict, ["workbenches", workbenchName, "toolbars"], 1, True)
               
        # Create the panel, use the toolbar name as title
        title = StandardFunctions.TranslationsMapping(workbenchName, panelName)
        panel = RibbonPanel(title=title, showPanelOptionButton=True)
        if addPanel is True:
            panel: RibbonPanel = self.currentCategory().addPanel(
                title=title,
                showPanelOptionButton=True,
            )
            # Update the dict of the currentCategory with the new panel
            self.currentCategory()._panels[title] = panel
        panel.setObjectName(panelName)
        panel.panelOptionButton().hide()
        panel.setAcceptDrops(True)
        
        # Add a drag function to the panel
        def mouseMoveEvent(self, e, customizeEnabled: bool):
            if e.buttons() == Qt.MouseButton.LeftButton and customizeEnabled is True:
                try:
                    drag = QDrag(self)
                    mime = QMimeData()
                    drag.setMimeData(mime)
                    pixmap = QPixmap(self.size())
                    self.render(pixmap)
                    drag.setPixmap(pixmap)
                    try:

                        drag.exec(Qt.DropAction.MoveAction)
                    except Exception:
                        drag.exec_(Qt.MoveAction)
                except Exception as e:
                    if Parameters.DEBUG_MODE is True:
                        print(e)
        
        panel.mouseMoveEvent = lambda e: mouseMoveEvent(panel, e, self.CustomizeEnabled)
        
        # get list of all buttons in toolbar
        allButtons: list = []
        if panelName.endswith("_newPanel") is False and panelName.endswith("_custom") is False:
            try:
                TB = mw.findChildren(QToolBar, panelName)
                allButtons = TB[0].findChildren(QToolButton)
                # remove empty buttons
                for i in range(len(allButtons)):
                    button: QToolButton = allButtons[i]
                    try:
                        if button.defaultAction() is None:
                            if isinstance(button.actions(), list):
                                button.setDefaultAction(button.actions()[0])
                            if isinstance(button.actions(), QAction):
                                button.setDefaultAction(button.actions())
                        button.setObjectName(button.defaultAction().data())
                    except Exception:
                        pass
            except Exception:
                pass
            
        # If it is a custom dropdown that is present on the panel, create a button for.
        if workbenchName in Dict["workbenches"]:
            if (
                panelName != ""
                and "toolbars" in Dict["workbenches"][workbenchName]
                and panelName
                in Dict["workbenches"][workbenchName]["toolbars"]
                and "commands" in Dict["workbenches"][workbenchName]["toolbars"][panelName]
            ):
                # Add custom dropdown buttons to the list that are on default panels
                button = QToolButton()
                for command in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"].keys():
                    if command is not None and command !="":
                        if command.endswith("_ddb"):
                            for key, value in Dict["dropdownButtons"].items():
                                if key == command:
                                    currentCategory = self.currentCategory()
                                    for CommandItem in self.List_Commands:
                                        if CommandItem[0] == value[0] and ActivateWorkbench is True:
                                            if (value[1] != "General" and value[1] != "Global" and value[1] != "Standard"):                                
                                                # Activate the workbench if not loaded
                                                if CommandItem[3] in self.isWbLoaded and self.isWbLoaded[CommandItem[3]] is False:    
                                                    Gui.activateWorkbench(value[1])
                                                    self.isWbLoaded[value[1]] = True
                                                    break
                                                if CommandItem[3] not in self.isWbLoaded:
                                                    Gui.activateWorkbench(value[1])
                                                    self.isWbLoaded[value[1]] = True
                                                    break
                                                
                                    # Set the current  category after activating the workbench
                                    self.setCurrentCategory(currentCategory)
                                    if ActivateWorkbench is True:
                                        Gui.activateWorkbench(currentCategory.objectName())

                                    # Get the actions and add them one by one
                                    QuickAction = self.returnCustomDropDown(key, dict=Dict)
                                    menu = QMenu()
                                    for action in QuickAction:
                                        if len(action) > 0:
                                            menu.addAction(action[0])
                                    button.setMenu(menu)
                                    # # Set the default action
                                    button.setDefaultAction(QuickAction[0][0])                                
                                    # # Store the commmandName as a property
                                    # button.setProperty("CommandName", command)
                                    # Set the commandName as objectName as backup
                                    button.setObjectName(command)
                                    button.setToolTip(command)
                                    # Add the button
                                    allButtons.append(button)
            
        # Add custom panels
        if panelName.endswith("_custom"):
            customList = self.List_AddCustomToolBarToWorkbench(workbenchName, panelName, Dict = Dict["customToolbars"])
            allButtons.extend(customList)

        # # Add new Panels
        if panelName.endswith("_newPanel"):
            if workbenchName in Dict["workbenches"]:
                if panelName in Dict["workbenches"][workbenchName]["toolbars"]:
                    if "commands" in Dict["workbenches"][workbenchName]["toolbars"][panelName]:
                        for key in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"].keys():
                            if key != "order" and key is not None and key != "":
                                button = self.CreateButtonFromCommand(key, ActivateWorkBench=ActivateWorkbench)
                                if button is not None:
                                    # button.setProperty("CommandName", key)
                                    button.setObjectName(key)
                                    # button.setToolTip(key)
                                    allButtons.append(button)
                    
        # If a new command needs to be added, create a button and add it to allButtons
        if ExtraCommand != "":
            ExtraButton = self.CreateButtonFromCommand(ExtraCommand, ActivateWorkBench=ActivateWorkbench)
            if ExtraButton is not None:
                ExtraButton.setObjectName(ExtraCommand)
                # ExtraButton.setToolTip(ExtraCommand)
                allButtons.append(ExtraButton)
                
        # add the extra commands to the command list that are present in the dict.
        if workbenchName in Dict["workbenches"]:
            if (
                panelName != ""
                and "toolbars" in Dict["workbenches"][workbenchName]
                and panelName
                in Dict["workbenches"][workbenchName]["toolbars"]
            ):
                for orderedToolbar in Dict["workbenches"][workbenchName]["toolbars"]:
                    if orderedToolbar.lower() == panelName.lower():
                        if "commands" in Dict["workbenches"][workbenchName]["toolbars"][panelName]:
                            for Command in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"]:
                                if Command != "order":
                                    if "IsExtra" in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][Command]:
                                        if Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][Command]["IsExtra"]:
                                            ExtraCommand = self.CreateButtonFromCommand(Command, ActivateWorkBench=ActivateWorkbench)
                                            if ExtraCommand is not None:
                                                ExtraCommand.setObjectName(Command)
                                                allButtons.append(ExtraCommand)
            
        # add separators to the command list.
        if workbenchName in Dict["workbenches"]:
            if (
                panelName != ""
                and "toolbars" in Dict["workbenches"][workbenchName]
                and panelName
                in Dict["workbenches"][workbenchName]["toolbars"]
            ):
                for orderedToolbar in Dict["workbenches"][
                    workbenchName
                ]["toolbars"]:
                    if orderedToolbar.lower() == panelName.lower():
                        if (
                            "order"
                            in Dict["workbenches"][workbenchName][
                                "toolbars"
                            ][panelName]
                        ) and type(Dict["workbenches"][
                                        workbenchName
                                    ]["toolbars"][panelName]["order"]) is list:
                            for j in range(
                                len(
                                    Dict["workbenches"][
                                        workbenchName
                                    ]["toolbars"][panelName]["order"]
                                )
                            ):
                                try:
                                    if (
                                        "separator"
                                        in Dict["workbenches"][
                                            workbenchName
                                        ]["toolbars"][panelName]["order"][j].lower()
                                    ):
                                        separator = QToolButton()
                                        separator.setText(
                                            Dict["workbenches"][
                                                workbenchName
                                            ]["toolbars"][panelName]["order"][j]
                                        )
                                        separator.setObjectName(separator.text())
                                        allButtons.insert(j, separator)
                                except Exception:
                                    pass

        if workbenchName in Dict["workbenches"]:
            # order buttons like defined in ribbonStructure
            if (
                panelName
                in Dict["workbenches"][workbenchName]["toolbars"]
                and "order"
                in Dict["workbenches"][workbenchName]["toolbars"][
                    panelName
                ]
            ):
                OrderList: list = Dict["workbenches"][
                    workbenchName
                ]["toolbars"][panelName]["order"]
                
                # XXX check that positionsList consists of strings only
                def sortButtons(button: QToolButton):
                    # Use the text from the button
                    Text = button.objectName()
                    # Define a position variable
                    position = None
                    # Try to get the position, if it fails, put it at the end
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

        # Define the rowCount and column count
        columnCount = 0
        smallButtons = []
        mediumButtons = []
        largeButtons = []
        # Set the maximum columns
        maxColumns = Parameters.MAX_COLUMN_PANELS

        # Define an action list of the actions that are byond the maximum columns
        ButtonList = []

        # Go through the button list:
        for i in range(len(allButtons)):
            button = allButtons[i]
            CommandName = button.objectName()
            
            # count the number of buttons per type. Needed for proper sorting the buttons later.
            buttonSize = "small"
            try:
                buttonSize = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][self.ReturnCommand_string(Dict=Dict, panel=panel, widget=button)]["size"]
                if buttonSize == "small":
                    NoSmallButtons_spacer += 1
                if buttonSize == "medium":
                    NoMediumButtons_spacer += 1
            except Exception:
                pass
            
            # Panel overflow behaviour ----------------------------------------------------------------
            #
            # get the number of rows in the panel and store the maximum number of rows per wb.
            if workbenchName not in self.MaxRowsPerWB:
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "SmallButtons", "Rows"])
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "MediumButtons", "Rows"])
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "LargeButtons", "Rows"])
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "SmallButtonsPresent"])
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "MediumButtonsPresent"])
                Standard_Functions_Ribbon.add_keys_nested_dict(self.MaxRowsPerWB, [workbenchName, "LargeButtonsPresent"])
                self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] = 0
                self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"] = 0
                self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"] = 0
                self.MaxRowsPerWB[workbenchName]["SmallButtonsPresent"] = False
                self.MaxRowsPerWB[workbenchName]["MediumButtonsPresent"] = False
                self.MaxRowsPerWB[workbenchName]["LargeButtonsPresent"] = False
            if buttonSize == "small":
                smallButtons.append(button)
                mediumButtons.clear()
                largeButtons.clear()
                if len(smallButtons) == 3:
                    columnCount = columnCount + 1
                    smallButtons.clear()
                    # Store the number of rows for this workbench
                    self.MaxRowsPerWB[workbenchName]["SmallButtons"]["Rows"] = 3
                    # Save that small buttons are present
                    self.MaxRowsPerWB[workbenchName]["SmallButtonsPresent"] = True
            if buttonSize == "medium":                
                smallButtons.clear()
                mediumButtons.append(button)
                largeButtons.clear()
                if len(mediumButtons) == 2:
                    columnCount = columnCount + 1
                    mediumButtons.clear()
                    # Store the number of rows for this workbench
                    self.MaxRowsPerWB[workbenchName]["MediumButtons"]["Rows"]  = 2
                    # Save that medium buttons are present
                    self.MaxRowsPerWB[workbenchName]["MediumButtonsPresent"] = True
            if buttonSize == "large":                
                smallButtons.clear()
                mediumButtons.clear()
                largeButtons.append(button)
                if len(largeButtons) == 1:
                    columnCount = columnCount + 1
                    largeButtons.clear()
                    # Store the number of rows for this workbench
                    self.MaxRowsPerWB[workbenchName]["LargeButtons"]["Rows"]  = 1
                    # Save that large buttons are present
                    self.MaxRowsPerWB[workbenchName]["LargeButtonsPresent"] = True

            # if the button has not text, remove it, skip it and increase the counter.
            if button.text() == "":
                continue
            # If the command is already there, remove it, skip it and increase the counter.
            elif shadowList.__contains__(CommandName) is True:                
                continue
            else:
                # If the number of columns is more than allowed,
                # Add the actions to the OptionPanel instead.
                if maxColumns > 0 and ignoreColumnLimit is False:
                    # if the last item before the optionpanel is an separator, skip it
                    if columnCount > maxColumns and "separator" in button.text():
                        continue
                    if columnCount > maxColumns and "separator" not in button.text():
                        if (
                            (buttonSize == "small" and len(smallButtons) == 0) or 
                            (buttonSize == "medium" and len(mediumButtons) == 0) or 
                            (buttonSize == "large" and len(largeButtons) == 0)
                        ):
                            ButtonList.append(button)
                            panel.panelOptionButton().show()
                            continue

                # If the last item is not an separator, you can add an separator
                # With an paneloptionbutton, use an offset of 2 instead of 1 for i.
                if "separator" in button.text() and i < len(allButtons):
                    separatorWidget = CustomWidgets.CustomSeparator()
                    rowSpan = 6
                    separator = panel.addWidget(separatorWidget, rowSpan=rowSpan, fixedHeight=False, alignment=Qt.AlignmentFlag.AlignTop)
                    separator.setObjectName(button.text())
                    separator.setDisabled(not enableSeparator)
                    separator.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
                    if enableSeparator is True:
                        separator.setFixedWidth(16)
                    separator.setStyleSheet(
                        "RibbonSeparator:hover {background: "
                        + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                        + ";}"
                                            )

                    # there is a bug in pyqtribbon where the separator is placed in the wrong position
                    # despite the correct order of the button list.
                    # To correct this, empty and disabled buttons are added for spacing.
                    # (adding spacers did not work)
                    if float((NoSmallButtons_spacer + 1) / 3).is_integer():
                        spacer_1 = panel.addSmallButton()
                        spacer_1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
                        spacer_1.setFixedWidth(self.iconSize)
                        spacer_1.setFixedHeight(1)
                        spacer_1.setEnabled(False)
                        spacer_1.setStyleSheet("background-color: none;border: none")
                        spacer_1.setObjectName("spacer")
                    if float((NoSmallButtons_spacer + 2) / 3).is_integer():
                        spacer_1 = panel.addSmallButton()
                        spacer_1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
                        spacer_1.setFixedWidth(self.iconSize)
                        spacer_1.setFixedHeight(1)
                        spacer_1.setEnabled(False)
                        spacer_1.setStyleSheet("background-color: none;border: none")
                        spacer_1.setObjectName("spacer")
                        spacer_2 = panel.addSmallButton()
                        spacer_2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
                        spacer_2.setFixedWidth(self.iconSize)
                        spacer_2.setFixedHeight(1)
                        spacer_2.setEnabled(False)
                        spacer_2.setStyleSheet("background-color: none;border: none")
                        spacer_2.setObjectName("spacer")
                    # reset the counter after a separator is added.
                    NoSmallButtons_spacer = 0
                    # Same principle for medium buttons
                    if float((NoMediumButtons_spacer-1) / 2).is_integer():
                        spacer_1 = panel.addMediumButton()
                        spacer_1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
                        spacer_1.setFixedWidth(Parameters.ICON_SIZE_MEDIUM)
                        spacer_1.setFixedHeight(1)
                        spacer_1.setEnabled(False)
                        spacer_1.setStyleSheet("background-color: none;border: none")
                        spacer_1.setObjectName("spacer")
                    NoMediumButtons_spacer = 0
                    continue
                else:
                    try:
                        CommandName = button.objectName()
                        # CommandName = self.ReturnCommand_string(dict, panel, button)
                        # CommandName = button.toolTip()
                        action = button.defaultAction()
                        Icon = QIcon()

                        if CommandName == "":
                            continue
                        
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
                            if panelName in Dict["workbenches"][workbenchName]["toolbars"]:
                                if CommandName in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"]:
                                    if "text" in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]:
                                        textJSON = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["text"]

                                        # There is a bug in freecad with the comp-sketch menu hase the wrong text
                                        if (
                                            CommandName == "PartDesign_CompSketches"
                                            and Dict["workbenches"][
                                                workbenchName
                                            ]["toolbars"][panelName]["commands"][CommandName][
                                                "text"
                                            ]
                                            == "Create datum"
                                        ):
                                            textJSON = "Create sketch"

                                        # Check if the original menutext is different
                                        # if so use the alternative, otherwise use original
                                        MenuName = CommandInfoCorrections(CommandName)["menuText"].replace("&", "")
                                        if (MenuName != Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["text"] and MenuName != "" and textJSON != ""):
                                            text = textJSON

                            # the text would be overwritten again when the state of the action changes
                            # (e.g. when getting enabled / disabled), therefore the action itself
                            # is manipulated.
                            action.setText(text)
                        except KeyError as e:
                            if Parameters.DEBUG_MODE is True:
                                print(f"No alternative text!. WB={workbenchName}, cmd={action.data()}, key={e}")
                            text = action.text()
                                                
                        # Try to get the icon from the stored freecad icons                      
                        FreeCAD_Icons = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resources", "FreeCAD Icons"))
                        for root, dirs, files in os.walk(FreeCAD_Icons):
                            for fileName in files:
                                if CommandName in fileName:
                                    Icon.addPixmap(QPixmap(os.path.join(root, fileName)))
                                    action.setIcon(Icon)
                                    break
                        
                        # If not get the Icon from FreeCAD or the data file
                        if Icon.isNull():
                            pixmap = ""
                            try:
                                pixmap = Dict["workbenches"][
                                    workbenchName
                                ]["toolbars"][panelName]["commands"][CommandName]["icon"]
                            except Exception:
                                pass
                            if action.data() is not None:
                                Icon = self.ReturnCommandIcon(action.data(), pixmap)
                            else:
                                Icon = self.ReturnCommandIcon(CommandName, pixmap)
                            if Icon is not None and Icon.isNull() is False:
                                action.setIcon(Icon)
                                
                        # Check if there is an Icon. if not add a replacement
                        if Icon.pixmap(64,64).toImage().bytesPerLine() < 256:
                            Icon = Gui.getIcon("preferences-workbenches")
                            action.setIcon(Icon)

                        # get button size from ribbonStructure
                        try:
                            buttonSize = Dict["workbenches"][
                                workbenchName
                            ]["toolbars"][panelName]["commands"][CommandName]["size"]
                            # If the size is empty. This button is removed from the panel
                            if buttonSize == "":
                                # Remove also from the ribbon structure if it is an extra (dragged) button
                                if "IsExtra" in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]:
                                    try:
                                        del Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]
                                        Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"]["order"].remove(CommandName)
                                    except Exception:
                                        pass
                                continue
                        except KeyError:
                            pass

                        # Check if this is an icon only toolbar
                        IconOnly = False
                        for iconToolbar in Dict["iconOnlyToolbars"]:
                            if iconToolbar == panelName:
                                IconOnly = True

                        btn = None
                        # Make sure that no strange "&" symbols are remainging
                        action.setText(action.text().replace("&", ""))
                        if buttonSize == "small":
                            showText = Parameters.SHOW_ICON_TEXT_SMALL
                            if (
                                IconOnly is True
                                # or Parameters.USE_FC_OVERLAY is True
                            ):
                                showText = False
                            try:
                                if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                    showText = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["textEnabled"]
                            except Exception:
                                pass

                            # Create a custom toolbutton
                            ButtonSize = QSize(
                                Parameters.ICON_SIZE_SMALL,
                                Parameters.ICON_SIZE_SMALL,
                            )
                            IconSize = QSize(
                                Parameters.ICON_SIZE_SMALL,
                                Parameters.ICON_SIZE_SMALL,
                            )
                            if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                try:
                                    size = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["ButtonSize_small"]                                    
                                    IconSize = QSize(size, size)
                                    ButtonSize = IconSize
                                except Exception:
                                    pass
                                
                            Menu = None
                            if button.menu() is not None:
                                Menu = button.menu()
                            btn = CustomControls(
                                Text=action.text(),
                                Action=action,
                                Icon=Icon,
                                IconSize=IconSize,
                                ButtonSize=ButtonSize,
                                FontSize=Parameters.FONTSIZE_BUTTONS,
                                showText=showText,
                                setWordWrap=False,
                                ElideMode=False,
                                MaxNumberOfLines=2,
                                Menu=Menu,
                                MenuButtonSpace=self.MenuButtonSpace,
                                parent=self,
                                ButtonStyle=pyqtribbon.RibbonButtonStyle.Small
                            )
                            btn.setObjectName(CommandName)
                            # add the button as a small button
                            # layout.addWidgets(btn, "small")
                            panel.addSmallWidget(
                                btn,
                                alignment=self.ButtonAlignment,
                                fixedHeight=False,
                            ).setObjectName(CommandName)  # Set fixedheight to false. This is set in the custom widgets
                        elif buttonSize == "medium":
                            showText = Parameters.SHOW_ICON_TEXT_MEDIUM
                            if (
                                IconOnly is True
                                # or Parameters.USE_FC_OVERLAY is True
                            ):
                                showText = False
                            try:
                                if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                    showText = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["textEnabled"]
                            except Exception:
                                pass

                            # Create a custom toolbutton
                            ButtonSize = QSize(
                                Parameters.ICON_SIZE_MEDIUM,
                                Parameters.ICON_SIZE_MEDIUM,
                            )
                            IconSize = QSize(
                                Parameters.ICON_SIZE_MEDIUM,
                                Parameters.ICON_SIZE_MEDIUM,
                            )
                            if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                try:
                                    size = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["ButtonSize_medium"]
                                    IconSize = QSize(size, size)
                                    ButtonSize = IconSize
                                except Exception:
                                    pass
                            if Parameters.LINK_ICON_SIZES is True:
                                size = Parameters.ICON_SIZE_SMALL*1.5
                                IconSize = QSize(size, size)
                                ButtonSize = IconSize
                                
                            Menu = None
                            if button.menu() is not None:
                                Menu = button.menu()
                            btn = CustomControls(
                                Text=action.text(),
                                Action=action,
                                Icon=Icon,
                                IconSize=IconSize,
                                ButtonSize=ButtonSize,
                                FontSize=Parameters.FONTSIZE_BUTTONS,
                                showText=showText,
                                setWordWrap=Parameters.WRAPTEXT_MEDIUM,
                                MaxNumberOfLines=2,
                                Menu=Menu,
                                MenuButtonSpace=self.MenuButtonSpace,
                                parent=self,
                                ButtonStyle=pyqtribbon.RibbonButtonStyle.Medium
                            )
                            btn.setObjectName(CommandName)
                            # add the button as large button
                            # layout.addWidgets(btn, "medium")
                            panel.addMediumWidget(
                                btn,
                                alignment=self.ButtonAlignment,
                                fixedHeight=False,
                            ).setObjectName(CommandName)  # Set fixedheight to false. This is set in the custom widgets
                        elif buttonSize == "large":
                            showText = Parameters.SHOW_ICON_TEXT_LARGE
                            if (
                                IconOnly is True
                                # or Parameters.USE_FC_OVERLAY is True
                            ):
                                showText = False
                            try:
                                if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                    if "textEnabled" in Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]:
                                        showText = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["textEnabled"]
                            except Exception as e:                         
                                if Parameters.DEBUG_MODE is True:
                                    print(CommandName + ", " + str(e.with_traceback(e.__traceback__)))
                                pass

                            # Create a custom toolbutton
                            ButtonSize = QSize(
                                Parameters.ICON_SIZE_LARGE,
                                Parameters.ICON_SIZE_LARGE,
                            )
                            IconSize = QSize(
                                Parameters.ICON_SIZE_LARGE,
                                Parameters.ICON_SIZE_LARGE,
                            )
                            if Parameters.BETA_FUNCTIONS_ENABLED is True:
                                try:                                    
                                    size = Dict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][CommandName]["ButtonSize_large"]
                                    IconSize = QSize(size, size)
                                    ButtonSize = IconSize
                                except Exception as e:
                                    if Parameters.DEBUG_MODE is True:
                                        print(e)
                                    pass
                            if Parameters.LINK_ICON_SIZES is True:
                                size = Parameters.ICON_SIZE_SMALL*3
                                IconSize = QSize(size, size)
                                ButtonSize = IconSize
                            Menu = None
                            if button.menu() is not None:
                                Menu = button.menu()
                            btn = CustomControls(
                                Text=action.text(),
                                Action=action,
                                Icon=Icon,
                                IconSize=IconSize,
                                ButtonSize=ButtonSize,
                                FontSize=Parameters.FONTSIZE_BUTTONS,
                                showText=showText,
                                setWordWrap=Parameters.WRAPTEXT_LARGE,
                                MaxNumberOfLines=2,
                                Menu=Menu,
                                MenuButtonSpace=self.MenuButtonSpace,
                                parent=self,
                                ButtonStyle=pyqtribbon.RibbonButtonStyle.Large
                            )
                            btn.setObjectName(CommandName)
                            # add the button as large button
                            panel.addLargeWidget(
                                btn,
                                fixedHeight=False,
                                alignment=self.ButtonAlignment,
                            ).setObjectName(CommandName) # Set fixedheight to false. This is set in the custom widgets                            
                        else:
                            if Parameters.DEBUG_MODE is True:
                                if buttonSize != "none":
                                    print(
                                        f"{action.text()} is ignored. Its size was: {buttonSize}"
                                    )
                            pass

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
                        shadowList.append(CommandName)

                    except Exception as e:
                        if Parameters.DEBUG_MODE is True:
                            raise e
                        continue
        
        # Set the panel title
        panel.setTitle(self.ReturnPanelTitle(panel, Dict))

        # Set the panelheight. setting the ribbonheigt, cause the first tab to be shown to large
        self.setPanelProperties(panel)
        
        # Add a checkbox to the titlebar. Used for enabling or disabling panels. Default is hidden
        titleLayout: QHBoxLayout = panel._titleLayout
        # EnableControl = QCheckBox()
        EnableControl = Toggle()
        EnableControl.setChecked(True)
        if workbenchName in Dict["workbenches"]:
            if panel.objectName() in Dict["workbenches"][workbenchName]["toolbars"]:
                if "Enabled" in Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]:
                    Enabled = Dict["workbenches"][workbenchName]["toolbars"][panel.objectName()]["Enabled"]
                    EnableControl.setChecked(bool(Enabled))
        EnableControl.setFixedWidth(32)
        EnableControl.setObjectName("EnablePanel")
        titleLayout.insertWidget(0, EnableControl)
        if showEnableControl is False:
            EnableControl.setHidden(True)

        # Setup the panelOptionButton
        panel = self.PopulateOverflowMenu(panel, ButtonList)
                
        # Add a spacer. Otherwise alignment of a panel with one button will always be to the top
        # if len(allButtons) == 1:
        spacer = QWidget()
        spacer.setObjectName("ExtraSpacer")
        spacer.setMinimumSize(0, panel.height() - panel._titleWidget.height())
        panel.addWidget(spacer, rowSpan=6)

        # Enable all buttons, so you can access them with a right click
        self.activateButtons()

        if panel._actionsLayout.count() > 1:            
            return panel
        else: 
            self.currentCategory().removePanel(panel.objectName())
            panel.deleteLater()    
            if Parameters.DEBUG_MODE is True:                  
                print(f"The panel \"{panel.title()}\" did not have any buttons and is not loaded!")
            return None
        return None
    
    def CreateNewPanel(self, title):
        if title == "":
            return
        else: 
            for key in self.currentCategory().panels().keys():
                if key == f"{title}_newPanel":
                    StandardFunctions.Mbox(translate("FreeCAD Ribbon", "This panel already exists!"))
                    return
            
            panel = self.currentCategory().addPanel(f"{title}_newPanel")
            panel.panelOptionButton().hide()
            panel.setTitle(title)
            panel.setObjectName(f"{title}_newPanel")
            self.setPanelProperties(panel)
            # Add a checkbox to the titlebar. Used for enabling or disabling panels. Default is hidden
            titleLayout: QHBoxLayout = panel._titleLayout
            # EnableControl = QCheckBox()
            EnableControl = Toggle()
            EnableControl.setChecked(True)                    
            EnableControl.setFixedWidth(32)
            EnableControl.setObjectName("EnablePanel")
            titleLayout.insertWidget(0, EnableControl)
            
            # Add the new panel to the dict
            workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
            StandardFunctions.add_keys_nested_dict(self.workBenchDict, ["newPanels", workbenchName, panel.objectName()])
            self.workBenchDict["newPanels"][workbenchName][panel.objectName()] = []
            
            self.AddedPanels.append(panel)
            
            for panel in self.RemovedPanels:
                if panel.objectName() == f"{title}_newPanel":
                    self.RemovedPanels.remove(panel)
                    panel.close()
        
        return
    
    def RemovePanelFromDict(self, panel: RibbonPanel):
        WorkBenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        WorkBenchTitle = self.currentCategory().title()
        
        # _newPanel
        if panel.objectName().endswith("_newPanel"):
            # Remove the panel from the newPanels dict
            if WorkBenchName in self.workBenchDict["newPanels"]:
                if panel.objectName() in self.workBenchDict["newPanels"][WorkBenchName]:
                    del self.workBenchDict["newPanels"][WorkBenchName][panel.objectName()]
            
            ## Remove the panel also from the workbench dict
            if WorkBenchName in self.workBenchDict["workbenches"]:
                orderList = []
                if "order" in self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]:
                    orderList: list = self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]["order"]
                    if panel.objectName() in orderList:
                        orderList.remove(panel.objectName())
                    
                    # update the order list
                    if panel.objectName() in self.workBenchDict["workbenches"][WorkBenchName]:
                        self.workBenchDict["workbenches"][WorkBenchName][panel.objectName()]["order"] = orderList
                
                # Remove the panel also from the workbench dict
                if panel.objectName() in self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]:
                    del self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][panel.objectName()]
            
            # Close the panel
            panel.close()
            self.RemovedPanels.append(panel)
            # Remove the panel from the current category dict
            # self.currentCategory().panels().pop(panel.objectName())
            # self.currentCategory().removePanel(panel.objectName())
            
        # _custom
        if panel.objectName().endswith("_custom"):
            if WorkBenchName in self.workBenchDict["customToolbars"]:
                if panel.objectName() in self.workBenchDict["customToolbars"][WorkBenchName]:
                    # Get the order list
                    orderList: list = self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]["order"]
                    
                    ListPanels = []
                    for command, toolbar in self.workBenchDict["customToolbars"][WorkBenchName][panel.objectName()]["commands"].items():
                        if toolbar not in ListPanels:
                            ListPanels.append(toolbar)

                    # Add the original panels
                    for toolbar in ListPanels:
                        TB = mw.findChildren(QToolBar, toolbar)
                        if TB is not None:
                            # Create the panel based on the toolbars
                            newPanel = self.CreatePanel(workbenchName=WorkBenchName, panelName=toolbar, addPanel=False, Dict=self.workBenchDict, showEnableControl=True, ActivateButtons=True)                                                                        
                            # show the enable checkboxes  
                            titleLayout: QHBoxLayout = newPanel._titleLayout
                            EnableControl = titleLayout.itemAt(0).widget()
                            if EnableControl is not None:
                                EnableControl.setVisible(True)
                                EnableControl.setChecked(True)
                            # Add the original panel to the orderList
                            if toolbar not in orderList:
                                orderList.append(toolbar)
                            # Add the panel
                            index = orderList.index(toolbar)
                            self.currentCategory().insertWidget(newPanel, index)
                            # Update the dict of the currentCategory with the new panel
                            self.currentCategory()._panels[newPanel.objectName()] = newPanel
                    
                    # Remove the custom panel
                    #
                    # Close the panel first before removing
                    panelToRemove = self.currentCategory().panels()[panel.objectName()]                       
                    panelToRemove.close()
                    self.RemovedPanels.append(panel)
                    # # Remove it
                    # self.currentCategory().removePanel(panel.objectName())
                    
                    # Remove the custom panel from the order list
                    if panel in orderList:
                        orderList.remove(panel.objectName())

                    # remove the custom toolbar from the workbenches dict
                    del self.workBenchDict["customToolbars"][WorkBenchName][panel.objectName()]
                    
                    # Remove the panel also from the workbench dict
                    if WorkBenchName in self.workBenchDict["workbenches"]:
                        orderList = []
                        if "order" in self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]:
                            orderList: list = self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]["order"]
                            if panel.objectName() in orderList:
                                orderList.remove(panel.objectName())
                            
                            # update the order list
                            if panel.objectName() in self.workBenchDict["workbenches"][WorkBenchName]:
                                self.workBenchDict["workbenches"][WorkBenchName][panel.objectName()]["order"] = orderList
                        
                        # Remove the panel also from the workbench dict
                        if panel.objectName() in self.workBenchDict["workbenches"][WorkBenchName]["toolbars"]:
                            del self.workBenchDict["workbenches"][WorkBenchName]["toolbars"][panel.objectName()]
                        
                    # Get the Dialog and remove the item from the list
                    Dialog = self.AddCommandsDialog.form
                    if Dialog is not None:
                        # remove the custom toolbar from the combobox
                        for i in range(Dialog.CustomToolbarSelector_CP.count()):
                            if (Dialog.CustomToolbarSelector_CP.itemText(i).split(", ")[0] + "_custom" == panel.objectName()):
                                if (Dialog.CustomToolbarSelector_CP.itemText(i).split(", ")[1] == WorkBenchTitle and Dialog.CustomToolbarSelector_CP.itemText(i).split(", ")[1] != ""):
                                    Dialog.CustomToolbarSelector_CP.removeItem(i)
                                    Dialog.CustomToolbarSelector_CP.setCurrentText(Dialog.CustomToolbarSelector_CP.itemText(i - 1))
                    
                    # Set the current text to new
                    Dialog.CustomToolbarSelector_CP.setCurrentText("New")

                    if (
                        Dialog.CustomToolbarSelector_CP.currentText()
                        == "New"
                    ):
                        Dialog.PanelSelected_CP.clear()
                        Dialog.PanelName_CP.clear()
        
        # Standard panels
        if panel.objectName().endswith("_custom") is False and panel.objectName().endswith("_newPanel") is False:
            titleLayout: QHBoxLayout = panel._titleLayout
            EnableControl: Toggle = titleLayout.itemAt(0).widget()
            if EnableControl is not None:
                EnableControl.setChecked(False)
        return
    
    def setPanelProperties(self, panel: RibbonPanel):
        # Test if the panel is not already deleted.
        # This is needed, if a combined panel was added and then removed by clicking cancel
        try:
            panel.objectName()
        except Exception:
            return
        # Set the panelheight. setting the ribbonheigt, cause the first tab to be shown to large
        # add an offset to make room for the panel titles and icons
        #
        # Set the font for the panel title
        Font = QFont()
        Font.setPixelSize(Parameters.FONTSIZE_PANELS)
        panel._titleLabel.setFont(Font)
        panel._titleLabel.setStyleSheet(f"color: {StyleMapping_Ribbon.ReturnStyleItem('FontColor')}")
        panel._titleWidget.setFixedHeight(QFontMetrics(Font).boundingRect(panel.title()).height())
                
        # Set the properties for the layouts
        panel._actionsLayout.setHorizontalSpacing(self.PaddingRight * 0.5)
        panel._actionsLayout.setSpacing(self.ButtonSpacing)
        panel._actionsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        panel._actionsLayout.setContentsMargins(0, self.TopMargin, 3, self.BottomMargin) # Left, Top, Right, Bottom
        panel._mainLayout.setSpacing(0)
        panel.setFixedHeight(self.ReturnRibbonHeight(Parameters.PANEL_HEIGHT_OFFSET))
        # Set the ribbonheight
        self.RibbonHeight = panel.height() + self.RibbonOffset
        # Correct the width of the (hidden) option button
        OptionButton = panel.panelOptionButton()
        OptionButton.setFixedSize(Parameters.ICON_SIZE_SMALL, self.RibbonOffset+QFontMetrics(Font).tightBoundingRect(panel.title()).height())
        # # Set the size policy to fixed. Otherwise resizing is not working properly
        panel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return
    
    def PopulateOverflowMenu(self, panel: RibbonPanel, ButtonList: list):
        # Create a list of actions from the button list
        actionList = []
        for i in range(len(ButtonList)):
            button = ButtonList[i]
            StyleSheet_Menu = (
                "* {font-size: " + str(Parameters.FONTSIZE_MENUS) + "px;}"
            )
            button.setStyleSheet(StyleSheet_Menu)
            if type(button.actions()) is list:
                if len(button.actions()) == 1:
                    actionList.append(button.actions()[0])
                if len(button.actions()) > 1:
                    actionList.append(button.actions())
            if type(button.actions()) is QAction:
                actionList.append(button.actions())
                
        # The option button
        OptionButton = panel.panelOptionButton()
        
        # If there are actions, create an overflow menu from the panel option button
        if len(actionList) > 0:
            Menu = CustomControls.CustomOptionMenu(
                OptionButton.menu(), actionList, self
            )
            OptionButton.setMenu(Menu)
            StyleSheet_Menu = (
                "* {font-size: " + str(Parameters.FONTSIZE_MENUS) + "px;}"
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
        OptionButton.setFixedWidth(Parameters.ICON_SIZE_SMALL)
        # Set the background color and remove the border
        OptionButton.setStyleSheet("RibbonPanelOptionButton{ background: "
                                   + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                                   + ";border: "
                                   + StyleMapping_Ribbon.ReturnStyleItem("Background_Color")
                                   + ";}RibbonPanelOptionButton::hover { background: "
                                   + StyleMapping_Ribbon.ReturnStyleItem("Background_Color_Hover")
                                   + ";}"
        )
        # Remove the tooltip
        OptionButton.setToolTip("")
        
        # If there are no actions, hide the button
        if len(actionList) == 0:
            panel.panelOptionButton().hide()
        return panel
    
    def RestoreJson(self):
        # get the path for the Json file
        JsonPath = ConfigDirectory
        JsonFile = os.path.join(JsonPath, "RibbonStructure.json")

        BackupFiles: list = []
        # returns a list of names (with extension, without full path) of all files
        # in backup path
        for name in os.listdir(pathBackup):
            if os.path.isfile(os.path.join(pathBackup, name)):
                if name.lower().endswith("json"):
                    BackupFiles.append(name)
        # Sort the backup files in reversed order
        BackupFiles.sort(reverse=True)

        if len(BackupFiles) > 0:
            SelectedFile = StandardFunctions.Mbox(
                translate("FreeCAD Ribbon", "Select a backup file"),
                "",
                21,
                "NoIcon",
                BackupFiles[0],
                BackupFiles,
            )
            BackupFile = os.path.join(pathBackup, SelectedFile)
            result = shutil.copy(BackupFile, JsonFile)
            StandardFunctions.Print(
                translate(
                    "FreeCAD Ribbon", "Ribbon bar set back to settings from: {}"
                ).format(result),
                "Warning",
            )

            message = translate(
                "FreeCAD Ribbon",
                "Settings reset to {}!\nYou must restart FreeCAD for changes to take effect.",
            ).format(SelectedFile)
            answer = StandardFunctions.RestartDialog(message=message)
            if answer == "yes":
                StandardFunctions.restart_freecad()

        return
    
    def ReturnCommand_string(self, Dict: dict, panel: RibbonPanel, widget) -> str:
        # Define a button and a command
        button = None
        command = ""
        
        # Try to get the command from the widget
        if type(widget) is CustomControls:
            command = widget.objectName()
            if command is not None and command != "":
                return command

        # if command is None or command == "":
        # Try to get the command button. This means that the widget is a custom toolbutton
        # button = widget.findChild(QToolButton, "CommandButton")
        # if the button is None and the widget is a QToolButton, us it instead
        # if button is None and type(widget) is QToolButton:
        button = widget
        if button is not None and command != "":
            command = button.defaultAction().data()
            if isinstance(button.actions(), list):
                if command is None or command == "":
                    command = button.actions()[0].objectName()
                    if command is None or command == "":
                        command = button.actions()[0].data()
            if isinstance(button.actions(), QAction):
                if command is None or command == "":
                    command = button.actions().objectName()
                    if command is None or command == "":
                        command = button.actions().data()
        if command is None or command == "":
            command = button.objectName()

        return command
    
    def RemoveButtonFromPanel(self, panel: RibbonPanel = None, widget = None):
        workbenchName = self.tabBar().tabData(self.tabBar().currentIndex())
        panelName = panel.objectName()
        
        # Get the command
        # command = self.ReturnCommand_string(Dict=self.workBenchDict, panel=panel, widget=widget.parent())
        command = widget.parent().objectName()
           
        try:
            orderList: list = self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["order"]
            if command != "" and command is not None and command in self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"]:
                self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]["size"] = ""              
                
                # if it is a button from a newPanel, remove it from the newPanel list
                if panelName.endswith("_newPanel"):
                    commandList = []
                    if panelName in self.workBenchDict["newPanels"][workbenchName]:
                        commandList = self.workBenchDict["newPanels"][workbenchName][panelName]
                    elif panelName in self.workBenchDict["newPanels"]["Global"]:
                        commandList = self.workBenchDict["newPanels"]["Global"][panelName]
                    elif panelName in self.workBenchDict["newPanels"]["Standard"]:
                        commandList = self.workBenchDict["newPanels"]["Standard"][panelName]
                    for item in commandList:
                        if item[0] == command:
                            commandList.remove(item)
                            self.workBenchDict["newPanels"][workbenchName][panelName] = commandList
                            break     

                # Remove also from the ribbon structure if it is an extra (dragged) button
                if "IsExtra" in self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"][command]:
                    try:
                        # Get the dict
                        Dict: dict = self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"]
                        # Remove the command and update the workbench dict
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["commands"] = StandardFunctions.remove_keys_with_values(Dict, command)
                        # Update the order list
                        orderList.remove(command)
                        self.workBenchDict["workbenches"][workbenchName]["toolbars"][panelName]["order"] = orderList

                    except Exception:
                        pass
     
            
            # Close the widget
            # widget.close()
            newPanel = self.CreatePanel(workbenchName, panelName, addPanel=False, Dict=self.workBenchDict, ignoreColumnLimit=True, showEnableControl=True, enableSeparator=True, ActivateButtons=True, ActivateWorkbench=False)
            # Add the panel to the list with long panels
            if newPanel.panelOptionButton().isVisible():
                self.longPanels.append(newPanel)
            # Replace the panel with the new panel
            self.currentCategory().replacePanel(panel, newPanel)
            # Update the dict of the currentCategory with the new panel
            self.currentCategory()._panels[newPanel.objectName()] = newPanel
            panel.close()
            
            # Restore the cursor
            QApplication.restoreOverrideCursor()
            return True     
        except Exception as e:
            if Parameters.DEBUG_MODE is True:
                print(e)

        return False
    
    def RemoveButtonFromQuickAccess(self, widget: QuickAccessToolButton, pos: QPoint):
        try:
            # Get a list of all buttons
            buttonList = self._titleWidget._quickAccessToolBar.findChildren(QToolButton)
            # Start with the index at -1. This way, the index is zero based
            index = -1
            # Go through the button list. if the passed position is withing the edges of a button,
            # You got the right one
            IsDeleted = False
            for button in buttonList:
                index = index + 1
                if button.objectName() == widget.objectName():                    
                    # Map the for corners of the button to global
                    pos_tl = button.mapTo(self._titleWidget._quickAccessToolBar, button.rect().topLeft())
                    pos_tr = button.mapTo(self._titleWidget._quickAccessToolBar, button.rect().topRight())

                    # If the position of the context menu event is within the global corners
                    # delete the button
                    if pos.x() >= pos_tl.x() and pos.x() < pos_tr.x():             
                        button.deleteLater()                                                
                        IsDeleted = True
                                
                        break
            
            if IsDeleted is True:
                # Update the quickAccessCommands list
                self.workBenchDict["quickAccessCommands"].remove(widget.objectName())
               
            # Delete the drag indicater
            try:
                self._titleWidget._quickAccessToolBar.removeAction(self.dragAction_QuickAccess)
                self._titleWidget._quickAccessToolBar.removeAction(self.dragIndicator_QuickAccess_Action)
            except Exception:
                pass
            return True
        except Exception:
            return False
        
    def activateButtons(self):
         # Enable all buttons, so you can access them with a right click
        if self.isLoaded:
            for child in mw.findChildren(QToolButton):
                try:
                    for subAction in child.actions():
                        subAction.setEnabled(True)                
                except Exception:
                    pass
                child.setEnabled(True)
            # Gui.updateGui()
        return
    
    def BuildQuickToolbar(self, ButtonList = []):
        # add quick access buttons
        toolBarWidth = 0
        # Add a counter to count the separators
        counter = 0
        
        OrderList = []
        for commandName in ButtonList:
            # Define a width
            width = 0
            # set the default padding to zero
            padding = 6

            try:
                # If there is 'separator' in the commandname, add a separator
                if "separator" in commandName:
                    # Increase the counter
                    counter = counter + 1
                    # Set the width and height
                    width = 12
                    height = self.QuickAccessButtonSize
                    # Create the separator
                    separator = QuickAccessSeparator(self.quickAccessToolBar())
                    separator.setObjectName(f"separator_{counter}")
                    separator.setFixedSize(width, height)
                    separator.setEnabled(True)
                    # Create the widget action from the separator
                    WidgetAction = QWidgetAction(self.quickAccessToolBar())
                    WidgetAction.setObjectName(f"separator_{counter}")
                    WidgetAction.setDefaultWidget(separator)
                    # Add the widgetaction to the toolbar      
                    self.quickAccessToolBar().addAction(WidgetAction)
                    # Update the toolbar width               
                    toolBarWidth = toolBarWidth + width
                    # Update the order list
                    OrderList.append(f"separator_{counter}")
                    continue
                
                # Create a button
                button = self.CreateQuickButtonFromCommand(commandName=commandName, padding=padding)

                # Set the height of the toolbar
                self.setQuickAccessButtonHeight(self.RibbonMinimalHeight)

                # Add the button to the quickaccess toolbar as an WidgetAction. This is needed for custom widgets
                # Otherwise you cannot get the index later during drag
                #
                # Create the widget action from the button
                WidgetAction = QWidgetAction(self.quickAccessToolBar())
                WidgetAction.setObjectName(commandName)
                WidgetAction.setDefaultWidget(button)
                # Add the widgetaction to the toolbar      
                self.quickAccessToolBar().addAction(WidgetAction)
                # Update the toolbar width   
                toolBarWidth = toolBarWidth + button.width()
                # Update the order list
                OrderList.append(commandName)
            except Exception as e:
                if Parameters.DEBUG_MODE is True:
                    StandardFunctions.Print(f"{commandName}, {e}", "Warning")
                continue
        
        # Update the ribbon structure with the order list
        self.ribbonStructure["quickAccessCommands"] = OrderList
        return toolBarWidth
    
    def CreateQuickButtonFromCommand(self, commandName, padding = 0):
        # Define a button
        button = None

        # If it is a standard freecad button, set the command accordingly
        if commandName.endswith("_ddb") is False and "separator" not in commandName:
            try:
                # Check if the workbench is loaded. If not, actions will be an empty list
                # Find the command its workbench and activate it
                QuickAction = Gui.Command.get(commandName).getAction()
                if len(QuickAction) == 0:
                    for CommandItem in self.List_Commands:
                        if CommandItem[0] == commandName and CommandItem[3] not in self.isWbLoaded:
                            Gui.activateWorkbench(CommandItem[3])
                            self.isWbLoaded[CommandItem[3]] = True
                            break
            except Exception:
                pass
            QuickAction = Gui.Command.get(commandName).getAction()

            if len(QuickAction) == 1:
                button = QuickAccessToolButton(Action=QuickAction[0], parent=self.quickAccessToolBar(), Size=self.QuickAccessButtonSize)
                
                # Set the command as objectName for future reference
                button.setObjectName(commandName)
                return button
                
            elif len(QuickAction) > 1:
                # set the padding for a dropdown button
                padding = self.PaddingRight
                menu = QMenu()
                menu.addActions(QuickAction)
                button = QuickAccessToolButton(Action=QuickAction[0], parent=self.quickAccessToolBar(), Menu=menu, Size=self.QuickAccessButtonSize, MenuButtonSpace=padding)

                # Set the command as objectName for future reference
                button.setObjectName(commandName)
                return button

        # If it is a custom dropdown, add the actions one by one.
        if commandName.endswith("_ddb") is True and "separator" not in commandName:
            menu = QMenu()
            # set the padding for a dropdown button
            padding = self.PaddingRight
            # Get the actions and add them one by one
            QuickAction = self.returnCustomDropDown(commandName, dict=self.ribbonStructure)
            for action in QuickAction:
                if len(action) > 0:
                    menu.addAction(action[0])
            button = QuickAccessToolButton(Action=QuickAction[0], parent=self.quickAccessToolBar(), Menu=menu, Size=self.QuickAccessButtonSize, MenuButtonSpace=padding)
              
            # Set the command as objectName for future reference
            button.setObjectName(commandName)
            return button
        
        # if it is a separator return a separator
        if "separator" in commandName:
            width = 12
            height = self.QuickAccessButtonSize
            separator = QuickAccessSeparator(self.quickAccessToolBar())
            separator.setObjectName(commandName)
            separator.setFixedSize(width, height)
            separator.setEnabled(True)
            button = separator
        
        # Set the command as objectName for future reference
        button.setObjectName(commandName)
        return button
        
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
            DataFile2 = os.path.join(ConfigDirectory, "RibbonDataFile2.dat")
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

    def ConvertRibbonStructure(self, checkFCVersion = True, RestartFreeCAD = False):
        # Define a result parameter
        isConverted = False
        # Get the FreeCAD Version
        version = App.Version()

        # Check if version is stored in the ribbon structure.
        # If so check if it is an older version.
        # If it is the same or newer version, return.
        if checkFCVersion is True:
            if "convertedWithVersion" in self.ribbonStructure:
                main = self.ribbonStructure["convertedWithVersion"][0]
                sub = self.ribbonStructure["convertedWithVersion"][1]
                patch = self.ribbonStructure["convertedWithVersion"][2]
                git_version = self.ribbonStructure["convertedWithVersion"][3]
                if main >= int(version[0]):
                    if sub >= int(version[1]):
                        if patch >= int(version[2]):
                            if git_version >= int(version[3].split(" ")[0]):
                                if Parameters.DEBUG_MODE is True:
                                    print("no conversion needed")
                                return

        # Convert the commands from menuname to the commandames
        #
        # Convert the custompanels
        if "customToolbars" in self.ribbonStructure:
            for WorkBenchName in self.ribbonStructure["customToolbars"]:
                for ToolbarName in self.ribbonStructure["customToolbars"][WorkBenchName]:
                    newDict = {}
                    if "commands" in self.ribbonStructure["customToolbars"][WorkBenchName][ToolbarName]:
                        currentDict: dict = self.ribbonStructure["customToolbars"][WorkBenchName][ToolbarName]["commands"]
                        for key, value in currentDict.items():
                            for CommandItem in self.List_Commands:
                                # Get the english menutext
                                MenuName = CommandItem[2]
                                # Get the translated menutext
                                MenuNameTtranslated = CommandItem[4]

                                if (MenuName.lower() == key.lower() or MenuNameTtranslated.lower() == key or CommandItem[0] == key)  and WorkBenchName == CommandItem[3]:
                                    try:
                                        Standard_Functions_Ribbon.add_keys_nested_dict(newDict, [CommandItem[0]], 1, True)
                                        newDict[CommandItem[0]] = value
                                    except Exception as e:
                                        if Parameters.DEBUG_MODE is True:
                                            StandardFunctions.Print(
                                                f"{e.with_traceback(e.__traceback__)}, 3",
                                                "Warning",
                                            )
                                        continue
                        self.ribbonStructure["customToolbars"][WorkBenchName][ToolbarName]["commands"] = newDict
                                    
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
                                # Go through the current order list if there is an datafile
                                DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
                                if os.path.exists(DataFile) is True:
                                    for i in range(len(OrderList)):
                                        MenuText = OrderList[i]
                                        # if it is an separator of custom dropdown button, just added ti the coverted list.
                                        # For everything else, find the commandname in the datafile
                                        if MenuText is not None:
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
        
        # Convert toolbar names to new names for certain WB's
        #
        # Fill the correction list -> {workbenchname [[new toolbar, old toolbar], [new toolbar, old toolbar]]}
        CorrectionList = {}
        MappingFile = os.path.join(os.path.dirname(__file__), "Toolbar name mapping.json")
        with open(MappingFile , "r") as File:
            CorrectionList.update(json.load(File))
        File.close()

        # Go through the workbenches in the json file to correct toolbar names
        for WorkBench in self.ribbonStructure["workbenches"]:
            Dict = {}
            OrderList = []
            # if the workench is in the correction list, continue
            if WorkBench in CorrectionList:
                # Get the corresponding toolbar correction list
                ToolBarCorrectionList = CorrectionList[WorkBench]
                # Go through the toolbars of the workbench in the json file                
                for toolbar in self.ribbonStructure["workbenches"][WorkBench]["toolbars"]:
                    for ToolBarToCorrect in ToolBarCorrectionList:
                        # If the toolbars match, update the json file
                        if ToolBarToCorrect[1] == toolbar or ToolBarToCorrect[0] == toolbar:
                            Standard_Functions_Ribbon.add_keys_nested_dict(Dict, ["workbenches", WorkBench, "toolbars", ToolBarToCorrect[1]], endEmpty=True)
                            Dict["workbenches"][WorkBench]["toolbars"][ToolBarToCorrect[1]] = self.ribbonStructure["workbenches"][WorkBench]["toolbars"][toolbar]
                        # if the toolbar doesn't match and is not the order list, just add it
                        if ToolBarToCorrect[1] != toolbar and ToolBarToCorrect[0] != toolbar and toolbar != "order":
                            Standard_Functions_Ribbon.add_keys_nested_dict(Dict, ["workbenches", WorkBench, "toolbars", toolbar], endEmpty=True)
                            Dict["workbenches"][WorkBench]["toolbars"][toolbar] = self.ribbonStructure["workbenches"][WorkBench]["toolbars"][toolbar]
                    # if the toolbar is the order list, update its contents
                    if toolbar == "order":
                        # Get the current orderlist
                        OrderList: list = self.ribbonStructure["workbenches"][WorkBench]["toolbars"]["order"]
                        # Go through the correction list. If the toolbar to correct is in the order list, replace it with the correction                       
                        for ToolBarToCorrect in ToolBarCorrectionList:
                            if ToolBarToCorrect[0] in OrderList:
                                index = OrderList.index(ToolBarToCorrect[0])
                                OrderList[index] = ToolBarToCorrect[1]
                # If the orderlist is not empty, set the orderlist as the new order list in the ribbon structure
                if len(OrderList) > 0:
                    Dict["workbenches"][WorkBench]["toolbars"]["order"] = OrderList
                self.ribbonStructure["workbenches"][WorkBench]["toolbars"] = Dict["workbenches"][WorkBench]["toolbars"]
        
        # Go through the workbenches in the json file to remove old toolbars                   
        for WorkBench in self.ribbonStructure["workbenches"]:
            # if the workench is in the correction list, continue
            if WorkBench in CorrectionList:
                # Get the corresponding toolbar correction list
                ToolBarCorrectionList = CorrectionList[WorkBench]
                for ToolBarToCorrect in ToolBarCorrectionList:
                    if ToolBarToCorrect[0] in self.ribbonStructure["workbenches"][WorkBench]["toolbars"]:
                        self.ribbonStructure["workbenches"][WorkBench]["toolbars"].pop(ToolBarToCorrect[0])

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
        JsonFile = Parameters.RIBBON_STRUCTURE_JSON

        # create a copy and rename it as a backup if enabled
        if Parameters.ENABLE_BACKUP is True:
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
        
        if RestartFreeCAD is True:
            message = translate(
                "FreeCAD Ribbon",
                "The file containing the Ribbon layout is updated.\nYou must restart FreeCAD for changes to take effect.",
            )
            answer = StandardFunctions.RestartDialog(message=message)
            if answer == "yes":
                StandardFunctions.restart_freecad()

        return isConverted

    # endregion

class EventInspector(QObject):
    def __init__(self, parent):
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event: QEvent):
        if event.type() == QEvent.Type.KeyRelease:
            try:
                # Get the main window and the ribbon
                mw = Gui.getMainWindow()
                RibbonBar: ModernMenu = mw.findChild(ModernMenu, "Ribbon")
                
                # Define variables
                Key = ""
                KeyModifier = ""
                StoredShortCutKey_Pin = "Alt+T"
                StoredShortCutKey_MenuBar = "Shift+M"
                
                # if modifiers are set, store its name
                if event.modifiers():                
                    # Get the name of modifier key
                    for keyModifierName, keyModifierItem in Qt.KeyboardModifier._member_map_.items():
                        if event.modifiers() == keyModifierItem:
                            KeyModifier = keyModifierName
                # Get the key name
                for keyName, keyItem in Qt.Key._member_map_.items():
                    if event.key() == keyItem:
                        Key = keyName
                
                # Check if the shortcuts are modified by the user. if so update the variables
                try:
                    CustomShortCuts = App.ParamGet(
                        "User parameter:BaseApp/Preferences/Shortcut"
                    )
                    if "Ribbon_Pin" in CustomShortCuts.GetStrings():
                        StoredShortCutKey_Pin = CustomShortCuts.GetString("Ribbon_Pin") 
                    if "Ribbon_Menubar" in CustomShortCuts.GetStrings():
                        StoredShortCutKey_MenuBar = CustomShortCuts.GetString("Ribbon_Menubar")                   
                except Exception:
                    pass
                            
                # Check if the shortcut for the pin button matches the pressed key and modifier key.
                # If so, use the pin function
                if StoredShortCutKey_Pin.split("+")[0] in KeyModifier:
                    if len(StoredShortCutKey_Pin.split("+")) > 1:
                        if StoredShortCutKey_Pin.split("+")[1] in Key:
                            RibbonBar.on_Pin_clicked()
                            return QObject.eventFilter(self, obj, event)
                else:
                    if StoredShortCutKey_Pin in Key:
                        RibbonBar.on_Pin_clicked()
                        return QObject.eventFilter(self, obj, event)
                
                # Check if the shortcut for the menubar matches the pressed key and modifier key.
                # If so, use the menubar function
                if StoredShortCutKey_MenuBar.split("+")[0] in KeyModifier:
                    if len(StoredShortCutKey_MenuBar.split("+")) > 1:
                        if StoredShortCutKey_MenuBar.split("+")[1] in Key:
                            RibbonBar.ToggleMenuBar()
                            return QObject.eventFilter(self, obj, event)
                else:
                    if StoredShortCutKey_MenuBar in Key:
                        RibbonBar.ToggleMenuBar()
                        return QObject.eventFilter(self, obj, event)
            except Exception:
                return False
        
        if event.type() == QEvent.Type.WindowActivate or event.type() == QEvent.Type.WindowDeactivate:
            mw = Gui.getMainWindow()
            DockWidget_Ribbon: QDockWidget = mw.findChild(QDockWidget, "Ribbon")
            if DockWidget_Ribbon is not None:
                RibbonBar: ModernMenu = mw.findChild(ModernMenu, "Ribbon")
                if DockWidget_Ribbon.isFloating() is False:
                    try:
                        DockWidget_Ribbon.setTitleBarWidget(QWidget())
                    except Exception:
                        pass       
        if event.type() == QEvent.Type.Close:
            OverlayParam_Top = App.ParamGet("User parameter:BaseApp/MainWindow/DockWindows/OverlayTop")
            String = OverlayParam_Top.GetString("Widgets")
            Parameters_Ribbon.Settings.SetStringSetting("StoredOverlayState", String)
            App.saveParameter()                           
            
        if event.type() == QEvent.Type.ApplicationActivated:
            mw = Gui.getMainWindow()
            mw.setWindowState(Qt.WindowState.WindowMaximized)
            Style = mw.style()
            RibbonBar: ModernMenu = mw.findChild(ModernMenu, "Ribbon")
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
        # If the window state changes and the titlebar is hidden, catch the event
        if (event.type() == QEvent.Type.WindowStateChange or event.type() == QEvent.Type.DragMove) and Parameters.HIDE_TITLEBAR_FC is True:            
            # Get the main window, its style, the ribbon and the restore button
            mw = Gui.getMainWindow()
            Style = mw.style()
            RibbonBar: ModernMenu = mw.findChild(ModernMenu, "Ribbon")
            RestoreButton: QToolButton = RibbonBar.rightToolBar().findChildren(QToolButton, "RestoreButton")[0]
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
                # mw.setWindowState(Qt.WindowState.WindowNoState)
                return QObject.eventFilter(self, obj, event)
        # If the event is a modfied event, update the title
        # This is done when switching from one part to another
        if (event.type() == QEvent.Type.ModifiedChange and Parameters.TOOLBAR_POSITION == 0):
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
            ribbon.setContentsMargins(0, 0, 0, 0)
            # Get the layout
            layout = ribbon.layout()
            # Set spacing and content margins to zero
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            # update the layout
            ribbon.setLayout(layout)
            ribbon.setObjectName("Ribbon")
            ribbonDock = QDockWidget()
            # set the name of the object and the window title
            ribbonDock.setObjectName("Ribbon")
            ribbonDock.setWindowTitle("Ribbon")
            # Set the titlebar to an empty widget (effectively hide it)
            ribbonDock.setTitleBarWidget(QWidget())
            ribbonDock.setContentsMargins(0, 0, 0, 0)
            ribbonDock.setWidget(ribbon)
            # Set the allowed areas to dock
            ribbonDock.setAllowedAreas(Qt.DockWidgetArea.TopDockWidgetArea|Qt.DockWidgetArea.BottomDockWidgetArea)
                                                
            # # make sure that there are no negative valules
            if Parameters.AUTOHIDE_RIBBON is True:
                ribbonDock.setMaximumHeight(ribbon.RibbonMinimalHeight)
            # Add the dockwidget to the main window
            mw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, ribbonDock, Qt.Orientation.Horizontal)
            # attach the ribbon to the dockwidget            
            ribbonDock.setEnabled(True)
            ribbonDock.setVisible(True)
            ribbonDock.show()

            return
