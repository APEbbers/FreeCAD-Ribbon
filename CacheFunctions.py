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
from PySide.QtGui import QIcon, QPixmap, QAction, QGuiApplication
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
    QLineEdit,
    QSizePolicy,
    QRadioButton,
    QLabel,
    QProgressBar,
)
from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread, QSize, QEvent
import sys
import json
from datetime import datetime
import shutil
import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Standard_Functions_Ribbon as StandardFunctions
from Standard_Functions_Ribbon import CommandInfoCorrections
import Parameters_Ribbon
import Serialize_Ribbon
import webbrowser
import StyleMapping_Ribbon

# Get the resources
ConfigDirectory = Parameters_Ribbon.CONFIG_DIR
pathIcons = Parameters_Ribbon.ICON_LOCATION
pathStylSheets = Parameters_Ribbon.STYLESHEET_LOCATION
pathUI = Parameters_Ribbon.UI_LOCATION
pathScripts = os.path.join(ConfigDirectory, "Scripts")
pathPackages = os.path.join(os.path.dirname(__file__), "Resources", "packages")
pathBackup = Parameters_Ribbon.BACKUP_LOCATION
sys.path.append(ConfigDirectory)
sys.path.append(pathIcons)
sys.path.append(pathStylSheets)
sys.path.append(pathUI)
sys.path.append(pathPackages)
sys.path.append(pathBackup)


# Define the translation
translate = App.Qt.translate

ReproAdress: str = ""

IsChanged = False

# Set the data file version. Triggeres an question if an update is needed
DataFileVersion = "1.3"

# Define list of the workbenches, toolbars and commands on class level
List_Workbenches = []
StringList_Toolbars = []
List_WorkBenchToolBarItems = []
List_Commands = []

# Create lists for the several list in the json file.
List_IgnoredToolbars = []
List_IconOnly_Toolbars = []
List_QuickAccessCommands = []
List_IgnoredWorkbenches = []
Dict_RibbonCommandPanel = {}
Dict_CustomToolbars = {}
Dict_DropDownButtons = {}
Dict_NewPanels = {}

List_IgnoredToolbars_internal = []

# Create the lists for the deserialized icons
List_CommandIcons = []
List_WorkBenchIcons = []

# Create a tomporary list for newly added dropdown buttons
newDDBList = []

