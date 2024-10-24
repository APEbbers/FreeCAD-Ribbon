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

# This script can be used to update "RibbonStructure.json" with modified command text from CommandList.json.
# An backup will be created in the folder ../Backupss


import FreeCAD as App
import FreeCADGui as Gui
import os
import json
from datetime import datetime
import shutil

ParentPath = os.path.dirname(os.path.dirname(__file__))

# Set the path where you want to save this new Json file
# JsonPath = os.path.dirname(__file__)
JsonPath = ParentPath

# Set the file name. Default is "RibbonStructure.json".
# This is the file used to reset the ribbon.
JsonName = "RibbonStructure.json"

# Define list of the workbenches, toolbars and commands on class level
List_Workbenches = []
Dict_Commands = {}
Dict_RibbonCommandPanel = {}


def main():
    ReadJson()
    ReadCommands()
    UpdateCommands()
    WriteJson()


def ReadJson():
    """Read the Json file and fill the lists and set settings"""
    # Open the JsonFile and load the data
    JsonFile = open(os.path.join(JsonPath, "RibbonStructure.json"))
    data = json.load(JsonFile)

    # Create a backup file
    OriginalPath = os.path.join(JsonPath, "RibbonStructure.json")
    Suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    BackupName = f"RibbonStructure_{Suffix}.json"
    pathBackup = os.path.dirname(__file__) + "/Backups"
    if os.path.exists(pathBackup) is False:
        os.makedirs(pathBackup)
    BackupFile = os.path.join(pathBackup, BackupName)
    shutil.copy(OriginalPath, BackupFile)

    # Get the dict with the customized date for the buttons
    try:
        Dict_RibbonCommandPanel["workbenches"] = data["workbenches"]
    except Exception as e:
        print(e)
        pass

    JsonFile.close()
    return


def ReadCommands():
    """Read the Json file and fill the lists and set settings"""
    # Open the JsonFile and load the data
    JsonFile = open(os.path.join(JsonPath, "CommandList.json"))
    data = json.load(JsonFile)

    # Get the dict with the customized date for the buttons
    try:
        Dict_Commands.update(data)
    except Exception as e:
        print(e)
        pass

    JsonFile.close()
    return


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


def UpdateCommands():
    # Go through the workbenches in the dict
    for WorkBench in Dict_RibbonCommandPanel["workbenches"]:
        # Go through the toolbars of the workbench
        for ToolBar in Dict_RibbonCommandPanel["workbenches"][WorkBench]["toolbars"]:
            # Continue if the "Toolbar" is not named order. This is the orderlist for the toolbars
            if ToolBar != "order":
                # Go through the commands in the toolbar
                for Command in Dict_RibbonCommandPanel["workbenches"][WorkBench][
                    "toolbars"
                ][ToolBar]["commands"]:
                    # Get the command (key) and its custom name (value) from the commandlist
                    # And compare them with the command in the Dict_RibbonCommandPanel
                    for key, value in Dict_Commands.items():
                        # If the command and key are equal and value is not empty or three dots,
                        # Get the custom name and change the text in the Dict_RibbonCommandPanel
                        if Command == key:
                            if value[2] != "" and value[2] != "...":
                                Dict_RibbonCommandPanel["workbenches"][WorkBench][
                                    "toolbars"
                                ][ToolBar]["commands"][Command]["text"] = value[2]


def WriteJson():
    # Open the JsonFile and load the data
    JsonFile = open(os.path.join(JsonPath, "RibbonStructure.json"))
    data = json.load(JsonFile)

    # RibbonTabs
    # Get the Ribbon dictionary
    data.update(Dict_RibbonCommandPanel)

    # get the path for the Json file
    JsonFile = os.path.join(JsonPath, JsonName)

    # Writing to sample.json
    with open(JsonFile, "w") as outfile:
        json.dump(data, outfile, indent=4)

    outfile.close()
    return


main()
