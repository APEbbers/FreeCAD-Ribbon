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

from PySide.QtGui import QIcon, QAction, QPixmap, QScrollEvent, QKeyEvent, QActionGroup
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
)

import json
import os
import sys
import webbrowser
import LoadDesign_Ribbon
import Parameters_Ribbon
import LoadSettings_Ribbon
import Standard_Functions_RIbbon as StandardFunctions
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

# import modules for keypress detection based on OS
if platform.system() == "Windows" or platform.system() == "Darwin":
    import keyboard_local as keyboard

# Get the main window of FreeCAD
mw = Gui.getMainWindow()

# Define a timer
timer = QTimer()


class ModernMenu(RibbonBar):
    """
    Create ModernMenu QWidget.
    """

    ReproAdress: str = ""

    ribbonStructure = {}

    wbNameMapping = {}
    isWbLoaded = {}

    MainWindowLoaded = False

    UseQtKeyPress = False

    borderColor = ""

    # use icon size from FreeCAD preferences
    iconSize = Parameters_Ribbon.ICON_SIZE_SMALL

    # Set a sixe factor for the buttons
    sizeFactor = 1.3

    def __init__(self):
        """
        Constructor
        """
        super().__init__(title="", iconSize=self.iconSize)
        self.setObjectName("Ribbon")

        # connect the signals
        self.connectSignals()

        # if FreeCAD is version 0.21 create a custom toolbar "Invidual Views"
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

        # Get the adress of the reporisaty adress
        self.ReproAdress = StandardFunctions.getRepoAdress(os.path.dirname(__file__))
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(translate("FreeCAD Ribbon", "FreeCAD Ribbon: ") + self.ReproAdress)

        # Set the icon size if parameters has none
        # Define the icon sizes
        if (
            Parameters_Ribbon.Settings.GetIntSetting("IconSize_Small") is None
            or Parameters_Ribbon.Settings.GetIntSetting("IconSize_Small") == 0
        ):
            Parameters_Ribbon.Settings.SetIntSetting("IconSize_Small", 30)

        if (
            Parameters_Ribbon.Settings.GetIntSetting("IconSize_Medium") is None
            or Parameters_Ribbon.Settings.GetIntSetting("IconSize_Medium") == 0
        ):
            Parameters_Ribbon.Settings.SetIntSetting("IconSize_Medium", 40)

        # read ribbon structure from JSON file
        with open(
            os.path.join(os.path.dirname(__file__), "RibbonStructure.json"), "r"
        ) as file:
            self.ribbonStructure.update(json.load(file))
        file.close()

        # Create the ribbon
        self.createModernMenu()
        self.onUserChangedWorkbench()

        # Set the custom stylesheet
        StyleSheet = Path(Parameters_Ribbon.STYLESHEET).read_text()
        # modify the stylesheet to set the border for a toolbar menu
        #
        # Get the border color
        StandardColors = mw.style().standardPalette()
        rgb = StandardColors.light().color().toTuple()
        hexColor = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
        StyleSheet = StyleSheet.replace(
            "border-left: 0.5px solid;", "border-left: 0.5px solid " + hexColor + ";"
        )
        StyleSheet = StyleSheet.replace(
            "border-top: 0.5px solid;", "border-top: 0.5px solid " + hexColor + ";"
        )
        StyleSheet = StyleSheet.replace(
            "border: 0.5px solid;", "border: 0.5px solid " + hexColor + ";"
        )
        self.setStyleSheet(StyleSheet)

        # get the state of the mainwindow
        self.MainWindowLoaded = True

        # Set these settings and connections at init
        # Set the autohide behavior of the ribbon
        self.setAutoHideRibbon(Parameters_Ribbon.AUTOHIDE_RIBBON)
        # connect the collapsbutton with our own function
        self.collapseRibbonButton().connect(
            self.collapseRibbonButton(),
            SIGNAL("clicked()"),
            self.onCollapseRibbonButton_clicked,
        )

        # Set the menuBar hidden as standard
        mw.menuBar().hide()
        if self.isEnabled() is False:
            mw.menuBar().show()

        # make sure that the ribbon cannot "dissapear"
        if self.ribbonVisible() is False:
            self.setMaximumHeight(45)
        else:
            self.setMaximumHeight(200)

        # ------- Bug when a workbench is activated --------------------------------
        #
        # # Get the keypress when on linux
        # if platform.system() == "Linux" or platform.system() == "Darwin":
        #     self.UseQtKeyPress = True

        # # Get the keypress when on windows or mac
        # if platform.system() == "Windows" or platform.system() == "Darwin":
        #     try:
        #         # connect the alt key to the menuBar
        #         keyboard.on_press_key("alt", lambda _: self.ToggleMenuBar())
        #     except Exception:  # Use Qt incase of an error
        #         self.UseQtKeyPress = True
        #
        # --------------------------------------------------------------------------
        return

    # The backup keypress event
    def keyPressEvent(self, event):
        if self.UseQtKeyPress is True:
            if event.key() == Qt.Key.Key_Alt or event.key() == Qt.Key.Key_AltGr:
                self.ToggleMenuBar()

    # implentation to add actions to the Filemenu. Needed for the accessiores menu
    def addAction(self, action: QAction):
        menu = self.findChild(RibbonMenu, "Ribbon")
        if menu is None:
            menu = self.addFileMenu()
        menu.addAction(action)
        return

    # used to scroll a ribbon horizontal, when it's wider than the screen
    def wheelEvent(self, event):
        x = 0
        # Get the scroll value (1 or -1)
        delta = event.angleDelta().y()
        x += delta and delta // abs(delta)

        # go back or forward based on x.
        if x == 1:
            self.currentCategory()._previousButton.click()
        if x == -1:
            self.currentCategory()._nextButton.click()

        return

    # region - Hover function needed for handling the autohide function of the ribbon
    def enterEvent(self, QEvent):
        TB = mw.findChildren(QDockWidget, "Ribbon")[0]

        if self.ribbonVisible() is False:
            TB.setMaximumHeight(200)
            self.setRibbonVisible(True)
        pass

    def leaveEvent(self, QEvent):
        TB = mw.findChildren(QDockWidget, "Ribbon")[0]

        if self._autoHideRibbon is True:
            TB.setMaximumHeight(45)
            self.setRibbonVisible(False)
        pass

    # endregion

    def connectSignals(self):
        self.tabBar().currentChanged.connect(self.onUserChangedWorkbench)
        mw.workbenchActivated.connect(self.onWbActivated)
        return

    def disconnectSignals(self):
        self.tabBar().currentChanged.disconnect(self.onUserChangedWorkbench)
        mw.workbenchActivated.disconnect(self.onWbActivated)
        return

    def ToggleMenuBar(self):
        wb = Gui.activeWorkbench()
        if wb.name() != "SketcherWorkbench":
            mw = Gui.getMainWindow()
            menuBar = mw.menuBar()
            if menuBar.isVisible() is True:
                menuBar.hide()
                return
            if menuBar.isVisible() is False:
                menuBar.show()
                return

    def createModernMenu(self):
        """
        Create menu tabs.
        """
        # add quick access buttons
        i = 2  # Start value for button count. Used for width of quixkaccess toolbar
        toolBarWidth = (self.iconSize * self.sizeFactor) * i
        for commandName in self.ribbonStructure["quickAccessCommands"]:
            i = i + 1
            width = 0
            button = QToolButton()
            QuickAction = Gui.Command.get(commandName).getAction()

            if len(QuickAction) <= 1:
                button.setDefaultAction(QuickAction[0])
                width = self.iconSize * self.sizeFactor
                button.setMinimumWidth(width)
            elif len(QuickAction) > 1:
                button.addActions(QuickAction)
                button.setDefaultAction(QuickAction[0])
                width = (self.iconSize * self.sizeFactor) + self.iconSize
                button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
                button.setMinimumWidth(width)

            # Add the button to the quickaccess toolbar
            self.addQuickAccessButton(button)

            toolBarWidth = toolBarWidth + width

        # Set the height of the quickaccess toolbar
        self.quickAccessToolBar().setMaximumHeight(self.iconSize * self.sizeFactor)
        # Set the width of the quickaccess toolbar.
        self.quickAccessToolBar().setMinimumWidth(toolBarWidth)
        # Set the size policy
        self.quickAccessToolBar().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Get the order of workbenches from Parameters
        WorkbenchOrderParam = "User parameter:BaseApp/Preferences/Workbenches/"
        WorkbenchOrderedList: list = (
            App.ParamGet(WorkbenchOrderParam).GetString("Ordered").split(",")
        )
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
        # when assembly4 wb is installed and positioned for the internal assemmbly wb
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
            param_string = param_string + "," + WorkbenchOrderedList[i]
        Parameters_Ribbon.Settings.SetStringSetting(
            WorkbenchOrderParam + "/Ordered", param_string
        )

        # add category for each workbench
        for i in range(len(WorkbenchOrderedList)):
            for workbenchName, workbench in list(Gui.listWorkbenches().items()):
                if workbenchName == WorkbenchOrderedList[i]:
                    name = workbench.MenuText
                    if (
                        name != ""
                        and name not in self.ribbonStructure["ignoredWorkbenches"]
                        and name != "<none>"
                    ):
                        self.wbNameMapping[name] = workbenchName
                        self.isWbLoaded[name] = False

                        self.addCategory(name)
                        # set tab icon
                        self.tabBar().setTabIcon(
                            len(self.categories()) - 1, QIcon(workbench.Icon)
                        )

        # Set the font size of the ribbon tab titles
        self.tabBar().font().setPointSizeF(10)
        self.tabBar().setFixedHeight(self.iconSize * self.sizeFactor)

        # Set the size of the collpseRibbonButton
        self.collapseRibbonButton().setFixedSize(self.iconSize, self.iconSize)

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

        # Add a button the enable or disable AutoHide
        pixmap = QPixmap(os.path.join(pathIcons, "pin-icon-open.svg"))
        pinIcon = QIcon()
        pinIcon.addPixmap(pixmap)
        pinButton = QToolButton()
        pinButton.setCheckable(True)
        pinButton.setIcon(pinIcon)
        pinButton.setText(translate("FreeCAD Ribbon", "Pin Ribbon"))
        pinButton.setToolTip(
            translate(
                "FreeCAD Ribbon", "Click to toggle the autohide function on or off"
            )
        )
        pinButton.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
            pinButton.setChecked(False)
        if Parameters_Ribbon.AUTOHIDE_RIBBON is False:
            pinButton.setChecked(True)
        pinButton.clicked.connect(self.onPinClicked)
        self.rightToolBar().addWidget(pinButton)

        # Set the widht of the right toolbar
        i = len(self.rightToolBar().actions())
        self.rightToolBar().setMinimumWidth(self.iconSize * self.sizeFactor * i)
        self.rightToolBar().setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Set the application button
        self.applicationOptionButton().setMinimumWidth(self.iconSize * self.sizeFactor)
        self.setApplicationIcon(Gui.getIcon("freecad"))
        self.applicationOptionButton().setToolTip(
            translate("FreeCAD Ribbon", "FreeCAD Ribbon")
        )

        # add the menus from the menubar to the application button
        self.ApplicationMenu()

        return

    def ApplicationMenu(self):
        Menu = self.addFileMenu()

        # add the menus from the menubar to the application button
        MenuBar = mw.menuBar()
        Menu.addActions(MenuBar.actions())

        # Add the ribbon design button
        Menu.addSeparator()
        DesignMenu = Menu.addMenu(translate("FreeCAD Ribbon", "Customize..."))
        DesignButton = DesignMenu.addAction(
            translate("FreeCAD Ribbon", "Ribbon Design")
        )
        DesignButton.triggered.connect(self.loadDesignMenu)
        # Add the preference button
        PreferenceButton = DesignMenu.addAction(
            translate("FreeCAD Ribbon", "Ribbon Preferences")
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
        # Add a about button for this ribbon
        # Get the version of this addon
        PackageXML = os.path.join(os.path.dirname(__file__), "package.xml")
        version = StandardFunctions.ReturnXML_Value(PackageXML, "version")

        Menu.addSeparator()
        AboutButton = Menu.addAction(
            translate("FreeCAD Ribbon", "About FreeCAD Ribbon ") + version
        )
        AboutButton.triggered.connect(self.on_AboutButton_clicked)

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
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            AboutAdress = self.ReproAdress + "wiki"
            webbrowser.open(AboutAdress, new=2, autoraise=True)
        return

    def onCollapseRibbonButton_clicked(self):
        # Get the ribbon
        TB = mw.findChildren(QDockWidget, "Ribbon")[0]

        # Set the height based on visibility of the ribbon
        if self.ribbonVisible() is False:
            TB.setMaximumHeight(45)
        else:
            TB.setMaximumHeight(200)

        return

    def onPinClicked(self):
        if self._autoHideRibbon is True:
            self.setAutoHideRibbon(False)
            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", False)
            self.onCollapseRibbonButton_clicked()
            return
        if self._autoHideRibbon is False:
            self.setAutoHideRibbon(True)
            Parameters_Ribbon.Settings.SetBoolSetting("AutoHideRibbon", True)
            self.onCollapseRibbonButton_clicked()
            return

        return

    def onUserChangedWorkbench(self):
        """
        Import selected workbench toolbars to ModernMenu section.
        """

        index = self.tabBar().currentIndex()
        tabName = self.tabBar().tabText(index)
        category = self.currentCategory()
        category

        # activate selected workbench
        tabName = tabName.replace("&", "")
        Gui.activateWorkbench(self.wbNameMapping[tabName])
        self.onWbActivated()
        self.ApplicationMenu()
        return

    def onWbActivated(self):
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

            # wait for 0.1s hoping that after that time the workbench is loaded
            timer.timeout.connect(self.onWbActivated)
            timer.setSingleShot(True)
            timer.start(100)
            return

        # create panels
        self.buildPanels()
        return

    def buildPanels(self):
        # Get the active workbench and get tis name
        workbench = Gui.activeWorkbench()
        workbenchName = workbench.name()

        # check if the panel is already loaded. If so exit this function
        tabName = self.tabBar().tabText(self.tabBar().currentIndex()).replace("&", "")
        if self.isWbLoaded[tabName]:
            return

        # Get the list of toolbars from the active workbench
        ListToolbars: list = workbench.listToolbars()
        if int(App.Version()[0]) == 0 and int(App.Version()[1]) <= 21:
            ListToolbars.append("Individual views")
        # Get custom toolbars that are created in the toolbar enviroment and add them to the list of toolbars
        CustomToolbars = self.List_ReturnCustomToolbars()
        for CustomToolbar in CustomToolbars:
            if CustomToolbar[1] == workbenchName:
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
            panel = self.currentCategory().addPanel(
                title=toolbar,
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
            NoSmallButtons = 0  # needed to count the number of small buttons in a column. (bug fix with adding separators)
            NoMediumButtons = 0  # needed to count the number of medium buttons in a column. (bug fix with adding separators)

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
                        NoSmallButtons += 1
                    if buttonSize == "medium":
                        NoMediumButtons += 1
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

                # If the number of rows devided by 3 is a whole number,
                # the number of columns is the rowcount devided by 3.
                columnCount = rowCount / 3
                # ----------------------------------------------------------------------------------------

                # if the button has not text, remove it, skipp it and increase the counter.
                if button.text() == "":
                    continue
                # If the command is already there, remove it, skipp it and increase the counter.
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
                        if float((NoSmallButtons + 1) / 3).is_integer():
                            panel.addSmallButton().setEnabled(False)
                        if float((NoSmallButtons + 2) / 3).is_integer():
                            panel.addSmallButton().setEnabled(False)
                            panel.addSmallButton().setEnabled(False)
                        # reset the counter after a separator is added.
                        NoSmallButtons = 0
                        # Same principle for medium buttons
                        if float((NoMediumButtons + 1) / 2).is_integer():
                            panel.addMediumButton().setEnabled(False)
                        NoMediumButtons = 0
                        continue
                    else:
                        try:
                            action = button.defaultAction()

                            # try to get alternative text from ribbonStructure
                            try:
                                text = self.ribbonStructure["workbenches"][
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
                                    text = "Create sketch"

                                # the text would be overwritten again when the state of the action changes
                                # (e.g. when getting enabled / disabled), therefore the action itself
                                # is manipulated.
                                action.setText(text)
                            except KeyError:
                                text = action.text()

                            if action.icon() is None:
                                commandName = self.ribbonStructure["workbenches"][
                                    workbenchName
                                ]["toolbars"][toolbar]["commands"][action.data()]
                                command = Gui.Command.get(commandName)
                                action.setIcon(Gui.getIcon(command.getInfo()["pixmap"]))

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
                                if Parameters_Ribbon.SHOW_ICON_TEXT_SMALL is False:
                                    btn.setMinimumWidth(
                                        Parameters_Ribbon.ICON_SIZE_SMALL
                                        + self.iconSize
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
                                if Parameters_Ribbon.SHOW_ICON_TEXT_MEDIUM is False:
                                    btn.setMinimumWidth(
                                        Parameters_Ribbon.ICON_SIZE_MEDIUM
                                        + self.iconSize
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
                                    fixedHeight=False,
                                )
                                btn.setMinimumWidth(btn.maximumHeight() + 10)
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
                                btn.setMinimumWidth(btn.height + 20)
                                btn.setDefaultAction(btn.actions()[0])

                            # add the button text to the shadowList for checking if buttons are already there.
                            shadowList.append(button.text())

                        except Exception as e:
                            if Parameters_Ribbon.DEBUG_MODE is True:
                                print(f"{e.with_traceback(None)}, 2")
                            continue

            # remove any suffix from the panel title
            if panel.title().endswith("_custom"):
                panel.setTitle(panel.title().replace("_custom", ""))

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
                # Set the standard toolbutton arrow instead of pyqt's symbol
                OptionButton.setArrowType(Qt.ArrowType.DownArrow)
                OptionButton.setToolButtonStyle(
                    Qt.ToolButtonStyle.ToolButtonTextBesideIcon
                )
                # Remove the image to avoid double arrows
                OptionButton.setStyleSheet(
                    "RibbonPanelOptionButton::menu-indicator {image: none;}"
                )
                # Set the optionbutton text
                OptionButton.setText("more...")

            # Set the margings. In linux seems the style behavior different than on Windows
            Layout = panel.layout()
            Layout.setContentsMargins(3, 3, 3, 3)

        self.isWbLoaded[tabName] = True

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
            if toolbar.objectName() not in [
                "",
                "draft_status_scale_widget",
                "draft_snap_widget",
            ]:
                toolbar.hide()
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
                    MenuText = Command.getInfo()["menuText"]

                    if MenuText == key:
                        try:
                            # Get the original toolbar as QToolbar
                            OriginalToolBar = mw.findChild(QToolBar, value)
                            # Go through all it's QtoolButtons
                            for Child in OriginalToolBar.findChildren(QToolButton):
                                # If the text of the QToolButton matches the menu text
                                # Add it to the button list.
                                if Child.text() == MenuText:
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
            # Disable connection after activation
            mw.workbenchActivated.disconnect(run)
            if disable:
                return

            ribbon = ModernMenu()
            ribbonDock = QDockWidget()
            # set the name of the object and the window title
            ribbonDock.setObjectName("Ribbon")
            ribbonDock.setWindowTitle("Ribbon")
            # Set the titlebar to an empty widget (effectivly hide it)
            ribbonDock.setTitleBarWidget(QWidget())
            # attach the ribbon to the dockwidget
            ribbonDock.setWidget(ribbon)

            if Parameters_Ribbon.AUTOHIDE_RIBBON is True:
                ribbonDock.setMaximumHeight(45)

            # Add the dockwidget to the main window
            mw.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, ribbonDock)

    def on_hovered(self, ribbonDock: QDockWidget):
        ribbonDock.setMaximumHeight(200)