def CreateCache(resetTexts=False, RestartFreeCAD=False):
    # Create a progressbar
    progressBar = QProgressBar(minimum=0, value=0)
    progressBar.setWindowFlags(
        Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
    )
    progressBar.setWindowFlag(Qt.WindowType.CustomizeWindowHint, True)
    progressBar.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, False)
    progressBar.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
    progressBar.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
    progressBar.setMinimumSize(400, 20)

    # Get the stylesheet from the main window and use it for this form
    (
        progressBar.setStyleSheet(
            "background-color: "
            + "none"
            + ";color: "
            + "none"
            + ";"
        )
    )
    progressBar.setMaximum(5)
    progressBar.setValue(0)

    # Load the workbenches
    loadAllWorkbenches(
        AutoHide=False,
        FinishMessage=translate(
            "FreeCAD Ribbon", "Ribbon UI: Data file is created."
        ),
        progressBar=progressBar,
        maximum=progressBar.maximum(),
    )

    # clear the lists first
    StringList_Toolbars.clear()
    List_Commands.clear()

    # get the system language
    FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/General")
    FCLanguage = FreeCAD_preferences.GetString("Language")

    # --- Workbenches ----------------------------------------------------------------------------------------------
    #
    # Create a list of all workbenches with their icon
    progressBar.setFormat(translate("FreeCAD Ribbon", "Create workbench list"))
    progressBar.setValue(progressBar.value() + 1)
    #
    List_Workbenches.clear()
    for WorkBenchName in Gui.listWorkbenches():
        try:
            if str(WorkBenchName) != "" or WorkBenchName is not None:
                if str(WorkBenchName) != "NoneWorkbench":
                    # Gui.activateWorkbench(WorkBenchName)
                    WorkBench = Gui.getWorkbench(WorkBenchName)
                    # Get the toolbar items
                    ToolbarItems: dict = WorkBench.getToolbarItems()
                    # Update the toolbar items with corrections
                    ToolbarItems: dict = StandardFunctions.CorrectGetToolbarItems(
                        ToolbarItems
                    )

                    IconName = ""
                    IconName = str(Gui.getWorkbench(WorkBenchName).Icon)
                    WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
                    WorkbenchTitleTranslated = StandardFunctions.TranslationsMapping(
                        WorkBenchName, WorkbenchTitle
                    )
                    List_Workbenches.append(
                        [
                            str(WorkBenchName),
                            IconName,
                            WorkbenchTitle,
                            ToolbarItems,
                            WorkbenchTitleTranslated,
                        ]
                    )
        except Exception:
            pass

    # --- Toolbars ----------------------------------------------------------------------------------------------
    #
    # Go through the list of workbenches
    progressBar.setFormat(translate("FreeCAD Ribbon", "Create toolbar list"))
    progressBar.setValue(progressBar.value() + 1)
    #
    i = 0
    for WorkBench in List_Workbenches:
        wbToolbars = []
        if (
            WorkBench[0] != "General"
            and WorkBench[0] != ""
            and WorkBench[0] is not None
        ):
            # Gui.activateWorkbench(WorkBench[0])
            wbToolbars = Gui.getWorkbench(WorkBench[0]).listToolbars()
            # Go through the toolbars
            for Toolbar in wbToolbars:
                ToolBarTtranslated = StandardFunctions.TranslationsMapping(
                    WorkBench[0], Toolbar
                )
                StringList_Toolbars.append(
                    [Toolbar, WorkBench[2], WorkBench[0], ToolBarTtranslated]
                )

    # Add the custom toolbars
    CustomToolbars = List_ReturnCustomToolbars()
    for Customtoolbar in CustomToolbars:
        StringList_Toolbars.append(Customtoolbar)
    CustomToolbars = List_ReturnCustomToolbars_Global()
    for Customtoolbar in CustomToolbars:
        StringList_Toolbars.append(Customtoolbar)

    # --- Commands ----------------------------------------------------------------------------------------------
    #
    # Create a list of all commands with their icon
    progressBar.setFormat(translate("FreeCAD Ribbon", "Create command list"))
    progressBar.setValue(progressBar.value() + 1)
    #
    List_Commands.clear()
    # Create a list of command names
    CommandNames = []
    for i in range(len(List_Workbenches)):
        # Gui.activateWorkbench(List_Workbenches[i][0])
        WorkBench = Gui.getWorkbench(List_Workbenches[i][0])
        WorkBenchName = List_Workbenches[i][0]
        # Get the toolbar items
        ToolbarItems: dict = WorkBench.getToolbarItems()
        # Update the toolbar items with corrections
        ToolbarItems: dict = StandardFunctions.CorrectGetToolbarItems(ToolbarItems)

        for key, value in list(ToolbarItems.items()):
            for j in range(len(value)):
                if value[j] != "Std_Workbench":
                    if value[j].startswith("Std_"):
                        Item = [value[j], "Standard"]
                    else:
                        Item = [value[j], WorkBenchName]
                    IsInList = False
                    for CommandNamesItem in CommandNames:
                        if CommandNamesItem == Item:
                            IsInList = True
                            break
                    if IsInList is False:
                        CommandNames.append(Item)
        # Add commands that are not in any toolbars
        for commandNamesItem in Gui.listCommands():            
            if commandNamesItem.lower().startswith("std_"):
                inList = False
                for CommandName in CommandNames:
                    if CommandName[0] == commandNamesItem:
                        inList = True
                
                # Skip "Std_Workbench".
                if commandNamesItem == "Std_Workbench":
                    continue
                
                if inList is False:                    
                    CommandNames.append([commandNamesItem, "Standard"])
            else:
                inList = False
                for CommandName in CommandNames:
                    if CommandName[0] == commandNamesItem:
                        inList = True
                
                if inList is False:
                    WorkBench = ""
                    for WorkBenchName in List_Workbenches:
                        if commandNamesItem.startswith(WorkBenchName) or WorkBenchName.startswith(commandNamesItem.split("_")[0]):
                            WorkBench = WorkBenchName
                            break
                    if len(commandNamesItem.split(", ")) > 1:
                        Command = Gui.Command.get(commandNamesItem.split(", ")[0])
                        i = int(commandNamesItem.split(", ")[1])
                        action = Command.getAction()[i]
                        Command = Gui.Command.get(action.objectName())
                        commandNamesItem = action.objectName()
                    Icon = StandardFunctions.returnQiCons_Commands(commandNamesItem)
                    if Icon is not None or Icon.isNull() is False:
                        CommandNames.append([commandNamesItem, WorkBench])

    # Go through the list
    for CommandName in CommandNames:
        # get the command with this name
        command = Gui.Command.get(CommandName[0])
        ChildCommands = returnDropDownCommands(command)
        WorkBenchName = CommandName[1]
        if command is not None:
            # get the icon for this command
            if CommandInfoCorrections(CommandName[0])["pixmap"] != "":
                IconName = CommandInfoCorrections(CommandName[0])["pixmap"]
            else:
                IconName = ""
            MenuName = CommandInfoCorrections(CommandName[0])["menuText"].replace(
                "&", ""
            )
            MenuNameTranslated = CommandInfoCorrections(CommandName[0])[
                "ActionText"
            ].replace("&", "")
            if len(ChildCommands) > 1:
                if not MenuName.endswith("..."):
                    MenuName = MenuName + "..."
                if not MenuNameTranslated.endswith("..."):
                    MenuNameTranslated = MenuNameTranslated + "..."

            List_Commands.append(
                [
                    CommandName[0],
                    IconName,
                    MenuName,
                    WorkBenchName,
                    MenuNameTranslated,
                ]
            )
            # Add children of the commands if there are any
            if len(ChildCommands) > 0:
                for childCommand in ChildCommands:
                    List_Commands.append(
                        [
                            childCommand[0],
                            childCommand[1],
                            childCommand[2],
                            WorkBenchName,
                            childCommand[3],
                        ]
                    )

    # add also custom commands
    Toolbars = List_ReturnCustomToolbars()
    for Toolbar in Toolbars:
        WorkbenchTitle = Toolbar[1]
        for WorkBench in List_Workbenches:
            if WorkbenchTitle == WorkBench[2]:
                WorkBenchName = WorkBench[0]
                for CustomCommand in Toolbar[2]:
                    command = Gui.Command.get(CustomCommand)
                    if CommandInfoCorrections(CustomCommand)["pixmap"] != "":
                        IconName = CommandInfoCorrections(CustomCommand)["pixmap"]
                    else:
                        IconName = ""
                    MenuName = CommandInfoCorrections(CustomCommand)[
                        "menuText"
                    ].replace("&", "")
                    MenuNameTranslated = CommandInfoCorrections(CustomCommand)[
                        "ActionText"
                    ].replace("&", "")
                    List_Commands.append(
                        [
                            CustomCommand,
                            IconName,
                            MenuName,
                            WorkBenchName,
                            MenuNameTranslated,
                        ]
                    )
    Toolbars = List_ReturnCustomToolbars_Global()
    for Toolbar in Toolbars:
        for CustomCommand in Toolbar[2]:
            command = Gui.Command.get(CustomCommand)
            if CommandInfoCorrections(CustomCommand)["pixmap"] != "":
                IconName = CommandInfoCorrections(CustomCommand)["pixmap"]
            else:
                IconName = None
            MenuName = CommandInfoCorrections(CustomCommand)["menuText"].replace(
                "&", ""
            )
            MenuNameTranslated = CommandInfoCorrections(CustomCommand)[
                "ActionText"
            ].replace("&", "")
            List_Commands.append(
                [CustomCommand, IconName, MenuName, Toolbar[1], MenuNameTranslated]
            )
    # Add general commands
    if int(App.Version()[0]) > 0:
        ListCommands = [
            "Std_Measure",
            "Std_ViewZoomOut",
            "Std_ViewZoomIn",
            "Std_ViewBoxZoom",
            "Part_SelectFilter",
            "Std_UnitsCalculator",
            "Std_Properties",
            "Std_BoxElementSelection",
            "Std_BoxSelection",
        ]
        for CommandName in ListCommands:
            command = Gui.Command.get(CommandName)
            if CommandInfoCorrections(CommandName)["pixmap"] != "":
                IconName = CommandInfoCorrections(CommandName)["pixmap"]
            else:
                IconName = ""
            MenuName = CommandInfoCorrections(CommandName)["menuText"].replace(
                "&", ""
            )
            MenuNameTranslated = CommandInfoCorrections(CommandName)[
                "ActionText"
            ].replace("&", "")
            List_Commands.append(
                [CommandName, IconName, MenuName, "Standard", MenuNameTranslated]
            )

    # # re-activate the workbench that was stored.
    # Gui.activateWorkbench(ActiveWB)

    # --- Serialize Icons ------------------------------------------------------------------------------------------
    #
    progressBar.setFormat(translate("FreeCAD Ribbon", "Serialize icons"))
    progressBar.setValue(progressBar.value() + 1)
    #
    WorkbenchIcon = []
    for WorkBenchItem in List_Workbenches:
        WorkBenchName = WorkBenchItem[0]
        Icon = Gui.getIcon(WorkBenchItem[1])
        if Icon is not None and Icon.isNull() is False:
            try:
                SerializedIcon = Serialize_Ribbon.serializeIcon(Icon)

                WorkbenchIcon.append([WorkBenchName, SerializedIcon])
                # add the icons also to the deserialized list
                List_WorkBenchIcons.append([WorkBenchName, Icon])
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    StandardFunctions.Print(
                        f"{e.with_traceback(e.__traceback__)}", "Warning"
                    )

    CommandIcons = []
    for CommandItem in List_Commands:
        CommandName = CommandItem[0]
        Icon = StandardFunctions.returnQiCons_Commands(CommandName, CommandItem[1])
        if Icon is not None and Icon.isNull() is False:
            try:
                SerializedIcon = Serialize_Ribbon.serializeIcon(Icon)

                CommandIcons.append([CommandName, SerializedIcon])
                # add the icons also to the deserialized list
                List_CommandIcons.append([CommandName, Icon])
            except Exception as e:
                if Parameters_Ribbon.DEBUG_MODE is True:
                    StandardFunctions.Print(
                        f"{e.with_traceback(e.__traceback__)}", "Warning"
                    )

    # Write the lists to a data file
    progressBar.setFormat(translate("FreeCAD Ribbon", "Write data files"))
    progressBar.setValue(progressBar.value() + 1)
    #
    # clear the data file. If not exists, create it
    DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
    open(DataFile, "w").close()

    # Open de data file, load it as json and then close it again
    Data = {}
    # Update the data
    Data["dataVersion"] = DataFileVersion
    Data["Language"] = FCLanguage
    Data["List_Workbenches"] = List_Workbenches
    Data["StringList_Toolbars"] = StringList_Toolbars
    Data["List_Commands"] = List_Commands
    Data["WorkBench_Icons"] = WorkbenchIcon
    Data["Command_Icons"] = CommandIcons
    # Write to the data file
    DataFile = os.path.join(ConfigDirectory, "RibbonDataFile.dat")
    with open(DataFile, "w") as outfile:
        json.dump(Data, outfile, indent=4)
    outfile.close()

    # Write a second data file with the list of commands, Language and data version only
    Data2 = {}
    Data2["dataVersion"] = DataFileVersion
    Data2["Language"] = FCLanguage
    Data2["List_Commands"] = List_Commands
    # Write to the data file
    DataFile2 = os.path.join(ConfigDirectory, "RibbonDataFile2.dat")
    with open(DataFile2, "w") as outfile:
        json.dump(Data2, outfile, indent=4)
    outfile.close()

    # Write a time stamp to preferences
    TimeStamp = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
    Parameters_Ribbon.Settings.SetStringSetting("ReloadTimeStamp", TimeStamp)

    if RestartFreeCAD is True:
        result = StandardFunctions.RestartDialog(includeIcons=True)
        if result == "yes":
            StandardFunctions.restart_freecad()
    # show the dialog
    progressBar.close()
    return


