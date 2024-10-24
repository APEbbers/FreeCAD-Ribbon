# *************************************************************************
# *                                                                       *
# * Copyright (c) 2024 Paul Ebbers                                        *
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

# This script can be used to generate a list of all commands with their names.
# This list can be updated with custom names for the commands.
# Use "UpdateCommandNames.py" to update the "RibbonStructure.json" with the custom names

import FreeCAD as App
import FreeCADGui as Gui
import os
import json

ParentPath = os.path.dirname(os.path.dirname(__file__))

# Set the path where you want to save this new Json file
# JsonPath = os.path.dirname(__file__)
JsonPath = ParentPath

# Set the file name. Default is "CommandList.json".
# This is the file used to reset the ribbon.
JsonName = "CommandList.json"

# Define list of the workbenches, toolbars and commands on class level
List_Workbenches = []
List_Commands = []

# This is the dict to generate
Dict_CommandNames = {}

# Create lists for the several list in the json file.
List_IgnoredToolbars = [
    "Clipboard",
    "Edit",
    "File",
    "Help",
    "Macro",
    "View",
    "Workbench",
]
List_IconOnlyToolbars = [
    "Structure",
    "Individual views",
]
List_QuickAccessCommands = [
    "Std_New",
    "Std_Open",
    "Std_Save",
    "Std_Undo",
    "Std_Redo",
    "Std_Refresh",
    "Std_Cut",
    "Std_Copy",
    "Std_Paste",
]
List_IgnoredWorkbenches = [
    "Inspection",
    "OpenSCAD",
    "Points",
    "Reverse Engineering",
    "Robot",
    "Test Framework",
]


def main():
    CreateLists()
    CreateCommandList()
    WriteJson()


def CreateLists():
    # Create a list of all workbenches with their icon
    List_Workbenches.clear()
    Workbenches = Gui.listWorkbenches()
    for WorkBenchName in Workbenches:
        if str(WorkBenchName) != "":
            if str(WorkBenchName) != "NoneWorkbench" or WorkBenchName is not None:
                if List_IgnoredWorkbenches.__contains__(WorkBenchName) is False:
                    Icon = None
                    IconName = str(Gui.getWorkbench(WorkBenchName).Icon)
                    if IconName != "":
                        Icon = Gui.getIcon(IconName)
                    WorkbenchTitle = Gui.getWorkbench(WorkBenchName).MenuText
                    List_Workbenches.append([str(WorkBenchName), Icon, WorkbenchTitle])

    # Store the current active workbench
    ActiveWB = Gui.activeWorkbench().name()
    # Create a list of all commands with their icon
    List_Commands.clear()
    # Create a list of command names
    CommandNames = []
    for WorkBenchItem in List_Workbenches:
        WorkBench = Gui.getWorkbench(WorkBenchItem[0])
        if str(WorkBenchItem[0]) != "NoneWorkbench":
            print(WorkBenchItem[0])
            Gui.activateWorkbench(WorkBenchItem[0])
            ToolbarItems = WorkBench.getToolbarItems()
            for key, value in ToolbarItems.items():
                MustBeIgnored = False
                for ToolBar in List_IconOnlyToolbars:
                    if ToolBar == key:
                        MustBeIgnored = True
                for ToolBar in List_IgnoredToolbars:
                    if ToolBar == key:
                        MustBeIgnored = True

                if MustBeIgnored is False:
                    for j in range(len(value)):
                        Item = [value[j], WorkBenchItem[0]]
                        # if CommandNames.__contains__(Item) is False:
                        IsInList = False
                        for k in range(len(CommandNames)):
                            if CommandNames[k][0] == value[j]:
                                IsInList = True
                        if IsInList is False:
                            CommandNames.append(Item)

    # Go through the list
    for CommandName in CommandNames:
        # get the command with this name
        command = Gui.Command.get(CommandName[0])
        WorkBenchName = CommandName[1]
        if command is not None and not List_QuickAccessCommands.__contains__(
            CommandName[0]
        ):
            # get the icon for this command
            if command.getInfo()["pixmap"] != "":
                Icon = Gui.getIcon(command.getInfo()["pixmap"])
            else:
                Icon = None
            MenuName = command.getInfo()["menuText"].replace("&", "")
            List_Commands.append([CommandName[0], Icon, MenuName, WorkBenchName])

    Gui.activateWorkbench(ActiveWB)

    return


def CreateCommandList():
    CommandList = {}
    for CommandItem in List_Commands:
        MustBeIgnored = False
        for Command in List_QuickAccessCommands:
            if Command == CommandItem[0]:
                MustBeIgnored = True

        if MustBeIgnored is False:
            add_keys_nested_dict(CommandList, CommandItem[0])

            WorkBenchName = CommandItem[3]
            MenuName = CommandItem[2]
            Dict_CommandNames[CommandItem[0]] = [WorkBenchName, MenuName, "..."]

    return


def WriteJson():
    # Create a resulting dict
    resultingDict = {}
    resultingDict.update(Dict_CommandNames)

    # get the path for the Json file
    JsonFile = os.path.join(JsonPath, JsonName)

    # Writing to sample.json
    with open(JsonFile, "w") as outfile:
        json.dump(resultingDict, outfile, indent=4)

    outfile.close()


def add_keys_nested_dict(dict, keys):
    for key in keys:
        if key not in dict:
            dict[key] = {}
        dict = dict[key]
    try:
        dict.setdefault(keys[-1], 1)
    except Exception:
        pass
    return


main()
