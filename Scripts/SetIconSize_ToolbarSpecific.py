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

# This script can be used to set the icon size for specific toolbars/panels.
# it is particular helpfull for global toolbars.
# For example set all icons for the structure panel to medium

import FreeCAD as App
import FreeCADGui as Gui
import os

import json

from PySide.QtWidgets import QToolBar, QToolButton

ParentPath = os.path.dirname(os.path.dirname(__file__))

# Set the path where you want to save this new Json file
# JsonPath = os.path.dirname(__file__)
JsonPath = ParentPath

# Set the file name. Default is "RibbonStructure_default.json".
# This is the file used to reset the ribbon.
JsonName = "RibbonStructure.json"

# Enter here the names of the toolbars for which you want to set the icon size
ToolbarToUpdate = ["Structure"]  # ToolbarToUpdate = ["Structure", "Individual views"]

# Set the size for the first icon in every toolbar/panel
IconSize = "medium"  # set to "small" or medium as per preference

# get the path for the Json file
JsonFile = os.path.join(JsonPath, JsonName)

ribbonStructure = {}
# read ribbon structure from JSON file
with open(JsonFile, "r") as file:
    ribbonStructure.update(json.load(file))
file.close()


def main():
    UpdateJson()
    WriteJson()


def UpdateJson():
    # update the order for each workbench toolbar
    #
    # Go through each workbench in the Json file
    for WorkBench in ribbonStructure["workbenches"]:
        # Go through the list with toolbars to update
        for Item in ToolbarToUpdate:
            # Go through the toolbars of the workbench. If the toolbar is the same as in the list if toolbars to update, continue
            for ToolBar in ribbonStructure["workbenches"][WorkBench]["toolbars"]:
                if ToolBar == Item:
                    # Go through all commands for this toolbar and set the size
                    for Command in ribbonStructure["workbenches"][WorkBench]["toolbars"][ToolBar]["commands"]:
                        ribbonStructure["workbenches"][WorkBench]["toolbars"][ToolBar]["commands"][Command][
                            "size"
                        ] = IconSize

    return


def WriteJson():
    # Create a resulting dict
    resultingDict = {}

    # RibbonTabs
    # Get the Ribbon dictionary
    resultingDict.update(ribbonStructure)

    # get the path for the Json file
    JsonFile = os.path.join(JsonPath, JsonName)

    # Writing to sample.json
    with open(JsonFile, "w") as outfile:
        json.dump(resultingDict, outfile, indent=4)

    outfile.close()
    return


main()