# region - helper functions

def List_ReturnCustomToolbars():
    """
    Returns custom toolbars as a list.
    each item is a list with:
    [
        Name,
        Workbench Title,
        List of commands
    ]
    """
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = []

    List_Workbenches = Gui.listWorkbenches().copy()
    for WorkBenchName in List_Workbenches:
        WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
        if str(WorkBenchName) != "" or WorkBenchName is not None:
            if str(WorkBenchName) != "NoneWorkbench":
                # Get the custom toolbars for this workbench
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

                    ListCommands = []
                    try:
                        # get list of all buttons in toolbar
                        TB = mw.findChildren(QToolBar, Name)
                        allButtons: list = TB[0].findChildren(QToolButton)
                        for button in allButtons:
                            if button.text() == "":
                                continue

                            action = button.defaultAction()
                            if action is not None:
                                Command = action.objectName()
                                ListCommands.append(Command)

                        Toolbars.append([Name, WorkbenchTitle, ListCommands, Name])
                    except Exception:
                        continue

    return Toolbars

def List_ReturnCustomToolbars_Global():
    """
    Returns custom toolbars as a list.
    each item is a list with:
    [
        Name,
        Workbench Title,
        List of commands
    ]
    """
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = []

    # Get the custom toolbars for this workbench
    CustomToolbars: list = App.ParamGet(
        "User parameter:BaseApp/Workbench/Global/Toolbar"
    ).GetGroups()

    for Group in CustomToolbars:
        Parameter = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
        )
        Name = Parameter.GetString("Name")

        ListCommands = []
        # get list of all buttons in toolbar
        try:
            TB = mw.findChildren(QToolBar, Name)
            allButtons: list = TB[0].findChildren(QToolButton)
            for button in allButtons:
                if button.text() == "":
                    continue

                action = button.defaultAction()
                if action is not None:
                    Command = action.objectName()
                    ListCommands.append(Command)

            Toolbars.append([Name, "Global", ListCommands, Name])
        except Exception:
            continue

    return Toolbars

