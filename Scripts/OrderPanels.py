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

# This script can be used to help order toolbars.
# it is particular helpfull to order global toolbars.
# For example set all view toolbars at the begining of the ribbon for eacht workbench.

import FreeCAD as App
import FreeCADGui as Gui
import os

import json

from PySide6.QtWidgets import QToolBar, QToolButton

ParentPath = os.path.dirname(os.path.dirname(__file__))

# Set the path where you want to save this new Json file
# JsonPath = os.path.dirname(__file__)
JsonPath = ParentPath

# Set the file name. Default is "RibbonStructure_default.json".
# This is the file used to reset the ribbon.
JsonName = "RibbonStructure.json"

# define panels/toolbars to sort. key=toolbarname, value is position S
ToolbarsToAdd = {"View": 0, "Views - Ribbon": 1, "Individual views": 2}

# get the path for the Json file
JsonFile = os.path.join(JsonPath, JsonName)

ribbonStructure = {}
# read ribbon structure from JSON file
with open(JsonFile, "r") as file:
    ribbonStructure.update(json.load(file))
file.close()


def main():
    UpdateOrder()
    WriteJson()


def UpdateOrder():

    # update the order for each workbench toolbar
    for WorkBench in ribbonStructure["workbenches"]:
        orderList: list = ribbonStructure["workbenches"][WorkBench]["toolbars"]["order"]
        for key, value in ToolbarsToAdd.items():
            if key not in orderList:
                orderList.insert(value, key)

        ribbonStructure["workbenches"][WorkBench]["toolbars"]["order"] = orderList
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