def Dict_ReturnCustomToolbars(WorkBenchName):
    """_summary_

    Args:
        WorkBenchName (string): the internal name of the workbench

    Returns:
        dict: a dict with the toolbar name as key and a list of commandnames as value
    """
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = {}

    if str(WorkBenchName) != "" or WorkBenchName is not None:
        if str(WorkBenchName) != "NoneWorkbench":
            # Get the custom toolbars for this workbench
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

                if Name != "":
                    ListCommands = []
                    # get list of all buttons in toolbar
                    try:
                        TB = mw.findChildren(QToolBar, Name)
                        allButtons: list = TB[0].findChildren(QToolButton)
                        for button in allButtons:
                            if button.text() == "":
                                continue
                            action = button.defaultAction()
                            Command = action.objectName()
                            ListCommands.append(Command)

                            Toolbars[Name] = ListCommands
                    except Exception:
                        continue

    return Toolbars

def Dict_ReturnCustomToolbars_Global():
    """_summary_
    Returns:
        dict: a dict with the toolbar name as key and a list of commandnames as value
    """
    # Get the main window of FreeCAD
    mw = Gui.getMainWindow()
    Toolbars = {}

    # Get the custom toolbars for this workbench
    CustomToolbars: list = App.ParamGet(
        "User parameter:BaseApp/Workbench/Global/Toolbar"
    ).GetGroups()

    for Group in CustomToolbars:
        Parameter = App.ParamGet(
            "User parameter:BaseApp/Workbench/Global/Toolbar/" + Group
        )
        Name = Parameter.GetString("Name")

        IsIgnored = False
        for ToolBar in List_IgnoredToolbars:
            if ToolBar == Name:
                IsIgnored = True

        if Name != "" and IsIgnored is False:
            ListCommands = []
            # get list of all buttons in toolbar
            TB = mw.findChildren(QToolBar, Name)
            allButtons: list = TB[0].findChildren(QToolButton)
            for button in allButtons:
                if button.text() == "":
                    continue
                action = button.defaultAction()
                Command = action.objectName()
                ListCommands.append(Command)
                Toolbars[Name] = ListCommands

    return Toolbars

def returnWorkBenchToolbars(WorkBenchName):
    wbToolbars = []
    try:
        for ToolbarItem in StringList_Toolbars:
            if ToolbarItem[2] == WorkBenchName:
                wbToolbars.append(ToolbarItem[0])
    except Exception:
        Gui.activateWorkbench(WorkBenchName)
        wbToolbars: list = Gui.getWorkbench(WorkBenchName).listToolbars()
    return wbToolbars

def returnToolbarCommands(WorkBenchName):
    try:
        for item in List_Workbenches:
            if item[0] == WorkBenchName:
                return item[3]
    except Exception:
        Gui.activateWorkbench(WorkBenchName)
        Toolbars = Gui.getWorkbench(WorkBenchName).getToolbarItems()
        return Toolbars

def returnDropDownCommands(command):
    Commands = []
    if command is not None:
        if len(command.getAction()) > 1:
            for i in range(len(command.getAction()) - 1):
                action = command.getAction()[i]
                if action is not None and (
                    action.icon() is not None and not action.icon().isNull()
                ):
                    Commands.append(
                        [
                            f"{command.getInfo()['name']}, {i}",
                            "actionIcon",
                            action.text(),
                            action.text(),
                        ]
                    )
    return Commands

def loadAllWorkbenches(AutoHide=True, HideOnly=False, FinishMessage="", progressBar: QProgressBar = None, maximum = 0):        
    if HideOnly is False:
        activeWorkbench = Gui.activeWorkbench().name()
        progressBar.show()
        lst = Gui.listWorkbenches()
        progressBar.setMaximum(len(lst) - 1 + maximum)
        for i, wb in enumerate(lst):
            msg = (
                translate("FreeCAD Ribbon", "Loading workbench ")
                + wb
                + " ("
                + str(i + 1)
                + "/"
                + str(len(lst))
                + ")"
            )
            print(msg)
            progressBar.setFormat(msg)
            progressBar.setValue(i)
            Gui.updateGui()  # Probably slower with this, because it redraws the entire GUI with all tool buttons changed etc. but allows the label to actually be updated, and it looks nice and gives a quick overview of all the workbenches…
            try:
                Gui.activateWorkbench(wb)
                List_Workbenches.append(wb)
            except Exception:
                pass
        if FinishMessage != "":
            print(FinishMessage)
        Gui.activateWorkbench(activeWorkbench)
  
        return
# endregion---------------------------------------------------------------------------------------
